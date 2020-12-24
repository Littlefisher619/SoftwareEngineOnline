"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

var _base = _interopRequireDefault(require("./base"));

var _http = _interopRequireDefault(require("../httpConfig/http.js"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

// 导入接口域名列表
// 导入http中创建的axios实例
// import qs from 'qs'
var team = {
  getlist: function getlist(param) {
    return _http["default"].get("".concat(_base["default"].group, "/"), {
      params: param
    });
  },
  createTeam: function createTeam(param) {
    return _http["default"].post("".concat(_base["default"].group, "/create/"), param, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
  },
  joinTeam: function joinTeam(groupid) {
    return _http["default"].get("".concat(_base["default"].group, "/").concat(groupid, "/join/"));
  }
};
var _default = team;
exports["default"] = _default;