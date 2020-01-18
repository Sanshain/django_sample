String.prototype.trim = function () {
  return this.replace(/^\s+|\s+$/g, '');
}; 

let d = 63;

let a = 6;
let c = 6;
const t = 0;

var r =() => 1;

//if ie10+ and not ie9-: //потом надо вынести в отдельный файл
// пока переопределил в common.js

/*
String.prototype.startsWith = function(search, pos)
{
      position = pos || 0;
      return 
			this.substr(pos, searchStr.length) === searchStr;
};
//*/
//заменю на обращения по индексу
