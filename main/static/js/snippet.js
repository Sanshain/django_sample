
/*!

	e - expected event object
*/
RefreshManager.Initialize = function(e){	

	//если это ссылка, берем из адреса
	//если это кнопка, берем из formAction-атрибута
	
	var target = 
		e.target.href.substr(location.origin.length)
		|| e.target.formAction;						
	//если иное, берем из атрибута data-to
	target =target||e.target.getAttribute('data-to');

	
	if (!target) {
		
		throw new Error('RefreshManager cant be initialized');
	};
		
	if (!window.atob){					//just for <ie10

		document.location.href = target;			
	}
	else {
		e.preventDefault();	
		
		var _rm = new RefreshManager(e);
		
			   _rm.target = target;
		return _rm;			//если нет, кастомизируем
	};
}



function RefreshManager(e, root_elem){
	
	var self = this;
	var root_elem=root_elem || 'content';   	//obsolete
	
	var unique_templates = 
		e.target.dataset['_refresh']
			.replace(/[\s]+/,'')
			.split(',');	
	
	this.aim_blocks = [];			// id блоков для запроса 
	
	
	var get_boxes = function(block_name){
		
		
		var details = block_name.split(">");
		
		var _box = document.getElementById(details[0]);
		
		if (!_box)
			throw new Error('root element not found');
	
		var _boxes = []; 		// боксы для анимации		
		
		if (details[1]){
		
			var signs = details[1].split('.');
			
			var sign = signs.indexOf('*');
			
			if (sign>=0){
				if (sign==0){
					//если не заданы одноуровневые поля
					
					//такого случая пока нет, но скорее всего брать все дочерние с id 
					
					//(либо data-state)
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
						self.aim_blocks.push('*'+_box.id);
						//применяем content_waiting к каждому элементу
					}
					else{
						//значит надо обновить корневой элемент: ничего не делаем
					}					
				}
			}
			else{
				//если нет обощителя, значит ищем каждый указанный элемент
				for(var key in signs)
				{
					var line = details[1].querySelector(
						'#'+elems[key]
					);
					_boxes.push(line);
					self.aim_blocks.push(elems[key]);
				}								
			}		
		}
		
		return _boxes.length ? _boxes : _box;
	}
	
						
	function _animate(elem, visible){
		if (!visible){ // скрываем
		
			//можно засунуть в класс
			elem.style.transition='0.5s ease-out';
			elem.style.opacity = 0;			
			elem.style.transform = 'scale(0.9,0.9)';								
			var _content = search_fixed(elem);

			if (!_content) return;
			else 
				_content.style.top = '0';
			
		}
		else{
		
			var temp_top = null;
		
			//тут написать спец ф-ю, которая ищет элементы с fixed до первого дерева с дочерними элементами больше 1			
			
			var _content = null;
			
			if (elem.id == 'main' || elem.id == 'content'){
				//var _content = elem.children[0];
				var _content = search_fixed(elem);
				
				if (_content){
//!
					temp_top = window.getComputedStyle(_content).top;		//либо 
					//temp_top = _content.offsetTop;
					_content.style.top = '0';//*/
				}
				
			}

			//показывает информацию через 1 сек
			setTimeout(function(){
				//возврат в top после анимации, чтобы не скроллился
				elem.style.transition = 'none';			
				elem.style.transform = 'none';
								
				if (temp_top) _content.style.top = temp_top;
				
				setTimeout(function(){
					elem.style.transition = '0.5s';
				}, 20);
				
			},1000);								

			elem.style.opacity =1;
//!
			if (!_content) return; //<-скорее всего это убрать
			
			elem.style.transform='scale(1,1)';			

		}
	}							
	
	
	/*!  регулярует вызов функции анимации...
	
		\brief регулярует вызов функции анимации для каждого..
		блока и подблока после получения данных
		
		@param deep - глубина ожидания
		@param box - блок, для которого ожидается анимация
		
	*/
	function _await__animate(deep, box){
	
		console.log(deep + ' - waiting for ' + box.id);
		
		
		if (!deep){ //animation отсутствия интернета
			
			alert('нет соединения с сервером');
			
			return false;
		}										
	
		setTimeout(function(){
			
			if (responsed_content){

				render_page(
					responsed_content.pop(), 
					responsed_content.pop()
				);	
				
				//происходит анимация
				setTimeout(function(){ //box.style.opacity =1;
					
					
					//box.className = 'block';
					_animate(box, true);
				}, 40);
			}
			else {
				
				_await__animate(--deep, box);
			}			

		},700);								
	}	
	
	
	var package_animate = function(block_name){
		
		var responsed_content = null;
		
		var _boxes = get_boxes(block_name);
		
		if (_boxes.length){
			
			for (var k=0;k<_boxes.length;k++){
				
				_animate(_boxes[k], false);
				
				_await__animate(3, _boxes[k]);
			}
		}
		else{
			_animate(_boxes, false);
			
			_await__animate(3, _boxes);
						
			self.aim_blocks.push(_boxes.id);			
		}
		
	}
	
	for (var key in unique_templates){
		
		package_animate(unique_templates[key]);
	}
		
	var nec_blocks = requested_blocks_by_require();

	//var blocks = aim_blocks.concat(nec_blocks);
	
	
	
	this.Commit = function(){
		var box_onload = function (resp, set_url)
		{
			responsed_content = [set_url,resp];			
		}		
			
		var ajax = new Ajax(this.target, box_onload);
		ajax.onfail = function(){
			//здесь может быть относительно 
			// навязчивое сообщение о том, что 
			//ваш браузер не поддерживает 
			//автоматические переходы
			alert('ваш браузер не смог осуществить частичное обновление контента страницы.'+
			' Нажмите ок, чтобы перейти напрямую');
			document.location.href = this.target;
		};
		
		var args = self.target.match(/\d+/g);//аргументы
		
		var q = [args, nec_blocks, self.aim_blocks];
		
		ajax.submit_json(q);		
	}
	
	
	
	
	
	
	
	
	
	
	function requested_blocks_by_require(){	
	
		var requared_blocks = 
			e.target.dataset['_require'].split('.');
			
		var r_blocks = [];
		
		
		for(var key in requared_blocks){
			
			var detail = requared_blocks[key].split('|');
			
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
				r_blocks.push(b_id);
		
		
		}
		
		return r_blocks;
		
	}
	
}








