{% import "test_macros.tpl" as macro_fields -%}
# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_{{ model.name | replace('.','_') }}(common.SingleTransactionCase):
    def test_crud_validaciones(self):
        {{ model.short_name }}_model = self.env['{{ model.name }}']
        vals = {
        {% for field in model.fields if not field.arguments['compute'] and not field.arguments['related'] %}
            {{  macro_fields|attr(field.type)(field) }}
        {%- endfor %}
        }
        {{ model.short_name }} = {{ model.short_name }}_model.create(vals)

        # Campos computados
        {%- for field in model.fields if field.arguments['compute'] -%}
            {{ macro_fields.compute_method(field) }}
        {%- endfor %}

        # Campos con api.constrain
        {%- for field in model.fields if field.arguments['constrains'] -%}
            {{ macro_fields.constrains_method(field) }}
        {%- endfor %}


if __name__ == '__main__':
    unittest2.main()