const fs = require("fs");
var accord         = require('accord');
var assign         = require('object-assign');
var path           = require('path');
var replaceExt     = require('replace-ext');

var less           = accord.load('less');

console.time('Time');

var options = {}

var _id = process.argv.indexOf("--src")+1;

var opts = assign({}, {
	 compress: false,
	 paths: []
}, options);

// opts.sourcemap = true;
opts.filename = process.argv[_id];

var str = fs.readFileSync(opts.filename, "utf8");

less.render(str, opts).then(function(res) {
	
	var file = {}
	
	file.contents = new Buffer(res.result);
	file.path = replaceExt(opts.filename, '.css');
	/*
	if (res.sourcemap) {
	  res.sourcemap.file = file.relative;
	  res.sourcemap.sources = res.sourcemap.sources.map(function (source) {
		 return path.relative(file.base, source);
	  });

	  applySourceMap(file, res.sourcemap);
	}//*/
	return file;
}).then(function(file) {
	
	fs.writeFileSync(file.path, file.contents)
	
	console.log('compilled successfull')
	
	console.timeEnd('Time');
	
}).catch(function(err) {
	
	// Convert the keys so PluginError can read them
	err.lineNumber = err.line;
	err.fileName = err.filename;

	// Add a better error message
	err.message = err.message + ' in file ' + err.fileName + ' line no. ' + err.lineNumber;
	
	console.log(err.message)
});

// https://ru.stackoverflow.com/questions/566796/%D0%9F%D0%B5%D1%80%D0%B5%D0%B4%D0%B0%D1%87%D0%B0-%D0%B8-%D0%BF%D1%80%D0%B8%D1%91%D0%BC-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85-%D0%BC%D0%B5%D0%B6%D0%B4%D1%83-%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%B0%D0%BC%D0%B8-c-%D0%B8-python