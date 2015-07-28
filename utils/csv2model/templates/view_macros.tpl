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