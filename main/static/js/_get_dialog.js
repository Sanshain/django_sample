//не получается, т.к. нет замыканий, контекстных переменных и прочего

var user_id = document.location.href.match(/\d+/)[0];

event.preventDefault();

var ajax_dialog = new Ajax(
	'/get_dialog/',
	function(resp){
		render_page(resp);
	}
);
		
ajax_dialog.postData('id='+user_id);


stack.push(
{
	'detail':document.querySelector('.detail').innerHTML,
	'dynamic_link' : document.getElementsByName('dynamic_link')[0].href
});					


//replaceState	
history.pushState(
	['detail','dynamic_link'],
	null,
	'/messages/to_'+user_id+'/'
); 	

//obsolete User.id instead user_id for inside page func