{%- macro overwrite_create_write(model) -%}
{%- if model.overwrite_create -%}
    @api.model
    def create(self, vals):
        {{ model.short_name }} = super({{ model.name | replace('.', '_')}}, self).create(vals)
        return {{ model.short_name }}
{% endif -%}
{% if model.overwrite_write %}
    @api.one
    def write(self, vals):
        res = super({{ model.name | replace('.', '_')}}, self).write(vals)
        return res
{%- endif -%}
{%- endmacro -%}

{%- macro sql_constraints(model) -%}
   {%- if model.get_unique_fields() %}
    _sql_constraints = [
    {%- for f in model.get_unique_fields() %}
        ('unique_{{ f.name }}','unique({{ f.name }})','Este {{ f.string or f.name }} ya está registrado'),
    {%- endfor %}
    ]
    {% endif -%}
{% endmacro -%}

{% macro many2many(field) -%}
            '{{ field.name }}': [
                (4, self.ref('{{ field.model.module.name }}.{{ field.name }}_01')),
                (0, 0, {
                    'field_name': valor,
                }),
            ],
{%- endmacro -%}

{% macro one2many(field) -%}
    {{ many2many(field) }}
{%- endmacro %}

{% macro many2one(field) -%}
    '{{ field.name }}': self.ref('{{ field.model.module.name }}.{{ field.name }}_01'),
{%- endmacro %}

{% macro text(field) -%}
    '{{ field.name }}': {{ field.generate_value() }},
{%- endmacro %}

{% macro char(field) -%}
    {{ text(field) }}
{%- endmacro %}

{% macro integer(field) -%}
    {{ text(field) }}
{%- endmacro %}

{% macro float(field) -%}
    {{ text(field) }}
{%- endmacro %}

{% macro html(field) -%}
    {{ text(field) }}
{%- endmacro %}

{% macro date(field) -%}
    {{ text(field) }}
{%- endmacro %}

{% macro datetime(field) -%}
    {{ text(field) }}
{%- endmacro %}

{% macro compute_method(field) %}
    @api.one
    {% if field.arguments['depends'] %}@api.depends({{ field.arguments['depends'] | replace(']','')| replace('[','') }}){% endif %}
    def _compute_{{ field.name }}(self):
        self.{{ field.name }} = 'Colocar valor calculado'
{%- endmacro %}

{% macro onchange_method(field) %}
    @api.onchange('{{ field.name }}')
    def _onchange_{{ field.name }}(self):
    {%- if field.arguments['constrains'] %}
        try:
            self._check_{{ field.name }}()
        Except Exception, e
            return {
                'title': "Error de Validación",
                'warning': {'message': e.message}
            }
    {%- else %}
        # https://www.odoo.com/documentation/8.0/howtos/backend.html#onchange
        pass
    {%- endif %}

{%- endmacro %}

{% macro constrains_method(field) %}
    @api.one
    @api.constrains('{{ field.name }}')
    def _check_{{ field.name }}(self):
        if self.{{ field.name }} == 'Condición de Validation':
            raise ValidationError("MENSAJE DE ERROR DE VALIDACIÓN")
{%- endmacro %}
