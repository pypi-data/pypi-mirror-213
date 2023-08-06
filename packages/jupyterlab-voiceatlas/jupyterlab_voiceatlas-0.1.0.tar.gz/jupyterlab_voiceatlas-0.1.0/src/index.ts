import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';

// import { SplitPanel } from '@lumino/widgets';
import { IMainMenu } from '@jupyterlab/mainmenu';
// import { PageConfig } from "@jupyterlab/coreutils";
import { MainAreaWidget, ToolbarButton } from '@jupyterlab/apputils';
import { Menu } from '@lumino/widgets';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import isEqual from "lodash.isequal";
import { Dialog, showDialog } from '@jupyterlab/apputils';
import { DocumentRegistry } from "@jupyterlab/docregistry";
import { NotebookPanel, INotebookModel, INotebookTracker } from "@jupyterlab/notebook";
import { DisposableDelegate, IDisposable } from "@lumino/disposable";

import { ChatlasWidget } from './widgets/ChatlasWidget';
import { loadSetting, configureNewAtlas } from './utils';
import { aboutVoiceAtlasDialog } from './widgets/AboutVoiceAtlas';
import { requestAPI } from "./handler";
import { ChatlasDropdownWidget } from './widgets/ChatlasDropdownMenuWidget';
import EditSettingsWidget from './widgets/EditSettingsWidget';
import isEmpty from 'lodash.isempty';
import { INotification } from 'jupyterlab_toastify';

const PLUGIN_ID = 'jupyterlab_voiceatlas:plugin'
const plugin: JupyterFrontEndPlugin<void> = {
    id: PLUGIN_ID,
    requires: [IMainMenu, ISettingRegistry, INotebookTracker],
    autoStart: true,
    activate
};

let globalAtlasId: string | undefined | null = undefined;
let globalNotebookName: string;
let globalApp: JupyterFrontEnd;
let globalPanel: NotebookPanel;

const openChatlas = (): void => {
    console.log(`Calling Chatlas => ${globalAtlasId}`)
    const content = new ChatlasWidget(globalAtlasId!, globalNotebookName)
    content.title.label = `Chatlas - ${globalNotebookName}`;
    const widget = new MainAreaWidget<ChatlasWidget>({ content })
    widget.id = `chatlas-${globalNotebookName}`
    console.log(`Current Notebook Panel Info => ${globalPanel.id}`)
    globalApp.shell.add(widget, 'main');
}

let button = new ToolbarButton({
    label: "Chatlas",
    onClick: openChatlas,
    tooltip: "Open Chatlas.",
});

export class ButtonExtension
    implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
    createNew(
        panel: NotebookPanel,
        _: DocumentRegistry.IContext<INotebookModel>
    ): IDisposable {
        return new DisposableDelegate(() => {
            button.dispose();
        });
    }
}

