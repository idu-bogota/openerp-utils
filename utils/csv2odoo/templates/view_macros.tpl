{% macro search_field(field) -%}
            <field name="{{field.name}}" />
            {%- if field.type == 'selection' %}
                {%- for opt in field.arguments['selection'] %}
                <filter name="filtro_{{field.name}}_{{ opt[0] }}"
                    string="{{ opt[1] }}"
                    help="Filtrar {{field.arguments['string'] or field.name}} {{ opt[1] }}"
                    domain="[('{{ field.name }}', '=', '{{ opt[0] }}')]"
                />
                {%- endfor -%}
            {%- elif field.view_arguments['search_param'] %}
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
    {%- if field.view_arguments['form_param'] == '_ATTRS_' -%}
        <field name="{{field.name}}"
            attrs="{
                'invisible': [('{{field.name}}', '=', 'CHANGE ME')],
                'required': [('{{field.name}}', '=', 'CHANGE ME')],
            }"
        />
    {%- elif field.view_arguments['form_param'] -%}
        <field name="{{field.name}}" widget="{{field.view_arguments['form_param']}}" />
    {%- else -%}
        <field name="{{field.name}}" />
    {%- endif -%}
{%- endmacro -%}

{% macro basic_views(model) %}
    <record model="ir.ui.view" id="{{ model.short_name | replace('.','_') }}_search">
        <field name="name">{{ model.name }}.search{% if model.namespace != model.module.namespace %}.{{ model.module.name }}{% endif %}</field>
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
        <field name="name">{{ model.name }}.form{% if model.namespace != model.module.namespace %}.{{ model.module.name }}{% endif %}</field>
        <field name="model">{{ model.name }}</field>
        <field name="arch" type="xml">
            <form>
                <header>
                {%- for field in model.get_view_fields('form') if field.name in ['state', 'stage_id'] %}
                    {{  form_field(field) }}
                {%- endfor %}
                </header>
                <sheet>
                    <group>
                    {%- for field in model.get_view_fields('form') if not field.view_arguments['form_tab_enabled'] and not field.name in ['state', 'stage_id'] %}
                        {{  form_field(field) }}
                    {%- endfor %}
                    </group>
                    <notebook>
                        {%- for tab in model.get_form_tabs() if tab != 'None' %}
                        <page string='{{ tab }}'>
                            <group>
                            {%- for field in model.get_view_fields('form') if field.view_arguments['form_tab_enabled'] and field.view_arguments['form_tab_param'] == tab %}
                                {{  form_field(field) }}
                            {%- endfor %}
                            </group>
                        </page>
                        {%- endfor %}
                    </notebook>
                </sheet>
                {%- if model.inherit and 'mail.thread' in model.inherit %}
                <div class="oe_chatter">
                    <field name="message_follower_ids" widget="mail_followers" groups="base.group_user"/>
                    <field name="message_ids" widget="mail_thread"/>
                </div>{% endif %}
            </form>
        </field>
    </record>
    <record model="ir.ui.view" id="{{ model.short_name | replace('.','_') }}_tree">
        <field name="name">{{ model.name }}.tree{% if model.namespace != model.module.namespace %}.{{ model.module.name }}{% endif %}</field>
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
    {%- if model.menu -%}
    <record model="ir.actions.act_window" id="{{ model.short_name | replace('.','_') }}_action">
        <field name="name">{{ model.name }}</field>
        <field name="res_model">{{ model.name }}</field>
        <field name="view_mode">tree,form</field>
    </record>
    {%- set parent_prefix = model.module.name | replace('.','_') %}
    {%- set parent = parent_prefix + '_conf_menu' if model.menu == 'conf' else parent_prefix + '_menu' %}
    <menuitem id="{{ model.short_name | replace('.','_') }}_menu"
        parent="{{ parent }}"
        name="{{ model.description or model.short_name }}" action="{{ model.short_name | replace('.','_') }}_action"
    />
{% endif -%}
{%- endmacro -%}

{% macro inherited_view(model) %}
{% if 'search' in model.view_configuration['extend_view'].keys() %}
    <record model="ir.ui.view" id="{{ model.short_name | replace('.','_') }}_search">
        <field name="name">{{ model.name }}.search.{{ model.module.namespace }}</field>
        <field name="model">{{ model.name }}</field>
        <field name="inherit_id" ref="{{ model.view_configuration['extend_view']['search'][0] }}" />
        <field name="arch" type="xml">
            <field name="{{ model.view_configuration['extend_view']['search'][1] }}" position="after">
            {%- for field in model.get_view_fields('search') %}
                {{ search_field(field) }}
            {%- endfor %}
            </field>
            <group position="inside">
            {%- for field in model.get_view_fields('search_group_by') %}
                {{ search_group_by_field(field) }}
            {%- endfor %}
            </group>
        </field>
    </record>
{%- endif -%}
{% if 'form' in model.view_configuration['extend_view'].keys() %}
    <record model="ir.ui.view" id="{{ model.short_name | replace('.','_') }}_form">
        <field name="name">{{ model.name }}.form.{{ model.module.namespace }}</field>
        <field name="model">{{ model.name }}</field>
        <field name="inherit_id" ref="{{ model.view_configuration['extend_view']['form'][0] }}" />
        <field name="arch" type="xml">
            <field name="{{ model.view_configuration['extend_view']['form'][1] }}" position="after">
                <group string="Extendidos en {{ model.module.name }}">
                {%- for field in model.get_view_fields('form') %}
                    {{  form_field(field) }}
                {%- endfor %}
                </group>
            </field>
        </field>
    </record>
{%- endif -%}
{% if 'tree' in model.view_configuration['extend_view'].keys() %}
    <record model="ir.ui.view" id="{{ model.short_name | replace('.','_') }}_tree">
        <field name="name">{{ model.name }}.tree.{{ model.module.namespace }}</field>
        <field name="model">{{ model.name }}</field>
        <field name="inherit_id" ref="{{ model.view_configuration['extend_view']['tree'][0] }}" />
        <field name="arch" type="xml">
            <field name="{{ model.view_configuration['extend_view']['tree'][1] }}" position="after">
            {%- for field in model.get_view_fields('tree') %}
                {{  form_field(field) }}
            {%- endfor %}
            </field>
        </field>
    </record>
{%- endif -%}
{%- endmacro -%}