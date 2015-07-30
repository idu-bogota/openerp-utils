{% for namespace in module.namespaces() -%}
    import {{ namespace | replace('.', '_') }}
{% endfor %}
