{% import "test_macros.tpl" as macro_fields -%}
# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_{{ model.name | replace('.','_') }}(common.SingleTransactionCase):
    def test_crud_validaciones(self):
        {{ model.shortname }}_model = self.env['{{ model.name }}']
        vals = {
        {% for field in model.fields if not field.arguments['compute'] and not field.arguments['related'] %}
            {{  macro_fields|attr(field.type)(field) }}
        {%- endfor %}
        }
        {{ model.shortname }} = {{ model.shortname }}_model.create(vals)
        # Por cada constrain crear una prueba
        # Por cada campo computed crear una prueba


if __name__ == '__main__':
    unittest2.main()