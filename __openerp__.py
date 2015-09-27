{
    "name" : "mi_carro_tu_carro_idu",
    "version" : "odoo8.0-rev2015060900",
    "author" : "Instituto de Desarrollo Urbano - STRT I+D+I",
    "category" : "idu", 
    "description" : """Módulo para compartir trasporte entre los empleados 
        del IDU
    """,
    "depends" : [
        'base',
        'base_idu',
        'website',
    ],
    "data" : [
        'views/mi_carro_tu_carro_idu_view.xml',
        'views/ws_micarro_tucarro.xml',
        'views/mi_carro_tu_carro_demo.xml',
    ],
    "test": [
    ],
    "installable" : True,
}