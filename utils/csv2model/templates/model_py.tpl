{{ module.name }}
  {%- for model in module.models %}
    - {{ model.name }}
      {%- for field in model.fields %}
      - {{ field.name }}
        {%- for k, v in field.arguments.iteritems() %}
        - {{ k }}: {{v}}
        {%- endfor %}
      {%- endfor %}
  {%- endfor %}
