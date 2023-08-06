import { Dialog, showDialog } from '@jupyterlab/apputils';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { INotification } from "jupyterlab_toastify";
import isEmpty from 'lodash.isempty';
import { requestAPI } from './handler';

import { EditSettingsWidget } from "./widgets/EditSettingsWidget"

export function loadSetting(setting: ISettingRegistry.ISettings): string {
    // Read the settings and convert to the correct type
    let atlasId = setting.get('atlasId').composite as string;
    console.log(
        `Atlas ID Loading Settings = ${atlasId}`
    );
    return atlasId;
}

export async function configureNewAtlas(settings: ISettingRegistry, pluginId: string, atlasId: string | undefined = undefined, pathToNotebook: string | undefined = undefined): Promise<any> {
    // Load the current Atlas ID from settings
    let currentAtlasID;

    if (atlasId) {
        currentAtlasID = atlasId
    } else {
        currentAtlasID = await Promise.all([settings.load(pluginId)])
            .then(([setting]) => {
                return loadSetting(setting);
            }).catch((reason) => {
                INotification.error(`Could not get the configuration. Please contact the administrator.`, { autoClose: 3000 });
                console.error(
                    `Something went wrong when getting the current atlas id.\n${reason}`
                );
            });
    }
    console.log(`Atlas ID from Configure Atlas => ${atlasId}`)

    // Pass it to the AtlasIdPrompt to show it in the input
    const newAtlasID = await showDialog({
        body: new EditSettingsWidget(currentAtlasID || ""),
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
    }
    if (atlasId) {
        let action = 'set';
        const saveNewAtlas = await requestAPI<any>('crud_atlas', {
            method: 'POST',
            body: JSON.stringify({ atlasId, action, pathToNotebook })
        });
        return saveNewAtlas.atlasId
    } else {
        // Save new atlas id in settings
        let newAtlasId = await Promise.all([settings.load(pluginId)])
            .then(([setting]) => {
                setting.set('atlasId', newAtlasID.value)
                INotification.success('Success', {
                    autoClose: 3000
                });
                return newAtlasID.value
            }).catch((reason) => {
                INotification.error(`Could not save the configuration. Please contact the administrator.`, {
                    autoClose: 3000
                });
                console.error(
                    `Something went wrong when setting a new atlas id.\n${reason}`
                );
            });

        console.log(`New Atlas ID => ${newAtlasId}`)
    }

}