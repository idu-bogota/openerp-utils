{% import "view_macros.tpl" as macro_fields -%}
<?xml version="1.0" encoding="utf-8"?>
<openerp>
<data>
    {% if namespace == module.namespace -%}
    <!--
    =================================================================
    Menú
    =================================================================
    -->{% if not module._nav_menu_item_id %}
     <menuitem id="{{ module.name }}_nav" name="{{ module.string }}"/>{% endif %}

     <menuitem id="{{ module.name }}_menu"
        name="{{ module.string }}"
        parent="{{ module.nav_menu_item_id }}"
        sequence="10"
    />
     <menuitem id="{{ module.name }}_conf_menu" parent="{{ module.nav_menu_item_id }}"
        name="Configuración {{ module.string }}"
        groups="base.group_configuration"
        sequence="30"
     />
     <menuitem id="{{ module.name }}_admin_menu" parent="{{ module.nav_menu_item_id }}"
        name="Administración {{ module.string }}"
        groups="base.group_configuration"
        sequence="100"
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