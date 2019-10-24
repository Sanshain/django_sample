var note_create = function(sender, e){
	//alert('d');
	//document.location.href = "{% url 'note_create' %}";
	//document.getElementById('id_Title').focus();
	//document.getElementById('id_Title').value = '';
	document.getElementById('win').removeAttribute('style');			
	document.getElementById('id_Content').focus();
	
	
	//document.querySelector('.visible').style.height = '80vh';
}

var note_submit = function(sender, e){
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
	
}

function HideModal(){
	document.getElementById('win').style.display='none';
	document.querySelector('.visible').style.height = '10vh';
}

function ExpandModal(){
	document.querySelector('.visible').style.height = '100vh';
	document.querySelector('.visible').style.width = '100vw';
	document.querySelector('.visible').style.left = '-15px';
	document.querySelector('.visible').style.marginTop = '0vh';
	document.querySelector('#id_Content').style.height = '65vh';
}		


//obsolete/ Insteade use go_to_dialog(this, event) 
function to_dialog(){
	
	var user_id = window.location.pathname.match(/\d+/).pop();
	var data = 'id=' + user_id;
	
	//window.location.href = _dialog;return;
	
	var _a = new Ajax(_get_dialog, 
		function(answer){
			//файл стиля диалога, кот надо добавить в хедер (если его там нет, т.к.он уже может быть в случае onpopstate)
			//тело диалога
			
			//alert(answer);
			var resp = JSON.parse(answer);
			
			/*
			var main = document.querySelector('main');
			var articles = document.querySelector('articles');
			var parent = main.parentNode;
			parent.removeChild(main);
			parent.removeChild(articles);//*/
			
			var el = document.createElement('link');
			el.rel = 'stylesheet';
			el.href = resp['dynamic_link'];
			document.querySelector('head').appendChild(el);
			
			document.querySelector('.detail').innerHTML = resp['main'];
			
			history.pushState(null,null, _dialog);

		}
	)						
	
	_a.postData(data);
}





