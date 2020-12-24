"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.setHomeworkName = exports.setinfo = void 0;

var _mutation = require("./mutation");

var setinfo = function setinfo(_ref, info) {
  var commit = _ref.commit;
  commit("info", info);
};

exports.setinfo = setinfo;

var setHomeworkName = function setHomeworkName(_ref2, homeworkName) {
  var commit = _ref2.commit;
  commit("homeworkName", homeworkName);
};

exports.setHomeworkName = setHomeworkName;