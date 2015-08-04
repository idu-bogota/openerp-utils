{%- for field in model.fields -%}
    "{{ field.name }}",
{%- endfor %}
{%- for i in range(10) %}
{% for field in model.fields -%}
    {{ field.generate_value() }},
{%- endfor -%}
{%- endfor -%}
