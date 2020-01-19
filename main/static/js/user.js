var Note = {}; 								/* пространство имен Note */
	


/*! Показывает окно создания записи...
	
	Вызов лежит в aside_inside блоке юзера
*/
function __createView(){

	//document.location.href = "{% url 'note_create' %}";
	
	//document.getElementById('id_Title').focus();
	//document.getElementById('id_Title').value = '';
	
	//document.querySelector('.articles_list').style.visibility='hidden';
	
	var new_art = document.getElementById('win');	
	
	//dom.get('.articles_list').style.transition ='1s';		
		

	window.onmousewheel = function(){ return false };
	
	//new_art.removeAttribute('style');	
	
	new_art.style.transition = "1s";	
	new_art.style.visibility = 'visible';
	new_art.style.opacity = 1;	
	
	
	setTimeout(function(){
		dom.get('.articles_list').style.opacity = 0;
		dom.get('.articles_list').style.visibility = 'hidden';	
	
		

	
		//document.getElementById('id_Content').focus();
	},1100);
	
	//document.querySelector('.visible').style.height = '80vh';	
};


/*! Скрывает окно создания записей...
	 (обратная note_create)
*/
function __hideView(){

	document.getElementById('win').style.visibility ='hidden';
	document.getElementById('win').style.transition ='1s';
	
	document.getElementById('win').style.opacity='0';

	dom.get('.articles_list').style.visibility = 'visible';
	//setTimeout(function(){ dom.get('.articles_list').style.display = 'block';} , 1000);
	
	window.onmousewheel = function(){ return true };
	
	dom.get('.articles_list').style.visibility = 'visible';	
	dom.get('.articles_list').style.opacity = 1;		
	
	
	setTimeout(function(){

		document.getElementById('win').style.transition ='2s';
		

		//document.getElementById('id_Content').focus();
	},1100);
	
	
	
	//document.querySelector('.articles_list').style.visibility='visible';
	
	//document.querySelector('.visible').style.height = '10vh';
	
};


/*! Добавляет запись в поток и отправляет на сервер...
 записей (статей) страницы. 
 
	И отправляет на сервер 
*/
function __post_View(sender, e){
	e.preventDefault();
	
	//отправляем данные формы на сервер
	this.new_note = this.new_note || new Ajax(
		_note_create ,function(answer){
			
			var value = JSON.parse(answer);
						
			var h = Elem('h4',value.title,'');
			h.style.marginTop = '5px';
			
			var note = Elem('div', '', 'Anote');
			note.appendChild(h);
			note.appendChild(Elem('div',value.content,''));
			
			var last_note = 
				dom.get('.articles_list').firstChild;
				
			last_note.parentNode.insertBefore(note,
				last_note
			);
		}
	);
	
	this.new_note.multipartJSON = 'multipart/form-data';
	this.new_note.post_form(document.querySelector('#note'))
	
	//скрываем article_editor:
	document.getElementById('win').style.visibility='hidden';
	document.getElementById('win').style.opacity='0';

	

	
	setTimeout(function(){
		
		window.onmousewheel = function(){ return true };
		
		document.getElementById('id_Title').value = '';
		document.getElementById('id_Content').value = '';
		
	
		
	}, 2000);
	
	
	setTimeout(function(){
		dom.get('.articles_list').style.visibility = 'visible';	
		dom.get('.articles_list').style.opacity = 1;
	}, 1000);

	
};







Note.createView = __createView;
Note.post_View = __post_View;
Note.hideView = __hideView;


function microButtonAnimated(container, content, name){
	elem = vom.add(container, 'div');
	elem.innerHTML = content;
	elem.id = name;
	elem.setAttribute('style', 'position:absolute;'+
		'top:5px;right:5px;height:10px;width:10px;'+
		'background-color:orange;'+
		'text-align:center;line-height:10px;'+
		'color:transparent;transition:1s, opacity 0s;'+'border-radius:0;opacity:0;'+
		
		'font-size:0.5em;padding-top:1px;'+
		'padding-left:1px;box-sizing:border-box');	
		
	elem.onmouseover = function(){
		
		var ang = this.ang || 405;
		elem.style.transform = 'rotate(' + ang + 'deg)';
		elem.style.backgroundColor = 'red';
		
		setTimeout(function()
		{
			elem.style.color = 'blue';
			elem.style.borderRadius = '5px';
		},1000);
	};
	
	elem.onmouseout = function(){
		elem.style.transform  = 'rotate(0deg)';
		elem.style.backgroundColor = 'orange';
		
		elem.style.borderRadius = '0px';
		
		setTimeout(function()
		{
			elem.style.color = 'transparent';			
		},1000);								
	};
	
	//i == 1|2|4|8
	this.setPosition = function(x, y, i){
		
		if(!i){
			elem.style.right = x+'px';
			elem.style.top = y+'px';			
		}else{
			elem.style.right = x+'px';
			elem.style.bottom = y+'px';					
			elem.style.top = 'auto';					
		}
		
		return this;
	};
	
	this.setAngle = function(ang){	
		elem.ang = ang;
		return this;
	};
	
	this.setCls = function(cls){
		elem.className = cls;
		return this;
	};
	
	this.click = function(func){
		elem.click = func;
		
		return this;
	}
	
	this.Elem = elem;
	
}




