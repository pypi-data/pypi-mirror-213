import { VDomModel, VDomRenderer } from '@jupyterlab/apputils';
import { interactiveItem, Popup, showPopup } from '@jupyterlab/statusbar';
import React from "react";
import { Menu } from '@lumino/widgets';
import { CommandRegistry } from '@lumino/commands';
import { Icons } from '../icons';
import { message } from "../messages";
import { h, VirtualElement } from '@lumino/virtualdom';
import { AuthManager, AuthState } from "../auth/authManager";
import { AutoTrigger } from "../autotrigger/autotrigger";
import { Worker } from "../recommendation/worker";
import { LOG_SOURCE, ReferenceTracker } from '../referencetracker/referencetracker';
import { Application } from "../application";
import { Keybindings } from '../keybindings/keybindings';
import { CommandIDs, MESSAGE_TO_CMD_ID_MAP, CWSPR_DOCUMENTATION } from '../utils/constants';
import { AUTO_SUGGESTION } from '../utils/stateKeys';
import { saveState } from "../utils/utils";

// TODO: figure out the right way to use this
class StatusBarWidgetModel extends VDomModel {
    constructor() {
        super();
    }
}

class StatusBarWidget extends VDomRenderer<StatusBarWidgetModel> {
    private _popup: Popup | null = null;
    private _commandsForNotAuthenticated: CommandRegistry = new CommandRegistry();
    private _commandsForAuthenticationInProgress: CommandRegistry = new CommandRegistry();
    private _commandsForAutoSuggestionEnabled: CommandRegistry = new CommandRegistry();
    private _commandsForAutosuggestionDisabled: CommandRegistry = new CommandRegistry();
    private _renderer: Menu.IRenderer = new StatusBarWidgetRenderer();
    private _keyShortcutsInfoRows = 5;

    constructor() {
        super(new StatusBarWidgetModel());
        this.addClass(interactiveItem)
        this.addClass("jp-Notebook-ExecutionIndicator")
        this.addClass("cwspr-statusbarwidget-parent")

        this._initializeCommands()
        AuthManager.getInstance().authStateChangedSignal.connect(this._onAuthStateChanged, this);
        Worker.getInstance().invocationStatusChangedSignal.connect(this._onInvocationStatusChanged, this);
    }

    private _onAuthStateChanged(sender: any, authState: AuthState) {
        this.update()
    }

    private _onInvocationStatusChanged(sender: any, status: boolean) {
        this.update()
    }

    private _addKeyShortcutsInfo(commands: CommandRegistry) {
        commands.addCommand(CommandIDs.keyShortcutTitle, {
            label: message('codewhisperer_key_shortcut_title'),
            icon: null,
            execute: async () => {},
            isEnabled: () => false,
        })
        commands.addCommand(CommandIDs.keyShortcutAccept, {
            label: message('codewhisperer_key_shortcut_accept'),
            icon: null,
            execute: async () => {},
            isEnabled: () => false
        })
        commands.addCommand(CommandIDs.keyShortcutManualTrigger, {
            label: message('codewhisperer_key_shortcut_manual_trigger'),
            icon: null,
            execute: async () => {},
            isEnabled: () => false
        })
        commands.addCommand(CommandIDs.keyShortcutNavigate, {
            label: message('codewhisperer_key_shortcut_navigate'),
            icon: null,
            execute: async () => {},
            isEnabled: () => false
        })
        commands.addCommand(CommandIDs.keyShortcutReject, {
            label: message('codewhisperer_key_shortcut_reject'),
            icon: null,
            execute: async () => {},
            isEnabled: () => false
        })
    }

    private _addCommandsForUnauthenticated() {
        if (Application.getInstance().isJupyterOSS()) {
            this._commandsForNotAuthenticated.addCommand(CommandIDs.startCodeWhisperer, {
                label: message("codewhisperer_start"),
                icon: Icons.startIcon,
                caption: message("codewhisperer_start"),
                execute: async () => {
                    this._handleClick();
                    if (AuthManager.getInstance().isAuthenticated() ||
                        AuthManager.getInstance().isAuthenticationInProgress()) {
                        return;
                    }
                    await AuthManager.getInstance().login();
                }
            });
        }
        this._commandsForNotAuthenticated.addCommand(CommandIDs.openDocumentation, {
            label: message('codewhisperer_documentation_open'),
            icon: Icons.documentationIcon,
            caption: message('codewhisperer_documentation_open'),
            execute: async () => {
                window.open(CWSPR_DOCUMENTATION, '_blank');
                this._handleClick();
            }
        });
    }