async function activate(
    app: JupyterFrontEnd,
    mainMenu: IMainMenu,
    settings: ISettingRegistry,
    notebookTracker: INotebookTracker,
    panel: NotebookPanel): Promise<void> {
    console.log('JupyterLab extension jupyterlab_voiceatlas is activated!');
    const { commands } = app;
    const openChatlas = 'voice-atlas-jlab-ext:openChatlas';
    const editSettings = 'voice-atlas-jlab-ext:editSettings';
    const createNewAtlas = 'voice-atlas-jlab-ext:createNewAtlas';
    const aboutVoiceAtlas = 'voice-atlas-jlab-ext:aboutVoiceAtlas';
    const helpVoiceAtlas = 'voice-atlas-jlab-ext:helpVoiceAtlas';

    requestAPI<any>('get_example')
        .then(data => {
            console.log(data);
        })
        .catch(reason => {
            console.error(
                `The jupyterlab_voiceatlas server extension appears to be missing.\n${reason}`
            );
        });

    Promise.all([app.restored, settings.load(PLUGIN_ID)])
        .then(([, setting]) => {
            loadSetting(setting);
        }).catch((reason) => {
            console.error(
                `Something went wrong when changing the settings.\n${reason}`
            );
        });

    commands.addCommand(openChatlas, {
        label: 'Open Chatlas',
        caption: 'Open Chatlas',
        execute: async () => {
            let atlasId = ''
            await Promise.all([settings.load(PLUGIN_ID)])
                .then(([setting]) => {
                    atlasId = loadSetting(setting);
                }).catch((reason) => {
                    console.error(
                        `Something went wrong when getting the current atlas id.\n${reason}`
                    );
                });

            if (isEqual(atlasId, "")) {
                atlasId = await configureNewAtlas(settings, PLUGIN_ID)
                return;
            }
            const content = new ChatlasWidget(atlasId, globalNotebookName)
            content.title.label = 'Voice Atlas for JupyterLab';
            const widget = new MainAreaWidget<ChatlasWidget>({ content })
            app.shell.add(widget, 'main');
        }
    });

    commands.addCommand(editSettings, {
        label: 'Edit Settings',
        caption: 'Settings',
        execute: async () => { globalAtlasId ? await configureNewAtlas(settings, PLUGIN_ID, globalAtlasId) : await configureNewAtlas(settings, PLUGIN_ID) }
    });

    commands.addCommand(createNewAtlas, {
        label: 'Create new atlas',
        caption: 'Create new atlas.',
        execute: () => {
            const url = "https://app.voiceatlas.com";
            window.open(url);
        }
    });

    commands.addCommand(aboutVoiceAtlas, {
        label: 'About Voice Atlas',
        caption: 'About Voice Atlas',
        execute: async () => {
            const { aboutBody, aboutTitle } = aboutVoiceAtlasDialog();
            const result = await showDialog({
                title: aboutTitle,
                body: aboutBody,
                buttons: [
                    Dialog.createButton({
                        label: 'Dismiss',
                        className: 'jp-About-button jp-mod-reject jp-mod-styled'
                    })
                ]
            });

            if (result.button.accept) {
                return;
            }
        }
    })

    commands.addCommand(helpVoiceAtlas, {
        label: 'Help',
        caption: 'Help.',
        execute: () => {
            const url = "https://help.voiceatlas.com";
            window.open(url);
        }
    });

    const menu = new Menu({ commands: app.commands });
    menu.title.label = 'NLP'

    menu.addItem({
        command: createNewAtlas,
        args: { origin: 'from menu' },
    });

    menu.addItem({
        command: editSettings,
        args: { origin: 'from menu' },
    });

    menu.addItem({
        command: openChatlas,
        args: { origin: 'from menu' },
    });

    menu.addItem({ type: 'separator' });

    menu.addItem({
        command: helpVoiceAtlas,
        args: { origin: 'from menu' },
    });

    menu.addItem({
        command: aboutVoiceAtlas,
        args: { origin: 'from menu' },
    });

    mainMenu.addMenu(menu, { rank: 1000 });
    app.docRegistry.addWidgetExtension("Notebook", new ButtonExtension());

    notebookTracker.currentChanged.connect(async (_, panel) => {
        if (panel) {
            notebookTracker.currentWidget?.update()
            panel.context.ready.then(async () => {
                let atlasId = panel.model?.metadata.get('atlas-id') as string;
                globalAtlasId = atlasId;
                globalNotebookName = panel.title.label.split(".")[0];
                globalPanel = panel;

                if (atlasId) {
                    panel.toolbar.insertItem(11, "chatlas", button);
                }
                globalApp = app;
                const chatlasDropdownMenu = new ChatlasDropdownWidget(atlasId)
                panel.toolbar.insertItem(10, "chatlasActions", chatlasDropdownMenu);

                chatlasDropdownMenu.menuOptionChanged.connect(async (_: ChatlasWidget, menuOption: string) => {
                    if (isEqual(menuOption, 'set')) {
                        const newAtlasID = await showDialog({
                            body: new EditSettingsWidget(atlasId || ""),
                            buttons: [Dialog.cancelButton(), Dialog.okButton({ label: "Save" })],
                            focusNodeSelector: "input",
                            title: "Settings"
                        })

                        if (newAtlasID.button.label === "Cancel") {
                            return;
                        }

                        if (isEmpty(newAtlasID.value)) {
                            INotification.error(`Please, insert a valid Atlas Id. Visit help.voiceatlas.com for more information.`, { autoClose: 3000 });
                            return;
                        } else {
                            console.log(`Saving Atlas ID => ${newAtlasID.value}`)
                            panel.model?.metadata.set('atlas-id', newAtlasID.value)
                            app.commands.execute('docmanager:save')
                            globalAtlasId = newAtlasID.value;
                            panel.toolbar.insertItem(11, "chatlas", button);
                        }
                    }
                    if (isEqual(menuOption, 'delete')) {
                        panel.model?.metadata.delete('atlas-id')
                        app.commands.execute('docmanager:save')
                        panel.toolbar.layout?.removeWidget(button)
                        globalAtlasId = undefined
                    }
                })
            })
        }
    })
}


export default plugin;