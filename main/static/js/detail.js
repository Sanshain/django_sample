
/*! async get friends for detail-template called onload/

*/
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



/*! action under user (Rule function instead go_to_dialog)...

	Получает из атрибутов кнопки (пока только той, что под аватаркой) параметры для запроса
	Делает запрос и рендерит страницу
*/
var do_action = function(sender, event){
	event.preventDefault();

	var user_id = document.location.pathname.match(/\d+/)[0];
	var set_url = sender.formAction; 	
	var get_view = sender.name ? '/'+sender.name+'/' : set_url;

	var __review_detail = function (resp){ 

		render_page(resp, set_url);

	}

	var review = new Ajax(
		get_view,				 
		__review_detail
	);
			
	review.postData('id='+user_id);			//User.id

};






