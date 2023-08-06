(self["webpackChunk_theNewFlesh_jupyterlab_henanigans"] = self["webpackChunk_theNewFlesh_jupyterlab_henanigans"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * Initialization data for the @quansight-labs/jupyterlab-theme-winter extension.
 */
const extension = {
    id: '@theNewFlesh/jupyterlab_henanigans',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager],
    autoStart: true,
    activate: (app, manager) => {
        console.log('JupyterLab extension @theNewFlesh/jupyterlab_henanigans is activated!');
        const style = '@theNewFlesh/jupyterlab_henanigans/index.css';
        manager.register({
            name: 'Henanigans',
            isLight: true,
            load: () => manager.loadCSS(style),
            unload: () => Promise.resolve(undefined)
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.9aee9d23ae4b10f41f84.js.map