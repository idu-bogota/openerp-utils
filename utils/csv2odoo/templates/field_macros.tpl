{% macro inheritance(model) %}
{%- if model.inherit %}
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

{%- macro overwrite_create(model) %}
    @api.model
    def create(self, vals):
        {{ model.short_name }} = super({{ model.name | replace('.', '_')}}, self).create(vals)
        return {{ model.short_name }}
{%- endmacro -%}

{%- macro overwrite_write(model) %}
    @api.one
    def write(self, vals):
        res = super({{ model.name | replace('.', '_')}}, self).write(vals)
        return res
{%- endmacro -%}

{%- macro sql_constraints(model) -%}
    _sql_constraints = [
    {%- for f in model.get_unique_fields() %}
        ('unique_{{ f.name }}', 'unique({{ f.name }})', 'Este {{ f.string or f.name }} ya está registrado'),
    {%- endfor %}
    ]
{%- endmacro -%}

{% macro arguments(field) -%}
    {%- if field.arguments['string'] %}
        string='{{ field.arguments['string'] }}',
    {%- endif -%}
    {%- if field.arguments['required'] %}
        required=True,
    {%- endif -%}
    {%- if field.arguments['readonly'] %}
        readonly=True,
    {%- endif -%}
    {%- if field.arguments['size'] %}
        size={{field.arguments['size']}},
    {%- endif -%}
    {% if field.arguments['related'] %}
        related='{{field.arguments['related']}}',
    {%- endif -%}
    {% if field.arguments['comodel'] %}
        comodel_name='{{field.arguments['comodel']}}',
    {%- endif -%}
    {% if field.arguments['fk_field'] %}
        inverse_name='{{field.arguments['fk_field']}}',
    {%- endif -%}
    {% if field.arguments['ondelete'] %}
        ondelete='{{field.arguments['ondelete']}}',
    {%- endif -%}
    {% if field.arguments['compute'] %}
        compute='_compute_{{ field.name }}',
    {%- endif -%}
    {% if field.arguments['help'] %}
        help='{{field.arguments['help']}}',
    {%- endif -%}
    {% if field.arguments['domain'] %}
        domain="{{field.arguments['domain']}}",
    {%- endif -%}
    {% if field.arguments['selection'] %}
        selection=[{% for i in field.arguments['selection'] %}
            {{ i }},
        {%- endfor %}
        ],
    {%- endif -%}
    {% if field.arguments['default'] %}
        default={{ field.generate_default() }},
    {%- endif -%}
    {% if True %}
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

{% macro boolean(field) -%}
    {{ field.name }} = fields.Boolean({{ arguments(field) }})
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
{% macro selection(field) -%}
    {{ field.name }} = fields.Selection({{ arguments(field) }})
{%- endmacro %}

{% macro compute_method(field) %}

    @api.one{% if field.arguments['depends'] %}
    @api.depends({{ field.arguments['depends'] | replace(']','')| replace('[','') }}){% endif %}
    def _compute_{{ field.name }}(self):
        self.{{ field.name }} = {{ field.generate_value() }}
{%- endmacro %}

{% macro onchange_method(field) %}

    @api.onchange('{{ field.name }}')
    def _onchange_{{ field.name }}(self):
    {%- if field.arguments['constrains'] %}
        try:
            self._check_{{ field.name }}()
        except Exception, e:
            return {
                'title': "Error de Validación",
                'warning': {'message': e.message}
            }
    {%- else %}
        # https://www.odoo.com/documentation/8.0/howtos/backend.html#onchange
        pass
    {%- endif -%}
{%- endmacro %}

{% macro constrains_method(field) %}

    @api.one
    @api.constrains('{{ field.name }}')
    def _check_{{ field.name }}(self):
        if self.{{ field.name }} == 'Condición de Validation':
            raise ValidationError("MENSAJE DE ERROR DE VALIDACIÓN")
{%- endmacro %}
