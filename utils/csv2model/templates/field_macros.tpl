{% macro inheritance(model) -%}
{%- if model.inherit -%}
    _inherit = {{ model.inherit }}
{%- endif -%}
{%- if model.inherits %}
    _inherits = {
    {%- for k,v in model.inherits.iteritems() %}
        '{{ k }}': '{{ v }}',
    {%- endfor %}
    }
{%- endif -%}
{%- endmacro %}

{% macro arguments(field) -%}
    {%- set add_line = False -%}
    {%- set padding = '' -%}
    {%- if field.arguments['string'] %}{{ padding }}string='{{ field.arguments['string'] }}',{% set padding = ' ' %}{% endif -%}
    {%- if field.arguments['required'] %}{{ padding }}required=True,{% set padding = ' ' %}{% endif -%}
    {%- if field.arguments['size'] %}{{ padding }}size={{field.arguments['size']}},{% set padding = ' ' %}{% endif -%}
    {% if field.arguments['related'] %}
        related='{{field.arguments['related']}}',
        {%- set add_line = True -%}
    {%- endif -%}
    {% if field.arguments['comodel'] %}
        comodel_name='{{field.arguments['comodel']}}',
        {%- set add_line = True -%}
    {%- endif -%}
    {% if field.arguments['fk_field'] %}
        inverse_name='{{field.arguments['fk_field']}}',
        {%- set add_line = True -%}
    {%- endif -%}
    {% if field.arguments['compute'] %}
        compute='{{field.arguments['compute']}}',
        {%- set add_line = True -%}
    {%- endif -%}
    {% if field.arguments['help'] %}
        help='{{field.arguments['help']}}',
        {%- set add_line = True -%}
    {%- endif -%}
    {% if field.arguments['domain'] %}
        domain='{{field.arguments['domain']}}',
        {%- set add_line = True -%}
    {%- endif -%}
    {% if add_line %}
    {# Adicionar un padding #}
    {%- endif -%}
{%- endmacro -%}

{% macro many2many(field) -%}
    {{ field.name }} = fields.Many2many({{ arguments(field) }})
{%- endmacro -%}

{% macro one2many(field) -%}
    {{ field.name }} = fields.One2many({{ arguments(field) }})
{%- endmacro %}

{% macro many2one(field) -%}
    {{ field.name }} = fields.Many2one({{ arguments(field) }})
{%- endmacro %}

{% macro text(field) -%}
    {{ field.name }} = fields.Text({{ arguments(field) }})
{%- endmacro %}

{% macro char(field) -%}
    {{ field.name }} = fields.Char({{ arguments(field) }})
{%- endmacro %}

{% macro integer(field) -%}
    {{ field.name }} = fields.Integer({{ arguments(field) }})
{%- endmacro %}

{% macro float(field) -%}
    {{ field.name }} = fields.Float({{ arguments(field) }})
{%- endmacro %}

{% macro html(field) -%}
    {{ field.name }} = fields.Html({{ arguments(field) }})
{%- endmacro %}

{% macro date(field) -%}
    {{ field.name }} = fields.Date({{ arguments(field) }})
{%- endmacro %}

{% macro datetime(field) -%}
    {{ field.name }} = fields.Datetime({{ arguments(field) }})
{%- endmacro %}