    private _addCommandsForAuthenticationInProgress() {
        this._commandsForAuthenticationInProgress.addCommand(CommandIDs.cancelLogin, {
            label: message("codewhisperer_cancel_login"),
            icon: Icons.startIcon,
            caption: message("codewhisperer_cancel_login"),
            execute: async () => {
                this._handleClick();
                if (!AuthManager.getInstance().isAuthenticationInProgress()) return;
                await AuthManager.getInstance().cancelLogin()
            }
        });
        this._commandsForAuthenticationInProgress.addCommand(CommandIDs.openDocumentation, {
            label: message('codewhisperer_documentation_open'),
            icon: Icons.documentationIcon,
            caption: message('codewhisperer_documentation_open'),
            execute: async () => {
                window.open(CWSPR_DOCUMENTATION, '_blank');
                this._handleClick();
            }
        });
    }

    private _addCommandsForAuthenticatedCommon(commands: CommandRegistry) {
        commands.addCommand(CommandIDs.openReferenceLog, {
            label: message('codewhisperer_reference_log_open'),
            icon: Icons.referenceLogIcon,
            caption: message('codewhisperer_reference_log_open'),
            isToggled: () => ReferenceTracker.getInstance().isReferenceLogDisposed(),
            execute: async () => {
                if (ReferenceTracker.getInstance().isReferenceLogDisposed()) {
                    Application.getInstance().jupyterApp.shell.add(
                        ReferenceTracker.getInstance().createReferenceLogWidget(),
                        'down',
                        {
                            ref: LOG_SOURCE,
                            mode: 'split-bottom'
                        });
                } else {
                    ReferenceTracker.getInstance().disposeReferenceLogWidget();
                }
                this._handleClick();
            }
        });
        commands.addCommand(CommandIDs.openDocumentation, {
            label: message('codewhisperer_documentation_open'),
            icon: Icons.documentationIcon,
            caption: message('codewhisperer_documentation_open'),
            execute: async () => {
                window.open(CWSPR_DOCUMENTATION, '_blank');
                this._handleClick();
            }
        });

        if (Application.getInstance().isSageMakerStudio()) return;

        commands.addCommand(CommandIDs.signOut, {
            label: message('codewhisperer_sign_out'),
            icon: Icons.signOutIcon,
            caption: message('codewhisperer_sign_out'),
            execute: async () => {
                this._handleClick();
                if (!AuthManager.getInstance().isAuthenticated()) return;
                await AuthManager.getInstance().logout()
            }
        });
    }

    private _initializeCommands() {
        this._addCommandsForUnauthenticated()
        this._addCommandsForAuthenticationInProgress()

        this._addKeyShortcutsInfo(this._commandsForAutosuggestionDisabled)
        this._commandsForAutosuggestionDisabled.addCommand(CommandIDs.resumeAutoSuggestion, {
            label: message('codewhisperer_resume_auto_suggestion'),
            icon: Icons.resumeIcon,
            caption: message('codewhisperer_resume_auto_suggestion'),
            execute: async () => {
                this._handleClick();
                AutoTrigger.getInstance().enabled = true;
                await saveState(AUTO_SUGGESTION, true)
            }
        });
        this._addCommandsForAuthenticatedCommon(this._commandsForAutosuggestionDisabled)

        this._addKeyShortcutsInfo(this._commandsForAutoSuggestionEnabled)
        this._commandsForAutoSuggestionEnabled.addCommand(CommandIDs.pauseAutoSuggestion, {
            label: message('codewhisperer_pause_auto_suggestion'),
            icon: Icons.pauseIcon,
            caption: message('codewhisperer_pause_auto_suggestion'),
            execute: async () => {
                this._handleClick();
                AutoTrigger.getInstance().enabled = false;
                await saveState(AUTO_SUGGESTION, false);
            }
        });
        this._addCommandsForAuthenticatedCommon(this._commandsForAutoSuggestionEnabled)
    }

    render(): React.ReactElement {
        const isInvocationInProgress = Worker.getInstance().isGetCompletionsRunning;
        const icon =
            AuthManager.getInstance().isAuthenticated() ?
                isInvocationInProgress ? (
                    <Icons.loadingIcon.react tag="span" className="cwspr-statusbarwidget-icon" />
                ) : (
                    <Icons.connectedIcon.react tag="span" className="cwspr-statusbarwidget-icon" />
                ) :
            AuthManager.getInstance().isAuthenticationInProgress() ? (
                <Icons.loadingIcon.react tag="span" className="cwspr-statusbarwidget-icon" />
            ) : (
                <Icons.disconnectedIcon.react tag="span" className="cwspr-statusbarwidget-icon" />
            );

        return (
            <div className='cwspr-statusbarwidget' onClick={() => this._handleClick()}>
                {icon}
                <span>{this._getStatusBarWidgetDisplayText()}</span>
            </div>
        );
    }

