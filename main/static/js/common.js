HTMLLIElement.prototype.appendChilds = function () {

  for ( var i = 0 ; i < arguments.length ; i++ )

    this.appendChild( arguments[ i ] );

};

/*!
	рассчитано на небольшое количество атрибутов (до 10 вне цикла, рекомендуемое - 2)
	
	* не поддерживает class
	
*/
HTMLElement.prototype.vs = function (dict) {

	for (var key in dict){
		this.setAttribute(key, dict[key]);
	}

	return this;
};



/*! ie10+ - во вставке изображения в текст

	Получает максимальный элемент из массива объектов
	используется в __upload_images в user.js
*/
function get_maxim(enumble, field_in){ //get_maximum
	
	//Array.from
	if (field_in) enumble = [].slice.call(enumble).map(
		function(item) //
		{
		  return item[field_in];
		});
	var m = Math.max.apply(null, enumble);
	
	return m > 0 ? m : 0;

}

/*!
	Рекурсивно ищет первый попавшийся fixed элемент с заданной глубиной поиска
	
	Используется в base для решения #6 issue

	Рассчитана на ie10+
*/
function search_fixed(container, deep){
	
	if (deep == 0) return null;
	else 
		deep = deep || 2;
	
	var childs=container.children; // ie9+,ниже- childNodes 
	
	var i=0; while(i<childs.length)
	{
		var elem = childs[i++];
		if (window.getComputedStyle(elem).position == 'fixed'){						//ie9+, ниже полифилл
			return elem;
		}
		else if (deep > 1){
			
			var r = search_fixed(elem, deep - 1);
			
			if (r != null) return r;			
		}
		
	}
	
	//можно так же firstElementChild - тоже ie9+
}











/*	
	решил через left:calc(100vw - 250px);  для aside
	пока не актуально
*/
function get_scroll_wide(elem){
	//var elem = document.body || elem;
	
	return window.innerWidth - document.body.clientWidth;
}





/*!!
	Только для ie10+. В итоге я вроде от нее отказался
*/

if (!String.prototype.startsWith) {
	
	String.prototype.startsWith = function(search, pos)
	{
		  position = pos || 0;
		  var r = this.substr(pos, search.length) === search;
		  /*
		  if (r){
			console.log(r);
		  }//*/
		  return r;
			
	};

}//*/