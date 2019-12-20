var last_mess_id;					// for Checking

/*!	Получает (и показывает) сообщения после проверки...

*/
var Get_Messages = function(response){

	if (response != 'nop' && response != ''){
		var messages = JSON.parse(response);
		var listMessages = document.querySelector('.messages');
		for (var key in messages)
		{
			var mess = vom.add(listMessages, 
				Elem('li', messages[key], 'y message')
			);
			vom.add(mess, Elem('span', key, 'mess_id'));
			vom.add(mess, Elem('sub', Time(), 'mess_time'));
		}
						
		if (listMessages.offsetHeight >= listMessages.parentElement.offsetHeight - 35)
		{
			listMessages.children[listMessages.children.length-1].scrollIntoView(false);				
		}
	
		document.bell_get();
	}
	
	Checking();
};


/*! Проверка (регулярная) сообщений на сервере...

*/
var Checking = function(){
	
	var messages = document.querySelectorAll('.mess_id');
	
	if (messages){
		last_mess_id = messages.length ? messages[messages.length-1].innerText : 0;
		
		var data = 'check='+ last_mess_id;
		//POST(data, Get_Messages);		
	}
	else if(last_mess_id)
	{
		//если last_mess_id уже был назначен ()
	}
		
};



/*! Отправляет сообщение на сервер по нажатию enter...
	
*/
function enter(sender, event){
		
	if(event.keyCode == 13){// && event.ctrlKey
	
		if (sender.value == "")
		{
			event.preventDefault(); return false;
		}
		//sender.parentElement.submit();				
		var value = sender.value;	
		
		var data = 'value=' + sender.value;	
			
		this.success = function(result){
		
			
			if (result == '_ok_'){
				
				var list = document.querySelector('.messages');
				var li = vom.add(list, Elem('li', value, 'message'));
				vom.add(li, Elem('sub', Time(), 'mess_time'));
				
				if (list.offsetHeight >= list.parentElement.offsetHeight - 35)			// в данном случае ==
				{
					list.style.height = list.parentElement.offsetHeight - 35 + "px";
					
					var offset = list.scrollHeight - list.clientHeight;
				
					list.parentElement.scrollTop = offset;							
				}						
				
			}
		}
			
		POST(data, success);

		sender.value = '';
					
		if (event.preventDefault) event.preventDefault();
		else event.returnValue = false;	


		
		//-
		if (document.bell_post) 
		//-
	
			document.bell_post();
			
		//-
		else console.log('document.bell_post is not defined');
		//-

		
	}
};

















/*!
	просмотр на весь экран
*/
function InitPreviver(){
	
	var container = document.createElement('div');
	
	container.style.position = 'fixed';
	container.style.top = "0px";
	container.style.left = "0px";
	container.style.right = "0px";
	container.style.bottom = "0px";
	container.style.zIndex = "100";
	container.style.position = "fixed";
	container.style.backgroundColor = 'rgba(105, 102, 102, 0.87)'; //'lightgray';	
	container.style.textAlign = 'center';
	container.style.lineHeight = '100vh';				
	container.style.display = 'none';
	
	document.querySelector('body').appendChild(container);
	
	return container;
}






//var temp_img_id = 0; //temp

//событие на загрузку файла
/*!
	После загрузки файла в озу js, отобразить его
*/
function img_load(e) {

	
	var parent = document.querySelector('.messages');
	var mess = document.createElement('li');
	mess.style.marginBottom = '7px';
	mess.style.height = '200px';
	
	var img = new Image(); 
	img.height = 200;
	img.src = e.target.result;
	
	img.style.backgroundSize = 'rgba(105, 102, 102,0.87)';
	img.style.cursor = 'pointer';		
	
	mess.appendChild(img);
	parent.appendChild(mess);
	
	mess.scrollIntoView(false); //- не до конца
	parent.parentElement.scrollTop += 10; 
	// при условии, что полосы прокрутки уже есть
	
	//итак, показали. Теперь надо отправить на сервер:
	var data =document.querySelector("#uploadImage").form;
	
	
	
	
	
	//это должно происходить на последнем FReader,
	// когда все данные уже загружены в форму
	/*
	var media_message = new Ajax(null, function(ans){
		alert(ans);
	});
	media_message.contentType = 'multipart/form-data';
	media_message.post_form(data);
	//media_message.contentType = 'application/x-www-form-urlencoded';//*/
	
	
	
	
	
	
	
	//возвращает картинку с вида на весь экран в сообщение
	var reduce_image = function(elem){
		
		img.style.height = '200px';
		img.align = 'left';
		imgContainer.style.display = 'none';
		mess.appendChild(img);
		
	};
	
	img.onclick = function(event){

		if (imgContainer.style.display != "block"){

			imgContainer.style.display = 'block';
			imgContainer.appendChild(img);	
			
			img.className = "img_in_message";
			img.align = 'middle';
			img.tabIndex = 0;
			img.focus();
		}
		else
			reduce_image(mess);		
		
	};
	
	mess.onkeydown = function(event){
		
		if (event.code == 'Escape') {
			reduce_image(mess);
		}
	};
	
};



// функция выборки файла
function loadImageFile(event) {
		
	var files = event.target.files;
	
	if (files.length > 1){
		var parent = document.querySelector('.messages');
		
		for (var i = 1; i < files.length; i++) {
			var file = files[i];
			
			if (!file.type.match('image')) continue;
			
			var picReader = new FileReader();
			picReader.onload = img_load;
			/*
			picReader.addEventListener("load", function (event) {
				var picFile = event.target;
				var div = document.createElement("span");
				div.innerHTML = "<img height=200 src='" + picFile.result + "'" + "title='" + file.name + "'/>";
				parent.insertBefore(div, null);
			});*/
			
			picReader.readAsDataURL(file);
		}				
	}
			
	var file = document.querySelector("#uploadImage").files[0];
	FReader.readAsDataURL(file);
	
	
	
	//итак, показали. Теперь надо отправить на сервер:
	var data =document.querySelector("#uploadImage").form;
	
	
	var media_message = new Ajax(null, function(ans){
		//alert(ans);
	});
	media_message.contentType = 'multipart/form-data';
	media_message.post_form(data);		
	
}


/*!
	@brief Должен находиться в windows.onload
	либо запускаться при динамической загрузке
	
	Пока не реализован
*/

function InitializePage(){					//reInit_detail

	imgContainer = InitPreviver();
	
	FReader = new FileReader();
	
	FReader.onload = img_load;
	
	dom.get("#uploadImage").onchange = loadImageFile;
	
	
	
	
	
	var list = document.querySelector('.messages');
	if (list.offsetHeight >= list.parentElement.offsetHeight - 35){
	// создаем скролл
	
		list.style.height = list.parentElement.offsetHeight - 35 + "px";
		list.children[list.children.length-1].scrollIntoView(false);
		document.querySelector('.dialog').scrollTop += 5;
	}

	//создаем звонки
	document.bell_get = new Bell("{% static 'music/get.mp3' %}");
	document.bell_post = new Bell("{% static 'music/post.mp3' %}");

	//проверка входящих
	setTimeout(Checking, 1000);	

	
	
	
	InitializePage = null;
	
}

if (vom.spa) InitializePage();

//vom.init_list.push(InitializePage);