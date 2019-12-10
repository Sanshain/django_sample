# django_test

this is an example of the use of a similar framework in the react front

Light-React

This framework does not have a virtual DOM. Developers of light react did not see meaning in virtual DOM. Instead they has used origian DOM of web-page.


All this product purpose is light making SPA site - site without refresh all page.

The page consist of two types of element: **switches** and **containers**. 

<h2 align=center> switches </h2>

Main and necessary attribute of **switch** is `data-_refresh`. This attribute contains elements `id`s in DOM needed to be refreshed. For example:

```
<a href='{% url %}' data-_refresh='content'>Refresh Content</a>
```

This means that on click on `<a>` element portion of the page by id='content' will be reloaded from server side.

More difficult sample of switch: 

```
<a data-_refresh='main>age.city,section,header'>Some Refresh</a>
```

This means that on click on `<a>` element elements by id equal to 'section','header' and (attention!) 'age' and 'city' contained inside 'main' if its exists (else  'main'). If there are too many inside elements to reloaded, available next note:

```
<a data-_refresh='main>age.*,section,header'>Some Refresh</a>
```

It means all elements inside element with id='main'on the same level with id='age' will be reloaded.



