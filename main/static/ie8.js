String.prototype.trim = function() 
{
	return this.replace(/^\s+|\s+$/g, ''); 
};	


//if ie10+ and not ie9-: //����� ���� ������� � ��������� ����
// ���� ������������� � common.js
String.prototype.startsWith = function(search, pos)
{
      position = pos || 0;
      return 
			this.substr(pos, searchStr.length) === searchStr;
};


//ie ��������������: