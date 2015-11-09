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
     <menuitem id="{{ module.name }}_nav" name="{{ module.string }}"/>

     <menuitem id="{{ module.name }}_menu" name="{{ module.string }}" parent="{{ module.name }}_nav"/>
     <menuitem id="{{ module.name }}_conf_menu" parent="{{ module.name }}_nav"
        name="Configuración"
        groups="base.group_configuration"
     />
     <menuitem id="{{ module.name }}_admin_menu" parent="{{ module.name }}_nav"
        name="Administración"
        groups="base.group_configuration"
     />
{% endif -%}
{%- for model in module.models if model.namespace == namespace %}
    <!--
    =================================================================
    {{model.name}}{% if model.description %}
    {{model.description}}{% endif %}
    =================================================================
    -->
    {%- if model.view_configuration['create_view'] == 'new'-%}
        {{ macro_fields.basic_views(model) }}
    {%- elif model.view_configuration['create_view'] == 'extend' -%}
        {{ macro_fields.inherited_view(model) }}
    {%- endif %}
    {{ macro_fields.menuitem(model) }}
{%- endfor %}
</data>
</openerp>