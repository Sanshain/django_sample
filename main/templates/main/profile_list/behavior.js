

function friend_act(sender, event)
{
    
    
    event.stopPropagation();
    
    
	var target = event.srcElement || event.target;							// e.srcElement - для IE8

	var addressee = 
	    Number(sender.parentNode.id) 
	    || sender.parentNode.id.substring(3);
	
	
	
	if (target.className.indexOf("friend") >= 0) {  // если элемент, по которому жмакнули - кнопка to_friend

		if (target.name == 'self')
			ToFriend(); 
		else
			ToFriend(addressee);

	} else {

		ToUser(addressee, event.which == 2);
	}
	
	
}





/*!
Отправляем заявку о дружбе
*/
function ToFriend(addressee)
{

	if (addressee)
		POST_AJAX({id : addressee}, to_friend); 
	
	else {
		
		alert('ToFriend');
		
																// move to edit Profile (`Profile` btn)
		var addressee = document.getElementById('me').name; 	//get id from buttom `To me` at top-menu

		var base_url = edit_self;
		base_url = base_url.replace('0', addressee); //can add links for return to list users after save
		document.location.href = base_url;//*/
	}
}


/*!
	\brief 

	@param addressee - id страницы для перехода
	@param tab_fl - колесиком - открываем в новой вкладке
*/
function ToUser(addressee, tab_fl)
{
	alert('ToUser');
	
	var base_url = user;

	base_url = base_url.replace('0', addressee);

	if (tab_fl && !ie()) {
		window.open(addressee, '_blank');	
	}
	else 
		document.location.href = base_url;
}

