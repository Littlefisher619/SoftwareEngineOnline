"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.getUrlKey = getUrlKey;

function getUrlKey(name) {
  var href = decodeURIComponent(location.href);
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(href) || [, ""])[1].replace(/\+/g, '%20')) || null;
}