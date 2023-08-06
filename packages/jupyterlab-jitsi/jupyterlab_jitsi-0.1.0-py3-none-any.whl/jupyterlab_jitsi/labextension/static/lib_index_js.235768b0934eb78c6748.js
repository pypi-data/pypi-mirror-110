(self["webpackChunkjupyterlab_jitsi"] = self["webpackChunkjupyterlab_jitsi"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
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
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jitsi', // API Namespace
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

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "fooIcon": () => (/* binding */ fooIcon),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _style_icon_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/icon.svg */ "./style/icon.svg");








const fooIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
    name: 'jupyterlab-jitsi:icon',
    svgstr: _style_icon_svg__WEBPACK_IMPORTED_MODULE_5__.default
});
const SETTINGS_ID = 'jupyterlab-jitsi:plugin';
// interface IJitsiOptions {
// }
class JitsiWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IFrame {
    constructor(options) {
        super();
        const queryElems = [];
        for (const k in options) {
            if (k === 'options') {
                const opts = options.options;
                const jopts = JSON.stringify(opts);
                queryElems.push(encodeURIComponent(k) + '=' + encodeURIComponent(jopts));
            }
            else {
                queryElems.push(encodeURIComponent(k) + '=' + encodeURIComponent(options[k]));
            }
        }
        this.query = queryElems.join('&');
        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.PageConfig.getBaseUrl();
        this.url = baseUrl + `jitsi/app/index.html?${this.query}`;
        console.log('Full URL: ', this.url);
        this.id = 'Jitsi';
        this.title.label = 'Jitsi';
        this.title.closable = true;
        this.node.style.overflowY = 'auto';
        this.node.style.background = '#FFF';
        this.sandbox = [
            'allow-forms',
            'allow-modals',
            'allow-orientation-lock',
            'allow-pointer-lock',
            'allow-popups',
            'allow-presentation',
            'allow-same-origin',
            'allow-scripts',
            'allow-top-navigation',
            'allow-top-navigation-by-user-activation'
        ];
    }
    dispose() {
        super.dispose();
    }
    onCloseRequest() {
        this.dispose();
    }
}
/**
 * Initialization data for the jupyterlab-jitsi extension.
 */
const extension = {
    id: 'jupyterlab-jitsi:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher],
    activate: (app, palette, settings, launcher) => {
        let _settings;
        const command = 'jitsi:open';
        let registeredCommands = [];
        const _loadSettings = () => {
            const enpoints = _settings.get('configured_rooms').composite;
            console.log(enpoints);
            // const enpoints = [{"name": "test"}];
            let i = 0;
            for (const c of registeredCommands) {
                c.dispose();
            }
            registeredCommands = [];
            for (const epconf of enpoints) {
                // const full_cmd = command + `:${i}`
                const full_cmd = command + `:${i}`;
                const widget = new JitsiWidget(epconf);
                const rcmd = app.commands.addCommand(full_cmd, {
                    label: `Connect to VNC ${i}: ${'name' in epconf ? epconf['name'] : epconf['host']}`,
                    execute: () => {
                        if (!widget.isAttached) {
                            // Attach the widget to the main work area if it's not there
                            app.shell.add(widget, 'main');
                        }
                        // Activate the widget
                        app.shell.activateById(widget.id);
                    },
                    icon: fooIcon
                });
                registeredCommands.push(rcmd);
                // Add a launcher item if the launcher is available.
                if (launcher) {
                    const lcmd = launcher.add({
                        command: full_cmd,
                        rank: 1,
                        category: 'Robotics'
                    });
                    registeredCommands.push(lcmd);
                }
                const pcmd = palette.addItem({
                    command: full_cmd,
                    category: 'Robotics'
                });
                registeredCommands.push(pcmd);
                i += 1;
            }
        };
        settings.load(SETTINGS_ID).then(setting => {
            console.log(setting);
            _settings = setting;
            const extensions = setting.get('configured_endpoints').composite;
            console.log(extensions);
            _loadSettings();
            setting.changed.connect(_loadSettings);
        });
        (0,_handler__WEBPACK_IMPORTED_MODULE_6__.requestAPI)('get_example')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The jupyterlab-jitsi server extension appears to be missing.\n${reason}`);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./style/icon.svg":
/*!************************!*\
  !*** ./style/icon.svg ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"iso-8859-1\"?>\r\n<!-- Generator: Adobe Illustrator 19.0.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->\r\n<svg version=\"1.1\" id=\"Layer_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\"\r\n\t viewBox=\"0 0 329.998 329.998\" style=\"enable-background:new 0 0 329.998 329.998;\" xml:space=\"preserve\">\r\n<g id=\"XMLID_873_\">\r\n\t<g id=\"XMLID_874_\">\r\n\t\t<path id=\"XMLID_875_\" d=\"M320.605,310c-16.068-45.459-50.888-80.607-93.903-97.994C258.722,191.566,280,155.723,280,115\r\n\t\t\tC280,51.589,228.411,0,165,0c-63.412,0-115,51.589-115,115c0,40.723,21.278,76.567,53.298,97.005\r\n\t\t\tc-43.016,17.387-77.836,52.535-93.904,97.994c-1.623,4.591-0.916,9.684,1.896,13.66c2.811,3.976,7.378,6.339,12.247,6.339h282.927\r\n\t\t\tc4.869,0,9.436-2.364,12.247-6.339C321.521,319.683,322.228,314.59,320.605,310z M79.999,115c0-46.869,38.131-85,85-85\r\n\t\t\tc46.869,0,85,38.131,85,85c0,46.869-38.131,85-85,85C118.13,200,79.999,161.869,79.999,115z M46.638,299.998\r\n\t\t\tC70.067,257.398,115.275,230,165,230c49.726,0,94.932,27.398,118.36,69.998H46.638z\"/>\r\n\t</g>\r\n\t<g id=\"XMLID_879_\">\r\n\t\t<path id=\"XMLID_880_\" d=\"M165,60c-30.327,0-55,24.673-55,55c0,30.327,24.673,55,55,55c30.327,0,55-24.673,55-55\r\n\t\t\tC220,84.673,195.327,60,165,60z M165,140c-13.785,0-25-11.215-25-25c0-13.785,11.215-25,25-25c13.785,0,25,11.215,25,25\r\n\t\t\tC190,128.785,178.785,140,165,140z\"/>\r\n\t</g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n<g>\r\n</g>\r\n</svg>\r\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.235768b0934eb78c6748.js.map