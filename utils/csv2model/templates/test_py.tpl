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
        self.assertEqual(
            user_oci_id,
            plan.user_id.id,
            'Usuario del Plan no es el asignado'
        )
        self.assertEqual(
            user_oci_id,
            plan.wbs_root_id.user_id.id,
            'Usuario del Plan.wbs_root_id no es el asignado'
        )
        self.assertEqual(
            user_oci_id,
            plan.project_id.user_id.id,
            'Usuario del Plan.project_id no es el asignado'
        )



if __name__ == '__main__':
    unittest2.main()