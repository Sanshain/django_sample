


function fragment_refresh(e){

	var root_elem='content';

	//если это ссылка, берем из адреса
	//если это кнопка, берем из formAction-атрибута
	
	var target = 
		e.target.href.substr(location.origin.length)
		|| e.target.formAction;					
	//если иное, берем из атрибута data-to
	target =target||e.target.getAttribute('data-to');
	
	//если цель не найдена, выкидываем ошибку
	if (!target) {
								
		alert('fragment_refresh без цели');
		throw new Error('fragment_refresh без цели');
	};
	
	//для <ie10 осуществляем прямой переход
	if (!window.atob){   //<ie10
	
		document.location.href = target;
	}
							
	
	e.preventDefault();
	
	
	
	/*определяем, есть ли те или иные элементы на странице, чтобы собщить серверу, какой из
	шаблонов рендерить и возвращать*/
	
	/*теоретически это можно получать на сервере 
	из адреса страницы, но тогда по сути придется проверять весь список адресов
	(регулярк) на соответствие, после нахождения
	необходимо распарсить шаблон и найти, есть ли там этот элемент. Проще найти тут:
	*/
	
	
	//content			
	
	//main(username|age|city),section
	var unique_templates = 
		e.target.dataset['_refresh']
			.replace(/[\s]+/,'')
			.split(',');
	
	//анимация ожидания (затухание) для каждого unique_template:
	
	//если заданы детальные блоки и они не были найдены, то анимируем контейнер и добавляем этот контейнер в список aim_blocks для отправки на сервер (чтобы сервер отправил цельный блок)
	
	var aim_blocks = [];
	for (var key in unique_templates){
		
		//ищем детальные элементы для переопределения
		var details = 
			unique_templates[key].split(">");
		
		//независимо от того, есть они или нет, 1й элемент будет корневой. Ищем его в любом случае, он нам пригодится
		var _box = document.getElementById(
			details[0]
		);
		
		if (!_box){
			alert('не найден корневой элемент');
			throw new Error('не нашел root элемент');
			
			//_box = root_elem
		}
		
		var _boxes = [];
		
		//если они заданы
		if (details[1]){
			var signs = details[1].split('.');
			
			//если есть обобщитель:
			var sign = signs.indexOf('*');
			if (sign>=0){
				if (sign==0){
				
				}
				else{
					var sample = _box.querySelector(
						'#'+signs[0]
					);
					
					//если типовой элемент найден
					if (sample){
						_boxes=_box.querySelectorAll(
							'[id]'
						);
						aim_blocks.push('*'+_box.id);
						//применяем content_waiting к каждому элементу
					}
					else{
						//значит надо обновить корневой элемент:
						
					}
				}
			}
			else{
				//если нет обощителя, значит ищем каждый указанный элемент
				for(var key in signs){
					var line = details[1].querySelector
					(
						'#'+elems[key]
					);
					_boxes.push(line);
					aim_blocks.push(elems[key]);
				}								
			}
			
			//ищем каждого из них

		}
		
		function _animate(elem, visible){
			if (!visible){ // скрываем
				elem.style.transition='0.5s ease-out';
				elem.style.opacity = 0;
				
				elem.style.transform = 'scale(0.9,0.9)' //+ ' translateY(-150px)';								
				
				//var _content = elem.children[0];
				var _content = search_fixed(elem);

				if (!_content) return;
				else _content.style.top = '0';
				
				
				/*
				if (window.getComputedStyle(_content).position == 'fixed')
				{								
					_content.style.top = '0';
				}//*/
				

				
				
				
			}
			else{
			
				var temp_top = null;
			
				//тут написать спец ф-ю, которая ищет элементы с fixed до первого дерева с дочерними элементами больше 1
				
				
				if (elem.id == 'main' || elem.id == 'content'){
					var _content = elem.children[0];
					
					if (window.getComputedStyle(_content).position == 'fixed'){
					
						//временно убираем top либо подгоняем его (пока фиксированно ставлю 0 для моего конкретного случая)
						
						//- в этом случае он будет себя как обычно
						
						
						temp_top = window.getComputedStyle(_content).top;
						
						_content.style.top = '0';//*/
						
						
						
						
					}									
				}//*/

				
				setTimeout(function(){
					//возврат в top после анимации, чтобы не скроллился
					elem.style.transition = 'none';
					
					elem.style.transform = 'none';
					
					
					if (temp_top){
					
						elem.children[0].style.top = temp_top;
					}//*/
					
					setTimeout(function(){
						elem.style.transition = '0.5s';
					}, 40);
					
					
				},1000);								

			
				elem.style.opacity =1;
																						
				var _content = elem.children[0];
				
				if (!_content) return;
				
				if (window.getComputedStyle(_content).position == 'fixed'){
																						elem.style.transform=
					'scale(1,1)';
					
					//+ ' translateY(-150px)';									
				}
				else elem.style.transform ='scale(1,1)';

			}
		}							
		
		
		function content_waiting(deep, box){
		
			console.log(
				deep + ' - waiting for ' +_box.id
			);
			
			if (!deep){
				//animation отсутствия интернета
				
				alert('нет соединения с сервером');
				
				return false;
			}										
		
			setTimeout(function(){
											
				if (responsed_content){

					render_page(
						responsed_content.pop(), 
						responsed_content.pop()
					);	
					
					setTimeout(function(){
						//box.style.opacity =1;
						
						//box.className = 'block';
						_animate(box, true);
					}, 40);
				}
				else{
					//анимация и рекурсия	
					
					content_waiting(--deep);
				}

			},700);								
		}						
		

		
		//если _boxes заданы и существуют, то анимируем их:						
		if (_boxes.length){
			
			
			for (var k=0;k<_boxes.length;k++){
				//оно, может и не надо
				/*
				var attribute=abstract_viewer.property(
					_boxes[key]
				);//*/
				
				/*
				_boxes[k].style.transition = '0.5s ease-out';
				_boxes[k].style.opacity = 0;	
				//*/
				//_boxes[k].className = ('hide');
				_animate(_boxes[k], false);

				//добавляет все блоки в запрос
				//aim_blocks.push(_boxes[k].id);

				content_waiting(3, _boxes[k]);
				
			}
			
		}
		//если нет, то блок анимируем контейнера:
		else{
			var attribute=abstract_viewer.property(_box);
			
			/*
			_box.style.transition = '0.5s ease-out';
			_box.style.opacity = 0;
			//*/
			//_box.className = ('hide');
			_animate(_box,false);
			
			content_waiting(3, _box);
			
			//if (details[1]) 
				aim_blocks.push(_box.id);
		}
		
		
	}					
	
	//это данные, которые будут загружены во время анимации:
	var responsed_content = null;
	var box_onload = function (resp, set_url)
	{
		responsed_content = [set_url,resp];
	
		//render_page(resp, set_url);
	}
	
	
	var ajax = new Ajax(target, box_onload);
	ajax.onfail = function(){
		//здесь может быть относительно 
		// навязчивое сообщение о том, что 
		//ваш браузер не поддерживает 
		//автоматические переходы
		alert('ваш браузер не смог осуществить частичное обновление контента страницы.'+
		' Нажмите ок, чтобы перейти напрямую');
		document.location.href = target;
	};
	
	
	//что отправляем на сервер? - :
	
	//define flag:
	
	//мы знаем из data-_refresh-атрибута, что содержимое, которое вернется с сервера, явлется[, например, для #_dialogs-селектора]  полноценным содержимым селектора '.content'. Для других элементов это может быть .main, .section и т.п.
	
	//однако, если на странице отсутствует блок .aside (что возможно в некоторых вариантах шаблонов), то его так же нужно запросить с сервера. То же самое касается и .section и др блоков
	
	

	
	//теперь, получаем все требуемые элементы для запрашиваемой с сервера страницы
	
	//получаем массив id-шников с их состояниями
	var required_blocks = 
			e.target.dataset['_require'].split('.');
						
	//проверяем их: если элемент существует и состояние соответствует, то
	
	var requested_blocks = [];
	
	for(var key in required_blocks){
		var detail = required_blocks[key].split('|');
		
		var b_id = detail.pop(); //id элемента
		var r_state =detail.length ?detail.pop(): '';
		var state = '';
		
		required_block = dom.obj(b_id);
		if (required_block && r_state){
			//получили блок. Теперь необходимо получить его состояние:
			
			//для (неуправляющего) простого тега (который содержит только текст) допускается атрибут data-state, который содержит состояние этого элемента (например data-state='1')
			state = 	
				required_block.getAttribute['data-state'];
			
			//если тег является управляющим (управляющие элементы не содержат своего состояния), то ловим состояние в его контенте, а именно - в элементе, управляющем позиционированием контента, - это первый элемент контента
			if (!state){
				var elem=
					required_block.children[0];
					
				//его состояние хранится в его id
				//либо в data-state, либо и там и там
				state = 
					elem? 
						elem.id+
						elem.dataset['state'] || ""
					:"";

				
			}
			
		}
		
		//теперь у нас есть required_block и r_state:
		//для выполнения условия required_block должен быть thruthy, а state==r_state
		
		if (required_block && r_state==state){
			continue;
		}
		else 
			requested_blocks.push(b_id);
		
		
	}
	
	
	//юзер на сервере получает всего лишь id юзера
	//попробуем изменить:
	/*!
		Для юзера нужны следующие поля:
		
		main(sex.age.city.ava.action),section,header
		
		#sex
		#age
		#city						
		#image? - #ava как управляющий
		#action%{formAction|value(innerText)} - слож
		
		#section|article_block__[\d]+			-упра
		#header|username[\d]* - управляющий
	*/
	
	
	
	var args = target.match(/\d+/g);//аргументы
	
	var nec_blocks = requested_blocks;
	
	var blocks = aim_blocks.concat(nec_blocks);
	
	var q = [args, nec_blocks, aim_blocks];
	
	ajax.submit_json(q);
}