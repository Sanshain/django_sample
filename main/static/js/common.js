HTMLLIElement.prototype.appendChilds = function () {

  for ( var i = 0 ; i < arguments.length ; i++ )

    this.appendChild( arguments[ i ] );

};





/*! ie10+ - во вставке изображения в текст

	Получает максимальный элемент из массива объектов
*/
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