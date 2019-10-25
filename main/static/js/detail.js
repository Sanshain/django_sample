
function async_get_friends(response){
	
	window.onpopstate = function(){
	
		console.time('check_for_popstate');

		new Viewer(history.state).render_back();		

		/*
		if (history.state)
			alert(JSON.stringify(Object.keys(history.state)));
		else 
			alert(0);//*/
		
		
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




//obsolete name = go_to_dialog
var do_action = function(sender, event){
	event.preventDefault();

	var user_id = document.location.pathname.match(/\d+/)[0];
	var set_url = sender.formAction; 	
	var get_view = sender.name ? '/'+sender.name+'/' : set_url;

	var __review_detail = function (resp){ 

		console.time('check_for_just_render');
		
		render_page(resp, set_url);
		
		console.timeEnd('check_for_just_render');

	}

	var review = new Ajax(
		get_view,				 
		__review_detail
	);
			
	review.postData('id='+user_id);			//User.id

};




/*!
	@param data - ответ от сервера (данные для рендеринга)
	@param url - url для изменения в адресной строке браузера
*/
var render_page = function(data, url)
{					

	while(typeof data =="string") data = JSON.parse(data);
	
	var view = new Viewer(data).render();
	
	
	if (url)// если это не происходит здесь, то остается (для несущ изм)
	{
		
		var closed_page = view.create_stored_page_and_go(url);
		
		alert('меняем адрес в render_pagу: '
			+ JSON.stringify(Object.keys(closed_page)));
	
	}
	
}


function Viewer(data){
	
	var stored_data = {};
	
	var new_view = data;
	

	
	
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
	
	/*!
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
	

	
	this.render_field = function(key, view)
	{
		
		var field=document.getElementById(key.toLowerCase());
		
		if (!field && key.startsWith('dynamic_c')){
			//если не найден скрипт
			
			const script = document.createElement('script');
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
	
	var property = function(view,field){
		var i=-1; var attr = ''; var attrs = [
			'href',
			'src',
			view.trimLeft().startsWith('<')?'innerHTML':'innerText'
		];
					
		while(!(field[ attr=attrs[++i] ])) if (i>1) break;	

		return attr;		
	};	
	
}






