HTMLLIElement.prototype.appendChilds = function () {

  for ( var i = 0 ; i < arguments.length ; i++ )

    this.appendChild( arguments[ i ] );

};





/*! ie10+ - во вставке изображения в текст

	Получает максимальный элемент из массива объектов
	используется в __upload_images в user.js
*/
function get_maxim(enumble, field_in){
	
	//Array.from
	if (field_in) enumble = [].slice.call(enumble).map(
		function(item) //
		{
		  return item[field_in];
		});
	var m = Math.max.apply(null, enumble);
	
	return m > 0 ? m : 0;

}


/*!!
	Только для ie10+
*/
if (!String.prototype.startsWith) {
	String.prototype.startsWith = function(search, pos)
	{
		  position = pos || 0;
		  return 
			this.substr(pos, searchStr.length) === searchStr;
	};

}