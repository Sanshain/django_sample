var Get_Messages = function(response){

	if (response != 'nop' && response != ''){
		var messages = JSON.parse(response);
		var listMessages = document.querySelector('.messages');
		for (var key in messages)
		{
			var mess = AppendNewElemTo(listMessages, Elem('li', messages[key], 'y message'));
			AppendNewElemTo(mess, Elem('span', key, 'mess_id'));
			AppendNewElemTo(mess, Elem('sub', Time(), 'mess_time'));
		}
						
		if (listMessages.offsetHeight >= listMessages.parentElement.offsetHeight - 35)
		{	
			listMessages.children[listMessages.children.length-1].scrollIntoView(false);				
		}
	
		document.bell_get();
			
	}
	
	Checking();
};

var last_mess_id;					// for Checking

var Checking = function(){
	
	var messages = document.querySelectorAll('.mess_id');
	
	if (messages){
		last_mess_id = messages.length ? messages[messages.length-1].innerText : 0;
		
		var data = 'check='+ last_mess_id;
		POST(data, Get_Messages);		
	}
	else if(last_mess_id)
	{
		//если last_mess_id уже был назначен
	}
		
};




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
				var li = AppendNewElemTo(list, Elem('li', value, 'message'));
				AppendNewElemTo(li, Elem('sub', Time(), 'mess_time'));
				
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
	@brief Должен находиться в windows.onload
	либо запускаться при динамической загрузке
*/
function InitializePage(){
	
}