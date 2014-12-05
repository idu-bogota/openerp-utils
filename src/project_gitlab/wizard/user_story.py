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
import gitlab
import re

_logger = logging.getLogger(__name__)

def get_connection_gitlab(param_model, cr):
    token = param_model.get_param(cr, SUPERUSER_ID, 'gitlab.token2', default=False)
    host = param_model.get_param(cr, SUPERUSER_ID, 'gitlab.host', default=False)
    c = gitlab.Gitlab(host, token)
    return c

class gitlab_wizard_user_story(osv.osv_memory):
    _name = 'gitlab_wizard.user_story'
    _description = 'Sincronizar en openerp los proyectos en GitLab'
    _columns = {
        'us_id': fields.char('User Story ID', size=200, required=True, help = 'PQR-01'),
        'description': fields.text('Description', required=True, help = 'el rol X quiere X para X'),
        'project_id': fields.many2one('gitlab.project', 'Project'),
        'stage_id': fields.many2one('gitlab.stage', 'Stage'),
        'user_id': fields.many2one('res.users', 'User'),
        'label_ids': fields.many2many('gitlab.label', 'gitlab_wizard_label', 'wizard_id', 'label_ids', 'Labels'),
    }

    def get_parts_issue_tittle(self, label):
#^(.*)(\[\w\])(\*\*.*\*\*)(.*)$)
        """Check if the label is related to a issue kanban stage
        """
        regex = re.compile("^(.*)(\[\w\])(\*\*.*\*\*)(.*)$)")
        found = regex.search(label)
        if found:
            parts = found.groups()
            if(len(parts) == 2):
                return parts[1]
        return False

    def create_issue_project(self, cr, uid, ids, context=None):
        gitlab_conn = get_connection_gitlab(self.pool.get('ir.config_parameter'), cr)
        #^(.*)(\[\w\])(\*\*.*\*\*)(.*)$
        #^(\-\s)([A-Z]*\-\d*)(\:\s)(.*)$
        for issue in self.browse(cr, uid, ids, context=context):
            str_labels = ''
            regex_title = re.compile("^(\-\s)([A-Z]*\-\d*)(\:\s)(.*)$")
            found_title = regex_title.findall(issue.us_id)
            for label in issue.label_ids:
                str_labels = 'col:' + issue.stage_id.name + ',' + label.name
                regex_criteria = re.compile("^(.*)(\[\w\])(\*\*.*\*\*)(.*)$",re.MULTILINE)
                found_criteria = regex_criteria.findall(issue.description)
                for criteria in found_criteria:
                    res = gitlab_conn.createissue(
                        issue.project_id.gitlab_id,
                        #[User Story-id][Criteria ID] Criteria title
                        '[{0}]{1} {2}'.format(found_title[0][1], criteria[1], criteria[2].replace('**','')),
                        #User Story\n\n Criteria Title Criteria Description
                        "{0}\n\n - {1} {2}".format(found_title[0][3], criteria[2], criteria[3]),
                        issue.user_id.gitlab_id,
                        '',
                        str_labels
                )
#            res = gitlab_conn.createissue(issue.project_id.gitlab_id, issue.us_id, issue.description, issue.user_id.name, '', )

        return {'type': 'ir.actions.act_window_close'}


gitlab_wizard_user_story()
