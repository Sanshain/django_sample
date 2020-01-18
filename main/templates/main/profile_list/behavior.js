function user_click(sender, e){	
	
	e.target = e.srcElement || e.target;							// e.srcElement - для IE8		
		
	// если элемент, по которому жмакнули, имеет базовый класс `friend` (предполагается, что такой класс может быть только у кнопки):
	if (e.target.className.indexOf("friend") == 0) {					
		
		if (!e.target.unfolded){									// то, если кнопок нет, создаем кнопки		
			e.target.unfolded = true;
			sender.style.height = '90px';
			e.target.style.backgroundColor = 'lightcyan';
			
			var top = 5;
			var step = 25;
			var butts = ['Личное','Забыть'];
			var styles = ['closer', 'leave']
			
			for(var i=1;i<3;i++){
				var butt = document.createElement('button');				
				butt.style.top = top + 10*i + i*step + "px";
				butt.className = "to_friend " + styles[i-1];
				butt.innerHTML = butts[i-1];			
				sender.appendChild(butt);
			}			
		}
		else{														// а если есть, удаляем кнопки
			e.target.unfolded = false;
			
			sender.style.height = '1.2rem';
			
			setTimeout(function(){
				if (e.target.unfolded = false){
					sender.removeChild(sender.lastElementChild);			// lastChild 
					sender.removeChild(sender.lastElementChild);							
				}
			}, 1000);
		}
		
		return;				
	}
	
	var addressee = Number(sender.id) || sender.id.substring(3);
	
	if(sender == e.target){											// по строке - переходим на страницу юзера
		
		ToUser(addressee);
	
	}
	else{															// по кнопке - обрабатываем
		
		if (e.target.name == 'self'){								// если это вы, то переходим к вам
			
			alert('Это ж вы!');			
			
			var base_url = "{% url 'edit_self' 0 %}";
			
			addressee = document.getElementById('me').name;
			
			base_url = base_url.replace('0', addressee)
			
			document.location.href = base_url;
			
			return;
		}
		else{														// если нет, то просто отправляем ajax-заявку о дружбе		
			
			var data = 'id=' + addressee;						
				
			POST_AJAX(data, '{% url 'to_friend' %}');					
		}		
		
	}
}	




function user_mousedown(sender, event){
	if (event.which == 2){										// колесиком - открываем в новой вкладке	
		ToUser(sender.id.substring(3));
	}
}


/*!
	Отправляем заявку о дружбе
*/
function ToFriend(addressee){
	
	if (addressee) POST_AJAX('id=' + addressee, '{% url 'to_friend' %}');
	else
	{
		
		var base_url = "{% url 'edit_self' 0 %}";		
		base_url = base_url.replace('0', addressee); //can add links for return to list users after save
		document.location.href = base_url;//*/
				
	}
}

function ToUser(addressee){
		var base_url = "{% url 'user' 0 %}";		
		
		base_url = base_url.replace('0', addressee);
		
		document.location.href = base_url;
}