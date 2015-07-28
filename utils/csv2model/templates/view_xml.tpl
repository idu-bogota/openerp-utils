{% import "view_macros.tpl" as macro_fields -%}
<?xml version="1.0" encoding="utf-8"?>
<openerp>
<data>
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
{%- for model in module.models %}
    <!--
    =================================================================
    {{model.name}}
    {{model.description}}
    =================================================================
    -->
    <record model="ir.ui.view" id="{{ model.short_name }}_search">
        <field name="name">{{ model.name }}.search</field>
        <field name="model">{{ model.name }}</field>
        <field name="arch" type="xml">
            <search>
            {%- for field in model.get_view_fields('search') %}
                {{  macro_fields|attr('search_field')(field) }}
            {%- endfor %}
                <group string="Agrupar por...">
                {%- for field in model.get_view_fields('search_group_by') %}
                    {{ macro_fields|attr('search_group_by_field')(field) }}
                {%- endfor %}
                </group>
            </search>
        </field>
    </record>
    <record model="ir.ui.view" id="{{ model.short_name }}_form">
        <field name="name">{{ model.name }}.form</field>
        <field name="model">{{ model.name }}</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                    {%- for field in model.get_view_fields('form') if not field.view_arguments['form_tab_enabled'] %}
                        {{  macro_fields|attr('form_field')(field) }}
                    {%- endfor %}
                    </group>
                    <notebook>
                        <page string='--TAB--'>
                            <group>
                            {%- for field in model.get_view_fields('form') if field.view_arguments['form_tab_enabled'] %}
                                {{  macro_fields|attr('form_field')(field) }}
                            {%- endfor %}
                            </group>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>
    <record model="ir.ui.view" id="{{ model.short_name }}_tree">
        <field name="name">{{ model.name }}.tree</field>
        <field name="model">{{ model.name }}</field>
        <field name="arch" type="xml">
            <tree>
            {%- for field in model.get_view_fields('tree') %}
                {{  macro_fields|attr('form_field')(field) }}
            {%- endfor %}
            </tree>
        </field>
    </record>
    <record model="ir.actions.act_window" id="{{ model.short_name }}_action">
        <field name="name">{{ model.name }}</field>
        <field name="res_model">{{ model.name }}</field>
        <field name="view_mode">tree,form</field>
    </record>
    <menuitem id="{{ model.short_name }}_menu"
        parent="{{ model.short_name }}_menu"
        name="{{ model.description or model.short_name }}" action="{{ model.short_name }}_action"
    />
{% endfor %}

</data>
</openerp>