Note.__upload_images = function(event){
	
	if (!event.target.files){
		//(кстати поддерж лишь 1 файл):
		
		/*! 
			отправляем на сервер сразу (только куда)
			
				либо
				
			отображаем только названия картинок
			
			*/
		
		
		
		
		alert(event.target.value);
		//а затем показываем анимацию
		
		return;
	}
	
	//для ie10 и выше:
	for (var i = 0; i < event.target.files.length; i++) {
	
		//само расширение будет проверять сервер
		if (!event.target.files[i].type.match('image')) 
		
			continue;		
		

		
		var reader = new FileReader();
		reader.onload = function(e){
			
			var previewer = dom.obj('article__imgpreviewer');
			
			
			var img = dom.createElement('div');
			img.className = 'article_img';
			
			img.setAttribute('style',
				'height: 50px; width: 50px;'+
				'margin: 7px;'+
				'background-size: 90% 90%;'+
				'background-repeat: no-repeat;'+
				'border: 1px solid gray;'+
				'cursor: pointer;'+
				'transition: 1s;'+
				'background-position: center;');
			//img.style.transform = 'scale(2,2)';

			var img_close = vom.add(img, 'div');
			img_close.innerHTML = '+';
			img_close.setAttribute('style', 'position:absolute;'+
				'top:5px;right:5px;height:10px;width:10px;'+
				'background-color:orange;'+
				'text-align:center;line-height:10px;'+
				'color:transparent;transition:1s, opacity 0s;'+'border-radius:0;opacity:0');
			img_close.onmouseover = function(){
				img_close.style.transform = 'rotate(405deg)';
				//img_close.style.opacity = '1';
				
				img_close.style.backgroundColor = 'red';
				
				setTimeout(function(){
					img_close.style.color = 'brown';img_close.style.borderRadius = '5px';
				},1000);
			}
			img_close.onmouseout = function(){
				img_close.style.transform  = 'rotate(0deg)';
				img_close.style.backgroundColor = 'orange';
				img_close.style.borderRadius = '0px';
				
				setTimeout(function(){
					img_close.style.color = 'transparent';
					
				},1000);								
			}
			img_close.onclick=function(){
				
			}
			
			/*
			var img_show = vom.add(img, 'div');
			img_show.innerText = '\u25B6';//\u25B6
			img_show.className = 'img_show';
			img_show.style = 'position:absolute;'+
				'bottom:5px;right:5px;height:10px;'+
				'background-color:beige;width:10px;'+
				'text-align:center;line-height:10px;'+
				'transition:1s;'+'border-radius:0;opacity:0;'+'color:blue;font-size:0.6em;'+
				'padding-left:1px;box-sizing:border-box';			//color:transparent;*/
				
				
			var img_show = new microButtonAnimated(
				img, 
				'\u25B6',
				'img_show').setAngle(360).click(function(e){
					
				});
			img_show = img_show.setPosition(5,5,1).Elem;
			
			img.id = get_maxim(previewer.children, 'id') + 1;
			img.onclick = function(event){
				var notearea = document.querySelector('#id_Content');
				
				//alert(notearea.selectionStart);
								
				
				var pos = notearea.selectionStart;
				var sel = notearea.selectionEnd;
				
				var template = '\n<`'+ img.id +'`>\n';
				
				var patt = notearea.value.indexOf(template);
				if (patt >= 0){
					alert("Это изображение уже добавлено");
					notearea.selectionStart = patt;
					notearea.selectionEnd = patt+7;
					notearea.focus();
					
					return;
				}
				
				notearea.value = 
					notearea.value.slice(0, pos) + 
					template + 
					notearea.value.slice(sel);
				notearea.selectionStart = notearea.selectionEnd = pos + 7;
				notearea.focus();
				
			};

			img.onmouseover = function(){
				img.style.transform = 'scale(2,2)';
				img.style.zIndex = '3';
				/*img_close.style.opacity = '1';
				img_show.style.opacity = '1';//*/
			};
			
			img.onmouseout = function(){
				img.style.transform = 'scale(1,1)';
				img.style.zIndex = '0';
				/*img_close.style.opacity = '0';
				img_show.style.opacity = '0';//*/
			};
			
			img.onmousemove = function(e){
				var x = e.offsetX || e.layerX;
				var w = img.style.width.replace(/\D+/g,"");
				var k = 0.5;
				
				if (x > w*k || e.target != img){
						
//document.querySelector('#username').innerText = -Math.pow(x - w*0.5,2)+1;
					var kX = Math.sqrt(x - w*k)/
							(Math.sqrt(w*k)*0.6);
				
					var y = e.offsetY || e.layerY;
					
					if (y>w/2 || e.target == img_show){
						img_close.style.opacity = 0.1;
						img_show.style.opacity = kX;
					}
					else{
						
						img_close.style.opacity = kX;
						img_show.style.opacity = 0.1;						
					}
					
					
				}
				else{
					img_close.style.opacity = '0';
					img_show.style.opacity = '0';
				}
				


			};			
			
			img.style.backgroundImage= 'url('+
				e.target.result
			+')';
			
			previewer.appendChild(img);
			
			
			/*var image = new Image(); 
			image.src = e.target.result;
			image.height = 50px;
			image.width = 50px;//*/
			
			
		}
		reader.readAsDataURL(event.target.files[i]);
				
	}
	
	
	
}

Note.__upload_titleImg = function(event){
	event.preventDefault();
	
}




/*! action under user (Rule function instead go_to_dialog)...

	Получает из атрибутов кнопки (пока только той, что под аватаркой) параметры для запроса
	Делает запрос и рендерит страницу
	
	Можно применять к любой кнопке на странице, применив
	sender.formAction 
*/
var do_action = function(sender, event){
	if (!window.atob)  location.href = sender.formAction;

	//sender.dataset
	
	event.preventDefault();

	var user_id = document.location.pathname.match(/\d+/)[0];
	var set_url = sender.formAction;
	var get_view = 
		sender.name ? '/'+sender.name+'/' : set_url;

	

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

	

