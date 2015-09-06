csv2odoo
========

Este es un script que permite crear un módulo para Odoo v8.0 utilizando la especificación de modelos y campos de un archivo CSV.

El script puede ser personalizado ajustando las plantillas disponibles, las cuales pueden ser pasadas como parámetro al script.

El script hace la generación de:

- Estructura de módulo Odoo
- Código de los modelos en python
- Vistas XML de los modelos
- Métodos base para constrains, campos calculados
- Plantilla de pruebas unitarias en python
- Archivos de carga de datos de demostración y de configuración inicial
- Archivos de configuración de seguridad

Este código generado puede ser usado para el desarrollo inicial del módulo y debe ser personalizado para completar la implementación del módulo y limpiar/ajustas las cosas que no sean necesarias

También sirve para estandarizar la forma en la que se escribe el código siguiendo en lo posible PEP8

USO
---

Para correr el script solo debe ejecutar:

    python ~/git/openerp-utils/utils/csv2odoo/main.py -f ARCHIVO.csv  -m 'NOMBRE_TECNICO_MODULO' -n NAMESPACE_DE_LOS_MODELOS -s 'NOMBRE DEL MÓDULO'

Para conocer las opciones disponibles ejecutar:

    python ~/git/openerp-utils/utils/csv2odoo/main.py -h


Estructura del archivo CSV
--------------------------

Se puede generar un archivo CSV de ejemplo el cual incluye las opciones disponibles:

    python ~/git/openerp-utils/utils/csv2odoo/main.py -g > petstore.csv

Las cabeceras del archivo son:

- model_name: Nombre del modelo a crear, no es necesario repetirlo en cada linea, el solo toma el primer valor que encuentre.
- name: Nombre del campo a crear
- type: Tipo de campo, ej. boolean, integer, date, datetime, many2one, one2many, many2many, selection
- params: Listado de parametros extras del campo, se debe diligenciar con el siguiente formato

    nombre:valor;nombre2:valor2

    A continuación se listan los parámetros aceptados y sus valores:

    - store: Si es True se coloca el valor del campo computado se almacena. Ej. store:True
    - related: Se indica el parametro related del campo. Ej, related:user_id.login
    - size: Indica el tamaño del string. Ej. size:200, por defecto es 255
    - compute: Indica que el campo es computado. Ej. compute:True. Se crea un bosquejo de la función que computa el valor del campo
    - domain: Si el campo es relacional, adiciona un dominio. Ej. domain:[('is_company','=',False)]
    - readonly: Indica que en la vista el campo es de solo lectura. Ej. readonly:True
    - depends: Si el campo es computado, se adiciona el decorado depends indicando el nombre de los campos de los cuale depende. Ej. depends=valor|name
    - selection: Indica cuales son los valores que va a tener el campo de selección. Ej. selection:Draft|Open|Closed.
    - default: Indica el valor por defecto a colocar, hay varias palabras claves para colocar funciones comunes en este atributo:
        - _NOW_: para campos de fecha y hora coloca el dia actual o la hora actual
        - _CURRENT_USER_: Util para asignar en campos res.users al usuario actual
        - _CONTEXT_: Indica que el valor por defecto puede ser tomado del contexto

