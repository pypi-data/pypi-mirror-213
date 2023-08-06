import { CodeEditor } from '@jupyterlab/codeeditor';
import { NotebookPanel } from '@jupyterlab/notebook';
import { Inline } from '../inline/inline';
import { Logger } from '../logging/logger';
import pino from 'pino';
import { IObservableString } from '@jupyterlab/observables';
import { CodewhispererAutomatedTriggerType } from '../telemetry/telemetry.gen';
import { RecommendationStateHandler } from '../recommendation/recommendationStateHandler';
import { loadState } from "../utils/utils";
import { Application } from "../application";
import { AUTO_SUGGESTION } from "../utils/stateKeys";

// TODO: Too many states maintained, only enabled is needed
export class AutoTrigger {

    private static instance: AutoTrigger;

    private logger: pino.Logger;

    public static getInstance(): AutoTrigger {
        if (!AutoTrigger.instance) {
            AutoTrigger.instance = new AutoTrigger()
        }
        return AutoTrigger.instance;
    }

    constructor() {
        this.enabled = true
        this.logger = Logger.getInstance({
            "name": "codewhisperer",
            "component" : "autotrigger"
        });
        Application.getInstance().loadStateSignal.connect(this.loadState, this)
    }

    public async loadState(sender: any) {
        // auto suggestion
        const isAutoSuggestionEnabled = await loadState(AUTO_SUGGESTION)

        // isAutoSuggestionEnabled is undefined if stateDB object is not init with the AUTO_SUGGESTION key
        this.enabled = isAutoSuggestionEnabled === undefined || isAutoSuggestionEnabled as boolean
    }

    public get isAutoSuggestionEnabled() : boolean {
        return this.enabled
    }

    public set isAutoSuggestionEnabled(value: boolean) {
        this.enabled = value
    }

    private filename: string

    public enabled: boolean
    private specialCharacters = new Set<string>(['(', '[', ':', '{']);
    public lastKeyStrokeTime = 0
    private _registeredEditors: CodeEditor.IEditor[] = []

    public registerListener(editor: CodeEditor.IEditor, panel: NotebookPanel | undefined, filename?: string) {
        if (this._registeredEditors.includes(editor)) {
            return
        }

        let changeHandler = async (sender: IObservableString, args: IObservableString.IChangedArgs) => {
            const now = performance.now();
            RecommendationStateHandler.instance.timeSinceLastDocumentChange = now - this.lastKeyStrokeTime;
            if (!this.enabled) {
                this.lastKeyStrokeTime = now;
                return;
            }

            const {autoTriggerType, triggerCharacter} = this.shouldAutoTrigger(args);
            this.invokeAutoTrigger(editor, panel, autoTriggerType, triggerCharacter, this.lastKeyStrokeTime);
            this.lastKeyStrokeTime = now;
        }
        changeHandler = changeHandler.bind(this)
        editor.model.value.changed.connect(changeHandler)

        // OK if the editors/cells are removed later, they will just be stale copies and be cleaned on next IDE restart
        this._registeredEditors.push(editor)
        this.filename = filename
    }

    public onSwitchToNewCell(editor: CodeEditor.IEditor, panel: NotebookPanel) {
        if (!this.enabled) {
            return
        }
        const cell = panel.content.activeCell
        if (cell.model.type === 'code' && editor.getCursorPosition().line === 0
            && editor.getCursorPosition().column === 0
            && editor.model.value.text.trim().length === 0) {
            this.invokeAutoTrigger(editor, panel, "NewCell", undefined, this.lastKeyStrokeTime);
        }
    }

    private invokeAutoTrigger(
        editor: CodeEditor.IEditor,
        panel: NotebookPanel | undefined,
        autoTriggerType: CodewhispererAutomatedTriggerType,
        triggerCharacter: string,
        triggerTime: number
    ) {
        this.logger.debug(`invokeAutoTrigger - ${autoTriggerType} - ${triggerCharacter} - ${triggerTime}`)
        if (autoTriggerType) {
            if (panel) {
                // invoke in a Notebook panel
                Inline.getInstance().getCompletionsInNotebookPanel(panel, {
                    triggerCharacter: triggerCharacter,
                    triggerTime: triggerTime,
                    automatedTriggerType: autoTriggerType,
                    triggerType: "AutoTrigger",
                    language: "ipynb"
                })
            } else if (editor) {
                // invoke in python file
                Inline.getInstance().getCompletionsInEditor(editor, this.filename, {
                    triggerCharacter: triggerCharacter,
                    triggerTime: triggerTime,
                    automatedTriggerType: autoTriggerType,
                    triggerType: "AutoTrigger",
                    language: "python"
                })
            }
        } else {
            this.logger.debug("Not Valid auto trigger character");
        }
        
    }

    shouldAutoTrigger(changeArgs: IObservableString.IChangedArgs): 
    { autoTriggerType: CodewhispererAutomatedTriggerType | undefined, triggerCharacter: string | undefined } {
        let autoTriggerType = undefined;
        let triggerCharacter = undefined;
        autoTriggerType = this.changeIsNewLine(changeArgs)
        if (!autoTriggerType) {
            autoTriggerType = this.changeIsSpecialCharacter(changeArgs).autoTriggerType;
            triggerCharacter = this.changeIsSpecialCharacter(changeArgs).triggerCharacter;
            if (!autoTriggerType) {
                autoTriggerType = this.changeIsIdleTimeTrigger(changeArgs)
            }
        }
        return { autoTriggerType: autoTriggerType, triggerCharacter: triggerCharacter };
    }

    private changeIsNewLine(changeArgs: IObservableString.IChangedArgs): CodewhispererAutomatedTriggerType | undefined {
        const shouldTrigger = (changeArgs.type === 'insert' && changeArgs.value.trim() === '' && changeArgs.value.startsWith('\n'))
        if (shouldTrigger) {
            return "Enter";
        } else {
            return undefined;
        }
    }

    private changeIsSpecialCharacter(changeArgs: IObservableString.IChangedArgs): 
    { autoTriggerType: CodewhispererAutomatedTriggerType | undefined, triggerCharacter: string | undefined } {
        const shouldTrigger = (changeArgs.type === 'insert' && this.specialCharacters.has(changeArgs.value))
        if (shouldTrigger) {
            return {autoTriggerType: "SpecialCharacters", triggerCharacter: changeArgs.value};
        } else {
            return {autoTriggerType: undefined, triggerCharacter: undefined};
        }
    }

    private changeIsIdleTimeTrigger(changeArgs: IObservableString.IChangedArgs): CodewhispererAutomatedTriggerType | undefined {
        const shouldTrigger = (performance.now() - this.lastKeyStrokeTime >= 2000 && changeArgs.type === 'insert')
        if (shouldTrigger) {
            return "IdleTime"
        } else {
            return undefined;
        }
    }

}