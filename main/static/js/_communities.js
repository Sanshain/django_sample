/*!  Elem

*/
function PopupIntroduce(switch_off, url){
	var inbox = document.createElement('div');
	inbox.className = 'insert_group';
	event.target.parentElement.appendChild(inbox);
	
	this.switch_off = switch_off;
	var self = this;
	
	
	var backdrop = vom.add(dom.body, 'div','fon');
	vom.add(inbox, 'div', 'pp_close').vs({title:'Закрыть'}).onclick = function(){
		if (confirm("Вы уверены, что не хотите создать группу?")){
			self.Destroy();
		}			
	};
	
	vom.add(inbox, 'div', 'pp_create').vs({
		tabindex:0
	}).onclick = function(){
		var community_creator = new Ajax(url, function(response){
			alert(response);
			self.Destroy();       
		});
		community_creator.submit_form(inbox);
	};		
	
	
	var titleInput = vom.add(inbox, 'input', '').vs({ 
		placeholder : 'Наименование сообщества',
		name : 'title'
	});
	/*
	vom.add(inbox, 'button', 'logo_plus').vs({
		onclick : "alert(0)",			
	}).innerText = '...';//*/
	
	vom.add(inbox, 'textarea', '').vs({
		placeholder : 'Краткое описание',
		name : 'definition'
	});
	/*
	vom.add(inbox, 'input', '').vs({
		type : 'file',
		name : 'logo',
		style : 'display:none;'
	});
	//*/
	
	
	//анимирует плавное появление:
	setTimeout(function()											//вместо requestAnimationFrame
	{									
		inbox.style.opacity = '1';
		inbox.style.transition = '0.6s';
		inbox.querySelector('input').focus();
	}
	, 20);		
	
	
	
	this.Destroy = function(func){
	
		inbox.style.opacity = '0';			
		backdrop.style.opacity = '0';
		
		if (this.switch_off) switch_off();
		
		setTimeout(function()											//вместо requestAnimationFrame
		{									
			inbox.parentElement.removeChild(inbox);								//parentNode	
			backdrop.parentElement.removeChild(backdrop);						//parentNode	
		}
		, 600);		
				
	}
	
}


var group_introduce = null;
function insert_group(event, url){
	if (event.target.innerText == '+')
	{
		// здесь может быть утечка:
		group_introduce = new PopupIntroduce(function(){
			event.target.innerText = '+';
		}, url);
		event.target.innerText = '-';
	}
	else
	{
		group_introduce.Destroy();			
	}
}