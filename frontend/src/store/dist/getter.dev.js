"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.homeworkName = exports.stuid = exports.stuname = exports.role = exports.username = void 0;

var username = function username(state) {
  return state.user.username;
};

exports.username = username;

var role = function role(state) {
  return state.user.role;
};

exports.role = role;

var stuname = function stuname(state) {
  return state.user.stuname;
};

exports.stuname = stuname;

var stuid = function stuid(state) {
  return state.user.stuid;
};

exports.stuid = stuid;

var homeworkName = function homeworkName(state) {
  return state.homework.homeworkname;
};

exports.homeworkName = homeworkName;