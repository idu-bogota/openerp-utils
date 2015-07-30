{% macro search_field(field) -%}
            <field name="{{field.name}}" />
            {%- if field.view_arguments['search_param'] %}
                <filter name="filtro_{{field.name}}"
                    string="Filtro para {{field.arguments['string'] or field.name}}"
                    domain="{{field.view_arguments['search_param']}}"
                />
            {%- endif -%}
{%- endmacro -%}

{% macro search_group_by_field(field) -%}
    <filter string="{{field.arguments['string']}}" context="{'group_by':'{{field.name}}'}"/>
{%- endmacro -%}

{% macro form_field(field) -%}
    {%- if field.view_arguments['form_param'] -%}
        <field name="{{field.name}}" widget="{{field.view_arguments['form_param']}}" />
    {%- else -%}
        <field name="{{field.name}}" />
    {%- endif -%}
{%- endmacro -%}

{% macro basic_views(model) %}
    <record model="ir.ui.view" id="{{ model.short_name | replace('.','_') }}_search">
        <field name="name">{{ model.name }}.search</field>
        <field name="model">{{ model.name }}</field>
        <field name="arch" type="xml">
            <search>
            {%- for field in model.get_view_fields('search') %}
                {{  search_field(field) }}
            {%- endfor %}
                <group string="Agrupar por...">
                {%- for field in model.get_view_fields('search_group_by') %}
                    {{ search_group_by_field(field) }}
                {%- endfor %}
                </group>
            </search>
        </field>
    </record>
    <record model="ir.ui.view" id="{{ model.short_name | replace('.','_') }}_form">
        <field name="name">{{ model.name }}.form</field>
        <field name="model">{{ model.name }}</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                    {%- for field in model.get_view_fields('form') if not field.view_arguments['form_tab_enabled'] %}
                        {{  form_field(field) }}
                    {%- endfor %}
                    </group>
                    <notebook>
                        <page string='--TAB--'>
                            <group>
                            {%- for field in model.get_view_fields('form') if field.view_arguments['form_tab_enabled'] %}
                                {{  form_field(field) }}
                            {%- endfor %}
                            </group>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>
    <record model="ir.ui.view" id="{{ model.short_name | replace('.','_') }}_tree">
        <field name="name">{{ model.name }}.tree</field>
        <field name="model">{{ model.name }}</field>
        <field name="arch" type="xml">
            <tree>
            {%- for field in model.get_view_fields('tree') %}
                {{  form_field(field) }}
            {%- endfor %}
            </tree>
        </field>
    </record>
{%- endmacro -%}

{% macro menuitem(model) %}
    <record model="ir.actions.act_window" id="{{ model.short_name | replace('.','_') }}_action">
        <field name="name">{{ model.name }}</field>
        <field name="res_model">{{ model.name }}</field>
        <field name="view_mode">tree,form</field>
    </record>
    <menuitem id="{{ model.short_name | replace('.','_') }}_menu"
        parent="{{ model.short_name | replace('.','_') }}_menu"
        name="{{ model.description or model.short_name }}" action="{{ model.short_name | replace('.','_') }}_action"
    />
{%- endmacro -%}

{% macro inherited_view(model) %}
    <record model="ir.ui.view" id="{{ model.short_name | replace('.','_') }}_search">
        <field name="name">{{ model.name }}.search.{{ model.module.namespace }}</field>
        <field name="model">{{ model.name }}</field>
        <field name="inherit_id" ref="{{ model.name }}_search" />
        <field name="arch" type="xml">
            <field name="name" position="after">
            {%- for field in model.get_view_fields('search') %}
                {{  search_field(field) }}
            {%- endfor %}
            </field>
            <group position="inside">
            {%- for field in model.get_view_fields('search_group_by') %}
                {{ search_group_by_field(field) }}
            {%- endfor %}
            </group>
        </field>
    </record>
    <record model="ir.ui.view" id="{{ model.short_name | replace('.','_') }}_form">
        <field name="name">{{ model.name }}.form.{{ model.module.namespace }}</field>
        <field name="model">{{ model.name }}</field>
        <field name="inherit_id" ref="{{ model.name }}_form" />
        <field name="arch" type="xml">
            <field name="name" position="after">
                <group string="Extendidos en {{ model.module.name }}">
                {%- for field in model.get_view_fields('form') %}
                    {{  form_field(field) }}
                {%- endfor %}
                </group>
            </field>
        </field>
    </record>
    <record model="ir.ui.view" id="{{ model.short_name | replace('.','_') }}_tree">
        <field name="name">{{ model.name }}.tree.{{ model.module.namespace }}</field>
        <field name="model">{{ model.name }}</field>
        <field name="inherit_id" ref="{{ model.name }}_tree" />
        <field name="arch" type="xml">
            <field name="name" position="after">
            {%- for field in model.get_view_fields('tree') %}
                {{  form_field(field) }}
            {%- endfor %}
            </field>
        </field>
    </record>
{%- endmacro -%}