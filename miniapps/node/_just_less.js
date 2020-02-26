const fs = require("fs");
var accord         = require('accord');
var less           = accord.load('less'); //accord.load
var path           = require('path');
var replaceExt     = require('replace-ext');


exports.render = async function (str, opts){
	
	var file = {}
	
	//try{
		res = await less.render(str, opts);
		
		file.contents = Buffer.from(res.result);
		file.path = replaceExt(opts.filename, '.css');


		fs.writeFileSync(file.path, file.contents)
		
		console.log('compilled successfull')
	/*	
	}
	catch(err) {
		
		// Convert the keys so PluginError can read them
		err.lineNumber = err.line;
		err.fileName = err.filename;

		// Add a better error message
		err.message = err.message + ' in file ' + err.fileName + ' line no. ' + err.lineNumber;
		
		console.log(err.message)
	};//*/

};



//may also using `exports` instead `this`
/*
this.test = function test(){
	console.log('require succ')
}
//*/
