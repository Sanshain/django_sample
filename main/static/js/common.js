HTMLLIElement.prototype.appendChilds = function () {

  for ( var i = 0 ; i < arguments.length ; i++ )

    this.appendChild( arguments[ i ] );

};

/*!
	���������� �� ��������� ���������� ��������� (�� 10 ��� �����, ������������� - 2)
	
	* �� ������������ class
	
*/
HTMLElement.prototype.vs = function (dict) {

	for (var key in dict){
		this.setAttribute(key, dict[key]);
	}

	return this;
};



/*! ie10+ - �� ������� ����������� � �����

	�������� ������������ ������� �� ������� ��������
	������������ � __upload_images � user.js
*/
function get_maxim(enumble, field_in){ //get_maximum
	
	//Array.from
	if (field_in) enumble = [].slice.call(enumble).map(
		function(item) //
		{
		  return item[field_in];
		});
	var m = Math.max.apply(null, enumble);
	
	return m > 0 ? m : 0;

}

/*!
	���������� ���� ������ ���������� fixed ������� � �������� �������� ������
	
	������������ � base ��� ������� #6 issue

	���������� �� ie10+
*/
function search_fixed(container, deep){
	
	if (deep == 0) return null;
	else 
		deep = deep || 2;
	
	var childs=container.children; // ie9+,����- childNodes 
	
	var i=0; while(i<childs.length)
	{
		var elem = childs[i++];
		if (window.getComputedStyle(elem).position == 'fixed'){						//ie9+, ���� ��������
			return elem;
		}
		else if (deep > 1){
			
			var r = search_fixed(elem, deep - 1);
			
			if (r != null) return r;			
		}
		
	}
	
	//����� ��� �� firstElementChild - ���� ie9+
}











/*	
	����� ����� left:calc(100vw - 250px);  ��� aside
	���� �� ���������
*/
function get_scroll_wide(elem){
	//var elem = document.body || elem;
	
	return window.innerWidth - document.body.clientWidth;
}





/*!!
	������ ��� ie10+. � ����� � ����� �� ��� ���������
*/

if (!String.prototype.startsWith) {
	
	String.prototype.startsWith = function(search, pos)
	{
		  position = pos || 0;
		  var r = this.substr(pos, search.length) === search;
		  /*
		  if (r){
			console.log(r);
		  }//*/
		  return r;
			
	};

}//*/