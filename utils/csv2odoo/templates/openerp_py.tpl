{
    'name': '{{ module.string }}',
    'version': '1.0',
    'depends': [{% for dependency in module.depends | sort %}
        '{{ dependency }}',{% endfor %}
    ],
    'author': "Grupo de Investigación, Desarrollo e Innovación - STRT - IDU",
    'category': 'IDU',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',{% for namespace in module.namespaces() if namespace == module.namespace %}
        'views/{{ namespace }}_view.xml',{% endfor %}{% for namespace in module.namespaces() if namespace != module.namespace %}
        'views/{{ namespace }}_view.xml',{% endfor %}{% for model in module.models if model.data in ['2', '3'] %}
        'data/{{ model.name }}.csv',{% endfor %}
    {%- for model in module.models -%}
      {%- if model.transitions %}
        'workflow/{{ model.short_name }}_workflow.xml',
      {%- endif -%}
    {%- endfor %}
    ],
    'test': [{% if module.groups %}
        'tests/001_users.yml',{% endif %}
    ],{% if options.load_demo_data %}
    'demo': [{% if module.groups %}
        'tests/001_users.yml',{% endif %}{% for model in module.models if model.data in ['1', '3'] %}
        'demo/{{ model.name }}.csv',{% endfor %}
    ],{% endif %}
    'installable': True,
    'description': """
## Dependencias módulos Python
## Configuración adicional
    """,
}
{{ "\n" }}
