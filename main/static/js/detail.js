function async_get_friends(response){
	
	var stack = [];
	var keys_by_stack = ['main','articles'];
	
	
	window.onpopstate = function(){
	
		console.time('check_for_popstate');
	      
		var stored_page = {};
		
		for(key in history.state) {
			
			var container= document.getElementById( key.toLowerCase());

			//if (!container) continue;

			if(container.href){
				stored_page[key]=container.href;
				container.href = history.state[key];
			}
			else{
				stored_page[key]=container.innerHTML;
				container.innerHTML=history.state[key];
			}
		}
	
		stack.push(stored_page);
		
		if (history.state)
			alert(JSON.stringify(Object.keys(history.state)));
		else 
			alert(0);
		
		
		console.timeEnd('check_for_popstate');

	};
	
	
	
	var len = response.length;
	var index = 0;
	var unitSeparator = String.fromCharCode(30);		
	
	while(index <len){
		
		//длина json до 30-го символа
		var currentUserDesc = response.indexOf(unitSeparator, index);
		
		var UserDesc = response.slice(index, currentUserDesc);
		var User = JSON.parse(UserDesc);
		var imglen=response.slice(currentUserDesc+=1, currentUserDesc+=5);
		index = currentUserDesc + Number(imglen);
		User.img=response.substr(currentUserDesc,imglen);
		
		var ava_img = document.createElement('img');
		ava_img.style.float = 'left';		
		ava_img.style.borderRadius = '20px';
		ava_img.style.margin = "10px 0 0 10px";	
		ava_img.src='data:image/jpeg;base64,'+ User.img; 
		
		var username = document.createElement('span');
		username.innerText = User.username+'sgdgdgdfg';
		username.style.paddingLeft = '9%';
		
		var user_div = document.createElement('div');
		user_div.id = 'un' + User.id;
		user_div.style.cursor = 'Pointer';
		user_div.style.marginBottom = '10px';
		user_div.style.lineHeight = '40px';
		user_div.style.whiteSpace = 'nowrap';
		user_div.style.lineHeight = '60px';
		user_div.className = 'friend_pick';	
		user_div.onclick = function()
		{
			var page = '/users/'+User.id + '/';
			var ajax_user = new Ajax(
				page,
				render_page);		
			ajax_user.postData(User.id);	
			
		};		
		
		user_div.appendChild(ava_img);				
		user_div.appendChild(username);				
		
		var asd = document.querySelector('.aside_menu');
		asd.appendChild(user_div);
		
	}
				
	//							
	
}


var go_to_dialog = function(sender, event){
	event.preventDefault();

	var user_id = document.location.pathname.match(/\d+/)[0];
	var get_view = '/'+sender.name+'/';
	var set_url = sender.formAction;


	var __review_detail = function (resp){ 
		
		render_page(resp, set_url);
		
		/*
		detail =
		{
			'detail':document.querySelector('.detail').innerHTML,
			'dynamic_link':document.getElementById('dynamic_link').href
		};	
		
		history.pushState(detail, null, set_url);//*/
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




	var present_data_page = {};
	for (key in next_user){
		var el = document.getElementById( key.toLowerCase() );
		
		present_data_page[key]=el.href ?
			el.href:
			el.innerHTML;
	}
	
	history.replaceState(present_data_page, null, null);
	

	var viewer = new Viewer(	
		present_data_page
	).render(next_user);
		
		
	/*
	var btnNoteCreate =document.querySelector('#note_create');
	if (btnNoteCreate) btnNoteCreate.style.display = 'none';
	*/
	
	//здесь можно проверить, является ли страница той же по маске
	
	if (!to) return;
	
	// если это не происходит здесь, то остается
	
	
	alert('меняем адрес в render_pagу: '
		+ JSON.stringify(Object.keys(present_data_page)));	
	
	
	history.pushState(null, null, to);
	
}


function Viewer(data_page){
	
	var stored_data = {};
	
	this.render = function(view){

		var present_data_page = {};
	
		for (key in view)
		{
			this.render_field(
				key, 
				view[key]
			);
		}

		
		


		
	}
	
	this.render_field = function(key, view)
	{
		
		
		stored_data[key]=el.href ?
			el.href:
			el.innerHTML;		
		
		
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

			if (field.href) {
				stored_data[key] = field['href'];
				field['href'] = view;
			}
			else if (field.src) 
			{
				stored_data[key] = field['src'];
				field['src'] = view;
			}
			else
			{
				var property=;
				
				stored_data[key] = field[property];
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



