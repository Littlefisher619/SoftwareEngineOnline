"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.homeworkName = exports.info = void 0;

var _homework = _interopRequireDefault(require("../api/homework"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

var info = function info(state, user) {
  state.user = JSON.parse(JSON.stringify(user));
};

exports.info = info;

var homeworkName = function homeworkName(state, _homeworkName) {
  state.homework.homeworkname = JSON.parse(JSON.stringify(_homeworkName));
};

exports.homeworkName = homeworkName;