require("subtest");

String.prototype.trimw = function () {
  return this.replace(/^\s+|\s+$/g, '');
};

var d = 63;
var a = 6;
var c = 6;
var t = 0;

var r = function r() {
  return 1;
};