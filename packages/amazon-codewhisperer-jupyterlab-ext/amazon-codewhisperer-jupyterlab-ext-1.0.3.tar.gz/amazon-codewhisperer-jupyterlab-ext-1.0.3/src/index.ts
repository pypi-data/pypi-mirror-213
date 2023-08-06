/*!
 * Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
import { JupyterFrontEnd, JupyterFrontEndPlugin, } from '@jupyterlab/application';
import { ContextConnector, ICompletionManager, KernelConnector, } from '@jupyterlab/completer';

import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { IEditorTracker } from '@jupyterlab/fileeditor'
import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { MergeConnector } from './connector/mergeconnector';

import { Worker } from './recommendation/worker'

import { IStateDB } from '@jupyterlab/statedb';

import { DocumentWidget } from '@jupyterlab/docregistry';
import { IStatusBar } from '@jupyterlab/statusbar';

import { Inline } from './inline/inline';
import { AutoTrigger } from './autotrigger/autotrigger';
import { CodeEditorWrapper } from '@jupyterlab/codeeditor';
import { ReadonlyJSONObject, UUID } from '@lumino/coreutils';
import { Telemetry } from './telemetry/telemetry';
import StatusBarWidget from "./statusbar/statusbarwidget";
import { CodeWhispererConnector } from './connector/codewhispererconnector';
import { AuthManager } from "./auth/authManager";
import { Logger } from './logging/logger';
import { Application } from "./application";
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { ReferenceTracker } from './referencetracker/referencetracker';
import { CommandIDs, NEW_CELL_AUTO_TRIGGER_DELAY_IN_MS, PLUGIN_ID, SettingIDs } from './utils/constants';
import { Keybindings } from './keybindings/keybindings';

/**
 * Initialization data for the extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [ISettingRegistry, ICompletionManager, INotebookTracker, IEditorTracker, IStateDB, IStatusBar, IRenderMimeRegistry],
  activate: async (
    app: JupyterFrontEnd,
    settings: ISettingRegistry,
    completionManager: ICompletionManager,
    notebooks: INotebookTracker,
    editorTracker: IEditorTracker,
    state: IStateDB,
    statusBar: IStatusBar,
    rendermime: IRenderMimeRegistry
  ) => {
    const logger = Logger.getInstance({
      "name": "codewhisperer",
    });

    // This is computed per browser refresh
    const activateStartTime = performance.now()

    /* ClientId is a UUID for identifying unique customers for telemetry. It should be specific to
    *  one installation of codewhisperer extension in a host. IStateDB is used for persistence in an extension.  
    *  See https://github.com/jupyterlab/extension-examples/tree/master/state for more details. 
    */
    app.restored.then(async () => {
      // Get the state of the extension
      state.fetch(PLUGIN_ID).then(value => {
        if (value) {
          Telemetry.clientId = (value as ReadonlyJSONObject)['clientId'] as string;
          logger.debug(`Restored - clientId: ${Telemetry.clientId}`);
        } else {
          // generate uuid for clientId
          Telemetry.clientId = UUID.uuid4();
          // save clientId to state
          state.save(PLUGIN_ID, { "clientId": Telemetry.clientId });
          logger.debug(`Generated - clientId: ${Telemetry.clientId}`);
        }
      });

      const loadSetting = (setting: ISettingRegistry.ISettings) => {
        Telemetry.getInstance().enableTelemetry(setting.get(SettingIDs.keyTelemetry).composite as boolean);
        Worker.getInstance().setOptOut(!(setting.get(SettingIDs.keyOptOut).composite as boolean));
        Worker.getInstance().setSuggestionsWithCodeReferences(setting.get(SettingIDs.keyReferences).composite as boolean);
        Logger.setLogLevel(setting.get(SettingIDs.keyLogLevel).composite as string);
        Keybindings.getInstance().keyBindings = [...app.commands.keyBindings];
        logger.debug(`Loaded settings`);

        if (Application.getInstance().isJupyterOSS()) return;
        const styleElement = document.createElement('style');

        styleElement.textContent = `
#jp-SettingsEditor-amazon-codewhisperer-jupyterlab-ext\\\:completer > div:first-of-type {
  display: none !important;
}

#jp-SettingsEditor-amazon-codewhisperer-jupyterlab-ext\\\:completer > div:first-of-type > input {
  pointer-events: none;
  opacity: 0.5;
}
        `;
        document.head.appendChild(styleElement);
      }

      Promise.all([app.restored, settings.load(PLUGIN_ID)])
        .then(([, setting]) => {
          loadSetting(setting);
          setting.changed.connect(loadSetting);
        })


      Application.getInstance().loadStateSignal.emit(null);
      await AuthManager.getInstance().refresh();
      const statusBarWidget = new StatusBarWidget();
      statusBar.registerStatusItem("aws-codewhisperer:status-bar-widget", {
        item: statusBarWidget,
        align: 'left',
        isActive: () => true,
        rank: 100,
      });
    });

    await Application.getInstance().loadServices(state, app);

    /* A listener that triggers whenever there is a new Notebook panel
    * This is to 
      1. register a listener for auto trigger in Notebook files
      2. Setup kernel completion & completion connectors using a merge connector.
    */
    notebooks.widgetAdded.connect(
      (sender: INotebookTracker, panel: NotebookPanel) => {

        logger.debug(`Notebookpanel added - ${panel.id}`);
        let editor = panel.content.activeCell?.editor ?? null;
        const session = panel.sessionContext.session;
        const options = { session, editor };
        const connector = new MergeConnector();
        const handler = completionManager.register({
          connector,
          editor,
          parent: panel
        }
        );

        const updateConnector = () => {

          logger.debug(`Notebookpanel updated - ${panel.id}`);

          editor = panel.content.activeCell?.editor ?? null;
          options.session = panel.sessionContext.session;
          options.editor = editor;
          handler.editor = editor;
          // this connector contains native & cw suggestions  
          const kernel = new KernelConnector(options);
          const context = new ContextConnector(options);

          const codewhispererConnector = new CodeWhispererConnector({ notebookPanel: panel });
          handler.connector = new MergeConnector(codewhispererConnector, kernel, context);
          AutoTrigger.getInstance().registerListener(editor, panel);

          // briefly after browser refresh finishes, enable the NewCell auto trigger
          // browser refresh will send false signal of NewCell auto trigger
          const currentWidget = app.shell.currentWidget
          if (currentWidget && currentWidget instanceof NotebookPanel && performance.now() - activateStartTime > NEW_CELL_AUTO_TRIGGER_DELAY_IN_MS) {
            AutoTrigger.getInstance().onSwitchToNewCell(editor, panel)
          }
        };
        // Update the handler whenever the prompt or session changes
        panel.content.activeCellChanged.connect(() => updateConnector());
        panel.sessionContext.sessionChanged.connect(() => updateConnector());

        // clear suggestion when panel lost focus
        const onPanelFocusOut = () => {
          logger.debug(`Notebookpanel focus out - ${panel.id}`);
          Inline.getInstance().onFocusOut()
        }
        // ensure only one listener is active at a time
        panel.node.removeEventListener('focusout', onPanelFocusOut)
        panel.node.addEventListener('focusout', onPanelFocusOut)
      }
    );

    /* A listener that triggers whenever there is a new editor other than Notebook panel
    * This is to register a listener for auto trigger in python files
    */
    editorTracker.widgetAdded.connect((sender: any, e) => {
      logger.debug(`Editor added - ${e.id}`);
      e.content.editor.host.addEventListener('focusin', () => {
        const filename = e.context.path.split('/').pop()
        AutoTrigger.getInstance().registerListener(e.content.editor, undefined, filename);
      })
    })



    // Add notebook completer command.
    if (!app.commands.hasCommand(CommandIDs.invokeNotebook)) {
      app.commands.addCommand(CommandIDs.invokeNotebook, {
        execute: () => {
          logger.debug("Executing command : invokeNotebook")
          if (Inline.getInstance().isInlineSessionActive()) {
            Inline.getInstance().acceptCompletion()
            return
          }
          // if pagination is in process, cancel pagination and let kernel completion show
          if (Worker.getInstance().isGetCompletionsRunning) {
            Inline.getInstance().removeCompletion()
          }
          const panel = notebooks.currentWidget;
          if (panel && panel.content.activeCell?.model.type === 'code') {
            return app.commands.execute(CommandIDs.invoke, { id: panel.id });
          }
        },
      });
    }

    // Add file editor completer command.
      app.commands.addCommand(CommandIDs.invokeFile, {
        execute: () => {
          logger.debug("Executing command : invokeFile")
          if (Inline.getInstance().isInlineSessionActive()) {
            Inline.getInstance().acceptCompletion()
            return
          }
          // if pagination is in process, cancel pagination and let kernel completion show
          if (Worker.getInstance().isGetCompletionsRunning) {
            Inline.getInstance().removeCompletion()
          }
          // code reference: https://github.com/jupyterlab/jupyterlab/blob/master/packages/fileeditor-extension/src/commands.ts#L1004
          const id = editorTracker.currentWidget &&  editorTracker.currentWidget.id
          if (id) {
            return app.commands.execute(CommandIDs.invoke, { id: id });
          }
        },
      });
    

    if (!app.commands.hasCommand(CommandIDs.selectNotebook)) {
      logger.debug("Executing command : selectNotebook")
      // Add notebook completer select command.
      app.commands.addCommand(CommandIDs.selectNotebook, {
        execute: () => {
          const id = notebooks.currentWidget && notebooks.currentWidget.id;

          if (id) {
            return app.commands.execute(CommandIDs.select, { id });
          }
        },
      });
    }

    if (!app.commands.hasCommand(CommandIDs.login)) {
      logger.debug("Executing command : login")
      app.commands.addCommand(CommandIDs.login, {
        execute: async () => {
          await AuthManager.getInstance().login()
        },
      });
    }


    if (!app.commands.hasCommand(CommandIDs.invokeInline)) {

      app.commands.addCommand(CommandIDs.invokeInline, {
        execute: async () => {
          logger.debug("Executing command : invokeInline")
          const currentWidget = app.shell.currentWidget
          if (currentWidget && currentWidget instanceof NotebookPanel) {
            logger.debug("Invoking Inline in NotebookPanel")
            await Inline.getInstance().getCompletionsInNotebookPanel(currentWidget as NotebookPanel, {
              triggerType: "OnDemand",
              triggerCharacter: undefined,
              automatedTriggerType: undefined,
              language: "ipynb",
              triggerTime: performance.now(),
            })
          } else if (currentWidget && currentWidget instanceof DocumentWidget) {
            logger.debug("Invoking Inline in Document")
            const doc = currentWidget as DocumentWidget<CodeEditorWrapper>
            const filename = doc.context.path.split('/').pop()
            await Inline.getInstance().getCompletionsInEditor(doc.content.editor, filename, {
              triggerType: "OnDemand",
              triggerCharacter: undefined,
              automatedTriggerType: undefined,
              language: "python",
              triggerTime: performance.now(),
            })
          } else {
            logger.error("Notebook or Editor not found")
          }
        },
      });
    }

    if (!app.commands.hasCommand(CommandIDs.rejectInline)) {
      logger.debug("Executing command : rejectInline")
      app.commands.addCommand(CommandIDs.rejectInline, {
        execute: async () => {
          Inline.getInstance().removeCompletion()
        },
      });
    }


    if (!app.commands.hasCommand(CommandIDs.acceptInline)) {
      logger.debug("Executing command : acceptInline")
      app.commands.addCommand(CommandIDs.acceptInline, {
        execute: async () => {
          Inline.getInstance().acceptCompletion()
        },
      });
    }

    if (!app.commands.hasCommand(CommandIDs.showNext)) {
      logger.debug("Executing command : showNext")
      app.commands.addCommand(CommandIDs.showNext, {
        execute: async () => {
          Inline.getInstance().showNext()
        },
      });
    }

    if (!app.commands.hasCommand(CommandIDs.showPrev)) {
      logger.debug("Executing command : showNext")
      app.commands.addCommand(CommandIDs.showPrev, {
        execute: async () => {
          Inline.getInstance().showPrev()
        },
      });
    }

    ReferenceTracker.createInstance(rendermime);

    Telemetry.init();

    logger.info('JupyterLab CodeWhisperer extension is activated!');
  },
};

export default extension;
