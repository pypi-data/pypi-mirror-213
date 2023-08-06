"use strict";
(self["webpackChunkjupyterlab_voiceatlas"] = self["webpackChunkjupyterlab_voiceatlas"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-voiceatlas', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ButtonExtension": () => (/* binding */ ButtonExtension),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var lodash_isequal__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! lodash.isequal */ "webpack/sharing/consume/default/lodash.isequal/lodash.isequal");
/* harmony import */ var lodash_isequal__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(lodash_isequal__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _widgets_ChatlasWidget__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./widgets/ChatlasWidget */ "./lib/widgets/ChatlasWidget.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _widgets_AboutVoiceAtlas__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./widgets/AboutVoiceAtlas */ "./lib/widgets/AboutVoiceAtlas.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _widgets_ChatlasDropdownMenuWidget__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./widgets/ChatlasDropdownMenuWidget */ "./lib/widgets/ChatlasDropdownMenuWidget.js");
/* harmony import */ var _widgets_EditSettingsWidget__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./widgets/EditSettingsWidget */ "./lib/widgets/EditSettingsWidget.js");
/* harmony import */ var lodash_isempty__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! lodash.isempty */ "webpack/sharing/consume/default/lodash.isempty/lodash.isempty");
/* harmony import */ var lodash_isempty__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(lodash_isempty__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var jupyterlab_toastify__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! jupyterlab_toastify */ "webpack/sharing/consume/default/jupyterlab_toastify/jupyterlab_toastify");
/* harmony import */ var jupyterlab_toastify__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(jupyterlab_toastify__WEBPACK_IMPORTED_MODULE_8__);
// import { SplitPanel } from '@lumino/widgets';

// import { PageConfig } from "@jupyterlab/coreutils";















const PLUGIN_ID = 'jupyterlab_voiceatlas:plugin';
const plugin = {
    id: PLUGIN_ID,
    requires: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_0__.IMainMenu, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__.INotebookTracker],
    autoStart: true,
    activate
};
let globalAtlasId = undefined;
let globalNotebookName;
let globalApp;
let globalPanel;
const openChatlas = () => {
    console.log(`Calling Chatlas => ${globalAtlasId}`);
    const content = new _widgets_ChatlasWidget__WEBPACK_IMPORTED_MODULE_9__.ChatlasWidget(globalAtlasId, globalNotebookName);
    content.title.label = `Chatlas - ${globalNotebookName}`;
    const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
    widget.id = `chatlas-${globalNotebookName}`;
    console.log(`Current Notebook Panel Info => ${globalPanel.id}`);
    globalApp.shell.add(widget, 'main');
};
let button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
    label: "Chatlas",
    onClick: openChatlas,
    tooltip: "Open Chatlas.",
});
class ButtonExtension {
    createNew(panel, _) {
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_6__.DisposableDelegate(() => {
            button.dispose();
        });
    }
}
async function activate(app, mainMenu, settings, notebookTracker, panel) {
    console.log('JupyterLab extension jupyterlab_voiceatlas is activated!');
    console.log('The correct one!');
    const { commands } = app;
    const openChatlas = 'voice-atlas-jlab-ext:openChatlas';
    const editSettings = 'voice-atlas-jlab-ext:editSettings';
    const createNewAtlas = 'voice-atlas-jlab-ext:createNewAtlas';
    const aboutVoiceAtlas = 'voice-atlas-jlab-ext:aboutVoiceAtlas';
    const helpVoiceAtlas = 'voice-atlas-jlab-ext:helpVoiceAtlas';
    (0,_handler__WEBPACK_IMPORTED_MODULE_10__.requestAPI)('get_example')
        .then(data => {
        console.log(data);
    })
        .catch(reason => {
        console.error(`The jupyterlab_voiceatlas server extension appears to be missing.\n${reason}`);
    });
    Promise.all([app.restored, settings.load(PLUGIN_ID)])
        .then(([, setting]) => {
        (0,_utils__WEBPACK_IMPORTED_MODULE_11__.loadSetting)(setting);
    }).catch((reason) => {
        console.error(`Something went wrong when changing the settings.\n${reason}`);
    });
    commands.addCommand(openChatlas, {
        label: 'Open Chatlas',
        caption: 'Open Chatlas',
        execute: async () => {
            let atlasId = '';
            await Promise.all([settings.load(PLUGIN_ID)])
                .then(([setting]) => {
                atlasId = (0,_utils__WEBPACK_IMPORTED_MODULE_11__.loadSetting)(setting);
            }).catch((reason) => {
                console.error(`Something went wrong when getting the current atlas id.\n${reason}`);
            });
            if (lodash_isequal__WEBPACK_IMPORTED_MODULE_4___default()(atlasId, "")) {
                atlasId = await (0,_utils__WEBPACK_IMPORTED_MODULE_11__.configureNewAtlas)(settings, PLUGIN_ID);
                return;
            }
            const content = new _widgets_ChatlasWidget__WEBPACK_IMPORTED_MODULE_9__.ChatlasWidget(atlasId, globalNotebookName);
            content.title.label = 'Voice Atlas for JupyterLab';
            const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
            app.shell.add(widget, 'main');
        }
    });
    commands.addCommand(editSettings, {
        label: 'Edit Settings',
        caption: 'Settings',
        execute: async () => { globalAtlasId ? await (0,_utils__WEBPACK_IMPORTED_MODULE_11__.configureNewAtlas)(settings, PLUGIN_ID, globalAtlasId) : await (0,_utils__WEBPACK_IMPORTED_MODULE_11__.configureNewAtlas)(settings, PLUGIN_ID); }
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
            const { aboutBody, aboutTitle } = (0,_widgets_AboutVoiceAtlas__WEBPACK_IMPORTED_MODULE_12__.aboutVoiceAtlasDialog)();
            const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: aboutTitle,
                body: aboutBody,
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.createButton({
                        label: 'Dismiss',
                        className: 'jp-About-button jp-mod-reject jp-mod-styled'
                    })
                ]
            });
            if (result.button.accept) {
                return;
            }
        }
    });
    commands.addCommand(helpVoiceAtlas, {
        label: 'Help',
        caption: 'Help.',
        execute: () => {
            const url = "https://help.voiceatlas.com";
            window.open(url);
        }
    });
    const menu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Menu({ commands: app.commands });
    menu.title.label = 'NLP';
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
        var _a;
        if (panel) {
            (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.update();
            panel.context.ready.then(async () => {
                var _a;
                let atlasId = (_a = panel.model) === null || _a === void 0 ? void 0 : _a.metadata.get('atlas-id');
                globalAtlasId = atlasId;
                globalNotebookName = panel.title.label.split(".")[0];
                globalPanel = panel;
                if (atlasId) {
                    panel.toolbar.insertItem(11, "chatlas", button);
                }
                globalApp = app;
                const chatlasDropdownMenu = new _widgets_ChatlasDropdownMenuWidget__WEBPACK_IMPORTED_MODULE_13__.ChatlasDropdownWidget(atlasId);
                panel.toolbar.insertItem(10, "chatlasActions", chatlasDropdownMenu);
                chatlasDropdownMenu.menuOptionChanged.connect(async (_, menuOption) => {
                    var _a, _b, _c;
                    if (lodash_isequal__WEBPACK_IMPORTED_MODULE_4___default()(menuOption, 'set')) {
                        const newAtlasID = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                            body: new _widgets_EditSettingsWidget__WEBPACK_IMPORTED_MODULE_14__["default"](atlasId || ""),
                            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: "Save" })],
                            focusNodeSelector: "input",
                            title: "Settings"
                        });
                        if (newAtlasID.button.label === "Cancel") {
                            return;
                        }
                        if (lodash_isempty__WEBPACK_IMPORTED_MODULE_7___default()(newAtlasID.value)) {
                            jupyterlab_toastify__WEBPACK_IMPORTED_MODULE_8__.INotification.error(`Please, insert a valid Atlas Id. Visit help.voiceatlas.com for more information.`, { autoClose: 3000 });
                            return;
                        }
                        else {
                            console.log(`Saving Atlas ID => ${newAtlasID.value}`);
                            (_a = panel.model) === null || _a === void 0 ? void 0 : _a.metadata.set('atlas-id', newAtlasID.value);
                            app.commands.execute('docmanager:save');
                            globalAtlasId = newAtlasID.value;
                            panel.toolbar.insertItem(11, "chatlas", button);
                        }
                    }
                    if (lodash_isequal__WEBPACK_IMPORTED_MODULE_4___default()(menuOption, 'delete')) {
                        (_b = panel.model) === null || _b === void 0 ? void 0 : _b.metadata.delete('atlas-id');
                        app.commands.execute('docmanager:save');
                        (_c = panel.toolbar.layout) === null || _c === void 0 ? void 0 : _c.removeWidget(button);
                        globalAtlasId = undefined;
                    }
                });
            });
        }
    });
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/style/IconsStyle.js":
/*!*********************************!*\
  !*** ./lib/style/IconsStyle.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "voiceAtlasIcon": () => (/* binding */ voiceAtlasIcon),
