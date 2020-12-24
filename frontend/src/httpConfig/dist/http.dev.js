"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

var _axios = _interopRequireDefault(require("axios"));

var _elementUi = require("element-ui");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

//项目已经全局引入element的话可以不单独引入
//整理数据
_axios["default"].defaults.transformRequest = function (data) {
  data = JSON.stringify(data);
  return data;
};

_axios["default"].defaults.withCredentials = true; //实例化axios

var instance = _axios["default"].create({
  timeout: 1000 * 12,
  withCredentials: true
});

var loadinginstace;
instance.interceptors.request.use(function (config) {
  if (localStorage.getItem('JWT_TOKEN')) {
    // 判断是否存在token，如果存在的话，则每个http header都加上token
    config.headers.Authorization = "Bearer ".concat(localStorage.getItem('JWT_TOKEN'));
  }

  loadinginstace = _elementUi.Loading.service({
    fullscreen: true
  });
  return config;
}, function (err) {
  // return Promise.reject(err);
  loadinginstace.close();
  console.log(err);
});
instance.interceptors.response.use(function (response) {
  loadinginstace.close();
  return response;
}, function (err) {
  loadinginstace.close();
  console.log(err);

  if (err && err.response) {
    switch (err.response.status) {
      case 400:
        _elementUi.Message.error("Error: 400 错误请求");

        break;

      case 401:
        _elementUi.Message.error("Error: 401 未授权请重新登陆");

        break;

      case 403:
        _elementUi.Message.error("Error: 403 拒绝访问");

        break;

      case 404:
        _elementUi.Message.error("Error: 404 请求错位,未找到该资源");

        break;

      case 405:
        _elementUi.Message.error("Error: 405 请求方法未允许");

        break;

      case 500:
        _elementUi.Message.error("Error: 500 服务端错误");

        break;

      case 501:
        _elementUi.Message.error("Error: 501 网络未实现");

        break;

      case 502:
        _elementUi.Message.error("Error: 502 网络错误");

        break;

      case 503:
        _elementUi.Message.error("Error: 503 服务不可用");

        break;

      case 504:
        _elementUi.Message.error("Error: 504 网络超时");

        break;

      case 505:
        _elementUi.Message.error("Error: 505 http不支持该请求");

        break;

      default:
        _elementUi.Message.error("\u8FDE\u63A5\u9519\u8BEF".concat(err.response.status));

    }
  } else {
    _elementUi.Message.error("未知错误");
  }

  return Promise.reject(err);
});
var _default = instance;
exports["default"] = _default;