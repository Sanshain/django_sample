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
function get_maxim(enumble, field_in){
	
	//Array.from
	if (field_in) enumble = [].slice.call(enumble).map(
		function(item) //
		{
		  return item[field_in];
		});
	var m = Math.max.apply(null, enumble);
	
	return m > 0 ? m : 0;

}







/*!!
	������ ��� ie10+
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