/* harmony export */   "voiceAtlasWordmarkIcon": () => (/* binding */ voiceAtlasWordmarkIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_voiceatlas_logo_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../style/voiceatlas_logo.svg */ "./style/voiceatlas_logo.svg");
/* harmony import */ var _style_VoiceAtlas_Wordmark_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../style/VoiceAtlas_Wordmark.svg */ "./style/VoiceAtlas_Wordmark.svg");



const voiceAtlasIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({ name: 'logo', svgstr: _style_voiceatlas_logo_svg__WEBPACK_IMPORTED_MODULE_1__["default"] });
const voiceAtlasWordmarkIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({ name: 'wordmark', svgstr: _style_VoiceAtlas_Wordmark_svg__WEBPACK_IMPORTED_MODULE_2__["default"] });


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "configureNewAtlas": () => (/* binding */ configureNewAtlas),
/* harmony export */   "loadSetting": () => (/* binding */ loadSetting)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var jupyterlab_toastify__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jupyterlab_toastify */ "webpack/sharing/consume/default/jupyterlab_toastify/jupyterlab_toastify");
/* harmony import */ var jupyterlab_toastify__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jupyterlab_toastify__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var lodash_isempty__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! lodash.isempty */ "webpack/sharing/consume/default/lodash.isempty/lodash.isempty");
/* harmony import */ var lodash_isempty__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(lodash_isempty__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _widgets_EditSettingsWidget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./widgets/EditSettingsWidget */ "./lib/widgets/EditSettingsWidget.js");





function loadSetting(setting) {
    // Read the settings and convert to the correct type
    let atlasId = setting.get('atlasId').composite;
    console.log(`Atlas ID Loading Settings = ${atlasId}`);
    return atlasId;
}
async function configureNewAtlas(settings, pluginId, atlasId = undefined, pathToNotebook = undefined) {
    // Load the current Atlas ID from settings
    let currentAtlasID;
    if (atlasId) {
        currentAtlasID = atlasId;
    }
    else {
        currentAtlasID = await Promise.all([settings.load(pluginId)])
            .then(([setting]) => {
            return loadSetting(setting);
        }).catch((reason) => {
            jupyterlab_toastify__WEBPACK_IMPORTED_MODULE_1__.INotification.error(`Could not get the configuration. Please contact the administrator.`, { autoClose: 3000 });
            console.error(`Something went wrong when getting the current atlas id.\n${reason}`);
        });
    }
    console.log(`Atlas ID from Configure Atlas => ${atlasId}`);
    // Pass it to the AtlasIdPrompt to show it in the input
    const newAtlasID = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
        body: new _widgets_EditSettingsWidget__WEBPACK_IMPORTED_MODULE_3__.EditSettingsWidget(currentAtlasID || ""),
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: "Save" })],
        focusNodeSelector: "input",
        title: "Settings"
    });
    if (newAtlasID.button.label === "Cancel") {
        return;
    }
    if (lodash_isempty__WEBPACK_IMPORTED_MODULE_2___default()(newAtlasID.value)) {
        jupyterlab_toastify__WEBPACK_IMPORTED_MODULE_1__.INotification.error(`Please, insert a valid Atlas Id. Visit help.voiceatlas.com for more information.`, { autoClose: 3000 });
        return;
    }
    if (atlasId) {
        let action = 'set';
        const saveNewAtlas = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('crud_atlas', {
            method: 'POST',
            body: JSON.stringify({ atlasId, action, pathToNotebook })
        });
        return saveNewAtlas.atlasId;
    }
    else {
        // Save new atlas id in settings
        let newAtlasId = await Promise.all([settings.load(pluginId)])
            .then(([setting]) => {
            setting.set('atlasId', newAtlasID.value);
            jupyterlab_toastify__WEBPACK_IMPORTED_MODULE_1__.INotification.success('Success', {
                autoClose: 3000
            });
            return newAtlasID.value;
        }).catch((reason) => {
            jupyterlab_toastify__WEBPACK_IMPORTED_MODULE_1__.INotification.error(`Could not save the configuration. Please contact the administrator.`, {
                autoClose: 3000
            });
            console.error(`Something went wrong when setting a new atlas id.\n${reason}`);
        });
        console.log(`New Atlas ID => ${newAtlasId}`);
    }
}


