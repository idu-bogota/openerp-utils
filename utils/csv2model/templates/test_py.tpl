# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_{{ model.name | replace('.','_') }}(common.SingleTransactionCase):
    def test_crud_validaciones(self):
        plan_model = self.env['plan_mejoramiento.plan']
        vals = {
            'name': 'Plan Interno',
            'dependencia_id': self.ref('plan_mejoramiento_idu.id_department_strt'),
            'origen_id': self.ref('plan_mejoramiento_idu.id_origen_01'),
            'proceso_id': self.ref('plan_mejoramiento_idu.id_proceso_01'),
            'user_id': user_oci_id,
        }
        plan = plan_model.create(vals)
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