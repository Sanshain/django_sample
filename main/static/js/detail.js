

function ChangePage(page,state){
	if (history.state){
		state = state || ['main','articles'];
		var stored_page = {}
		
		//-
		console.log(history.state);
		//-
		
		history.state.forEach(
			function(key){
				
				stored_page[key] = !key=="dynamic_link"?
					document.querySelector('.'+key).innerHTML:
					document.getElementsByName("dynamic_link")[0].href;				
			}
		);
				
		
		stack.push(stored_page);
		history.pushState(state, null, page); 
			
		return true;
	}
	
	return false;
}