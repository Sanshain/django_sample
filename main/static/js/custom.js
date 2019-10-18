
/*!
@brief Класс-элемент: создает html-элемент

@param 1 - название HTML-элемента
@param 2 - стиль (класс)
@param 3 - содержимое
@param 4 - ассоциативный массив атрибутов

 
*/
function Elem(type_name, txt, css_cls)
{		
	var elem = document.createElement(type_name);	
	elem.innerText = txt;	
	
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


function Time(){
	Data = new Date();
	Hour = Data.getHours();
	Minutes = Data.getMinutes();	
	return Hour+":"+Minutes;
}


function Bell(sound) 
{
	if (ie8()) return function(){};
	
	
	 var audio = new Audio(); // Создаём новый элемент Audio
	 audio.src = sound;       // Указываем путь к звуку 
	 
	 var player = function(){
		 audio.play();            // запускаем
	 }
	 
	 return player;
}

function ie8(){	
	if (!document.addEventListener) return 8;
	
	return false;
}