/***/ }),

/***/ "./lib/widgets/AboutVoiceAtlas.js":
/*!****************************************!*\
  !*** ./lib/widgets/AboutVoiceAtlas.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "aboutVoiceAtlasDialog": () => (/* binding */ aboutVoiceAtlasDialog)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_IconsStyle__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/IconsStyle */ "./lib/style/IconsStyle.js");


function aboutVoiceAtlasDialog() {
    const versionInfo = (react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { className: "jp-About-version-info" },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { className: "jp-About-version" }, "1.0")));
    const aboutTitle = (react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { className: "jp-About-header" },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_style_IconsStyle__WEBPACK_IMPORTED_MODULE_1__.voiceAtlasIcon.react, { margin: "7px 9.5px", height: "auto", width: "58px" }),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "jp-About-header-info" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_style_IconsStyle__WEBPACK_IMPORTED_MODULE_1__.voiceAtlasWordmarkIcon.react, { height: "auto", width: "196px" }),
            versionInfo)));
    const externalLinks = (react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { className: "jp-About-externalLinks" },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("a", { href: 'https://voiceatlas.com', target: "_blank", rel: "noopener noreferrer", className: "jp-Button-flat" }, "About Voice Atlas")));
    const copyright = (react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { className: "jp-About-copyright" }, '© 2019-2022 Voice Atlas by Navteca LLC'));
    const aboutBody = (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "jp-About-body" },
        externalLinks,
        copyright));
    return { aboutBody, aboutTitle };
}


/***/ }),

/***/ "./lib/widgets/ChatlasDropdownMenuWidget.js":
/*!**************************************************!*\
  !*** ./lib/widgets/ChatlasDropdownMenuWidget.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ChatlasDropdownWidget": () => (/* binding */ ChatlasDropdownWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);




;
const ChatlasDropdownMenuComponent = (info) => {
    const [selected, setSelected] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)("");
    function _onSelect(event) {
        event.preventDefault();
        const newValue = event.target.value;
        setSelected(newValue);
        info.signal.emit(newValue);
        console.log(`Selected Option => ${newValue}`);
    }
    console.log(`Info => ${info.atlasId}`);
    const TOOLBAR_CELLTYPE_DROPDOWN_CLASS = 'jp-Notebook-toolbarCellTypeDropdown';
    const options = [
        { value: 'set', label: 'Add/Modify Atlas Id' },
        { value: 'delete', label: 'Remove Chatlas' }
    ];
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.HTMLSelect, { className: TOOLBAR_CELLTYPE_DROPDOWN_CLASS, onChange: _onSelect, value: selected, "aria-label": 'Chatlas Actions', title: 'Chatlas Actions' },
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("option", { value: "", disabled: true, selected: true }, "Chatlas Actions"),
        options.map((item, _) => {
            return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("option", { value: item.value }, item.label);
        })));
};
class ChatlasDropdownWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(atlasId) {
        super();
        this._signal = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this.info = {
            atlasId: '',
            signal: this._signal
        };
        this.info.atlasId = atlasId;
    }
    get menuOptionChanged() {
        return this._signal;
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_1___default().createElement(ChatlasDropdownMenuComponent, Object.assign({}, this.info));
    }
}


/***/ }),

/***/ "./lib/widgets/ChatlasWidget.js":
/*!**************************************!*\
  !*** ./lib/widgets/ChatlasWidget.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ChatlasWidget": () => (/* binding */ ChatlasWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);

class ChatlasWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(atlasId, notebookName) {
        super({ node: ChatlasWidget.createChatlasWidget(atlasId, notebookName) });
    }
    static createChatlasWidget(atlasId, notebookName) {
        const script = document.createElement('script');
        script.setAttribute("src", "https://bot.dev.voiceatlas.com/v1/chatlas.js");
        script.setAttribute("async", "");
        document.body.appendChild(script);
        // Verify if custom element already exists
        // if exists change attribute
        // else define it
        const chatlas = document.createElement('app-chatlas');
        chatlas.setAttribute('name', notebookName);
        chatlas.setAttribute('id', notebookName);
        chatlas.setAttribute("atlas-id", atlasId);
        chatlas.setAttribute("full-screen", "true");
        chatlas.setAttribute("voice-enabled", "true");
        document.body.appendChild(chatlas);
        return chatlas;
    }
}


/***/ }),

/***/ "./lib/widgets/EditSettingsWidget.js":
/*!*******************************************!*\
  !*** ./lib/widgets/EditSettingsWidget.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EditSettingsWidget": () => (/* binding */ EditSettingsWidget),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var lodash_isequal__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! lodash.isequal */ "webpack/sharing/consume/default/lodash.isequal/lodash.isequal");
/* harmony import */ var lodash_isequal__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(lodash_isequal__WEBPACK_IMPORTED_MODULE_1__);


class EditSettingsWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(atlasId) {
        super({ node: EditSettingsWidget.createSettingsWidget(atlasId) });
    }
    static createSettingsWidget(atlasId) {
        const body = document.createElement("div");
        const existingLabel = document.createElement("label");
        existingLabel.textContent = "Atlas ID:";
        const input = document.createElement("input");
        input.classList.add('input');
        input.value = lodash_isequal__WEBPACK_IMPORTED_MODULE_1___default()(atlasId, "") ? "" : atlasId;
        input.placeholder = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx";
        body.appendChild(existingLabel);
        body.appendChild(input);
        return body;
    }
    get inputNode() {
        return this.node.getElementsByTagName("input")[0];
    }
    getValue() {
        return this.inputNode.value;
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (EditSettingsWidget);


/***/ }),

/***/ "./style/VoiceAtlas_Wordmark.svg":
/*!***************************************!*\
  !*** ./style/VoiceAtlas_Wordmark.svg ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<svg width=\"808px\" height=\"107px\" viewBox=\"0 0 808 107\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n    <title>Bitmap</title>\n    <g id=\"Page-1\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\n        <image id=\"Bitmap\" x=\"0\" y=\"0\" width=\"808\" height=\"107\" xlink:href=\"data:image/png;base64,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\"></image>\n    </g>\n</svg>");

/***/ }),

