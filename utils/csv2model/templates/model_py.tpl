{{ module.name }}
  {%- for k in module.models %}
    - {{ k }}
  {%- endfor %}
