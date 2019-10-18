/*
window.onload = function(){
	var imagePut = document.getElementsByName('Image')[0];
	imagePut.onchange = file_upload;
}//*/

//загрузка файла
function file_upload(sender)									 // event
{
	
	if (sender.value!="")
	{
		var widget = sender.parentElement.children[0].children[0];//span
		widget.innerText = sender.value.split(/[\\/]/).pop();
		widget.style.color = 'green';
		widget.style.backgroundColor = 'gray'
							
					
		widget.appendChild(document.createElement('br'));
		widget.appendChild(document.createElement('hr'));
		widget.parentElement.style.height = '150px';
		
		widget.style.height = '150px';		
											
		var img = document.createElement('img');
		
		//ставим все по нулям:				
		img.style.height = '0px';
		img.style.width = '0%';						
		
		var reader = new FileReader();    				
		
		reader.onloadend = function () { 			//происходит. когда картинка загружена. Работает начиная с ie10 и выше
			img.src = reader.result;
			widget.appendChild(img);
			
			var w = 0;								//ставим стартовое значение для анимации ширины w = 0						
			
			var timerId = setInterval(function() {	// начать повторы с интервалом 10 mсек:
			  img.style.height = ++w + 'px';		// увеличиваем высоту в 1 px
			  img.style.width = w + '%';			// увеличиваем ширину в 1%
			  if (w == 85) clearInterval(timerId);	// прекращаем на ширине = __
			}, 10);
		};								
		
		(function () {
			reader.readAsDataURL(sender.files[0]);					
		})();
		//setTimeout(func, 0);						//зачем
						
	}
	
 
}	