/***/ "./style/voiceatlas_logo.svg":
/*!***********************************!*\
  !*** ./style/voiceatlas_logo.svg ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<svg width=\"108px\" height=\"108px\" viewBox=\"0 0 108 108\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n    <title>LogoBlue@108</title>\n    <g id=\"Page-1\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\n        <image id=\"LogoBlue@108\" x=\"0\" y=\"0\" width=\"108\" height=\"108\" xlink:href=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGwAAABsCAYAAACPZlfNAAAABGdBTUEAALGOfPtRkwAAADhlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAAqACAAQAAAABAAAAbKADAAQAAAABAAAAbAAAAADaE/gkAAAnbUlEQVR4Ae19CWAcxZV2VXX3HBqdluUD2WBjsMHmiGNCuLI4PrGDneUY3xw2rCG7gQAhkF0WEJAf/j/8SQhZQnDC6QukmBsbH4AIdxLDgrGNbWx8X7J1S3N0V9d+r6WxR9JMz0jWSCJLGzEzfVS9el+9V++9elXN2dfkUEoJkBqor6/36abpN3XdJyzLZwnhMRizcV3SHzMM5zs1i3OuMdMU9El/JmNCt+2orethw7LClmGEs7OzQ7i1AddteqanH7ynEgjmE205oVAoV0pJf34hRIMhZViC0YFoNMQKCsJgdKQ9bUC5XlZV5WvwePyaafpMTfPZth3QNC2Ev1q/31+L8upQrmpPuV11b48CjECqra0tALN6g4k5BBAxMSsrqw4Mqc8UE5s7R3ZjY2MOdQ4CEHXX4fyh3NzcqkzV2xGQewRgYExOuKamN3RSgRSivrsZRQDGOo5m29nQxVW+vLxDAI46Trce3QoYmFKIceg4ZRgSzDgcCAQO49PqVo60qhzg6Q0NDYX4LOSmqWH82wupO9zqti772eWAUe+F4dCbAyhb08I5OTn7ABKNGz3+AO25dXV1/dHJvOhk+2CwkNR16VjXpYA5EiXlAAAVAlB70NiGHo9SAgIBXADAFQsYQmjL7q6UuC4BDA30oYGDSKVk9+q1DUCRKf21P9Auf31l5Ymk0tEBt6Nd4Uw3KqOAoUECZvlxKhIpgu7fg0YdzHSDuqN8dMY+UJPF3OutgFuwF8BlzKfLGGAAK6uhqmoIHNuGvLy8nWhEjzImOhtYtFeHpTtQwqoMFBRsRXsbO7sOKi8jgMV6XBZjX/GCgupMEN5Ty1RVVflAavDXQqOQCqyurh5Sd/jwCHz39lSmZpouajvxgHhBPMl0fR0qH4R56iorTwtVVZ2A7xmR3A4R1k0PEQ+IF8QT4k03kZG4WhDkr6+qOhNme+/Ed/zvPUs8Id4Qj3oEF0BINoyLkTU1Nb16BEE9kAjiDfGIeNWt5IEAX01l5Q+gqwu6lZCvQeXgVW4zaL5uITcmWfjM6RYCvoaVEq/QwScT77qUfFTob+4tuV1a8T9AZaSNmnnXNWMawPLQIPrNmNXx3kO8azZEMms9AixBZuo31mDHwYo9STxsNvkz56eRI0i+RazSbz6PjQPES+Jpe0pJ28GlcBOLRosQbd+AOJnrHFAwWOqp1uR0IbVNfXx56xcunPi1nEZpDyPp3qkzl/S1mOeCCLP3yn0b/lZeXuIaP4XG4oj2D2ceT0W6gXE9HaJQcFZjdXVxVhpgsWBQCzPrbKbErxQmjPaFqzaOnbH0LSjrVw/m1n6+dsF1SF76xzmC15T2qqpl5zImpzZa7Byh82Iu5d+swMmz0Moqt5ZSx8fxJXg7HJ+Us5IyYJxSwlCQgFUzIsD5rnQCuedPfTzH7/MvElyfatsWUs0EAvZao7KtaiXEh4rZLxVIbXVZ2bQKt8b09GtTZi4ZEVb8h0yqSVzoJ4GRuYpZPqUY0ur0iM2sH1V9Wbdo7drUHZQCxg1KDUSUfz1Ac52aSQkYMokGRKNRT35+/rZUTBw9+i1d77dnmlDG47aSPgbqnQkBqoVaoulhrnidzeUWbosXmDeybNXCK79KVW5PuT56dInu6z/8HHTEmcrm49GePrYtA+iETZrKaS9arGmUKfm51O2L31wyeye1PlUbQtXVg5XHYyJDbLfbva6AQbp8ENdTs/Lz1wF5V31MlYy+dNEAXRMruRDDlS1d6hVKIJmTSblX2eo5PcCfWPH0jK0uD3TvpZIScdEXw74vFbuOKT4W7cuxpYX81eQ4CM2rbDvyK+tg9M7y8rkpZ6LBax28Ph283gheJ73fFTCYnqfg4cp0BsRJkx72WjmFdwjNc4e0ommZqigbvdEI2VLuUkw+7VXRJ5aXzd3fvei0rH3MrMVna5Z+A2dqMhMiF0BBmpIDFXua2gZZqzK8bNLyhZv+xliJq6qj58iwA3C9kCPyRayc1p9JAQNYlNbVL6ewcH3rh9r+LhHjZw0/g1v2KsVUkVIpaWtRBLVN6N56ZckNXNm/PaGgtmxBNxsnk68u7Wc2yptA6BVcE0W2RRLVvkPTPMyW0ecP1MgrP1t1ZVqWsjOXaBj7kyX2JAQMKPOG6uozAvn5m9FTUibMjJryWFahL/ePXNNnSRltX6vi7kb6u82FVoPxb2mWLR5+uWzaprjLXfIVLolWI+xJNrNvEcI4B0AhhNS+DtiCUKGZnMnZ5oEtL6Qy8+k58N4P3g8F7z8D79uIckLVRXmDlIqWDlg0EOcHcidz3QiiMlSZsA+0aEOyH1jLINAjKVV7XkizF4+9fPFs8umS3d/Z5yfNXjSgSrcegJ5+FG7JP9lW9JjAgoXMdM1rMFsr8fc6vR/oTckc4jnxnjBI1L6EgFGSJ8atPYkeaH2uqGg43C1VwWz7T2D4pyAprOleqHvSICnpa12c81tJywcPZaSuex+sZNYvpwSfOT7hjZ14csLMJWMsS3tKs7V/xThVzJSEqdf+g0AiVSg0tJ+zQ9IKrwZfSiGjblZYi4qI9xiO+rc42fyjDUdp7MK1IreBr01BUCOjAw1GIOrxS9MYYWtyHLQI1IoaCeINW5oQ9Y6oFViTmmiE5L6nCfu+15fOerdN3cd4AhLsR1RmHtyNn9g2OxF87RBQQujkc6LfWocFV+8oW381qlvvmTtDew7kNkS/XHEjjRVtVFwy8oHDMFyjxRgt0sLbAIZQyelw4HZANDuYPl0iTprUyxjgzfF7jMB3MB4F4f3/gCvtODiTDLZuMhqTn+e6hXFgMwa4+7936hdLS0pSW1zJCzt6ZfLVT/azGrNvY5qaZVt2H4DVhh9H7070jUOT6EDBZtAIH+NXaUg1Lj9c0fiVr06PrF07H65Q23EoUUmtz6GT0oTnCQgFrou/1oJA3JQD3TkQIrkh/qa0vkPKxonod7KEaHx56SyqRDGcGxWu8hb5CgYqLmdLLmYJJoYgItB+4LhQmjB22rb5qC9U+7tXXrkuZRjHje4ply05JazzewUXE2mJUTs6v1MsqXy4InDN+F80Lp6MNFgrKnx67fqyIEJvXGE8zLWVMQpLlzatfnbmPocfbgQluAYzfzjy93dBeI6smmkBGHnbUtcbcdOBBM+7neITgqWDmLBW2zbP54K/r9nqeREIv778Kcev4gOCpb4TQw0D/NlZM7BEcp7g2iAKXbVPVZLDrR2Eil3o1fPuf23Jxa6xumQETwwuPttk4n5NiPPg4MOwSFtTNUkUjCvFVTmz1KPKNt+o3vle7dq1C5wY6cXTF54ZYsalwrYna4ZvmGVGFjWwfT/9oOyWlNZ2a3ohPH01y8ry5+d/Fbt2BDBIF2+sqRmZlZdH5mTKqEasAPocPfpJn97Hc58Q3p/CykMgQJOwtMLMNndCAS7zZxmLX3nqcscZBHD+YdHoYOET85XSrsJa1nxptyceDEnTtCpIWin3yrsR2mpX+vekmaUXWrZ9P3y/s+Cwp22B0viETgblp6A95MNmY86LrG5tNZnqo+Y/ZhTV54+xpT0XHXaMMLQc+JQeqErEFUWtR5oXv8a977OyaWkbHsRXYKIDkzOAySfAxOlVRwCjWVCc7I1BbjPdnP6BsM30U0ZBN7wOf6UXKol7lIwGI6rsKAV6lxg+8fjyZ2ZQ+fz8qS9l52fXnxW19NvBvIkkaelLG4clpldBry6TeeLWNQum1cRVmvTruOCi0xGYfRw3IINJNsX/kt599AKpP2iFGhgTC2zN+MO+T+Xu9eunRclnqzPUOGnZ14F3Y+H+Z0FrtIiEIPIDQ8R8LRQOzXzv5WuOqLajpbt/g/ExFDw9hHT3SrrzCGCtL7gXc/QqOc29fDlLAczUpE4zENG4B6vGzQNwjhcYNnt0edk0JwQ1YcIzAbtAn4cB+w704b5pSxvKxIwAgtzmfUoZf1hT5g6aA5bQ74T2uxxgHWn30Za0/QYQYPnBqODqbSXlf1Ztq/soFn0fO7P0XM2St6NhE+GzYZ10ci3hGCZKXlG5te652PNta0t8prUgOYSTOsSFbwPFj2Oil/jxlmfJadZ7nzJVaKwMUeuEPl38E9CVxGSs9pcb0RMfKGAvPVdWViapHKNw2LeUzn+pMYEgKzRyC0mNLyXuuwOatkfa1oNZBbl/fGXBlISGyEXBhcOkMO4AWDPTlSyodZDgLHh/yNSq/3/50usOUc0TL13YH7sP/FQodS3UXR6s4JS0EmDgzwaLRcaWtzNW2hqbGJOdBeDtAYuI1wrOyGNc3gFVECuHTic9yKSX0tSgNE/Dbg1/quKXPT1p+rNDaBxYvWzm3yN243Qw4GFYbjaNGSkPGvwZK4Z6vCFUWTd9PsaS1s9MmLF0oMW1G8HVIO5OSw02O/37bWFfZR5sLImBNW764h8q3Vihc+0m1JtHRlM6HYvu03TPcA/zXnMSguStaXT7TZjQ4nzc46QTOlyhrRV0XW+3ftW18BXQ0d92UwdtiQHbMPViK8sPc3gm+udrY4NLL6f73imbV8Grzf8AsPegE9RTL091YGKUeDZE08UN2yqzJ4ODR9TdD2YtLpCSkyTMBrKYn0vtA2qIUIDCdUpZ18j9m5bR1EhwfmneuMuXPgjFvgiln0mdLp2y4mmn4AEGoJ8M8uWfGH8+ne+0kwJhRPc6gJEf0rw/RTrPO/d8L/hEEZTg7TEPP+0HYzeCy1Bl0CxsmC7EE+OmLb4vGHzfvwpRbcXqfgsL6xbF+UEqP9VBoNmKjYRk/Nv4aYvPo/tpuidishkw0+bhZ146Bg2BhXLKpR2+Nl8ZK0nyJ162ZERVjf1ndOgbUUZ20zxfvGGVijq6TmMh4oqe7CKmGTen80T8PbTtRZOvyJgOHSkwfsEXYfXxN6X6nh82G0JZ3uutaAhjGB/PhTGQ9FO7pQ1jgGQiByGsW6vljqHjpy69eXXZzL2jpryyON9XU6sJ/UGANtBRPy5EESCYsxqDIN5eqNn9lm2OwIzwtegQA9wnU5sKhVOO2X75qhTq5289dyUCB1xNDC65CNsb/Baux0koT6Sj/uJJJJAcCxOb72Ds/CQSbXhJKHNF/D1pfq8HYH7CirJAcuBRF7crdtiyFj7hkueLMN1/MXg/FxbVBQ6R7Z1mIUtS6CYI+xDey9w3n5ux9dzgr/05vHii4vZDsAlPSAUaA4PQlyuhbt8Gq3pBfV2YDpMdsJj9om6Ln7/ePKUz7rIll3FdPAIV2xez4mhx+lLlAAVpxURuteDsJcm0p0HMe8hjoXhihw5Y8ac4QWGAVaRbVsBfULC9QyXFPdRk7Z06QWk2ZmjZRTDh2ydxTVafBIPewKZQt6xcOmv9uXC0A8pGogt7GANwcWrQAC3+YRwCVqkZ3aQG1Svcarxt1bK5jnM/dtoiOPR6CR4fBMmIa2GKr06nc/yuw+g4C6HzH1u1bDP8zmOPfSKHcZCFKBQPVVYeLz2eKMJRHZqanzBhZUDmHriR6/4P1jx7+dukSgg4rc+pF4Ntt2NC8pwmwyD1gN/EDjRVCArvvwNm3bSmbM468tWsPO1SjWsPgSe9YCKn4Fx6lwks9I5yJeyfvNEc/5wQXHoN9NhdtrKPb49hQdMpMJYiMOoWQTn/as1zX2DytQmoycHS0yM8+u396sul68tKOiRlCFP105AMRVv0DMUGSwfTSWFrzYZRox4zCk7KmaML3xO0ZxdT2ptCqEdybfEqxF+OCJZm9+fyepjptwHIovTHtybQIKVvC1v8mNTU6H9+Mt8wPFdhjHoAYEKfp9sBWlPd9NtR20x+JiT7UR7XPiJ6YbZfCdPgHoA1KF2wIPXkW4Ik+QFmqe8qUMZbVBbVMi64BMMD/xE06lSMw9lYsH6JPLjx1XRmnltTrSor8+p0vS9lnp6B6ZRNqDjS+qZUv8cEny7WmPEWpOhkUlXOpB1GePDyDVhn/3dl6fS30MvExEuGnG57Pb8Wio/B+ILGpTMegBFCi+BWZGE1/HjVs/N2jQ6W9tOZhal7/jO7neNKfFuanGK1D1rzer0+b+WKFZMjY4KLLtE1/f+B+pPTTQloKoeF0Xl+Z9Tn/wLlOFNS44OLvwWz8DZE8i8BUD4y6WEAIb/DXAtvZuIbL1zaYo4rnrZk38EzL6ZbhlGWp6cjYFHBnBnzhe5xwKLfRBjUFTSXmIDetmL8tOcenTDj+OKVL1zxqZB1QYpIwLSg6DDdnuKAYa+kFw0fo6T/3nHBx/LKEc6ymFwARjwPZznF84kvk0EAoCIYJx9QTHubwBo/bdH5MHjuREc7KV2wyFCB6tuqWHgOwLqTwPrnq1/IHzd9yS+g06FpjJnomQCLNCDa4oDmGaUZkdmJKXM/SxgRVqgW9XbgGHPp4hMgRT8mQlofdI56BCTvOmR5rxk3/dlLV5ZdW9nA9LshGf8ChVeRjn+FQvCfzBaadjHjgVuDQaWVj9i6jUv1K4SvNqRVRiviKOKuhHoyaoZfpPjjhCtKB0OV3wOmYvG4DS2c+qAUALj+5Z6weckalfUigT5uxtLRDaHwagD57ygLDnsTUPGlkQGDFt06euaShPka8fcm+k5YwXFtjxnUXAyi1PBn74UKRHQ+Gd7UqyLEgKGYGFgKM/kBuOr+fRvFs/B3pgOLdXg+tfWA8qUtewvuubLKXjgvuH44Z7Xmp8gjvh91VwH8RG1LeA5WK0qz/mKb6tG/vDRv98RgaS87YpVA4r8LPoAfqVQ1qWlPBGPxkxHDnLX8pTnrR7MKPzrkz5jNX8bVsygnE2UlrJ/8QUSGBurSRjivJB0106IcwqpDgE1i1gUgbgaIa1Fgoh9EJBjrQWrHTZLbC/qeVjWwemv9u1znc5W0P4allhZooHUgQgXXIynnbERDkKsfKceY+AwmS5P1mBbkELDo3bRV7O8axf4tSCvHHKv5L+h5E2BkZJM0ux8ElhHBMwtCDeqn7yyasx/WXx9D9HpIY3oJZ3ZOSpcDFTRpJP2acTMGn+leX9urDmC0R27bS4nP4AFO0ylRru7FAgBM/qVqZKwcmkw3fZrQpmoq74m+JxacsmpT1WeYCJxvW/ITDMgpaaC6IUunQg3fjIUIhW+WXbkXpS7EeLbdGZdiVSX7hL2NwbVcNbL3MfsbNvodupDr2hVw1PulYxFCG0QVM/9gRSN3vfvalpox058+0WTWnwQ35kgVzQJ9yWpucZ40EjpJDrONu2gtArWrxQ1uP4BVuyTsnnvu4QXe3LNhOJyJHhsFo9KjkohAgzDXZUAtnWcK+fikQbmnVW6rX2/o7EcgeiM6QIqyHEcY+/7qF8CBuCoYLBMNkfBmFPs6+o2rqBNH8HQERs/nullxePTVpX25tG5AvTAyUlSLZ9E3TYQtngrVq3vKX7y65qI5Q04WyvdHdLQJ0o56U0snMSB2OJJugnfjtaJ93yGexq6k+gS9qeew4gu5++67oVO0j3RujUcuwyMgdA+mDQBcmnWCu1ApOgAfiXnZx3oPzRm6Y532mYCDjDSzPSmtR2c8s/pBqmZVa+GRNIOLtVivwRH6FEAm5TxdQAfzwXj5VsRf2M9TH52LFSYYtximOpI+5jQdBgaGUMwYS6vk3ddmV5Nkyajn95jyuAAdAN6y+/NH+QeVqhkAilcyhfQGxoKc6RuIp0fvSf2NU2ZOh7KkUPZFc0qHSdOeD6LnYGYWEYhoerY2OZuIGzLbetdW+tUNbHdFQB0XhMX9CCB1H0/oWa7VwnBZOjCr/03bq7f7PF7/rRiHADrD0p/E7Se1iev7LKUe0DibBx0MLeGujqgTINvrY00PzH590SdbJlxyYm9leKAGkWmlLE+6YGHso0nbBtT3si75fy1fNvOj1NC0vYOwErSve9tL6Z15fdG0Tauf++JnSIuZgvFoBVaiYFvyNIojSUPvxP3nMmb+Mt/TxzC81oswUB5BDM89AYieVTIXoH1/b2jPuPIX51ab0noLPf5jNwmlsQNKua8m1N2AaUQqsKgdeOaQsrWfV2zcv23KlFE+ZWj/B+PP2LTBQufShBcBCft9pYtp0YOb53YULAcR2oOfth/ILij4ND2Ikt9FQdpcZf2r0rXbwBlsY26lRo4apBl1MJN/Yx7of1+kaGffgNCfFswYg3MuehYKTogQxpUX67nnmgBjMICsn8HJhpSppFJG1DcDkbwhzVcwpmLex7zd5DWPsYqKsF409Gb4WHcgLyUvLcmCC4EG1Clu/V6zPQ+uLJvmJNGkrNjlBsIKRhc8yU44PiibFsrl+kOWFboCg+MX6flY6POWmQPH9XqjaPfk6LbwQZgx9yJagr3i3fAmA8T2Y9HcWbnMPJ0cYKjE9xAq+txNyqiZJGmpDgCDCuTb3G8vLC/7twaj90kXYvy7MV2woAKR4sB2IX3iWutA8Z2dARbRTFghLN4065yqEelcp6Dnm3/evoZ72XTY8X+lATud5xi3C9Gj/yPnlN59G8LhT5ActwjMd38WQxXGhWIp+Hk0u8wN8THGxL8i07Zt6CUtIppuoo4C7VCF7vL76K5tlUhl6w0z8S5UBvM/dUHkoqBTrOfSnLn6uS1IMfi+u4pPXeSROwgr510kkIh2JYYcKSHhlxJ71cLp65VRcxUk5UNIWoouTdICF4nrIzxm+Cfv1e7Cchu1FEmeX1BwNflBY5mdBe/qfDu/90mYHjkAg+JvkLAd7tKZvES6gjptZL08G7Hsj8qxMqeamzcAhJGoCwaVO2KYdQdW9jrDELNX/Xnrh7HpFfca07tKGNF7YwS9OIZVV1OKQCceXK1ect2Xmse8Bvl8MLmhYtwOGBJwrLFhlpgxofeQszW7fjNMumdIL7k9RlEpDBQjpSlH0TeYCf+NaBsc8qYsWddnE1wkdQobfge37dIizbNvorQRjRBwrkEbaHQ7qHOh/s26YHOXL96AVatNc2Fuz7TrGt4XQ1gJestPg2H42vVwWjdz9fqirVs0Ia9DU79Mq9dzUYQcipsjAa3RMuVKYPAhdEDy2oiJSp6ATIfvTpyzqJ8/nLdVcfMTWGV1sEqSP5fwCtwFJijDdBHWx21kbIMmdfMWmPBQhe7mf1PbOBZqyOtWSA0dppPBAr30ch/CSiApMkRv+UnYhmM+WWKHDxR/wlnDXWBHCiaSqS+9GNz/yWjwwqm1dkDuluEsVHdygxHjsK4pz+lmRDv1lVemNCKp93Oco73x20U9YpI0+7wVqmfVqjO3HapkQ0dx4R0DiQNvXKQL9eBfI+PWvZXb6tqdP58ukYQRYSWQGhCmVzKl+2B776NBN3qAvQhjYDFiiVBx7owEsLno0ZfujtSFMP/zDr5jGsVFWsi/4tZQqKPhFJuzWXQLfKwtqVRY63YgzmijmtfwprFto8svxMS5fRn+UmzcCbeEaxIzyc/XSWNJe9OwW9Pg9pswIqyIEw30+iX0LHdOupWW4hqSMSN+Q/0XevAm6snJD8iTRI/W+HkDcwtOYTK8Gws4VgDEpIYL6Kb+j/klMdzot7+Pz6fvkjbbjAnpEOzg5FXFXaGxy5JWFf735l6pHfIXVwxlXEfoyXaVLkcqbXu7R5m//qAsGI4rslO/EjaEEQptID8Ma6A1WruUyV0y1d76nK+4sn4P5iNQ68JIXMJOOsUepY2r2BCo1Hn4HUQWKpP7V4gsIjAIVUrbBw1asXhOHaLvW/H9YLpqEauSiaKPTK62rC+bZlqWOR5pCAPdyKQ2QL7wiHo0JOq34LeL3jxm/LIJI8LK0TXxqcDHXHSSAtZifJEWfxV278fuKo7MddlL2up7/c+v8kcUB/O1vxJTkx4kZcoexCx7MI03YOVOtGkXoE/6SPwFkmsAVh6ujVRg5WQOwlHfQ48udFOr1IEwGfq5ll2wjJzr+PI6+zu9iI4wonKdFlGatmVZTrJ9Z1cWX16NWV8B6X4G1cKZBIuSHFAAXgjNSao26wwVbjyM5NT34VwnV4tgHaSqL7b0P+Hc4G98Spp7YcDsTWeey2G8sivgCX7sjeyujXDtNMwaDUMXcPFNoScQxsDc7DP23gpa+5ZJ6YLLczSVPtYFEc/L7DhG2Kx9ZX4IWSlrMC2xzX0sA0OU6AUF8N0K375aIa1PQV9NUtcA7MKYhQ7Hjy9kA3qpnOyDYPhe6H7XjkE0NalDvo6bag+lnyFP6xwEswvdxj+i3ZJyh25EXl+16oqES5yo7M444sYvZ7GKAxh0Iy1pqUOOYgqr6FhJ4KpeRivQq5enVHFM5qG204ez4TC35U6AsSUpYOjgoB8iq/UPa7JPr5BVhx/78FfvxvijrREfR0WketINy71QqN/ClIprgJdoR3Ur8NrU/RkeuxhhQtgQRkRvTMKgrhW9ba5D2TxHG576W4URaITEvIFQD6YdkqlFjCpMYe9BMbjKz/rBbq7FJBjthOpSAUYuwYowEVqEmCaW6bIKPAOpdHsG45CSUVimGz01Wp3cf+g4yOqJyOxysQ7hNDB6xlpDbXEhqFMuESaETaywI4BhMUQVvaATF11CC7HHOv5JVhjjueuRt7jdXS2S0IhCI8QGYx0ZZpbZJhgWySuG4QFGw1CAseAcqgbGSk3yB9BdqPWKoaPKHXl5Ppjl+mBE6gvQj47wpfXzRDPq2eFjWZ85bWl9Qyf+JiwIE8ImVuwRwoAkvYanil7QGbuYoU/sTIRNVzn7xFUtEtc4DyBxdHCj7m9EyGkHxjFXqQT3c9HIfIb9DbHyBNKlYFkllzAHF43B19MqnfRqTQ2GNwr3JvkzDs0a+yRs11NnyKixQVgQJoRNDIsjgNEJevUtGpxpwJjU/RGsm0XMze1waPSDgQMGMCTZ2Pwg+FidTMWR+4xm+aFK80ZvP8EDltN6N/pLejhl2WKPySLkh0Jy2EAqIxUO3OafUhuSFtxJFwgLwiS+uBaAoQF19J5K3Ogsz4y/sTO/767fb2Ibok0YP5r0Eukm5w9sdsYc6uEYK5TtgzXfD70fCeA69bSKZIA10+fTlMj1mwa2xoBJoJDUBlXpdsBlCPkEBJni/tjFAG3H0lp6ookGhx6iqZlGh2bFNlIb3Mo91muEAWFBmMSX1Wa8Qgh/L5I9MPgyx1GLv7mzvo/M7mfVRNgOaZjrsWMbJbNAIhQlJ9LGTQZEhehCBgw6veDZo+b/XVeHN0ewywAyfamPJZh1AZNxuw4fLkuv1Txhn0LSJy3wcAcMaai+KItoV199j3dP7clYKUtdAkY+pyxbzcTTmCPlGHcZch6EaVoRGDRqN7Xhy85iSIJygEF/BixaX2oDGAa4w8gdGACEsZF2Zl7bS+PF1KkvbW7goRswcuZHpZ2H3DfsSs2yscAgD+EecuKz0bu9wlabz/MeFBt0Z3IchoTbQSaB8FQb0simiSNaSeN2O65hAytdixji8OH+Qvkx+anUB1CvJvL3a21u1wpuNWBbvjrhYbVY4F4Li/5wTnZgS9lTlyToNSkqS/My8R6bXPqQa3O49SNtAKMbVJOUFePr5tYPdNbvl1/+IYn6W8nKGzXq78aoUfuMzVUhUVj4V1PtGiSFzwszOlmIyoEGwoGtNhF4Ny2JGU1kiLgjjMY2hed8voJIo2b9RotIEcm1QoMGsfBTJak3V05G/7Gch3QV8wTSRWUmBAxh/ENA+Dgg7YeUOQPysRDQkWfXrj3LXLuWOeNEeRkWx122GFoKe2CRf+zY47FSAdQRMTryhRm6yS0kl1DUyu0AwtC8YVZWdhVJzAG3e7viGvEcvPdjC1kElNseCQEDSAoe9m56qTQewXR39x/I10BOtNiPXPbNQM4AbjTGGQhJGdiHhdKckPoLJCnh0ZttRxswg+SBOMLsc7M7cE2aLlnDXd1y4jle5L2bMEhUd0LA6EYaywBaEcSzDzKD27VjWqKKjvlcrnmIRXxPMGWVS2ZiO3KWi1AV/lQ+HNlsSF8OApBZAGydbofDyiMLsYLI02R1utTOVQRJjRkbj1xqbnOJeA0Jk8T7NhebTyQFjK4DqO30ogEUUgnEYfp231H+lDOekLQnlHiabS4a6TUqqiLqgkGjo++te3YIVqf4yD9zPWBYQUq7HTDwmF40UEwvGnCj1xUwgBTGXEwFNl45HoVscyuou685+X/YcpLoKMff+OASsnKdbKejlkdb8LAQo5ZbZIF270E89ni95Ge6zly3cJwTkYy5sr3IhwvQC10SXe+p57BuE1EPGPlC1IIJIRgXUQxxzWY+GS74I/yUVhP2at0KGPGWeEy8TsVPVwmjh9FYZLKqrRDXYfikiHnGQzKpiE7nOoK4GLjlqxjfNsKhpsgN/DqWDUM/B864V1eagTklLBcyd0U12W1tAk+94O3g5p0cUti0wCOdxtM9NCCm+8K3dMvsivuwAze0yIXi/a27vIbUPDb3BbhVn2Xa/iwkceVgzfFXoZN77S8v6byU6nTbBbDa/cK3dMt27vvmlYrtYlfKmzvySsWUY1h8rdix9Cv4Qzkw9zM+0Rlf7z/id+Ih8RI83Z7R9kGMv3kt8DFyGBZh17wWOEYnQHNevE0vkY6d++YzPQ6Ad7FX3HfyApQU9aPi7ObXtFNk/ZsjDQ6AZznNb0nPZNJuckpAgK+ZgIxOeCan4OtzhbRRcwdHgk83HiRpBBrp5W4ko0dXTbzpVslqzR2A5qcF099Yj605g2l7WIPEG+JR26vdeAYEeeoqK08j3wLf03bIu5HkjFZNPCBeEE+INxmtrKOFgzBBzrXz4s1OXTfdUYq65znwwUs8IF4QTzqTioxIAoWxhGUVZzH2VUe2pu3MBnZ1WRTIRR7DYCQz7cnEPGJGACMmoWdlYaAdglWUDfDmdyJo3K3zaZkGDu3VYVwcT1F3BHK3or0ZSePOGGDNoAm8guI4FYkUZarHZRqIdMqPaRSO+SyaIqEZjnSe68g9GQUsRhB6nw+NGkSJkXinIy0Y75bEnhg9nfWJdvmbczAkzc6jXa6Tj51Rb5cAFiMUJm6hkHIAvacYDdyDBmZ05WKs3s7+BFABdMBitMWPtux2y8Ho7Lq7FDAiHo3l9FJpelc0GhsBcKRCMpZl3JkMA+25AOo4AOWl3E1KBwTtbfMOOrPSVmV1OWDx9TsSB+CQ1oX9VPjhQCBwGJ89yjgBSDqtIsFnIal0SmXvSomK5xd971bAYsSAGTnhmpreGKkLpBD1+E0vnG6xzCZ2b1d8on56Y0YBOk9vWp8FR6qKVpHgd4uFCV1BS+s6egRgMaLiGYW1YM5bA+lFdLRoHvfUg2EZUT9UL8rPppeq0eJ8Wu9Ny1S7u+PE+BL/2aMAiyesmYk5xERaRY8/bNAsGgx6yYthhAOmGWb5+bR3RbsSaFCulzZDo/21aDsg2mGGAKJ9MGhrhebOcWRNcTxNPeF7jwWsNXPAaArxBGCw+HTT9Ju67kM0xUevt6A3JuA69tXFgjNsFe584maAqdEWufRJf8hlc7YbxDgUpo22aO8m2g4It9J+9hnznVq35Vh+/w9QixDHQtVe1AAAAABJRU5ErkJggg==\"></image>\n    </g>\n</svg>");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.9568c4c45c4e4bb914f0.js.map