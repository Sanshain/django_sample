
/*!
@brief Класс-элемент: создает html-элемент

@param 1 - название HTML-элемента
@param 2 - стиль (класс)
@param 3 - содержимое
@param 4 - ассоциативный массив атрибутов

 
*/
function Elem(type_name, txt, css_cls){		
	var elem = document.createElement(type_name);	
	elem.innerText = txt;	//value
	
	if (css_cls) {
		elem.className = css_cls;
	}
	
	return elem;	
}


/*!
	@brief Добавляет html-элемент в контейнер
*/
function AppendNewElemTo(container, elem){
	if (typeof container == 'string') 
	{
		container = document.querySelector(container);
	}	
	container.appendChild(elem);
	
	return elem;
}


var doc = document;
var loc = document.location;

doc.get = function(attr, container){
	
	container = container || doc;
	
	var elem = container.getElementById(attr);
	
	//-
	var warn_flag = elem ? false : true;
	//-
	
	elem = elem || container.querySelector(attr);
	elem = elem || container.getElementsByName(attr)[0];
	
	//-
	if (elem != null && warn_flag){
		if (el.tagName != "LINK")
		{
			console.log('warning: not id для doc.get ' +attr);
		}
	}else (elem == null){
		alert('warning: not find by _doc.get_ the `' +attr + '`');
	}//-
	
	return elem;
	
}





/*!
	@brief вернет время в формате 23:00
*/
function Time(){
	Data = new Date();
	Hour = Data.getHours();
	Minutes = Data.getMinutes();	
	return Hour+":"+Minutes;
}








/*!
	@brief Добавляет html-элемент в контейнер
*/
function Bell(sound) {
	if (ie8()) return function(){};
	
	 var audio = new Audio(); // Создаём новый элемент Audio
	 audio.src = sound;       // Указываем путь к звуку 
	 
	return function(){
		 audio.play();            // запускаем
	}	 
}






/*!
	@brief Проверяет, яляется ли браузер ie8
*/
function ie8(){
	if (!document.addEventListener) return 8;
	
	return false;
}


