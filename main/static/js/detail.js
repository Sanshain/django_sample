
var go_to_dialog = function(sender, event){
	event.preventDefault();

	var user_id = document.location.pathname.match(/\d+/)[0];
	var get_view = '/'+sender.name+'/';
	var set_url = sender.formAction;


	var __review_detail = function (resp){ 
		
		render_page(resp); 
		detail =
		{
			'detail':document.querySelector('.detail').innerHTML,
			'dynamic_link':document.getElementById('dynamic_link').href
		};	
		
		history.pushState(detail, null, set_url);
		//'/messages/to_'+user_id+'/'
	}

	var review = new Ajax(
		get_view,				 
		__review_detail
	);
			
	review.postData('id='+user_id);			//User.id

};





var render_page = function(next_user, to)
{					


	while(typeof next_user =="string") next_user=JSON.parse(next_user);

	var field = new FieldViewer(	//obsolete:
		go_to_dialog //в итоге подгрзится с сервера ссылка на этот метод
	);
	for (attr in next_user)
	{
		field.render(
			attr, 
			next_user[attr]
		);
	}
		
	/*
	var btnNoteCreate =document.querySelector('#note_create');
	if (btnNoteCreate) btnNoteCreate.style.display = 'none';
	*/
	
	if (!to) return;//либо с сервера либо страница останется неизвестной
	
	var stored_page = {};
	for (key in next_user){
		
		var el = document.getElementById( key.toLowerCase() );
		
		stored_page[key]=el.href ?
			el.href:
			el.innerHTML;
	}
	
	history.pushState(stored_page, null, to);
	
}


function FieldViewer(e){
	
	this.events = e;
	
	this.render = function(key, view)
	{
		
		var field=document.getElementById(key.toLowerCase());
		
		if (!field && key.startsWith('dynamic_c')){
			//если не найден скрипт
			
			const script = document.createElement('script');
			script.src = view;
			script.id = key;
			document.head.appendChild(script);	
			return;
		}
		else if (typeof view == "string")
		{	

			if (field.href) field.href = view;
			else if (field.src) field.src = view;
			else
			{
				var property=view.startsWith('<')?'innerHTML':'innerText';
				field[property]=view;
			}
			
		} else if (typeof view == "object")
		{
			for (k in view) 
			{
				
				if (k.startsWith('on')) field.setAttribute(k, view[k]);
				else 
					field[k] = view[k];
			}
		}
		
		
		
		else{
			console.log('not find field for key - ' + key);
		}
	};	
	
}















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