    private _getStatusBarWidgetDisplayText(): string {
        if (AuthManager.getInstance().isAuthenticated()) {
            return message('codewhisperer_status_widget_text_authenticated');
        } else if (AuthManager.getInstance().isAuthenticationInProgress()) {
            return message('codewhisperer_status_widget_text_auth_in_progress');
        } else {
            return message('codewhisperer_status_widget_text_not_authenticated');
        }
    }

    /**
     * Handle a click on the status item.
     */
    private _handleClick(): void {
        const menu = this._getMenu();
        if (this._popup !== null && !this._popup.isDisposed) {
            this._popup.dispose();
            this._popup = null;
            return;
        }
        this._menuToggled()
        menu.aboutToClose.connect(this._menuToggled, this);

        this._popup = showPopup({
            body: menu,
            anchor: this,
            align: 'left'
        });
    }

    private _menuToggled(): void {
        this.toggleClass('jp-mod-clicked');
    }

    private _getMenu(): Menu {
        const autoTriggerEnabled = AutoTrigger.getInstance().enabled;
        let commands;

        if (AuthManager.getInstance().isAuthenticated()) {
            if (autoTriggerEnabled) {
                commands = this._commandsForAutoSuggestionEnabled;
            } else {
                commands = this._commandsForAutosuggestionDisabled;
            }
        } else if (AuthManager.getInstance().isAuthenticationInProgress()) {
            commands = this._commandsForAuthenticationInProgress;
        } else {
            commands = this._commandsForNotAuthenticated;
        }

        const menu = new Menu({ commands: commands, renderer: this._renderer });
        menu.addClass('cwspr-statusbarwidget-menu');

        this._addCommands(menu, commands);
        if (AuthManager.getInstance().isAuthenticated()) {
            menu.insertItem(this._keyShortcutsInfoRows, { type: 'separator' });
        }

        menu.update()
        return menu;
    }

    private _addCommands(menu: Menu, commands: CommandRegistry) {
        for (let i = 0; i < commands.listCommands().length; i++) {
            menu.addItem({
                command: commands.listCommands()[i]
            });
        }
        menu.update()
    }
}

class StatusBarWidgetRenderer extends Menu.Renderer {
    renderItem(data: Menu.IRenderData): VirtualElement {
        let className = this.createItemClass(data);
        let dataset = this.createItemDataset(data);
        let aria = this.createItemARIA(data);
        return h.li(
            {
                className,
                dataset,
                tabindex: '0',
                onfocus: data.onfocus,
                ...aria
            },
            this.renderIcon(data),
            this.renderLabel(data),
            this.renderShortcut(data),
            this.renderSubmenu(data),
            this._renderCodeWhispererShortCut(data)
        );
    }

    _renderCodeWhispererShortCut(data: Menu.IRenderData): VirtualElement {
        const keyShortcutButtons = this._getKeyShortcutButtons(data)
        return h.div(
            {
                className: 'cwspr-key-shortcut-menu'
            },
            ...keyShortcutButtons
        );
    }

    _getKeyShortcutButtons(data: Menu.IRenderData): h.Child[] {
        if (data.item.isEnabled || data.item.label == message('codewhisperer_key_shortcut_title')) return [""]
        let children: h.Child[]
        switch (data.item.label) {
            case message("codewhisperer_key_shortcut_accept"):
                children = Keybindings.getInstance().getKeybinding(MESSAGE_TO_CMD_ID_MAP["codewhisperer_key_shortcut_accept"]);
                break;
            case message("codewhisperer_key_shortcut_manual_trigger"):
                children = Keybindings.getInstance().getKeybinding(MESSAGE_TO_CMD_ID_MAP["codewhisperer_key_shortcut_manual_trigger"]);
                break;
            case message("codewhisperer_key_shortcut_navigate"):
                children = ["Up & Down"];
                break;
            case message("codewhisperer_key_shortcut_reject"):
                children = Keybindings.getInstance().getKeybinding(MESSAGE_TO_CMD_ID_MAP["codewhisperer_key_shortcut_reject"]);
                break;
            default:
                children = [];
                break;
        }
        return children.map((text) => h.div({className: 'cwspr-key-shortcut-button'}, text))
    }
}

export default StatusBarWidget;