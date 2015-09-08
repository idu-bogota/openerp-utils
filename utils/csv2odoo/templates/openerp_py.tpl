{
    'name': '{{ module.string }}',
    'version': '1.0',
    'depends': [
        'base',
        'base_idu'
    ],
    'author': "Grupo de Investigación, Desarrollo e Innovación - STRT - IDU",
    'category': 'IDU',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',{% for namespace in module.namespaces() if namespace == module.namespace %}
        'views/{{ namespace }}_view.xml',{% endfor %}{% for namespace in module.namespaces() if namespace != module.namespace %}
        'views/{{ namespace }}_view.xml',{% endfor %}{% for model in module.models if model.namespace == module.namespace and model.menu == 'conf' %}
        'data/{{ model.name }}.csv',{% endfor %}
    {%- for model in module.models -%}
      {%- if model.transitions %}
        'workflow/{{ model.short_name }}_workflow.xml',
      {%- endif -%}
    {%- endfor %}
    ],
    'test': [{% if module.groups %}
        'tests/001_users.yml',{% endif %}
    ],
    'demo': [{% for model in module.models if model.namespace == module.namespace and model.menu != 'conf' %}
        'demo/{{ model.name }}.csv',{% endfor %}
    ],
    'installable': True,
    'description': """
## Dependencias módulos Python
## Configuración adicional
    """,
}
{{ "\n" }}
