# django_test

this is an example of the use of a similar framework in the react front

Light-React

This framework does not have a virtual DOM. Developers of light react did not see meaning in virtual DOM. Instead they has used origian DOM of web-page.


All this product purpose is light making SPA site - site without refresh all page.

The page consist of two types of element: **swithches** and **containers**. 

Main and necessary attribute of **switch** is `data-_refresh`. This attribute contains elements `id`s in DOM needed to be refreshed. For example:

```
<a href='{% url %}' data-_refresh='content'>Refresh Content</a>
<a data-_refresh='main>age.*,section,header'>Some Refresh</a>
```

This means that on click on <a> element portion of the page by id='content' will be reloaded from server side.

