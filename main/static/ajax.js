
var ENCTYPE = 'application/x-www-form-urlencoded';


function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {							
			
			var cookie = cookies[i].trim();										//совместимо с ie8
			
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}//*/
		}
	}
	return cookieValue;
}



//подробно https://learn.javascript.ru/ajax-xmlhttprequest

///без подтверждения
function POST_AJAX(data, url){
					
	if (url == undefined) url = window.location.href;
					
	var csrftoken = getCookie('csrftoken');	

	data = 'csrfmiddlewaretoken=' + csrftoken + '&' + data;		

	// 1. Создаём новый объект XMLHttpRequest			
	var xhr = new XMLHttpRequest();				
	
	// 2. Конфигурируем его: GET-запрос на URL /submit
	xhr.open("POST", url, true);						//метод, адрес, асинхрон/неасинхронный
	
	// 3. Устанавливаем заголовк ENCTYPE
	xhr.setRequestHeader('Content-Type', ENCTYPE);	
	
	xhr.timeout = 3000;						
	
	xhr.onreadystatechange = function() {					
				
		if (XMLHttpRequest['status']){										//для ie8
			if (xhr.status != 200) 
			{					
				alert("Не удалось отправить запрос: " + xhr.statusText + ' на ' + this.readyState + " этапе");					
			}
		}			
		
		if (this.readyState == 3) {
			//alert('responseText:' + this.responseText );					
			
			var elem = document.getElementById(this.responseText).querySelector('.to_friend');
			if (1 + elem.className.indexOf('sended') > 0)			  				//elem.classList.contains('sended')
			{
				elem.innerText = 'Дружить';
				elem.className = elem.className.replace('sended','').trim();		//elem.classList.remove('sended');
			}
			else
			{							
				elem.innerText = 'Раздумать';
				elem.className+= ' sended';											//elem.classList.add('sended');							
			}
			
		}						
		
		//if (this.readyState == 4) alert('запрос завершен');
	}		
	
	xhr.send(data);
	
}

//подробно https://learn.javascript.ru/ajax-xmlhttprequest
function POST(data, func, csrftoken){				
					
	if (csrftoken == undefined) csrftoken = getCookie('csrftoken');	

	data = 'csrfmiddlewaretoken=' + csrftoken + '&' + data;		
	var url = window.location.href;

	// 1. Создаём новый объект XMLHttpRequest			
	var xhr = new XMLHttpRequest();				
	
	// 2. Конфигурируем его: GET-запрос на URL /submit
	xhr.open("POST", url, true);						//метод, адрес, асинхрон/неасинхронный
	
	// 3. Устанавливаем заголовк ENCTYPE
	xhr.setRequestHeader('Content-Type', ENCTYPE);	
	
	xhr.timeout = 30000;													// для лонг пул				
	
	var unresponsed = true;
	
	xhr.onreadystatechange = function() {							
				
		if (XMLHttpRequest['status']){										//для ie8
			if (xhr.status != 200) 
			{					
				alert("Не удалось отправить запрос: " + xhr.statusText + ' на ' + this.readyState + " этапе");					
			}
		}			
		
		if (this.readyState == 3) {				
		
			//unresponsed = false;							
			//func(this.responseText);
			
			console.log('3: ' + this.responseText);
			
			//alert("responseText3: " + this.responseText);			

		}	

		if (this.readyState == 4 && unresponsed) {	
			
			console.log('4: ' + this.responseText);
			
			unresponsed = false;			
			
			//alert("responseText4: " + this.responseText);
				
			func(this.responseText);
		}		
				
	}		
	
	xhr.send(data);
	
}



function Ajax(url, func, csrftoken) { 

	//-
	if (!('\v'=='v')) console.time('server_response_time');
	//-

	this.url = url || document.location.href;//целевйой урл
	this.csrftoken = csrftoken;		// csrftoken-токен
	this.func = func;				// функция принятия ответа
	this.contentType = null;
	var self = this;
	
	this.__post = function(data, func, url) {				
				
		var unresponsed = true;								// 0.1. устанавливаем флаг ответа
		
		var xhr = new XMLHttpRequest();						// 1. новый объект XMLHttpRequest					
		xhr.open("POST", url, true);						// 2. Конфигурируем: тип, URL, асинхрон/неасинхронный
		
		if (data instanceof Object) {  
		
			
			//если. например, форма без содержания
			if (this.contentType == null){
				
				// на случай в виде json
				
				xhr.setRequestHeader("X-CSRFToken",data['csrfmiddlewaretoken']);				
				
				xhr.setRequestHeader(
					'Content-Type', 
					'application/json'
				);
						
				data = JSON.stringify(data); // на случай json
			}
			else	//для формдата с содержанием
			{
				// на случай formdata		
				//xhr.setRequestHeader('Content-Type', "multipart/form-data");
				
				/*
				xhr.setRequestHeader(
					'Content-Type', 
					this.contentType
				);//*/
			}

			
			
		}
		else{ 								//на обычный текст 
			xhr.setRequestHeader('Content-Type', ENCTYPE);		// 3. Устанавливаем заголовк ENCTYPE	

			//alert('simple');
		}
		
		xhr.onreadystatechange = function() {				// получаем результат				
					
			if (XMLHttpRequest['status']){										//для ie8
				if (xhr.status != 200) 
				{					
					alert("Проверьте соединение с интернетом: " + xhr.statusText + ' в статусе ' + this.readyState);
					
					return;
				}
	
			}
			
			if(this.readyState == 4 && this.status == 200)
			{
				func(this.responseText, url); 
				
				//-
				if (!('\v'=='v')) console.timeEnd('server_response_time');
				//-
			}			
		
		}		
		
		xhr.send(data);		
	};
	
	
	/*! вернет объект js с полями формы либо FormData
		в зависимости от this.contentType
	*/
	var getdata = function(frm){
		
		if (self.contentType == null){
			var data = {'csrfmiddlewaretoken':frm.elements[0].value};
			for(var i=1; i<frm.elements.length - 1; i++)   
			{ 
				var elem = frm.elements[i];     
				data[elem.id] = elem.value;

			}

			return data;
		}
		
		var fdata = new FormData(frm);
		//fdata.csrfmiddlewaretoken = frm.elements[0].value;
		return fdata;

	};

	
	
	
	
	this.postData = function(data, func){
		
		//$("input[name=csrfmiddlewaretoken]").val()
		data = 'csrfmiddlewaretoken=' + (this.csrftoken || getCookie('csrftoken')) + '&' + (this.data || data);	
		
		this.__post(data, this.func || func, this.url);
	};
	
	this.post_form = function(frm, func){		
		
		var data = getdata(frm);
		
				
		this.__post(data, this.func || func, this.url || window.location.href);
		
	};
	

	
} 

