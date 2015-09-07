{% import "test_macros.tpl" as macro_fields -%}
# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_security_{{ group.name | replace('.','_') }}(common.SingleTransactionCase):
    def test_security(self):
        pass


if __name__ == '__main__':
    unittest2.main()