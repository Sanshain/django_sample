
/*! render for part of page...

	@param data - ответ от сервера (данные для рендеринга)
	@param url - url для изменения в адресной строке браузера
*/
var render_page = function(data, url){					

	while(typeof data =="string") data = JSON.parse(data);
	
	var view = new Viewer(data).render();
	
	
	if (url)// если это не происходит здесь, то остается (для несущ изм)
	{
		
		var closed_page =view.create_stored_page_and_go(url);
		/*
		alert('меняем адрес в render_pagу: '
			+ JSON.stringify(Object.keys(closed_page)));
		*/
	}
	
}


						/* class Viewer*/

/*! Class for present new part of page...

	Рендерит поля страницы на основе входных данных
*/
function Viewer(data){
	
	
	/*! render part of page from history.state...
	when user back transfer 
	
		Рендерит при возврате назад на основе history.state
		
		(в отличие от render+render_field не сохраняет историю)
	*/
	this.render_back = function(){
		
		for(key in history.state) {
			
			var field=document.getElementById(key.toLowerCase());
			var view = history.state[key];
			
			if (typeof view == "string") 
				
				field[property(view, field)] = view;
				
			else if (typeof view == "object")
			{
				for (k in view) 
				{

					if (k.startsWith('on')) field.setAttribute(k, view[k]);
					else 
						field[k] = view[k];
				}
			}			
		}		
		
	}	
	
	/*! render part of page vs history.state saving...
	
		Ключевой метод этого класса
	*/
	this.render = function(){

		for (key in new_view)
		{
			this.render_field(
				key, 
				new_view[key]
			);
		}
		
		return this;
	}
	
	/*!	Save history.state before setting/going to next view
	
		@brief create_stored_page_and_go
	*/
	this.create_stored_page_and_go = function(to_url){
		
		if (stored_data){
			history.replaceState(stored_data,null,document.location.pathname);
			
			history.pushState(null, null, to_url);			
		}else 
			new Error('stored_data is not defined. Call `render` first');
		
		return stored_data;
	}
	
	/*! Render certain/definite fielt for view
	
	*/
	this.render_field = function(key, view){
		
		var field=document.getElementById(key.toLowerCase());
		
		if (!field && key.startsWith('dynamic_c')){
			//если не найден скрипт
			
			var script = document.createElement('script');
			script.src = view;
			script.id = key;
			document.head.appendChild(script);	return;
			
		}
		else if (typeof view == "string")
		{	
			
			var attr = property(view,field);
			
			stored_data[key] = field[attr]; 
			
			field[attr] = view;
			
		} else if (typeof view == "object")
		{
			stored_data[key] = {};
			for (k in view) 
			{
				if (1+['object','function'].indexOf(typeof field[k]))
				{
					stored_data[key][k]=field.getAttribute(k);
				} else stored_data[key][k]=field[k];
				
				if (k.startsWith('on')) field.setAttribute(k, view[k]);
				else 
					field[k] = view[k];
			}
		}
		
		
		
		else{
			console.log('not find field for key - ' + key);
		}
		
		
	};		
	
	/*! Get or find property_name for replacement its value
		
		Имя свойства для переопределения может быть разное. Эта функция определяет его для каждого конкретного элемента
	*/
	var property = function(view,field){
		var i=-1; var attr = ''; var attrs = [
			'href',
			'src',
			view.trimLeft().startsWith('<')?'innerHTML':'innerText'
		];
					
		while(!(field[ attr=attrs[++i] ])) if (i>1) break;	

		return attr;		
	};	
	
	
	var stored_data = {};
	var new_view = data;
}
