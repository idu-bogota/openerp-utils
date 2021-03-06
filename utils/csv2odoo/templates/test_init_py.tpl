{% for model in module.models if model.namespace == module.namespace and model.data in ['1', '3'] -%}
    import test_{{ model.name | replace('.', '_') }}
{% endfor %}
{%- for group in module.groups -%}
    import test_domain_{{ group.name | replace('.', '_') }}
{% endfor %}
{% for model in module.models -%}
{%- if model.transitions -%}
    import test_workflow_{{ model.short_name | replace('.', '_') }}
{% endif -%}
{% endfor %}
