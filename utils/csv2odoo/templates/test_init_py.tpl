{% for model in module.models if model.namespace == module.namespace and model.menu != 'conf' -%}
    import test_{{ model.name | replace('.', '_') }}
{% endfor %}
{%- for group in module.groups -%}
    import test_domain_{{ group.name | replace('.', '_') }}
{% endfor %}