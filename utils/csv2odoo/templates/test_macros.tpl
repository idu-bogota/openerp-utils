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

{% macro boolean(field) -%}
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

{% macro selection(field) -%}
    {{ text(field) }}
{%- endmacro %}


{% macro compute_method(field) %}
        {%- if field.arguments['depends'] %}
        vals_upd = {{ '{' }}{% for field_name in field.arguments['depends'] %}
            '{{ field_name }}': 'Valor a usarse para calculo',
            {%- endfor %}
        }
        {{ field.model.short_name }}.write(vals_update)
        {%- endif %}
        self.assertEqual({{ field.model.short_name }}.{{ field.name }}, 'Valor Esperado')
{%- endmacro -%}

{% macro constrains_method(field) %}
        vals_upd = {
            '{{ field.name }}': 'Valor a usarse para romper la validación',
        }
        try:
            {{ field.model.short_name }}.write(vals_update)
        except ValidationError, e:
            pass
        else:
            self.fail('No se generó exception de validación para "{{ field.name }}"')
{%- endmacro %}
