"id",
{%- for field in model.fields -%}
    "{{ field.name }}"{% if not loop.last %},{% endif %}
{%- endfor %}
{%- for i in range(10) %}
"{{ model.short_name | replace('.', '_') }}_{{ i }}",{% for field in model.fields -%}
    {{ field.generate_value() }}{% if not loop.last %},{% endif %}
{%- endfor -%}
{%- endfor -%}
