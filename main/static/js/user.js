function Note(){} /* пространство имен Note */
	


/*! Показывает окно создания записи...
	
	Вызов лежит в aside_inside блоке юзера
*/
Note.createView = function(){
	//document.location.href = "{% url 'note_create' %}";
	
	//document.getElementById('id_Title').focus();
	//document.getElementById('id_Title').value = '';
	
	document.getElementById('win').removeAttribute('style');			
	document.getElementById('id_Content').focus();
	
	
	//document.querySelector('.visible').style.height = '80vh';	
};


/*! Скрывает окно создания записей...
	 (обратная note_create)
*/
Note.hideView = function(){
	
	document.getElementById('win').style.display='none';
	//document.querySelector('.visible').style.height = '10vh';
	
};


/*! Добавляет запись в поток и отправляет на сервер...
 записей (статей) страницы. 
 
	И отправляет на сервер 
	
*/
Note.post_View = function(sender, e){
	e.preventDefault();
	
	//отправляем данные формы на сервер
	this.new_note = this.new_note || new Ajax(_note_create ,function(answer){
		//alert(answer);
		var value = JSON.parse(answer);
		
		var ja = document.createElement('div');
		
		var h = Elem('h4',value.title,'');
		h.style.marginTop = '5px';
		var note = Elem('div', '', 'Anote');
		note.appendChild(h);
		note.appendChild(Elem('div',value.content,''));
		
		var last_note = document.querySelector('.articles_list').firstChild;
		document.querySelector('.articles_list').insertBefore(note,last_note)
	});
	
	this.new_note.post_form(document.querySelector('#note'))
	
	document.getElementById('win').style.display='none';
	document.getElementById('id_Title').value = '';
	document.getElementById('id_Content').value = '';	
};







/*! action under user (Rule function instead go_to_dialog)...

	Получает из атрибутов кнопки (пока только той, что под аватаркой) параметры для запроса
	Делает запрос и рендерит страницу
*/
var do_action = function(sender, event){
	event.preventDefault();

	var user_id = document.location.pathname.match(/\d+/)[0];
	var set_url = sender.formAction; 	
	var get_view = sender.name ? '/'+sender.name+'/' : set_url;

	var __review_detail = function (resp)					//
	{ 
		render_page(resp, set_url);
		
		
	}

	var review = new Ajax(
		get_view,				 
		__review_detail
	);
			
	review.postData('id='+user_id);			//User.id

};

	

