# -*- coding: utf-8 -*-
##############################################################################
#
#    Grupo de Investigación, Desarrollo e Innovación I+D+I
#    Subdirección de Recursos Tecnológicos - STRT
#    INSTITUTO DE DESARROLLO URBANO - BOGOTA (COLOMBIA)
#    Copyright (C) 2015 IDU STRT I+D+I (http://www.idu.gov.co/)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.exceptions import AccessError
from openerp import models, fields, api
from openerp.addons.base_idu.tools import direcciones
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class fields_security_mixin(models.AbstractModel):
    _name = 'models.fields.security.mixin'

    _write_fields_whitelist = {}
    _write_fields_blacklist = {}

    def check_field_access_rights(self, cr, user, operation, fields, context=None):
        """Just allow to write on specific fields for some groups referenced at _write_fields_whitelist"""

        res = super(fields_security_mixin, self).check_field_access_rights(cr, user, operation, fields, context)
        if hasattr(self, '_write_fields_whitelist') and self._write_fields_whitelist:
            whitelisted_groups = self._write_fields_whitelist.keys()
            if operation == 'write' and whitelisted_groups and self.user_has_groups(cr, user, groups=','.join(whitelisted_groups), context=context):
                fields_set = set(fields)
                for group in whitelisted_groups:
                    fields_allowed = set(self._write_fields_whitelist[group])
                    is_allowed = fields_allowed.issuperset(fields_set)
                    if self.user_has_groups(cr, user, groups=group, context=context) and not is_allowed:
                        _logger.warning('Access Denied by ACLs for operation: %s, uid: %s, model: %s, fields: %s',
                            operation, user, self._name, ', '.join( fields_set - fields_allowed)
                        )
                        raise AccessError(
                            _('The requested operation cannot be completed due to security restrictions. '
                            'Please contact your system administrator.\n\n(Document type: %s, Operation: %s)') % \
                            (self._description, operation)
                        )
        if hasattr(self, '_write_fields_blacklist') and self._write_fields_blacklist:
            blacklisted_groups = self._write_fields_blacklist.keys()
            if operation == 'write' and blacklisted_groups and self.user_has_groups(cr, user, groups=','.join(blacklisted_groups), context=context):
                fields_set = set(fields)
                for group in blacklisted_groups:
                    fields_denied = set(self._write_fields_blacklist[group])
                    is_denied = fields_denied.issuperset(fields_set)
                    if self.user_has_groups(cr, user, groups=group, context=context) and is_denied:
                        _logger.warning('Access Denied by ACLs for operation: %s, uid: %s, model: %s, fields: %s',
                            operation, user, self._name, ', '.join( fields_set - fields_denied)
                        )
                        raise AccessError(
                            _('The requested operation cannot be completed due to security restrictions. '
                            'Please contact your system administrator.\n\n(Document type: %s, Operation: %s)') % \
                            (self._description, operation)
                        )
        return res


class soft_delete_mixin(models.AbstractModel):
    _name = 'models.soft_delete.mixin'

    active = fields.Boolean(
        string='No borrado',
        default=True,
    )

    @api.multi
    def unlink(self):
        self.check_access_rights('unlink')
        self.check_access_rule('unlink')
        self.write({ 'active': False })
