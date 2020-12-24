"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

var _base = _interopRequireDefault(require("./base"));

var _http = _interopRequireDefault(require("../httpConfig/http.js"));

var _qs = _interopRequireDefault(require("qs"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

// 导入接口域名列表
// 导入http中创建的axios实例
var homework = {
  getlist: function getlist() {
    return _http["default"].get("".concat(_base["default"].homework));
  },
  tasklist: function tasklist(taskid, params) {
    return _http["default"].get("".concat(_base["default"].homework).concat(taskid, "/tasklist/"), {
      params: params
    });
  },
  "static": function _static(taskid) {
    return _http["default"].get("".concat(_base["default"].homework).concat(taskid, "/statistics/"));
  }
};
var _default = homework;
exports["default"] = _default;