var render_field = function(key, view, e)
{
	
	var field=document.getElementById(key.toLowerCase());
	var value = view[key];
	
	if (!field && key.startsWith('dynamic_c')){
		//вставляем скрипт
		const script = document.createElement('script');
		script.src = value;
		document.head.appendChild(script);	
	}
	else if (typeof value == typeof ""){
	
		//obsolete if field.tagName == 'LINK' - long note
		if (field.href) field.href = value;
		else if (field.src) field.src = value;
		else{
			var property=value.startsWith('<')?'innerHTML':'innerText';
			field[property]=value;
		}
	
	} else if (typeof value == "object")
	{
	
		Object.keys(value).forEach(
			function(key){
				/*
				if (key.startsWith('on'))  //
					// ie8? ie9+ addEventListener (9+)
					field.setkeyibute(key,value[key]); 
				else 
				//*/
					
					field[key] = value[key];
			}
		);
		
		field.onclick = e;

	}
	else{
		console.log('not find field for key - ' + key);
	}
};













/*!
	@brief Сменяет адрес в адресной строке на новый, 
	а так же записывает в stack изображение этой страницы
	
	логирует history.state текущей страницы
	
*/
function ChangePage(page,state){
	if (history.state){
		state = state || ['main','articles'];
		var stored_page = {}
		
		//-
		console.log(history.state);
		//-
		
		history.state.forEach(
			function(key){
				
				stored_page[key] = !key=="dynamic_link"?
					document.querySelector('.'+key).innerHTML:
					document.getElementsByName("dynamic_link")[0].href;				
			}
		);
				
		
		stack.push(stored_page);
		history.pushState(state, null, page); 
			
		return true;
	}
	
	return false;
}


function page_popstate(){
	
	var view = (stack.pop());
	var stored_page = {};
	
	for(key in view) {
							
		if(key=="dynamic_link"){
			var link = document.getElementsByName("dynamic_link")[0];
			stored_page[key]=link.href;
			link.href = view[key];
		}
		else{
			var container = document.querySelector('.'+key);
			stored_page[key]=container.innerHTML;
			container.innerHTML=view[key];						
		}
	}
	stack.push(stored_page);
	
	alert(history.state);
}



function page_popstate_v1(){
	
	var view = (stack.pop());
	var stored_page = {};
	
	for(key in view) {
							
		if(key=="dynamic_link"){
			var link = document.getElementsByName("dynamic_link")[0];
			stored_page[key]=link.href;
			link.href = view[key];
		}
		else{
			var container = document.querySelector('.'+key);
			stored_page[key]=container.innerHTML;
			container.innerHTML=view[key];						
		}
	}
	stack.push(stored_page);
	
	alert(history.state);
}



