FLICKR_UPLOADER
===============

Modulo para subir fotos a Flickr utilizando el API de flickerapi de Python versión 1.4.3, el modulo devuelve una URL estatica de la imagen que se subio.

Para hacer funcionar este modulo hay que instalar la librería de flickrapi: sudo easy_install flickrapi, despues de instalada, se debe editar el archivo:

/usr/local/lib/python2.7/dist-packages/flickrapi-1.4.3-py2.7.egg/flickrapi/__init__.py

En las lineas 401, 455, 469 y 493

Cambiar “http” por “https” (En la ultima version de API no es necesario hacer esto)


PARAMETROS PARA FLICKUPLOADER
==============================
flickr.api.key
flickr.api.secret
flickr.api.login


REDUCCION DE TAMAÑO A IMAGENES
==============================
Es necesario instalar PIL(Python Imaging Library):
sudo easy_install PIL