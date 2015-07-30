{
    'name':  {{ module.name }},
    'version': '1.0',
    'depends': [
        'base'
    ],
    'author': "Grupo de Investigación, Desarrollo e Innovación - STRT - IDU",
    'category': 'IDU',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',{% for namespace in module.namespaces() %}
        'views/{{ namespace }}_view.xml',{% endfor %}{% for model in module.models if model.namespace == module.namespace %}
        'data/{{ model.name }}.csv',{% endfor %}
    ],
    'test': [{% for model in module.models if model.namespace == module.namespace %}
        'tests/{{ model.name }}.yml',{% endfor %}
    ],
    'demo': [{% for model in module.models if model.namespace == module.namespace %}
        'demo/{{ model.name }}.csv',{% endfor %}
    ],
    'installable' : True,
    'description': """
## Dependencias módulos Python
## Configuración adicional
    """,
}
