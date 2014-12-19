# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from osv import osv, fields
import logging
from openerp import SUPERUSER_ID
from project_gitlab.project_gitlab import get_connection_gitlab
import gitlab
import re

_logger = logging.getLogger(__name__)

class gitlab_wizard_user_story(osv.osv_memory):
    _name = 'gitlab_wizard.user_story'
    _description = 'Sincronizar en openerp los proyectos en GitLab'
    _columns = {
        'us_id': fields.text('Historia de usuario', required=True, help = 'Línea completa de la historia de usuario'),
        'description': fields.text('Criterios de aceptación', required=True, help = 'Criterios de aceptación'),
        'project_id': fields.many2one('gitlab.project', 'Project/repository', required=True),
        'stage_id': fields.many2one('gitlab.stage', 'Stage', required=True),
        'user_id': fields.many2one('res.users', 'User', required=True),
        'label_ids': fields.many2many('gitlab.label', 'gitlab_wizard_label', 'wizard_id', 'label_ids', 'Labels', required=True),
    }

    def create_issue_project(self, cr, uid, ids, context=None):
        gitlab_conn = get_connection_gitlab(self.pool.get('ir.config_parameter'), cr)

        for issue in self.browse(cr, uid, ids, context=context):
            str_labels = ''
            regex_title = re.compile("^(\-\s)([A-Z]*\-\d*)(\:\s)(.*)$")
            regex_criteria = re.compile("^(.*)(\[\w\])\s(\*\*.*\*\*)(.*)$",re.MULTILINE)
            found_title = regex_title.findall(issue.us_id)
            for label in issue.label_ids:
                str_labels = 'col:' + issue.stage_id.name + ',' + label.name
                found_criteria = regex_criteria.findall(issue.description)
                for criteria in found_criteria:
                    res = gitlab_conn.createissue(
                        issue.project_id.gitlab_id,
                        #[User Story-id][Criteria ID] Criteria title
                        '[{0}] {1} {2}'.format(found_title[0][1], criteria[1], criteria[2].replace('**','')),
                        #User Story\n\n Criteria Title Criteria Description
                        description="{0}\n\n - {1} {2}".format(found_title[0][3], criteria[2], criteria[3]),
                        assignee_id=issue.user_id.gitlab_id,
                        labels=str_labels
                    )
                    _logger.info(res)

        return {'type': 'ir.actions.act_window_close'}


gitlab_wizard_user_story()