- comodel: Indica el nombre del modelo relacionado en campos relacionales. En el caso de one2many, se debe colocar el nombre del campo relación. Ej. petstore.pet,owner_id
- string: La etiqueta a usarse para el campo
- help: Mensaje de ayuda
- required: 1 o 0, para indicar si el campo es obligatorio
- unique: 1 o 0, para indicar si se debe generar una restricción unique
- constrains: 1 o 0, crea una funcion con api.constrain
- onchange: 1 o 0, crea una funcion con api.onchange
- view_tree: 1, 0 o widget, indica si se despliega el campo en la vista tree y si se debe usar un widget en particular
- view_form: 1, 0, widget, _ATTRS_, indica si se despliega el campo en la vista form y si se debe usar un widget en particular o si se adiciona un codigo base attrs
- view_search: 1,0 o dominio, indica si se agrega el campo en la vista search y si se indica un dominio se crea un filtro usando ese dominio
- view_search_group_by: 1 o 0, indica si el campo puede ser usado para agrupar en la vista tree
- view_form_tab: 0 o nombre del tab, el campo va a aparecer en un tab en la vista form.
- menu: conf o main, indica en que menú va a aparecer, también se usa para generar datos de carga por defecto (conf)
- description: Descripción corta del modelo, no usar tíldes y menor de 64 bytes.
- inherits: Indica los modelos a los cuales hacer herencia tipo delegación
- inherit: Indica los modelos de los cuales se hereda (herencia de clase) o se extienden (herencia de prototipo)
- overwrite_write: Indica si se crea un metodo write que sobreescribe al padre
- overwrite_create: Indica si se crea un metodo create que sobreescribe al padre
- views: Indica si se desea crear una vista nueva "new", si no se desea crear o extender una vista "none" y extend, si se quiere crear una vista que extienda de otra. Cuando una vista es extendida se puede indicar que tipo de vistas extender indicando el id de la vista original y el campo sobre el cual aplicar la extensión. ej. "extend:form=id_vista_form_a_extender|fieldname_a_usar_para_la_extension,tree=vista_id|campo,search=vista_id|campo". Si no se desea extender alguna vista simplemente se quita: "extend:tree=vista_id|campo" esto solo crea una extensión de la vista tree. Si se deja solo extend el crea vistas por defecto para que manualmente se ajusten.

Con el archivo de ejemplo se puede generar el módulo, pero este no va a instalar ya que:

1. Los valores de campos relacionales no se crean en los datos de demostración (demo/*.csv) y de configuracion (data/*.csv) y ya que son requeridos en el modelo va a dar error.

Para que el modulo sea instalable sin hacer modificaciones adicionales, usted puede generar el código y modificar el archivo __openerp__.py comentando las lineas que se muestran a continuación:

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/petstore_view.xml',
        'views/res_view.xml',
        'data/petstore.breed.csv',
    ],
    'test': [
    ],
    'demo': [
        #'demo/petstore.pet.csv',
    ],


Control de Acceso
-----------------

También se puede adicionar un archivo CSV que indique el esquema general de control de acceso, este genera el archivo ir.model.access.csv y el archivo security.xml que incluye la definición de grupos y dominios de acceso.

Puede generar un archivo de ejemplo:

    python ~/git/openerp-utils/utils/csv2odoo/main.py -G > petstore_security.csv

Para generar el módulo incluyendo la generación del esquema de control de acceso puede ejecutar:

    python ~/git/openerp-utils/utils/csv2odoo/main.py -f ARCHIVO.csv  -m 'NOMBRE_TECNICO_MODULO' -n NAMESPACE_DE_LOS_MODELOS -s 'NOMBRE DEL MÓDULO' -S ARCHIVO_seguridad.csv

La estructura del archivo CSV de seguridad es:

- model_name: Nombre del modelo al cual se le aplicará la regla de acceso
- group: Nombre del grupo de seguridad a crearse y al que le aplicará la regla. Puede usar nombres de grupos ya existentes para asignar controles.
- create: Indica con 1 o 0 si se le da acceso al modelo a los miembros del grupo. Se puede definir un dominio para que se cree una regla de dominio para la operación de creación, puede invocar reglas preestablecidas como _ALL_ (acceder a todos los regitros) y _OWN_ (Acceder solo a los registros propios)
- read: Indica con 1 o 0 si se le da acceso al modelo a los miembros del grupo. Se puede definir un dominio para que se cree una regla de dominio para la operación de creación, puede invocar reglas preestablecidas como _ALL_ (acceder a todos los regitros) y _OWN_ (Acceder solo a los registros propios)
- write: Indica con 1 o 0 si se le da acceso de actualización al modelo a los miembros del grupo. Se puede definir un dominio para que se cree una regla de dominio para la operación de actualización, puede invocar reglas preestablecidas como _ALL_ (acceder a todos los regitros) y _OWN_ (Acceder solo a los registros propios)
- delete: Indica con 1 o 0 si se le da acceso de eliminación al modelo a los miembros del grupo. Se puede definir un dominio para que se cree una regla de dominio para la operación de eliminación, puede invocar reglas preestablecidas como _ALL_ (acceder a todos los regitros) y _OWN_ (Acceder solo a los registros propios)
