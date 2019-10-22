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