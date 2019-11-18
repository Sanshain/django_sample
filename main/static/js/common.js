HTMLLIElement.prototype.appendChilds = function () {

  for ( var i = 0 ; i < arguments.length ; i++ )

    this.appendChild( arguments[ i ] );

};


/*! использование Math.round() даст неравномерное распределение!

*/
function getRandomInt(min, max){
	
  return Math.floor(Math.random() * (max - min + 1)) + min;
};



function SetUniqueValue(enumble, field_in, val){
	
	var value = val || getRandomInt(0, 1000);
	
	if (field_in) enumble = Array.from(enumble)
		.map(function(item) 
		{
		  return item[field_in];
		});	
	
	if (enumble.indexOf(value) != -1) {
		return value;
	}
	else{
		return SetUniqueValue(enumble, (val+1 || void 0));
	}

}

function get_maxim(enumble, field_in){
	
	//Array.from
	if (field_in) enumble = [].slice.call(enumble).map(
		function(item) 
		{
		  return item[field_in];
		});
	var m = Math.max.apply(null, enumble);
	
	return m > 0 ? m : 0;

}