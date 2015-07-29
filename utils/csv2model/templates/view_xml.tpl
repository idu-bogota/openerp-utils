{% import "view_macros.tpl" as macro_fields -%}
<?xml version="1.0" encoding="utf-8"?>
<openerp>
<data>
    {% if namespace == module.namespace -%}
    <!--
    =================================================================
    Menú
    =================================================================
    -->
     <menuitem id="{{ module.name }}_nav" name="{{ module.name }}"/>

     <menuitem id="{{ module.name }}_menu" name="{{ module.name }}" parent="{{ module.name }}_nav"/>
     <menuitem id="{{ module.name }}_configuracion_menu" parent="{{ module.name }}_nav"
        name="Configuración"
     />
     {% endif -%}
{%- for model in module.models if model.namespace == namespace %}
    <!--
    =================================================================
    {{model.name}}{% if model.description %}
    {{model.description}}{% endif %}
    =================================================================
    -->
    {% if namespace == module.namespace -%}
        {{ macro_fields.basic_views(model) }}
        {{ macro_fields.menuitem(model) }}
    {%- else -%}
        {{ macro_fields.inherited_view(model) }}
        {{ macro_fields.menuitem(model) }}
    {%- endif -%}
{% endfor %}

</data>
</openerp>