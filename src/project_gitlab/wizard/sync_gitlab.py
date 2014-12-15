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
import gitlab
import logging
import re
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)

def get_connection_gitlab(param_model, cr):
    token = param_model.get_param(cr, SUPERUSER_ID, 'gitlab.token', default=False)
    host = param_model.get_param(cr, SUPERUSER_ID, 'gitlab.host', default=False)
    c = gitlab.Gitlab(host, token)
    return c

class gitlab_wizard_sync(osv.osv_memory):
    _name = 'gitlab_wizard.sync'
    _description = 'Sincronizar en openerp los proyectos en GitLab'
    _columns = {}

    def sync(self, cr, uid, ids, context=None):
        gitlab_conn = get_connection_gitlab(self.pool.get('ir.config_parameter'), cr)
        projects = gitlab_conn.getprojects()
        self.gitlab_walk_projects(cr, uid, projects, gitlab_conn)

        return {'type': 'ir.actions.act_window_close'}

    def create_user(self, cr, uid, user):
        """Checks if there is a gitlab.project at Odoo instance otherwise creates one.
        @return project_id
        """
        if isinstance(user, dict):
            user_id = None
            user_model = self.pool.get('res.users')
            user_ids = user_model.search(cr, uid, [('login', '=', user['username'])])
            user_data = {
                'login': user['username'],
                'name': user['name'],
                'new_password': user['username'],
                'gitlab_id': user['id'],
            }
            if not len(user_ids):
                user_id = user_model.create(cr, uid, user_data)
            else:
                user_id = user_ids[0]
                user_model.write(cr, uid, user_id, user_data)
        else:
            user_id = 0
        return user_id

    def create_project(self, cr, uid, project):
        """Checks if there is a gitlab.project at Odoo instance otherwise creates one.
        @return project_id
        """
        project_id = None
        project_model = self.pool.get('gitlab.project')
        project_ids = project_model.search(cr, uid, [('gitlab_id', '=', project['id'])])
        project_data = {
            'name': project['name'],
            'gitlab_id': project['id'],
            'namespace_id': project['namespace']['name'],
        }
        if not len(project_ids):
            project_id = project_model.create(cr, uid, project_data)
        else:
            project_id = project_ids[0]
            project_model.write(cr, uid, project_id, project_data)
        return project_id

    def get_stage_from_label(self, label):
        """Check if the label is related to a issue kanban stage
        """
        regex = re.compile("^(col:)(.*)$")
        found = regex.search(label)
        if found:
            parts = found.groups()
            if(len(parts) == 2):
                return parts[1]
        return False

    def create_labels(self, cr, uid, labels):
        result = []
        label_model = self.pool.get('gitlab.label')
        for label in labels:
            if self.get_stage_from_label(label):
                continue
            label_ids = label_model.search(cr, uid, [('name', '=', label)])
            labels_data = {
                'name': label,
            }
            if not len(label_ids):
                label_id = label_model.create(cr, uid, labels_data)
                result.append(label_id)
            else:
                label_id = label_ids[0]
                label_model.write(cr, uid, label_id, labels_data)
                result.append(label_id)
        return [(6, 0, result)]

    def create_stage(self, cr, uid, labels):
        """Return one stage for the Issue to create/update"""
        stage_model = self.pool.get('gitlab.stage')
        for label in labels:
            stage = self.get_stage_from_label(label)
            if not stage:
                continue
            stage_ids = stage_model.search(cr, uid, [('name', '=', stage)])
            stages_data = {
                'name': stage,
            }
            if not len(stage_ids):
                return stage_model.create(cr, uid, stages_data)
            else:
                return stage_ids[0]
            return False

    def create_milestone(self, cr, uid, milestone):
        """ Check if there is an gitlab.milestone at Odoo instance, otherwise creates one.
        @return milestone_name
        """
        if isinstance(milestone, dict):
            milestone_model = self.pool.get('gitlab.milestone')
            milestone_ids = milestone_model.search(cr, uid, [('name','=',milestone['title'])])
            milestone_data = {
                'name': milestone['title'],
                'gitlab_id': milestone['id'],
                'gitlab_idd': milestone['iid'],
            }
            if not len(milestone_ids):
                _logger.debug('Creando milestone con título: {0}'.format(milestone['title']))
                milestone_id = milestone_model.create(cr, uid, milestone_data)
            else:
                milestone_id = milestone_ids[0]
                milestone_model.write(cr, uid, milestone_id, milestone_data)
        else:
            milestone_id = 0

        return milestone_id

    def create_issue(self, cr, uid, issue, project_idd):
        """ Check if there is an gitlab.issue at Odoo instance, otherwise creates one.
        @return issue_id
        """
        issue_model = self.pool.get('gitlab.issue')
        issue_ids = issue_model.search(cr, uid, [('gitlab_id', '=', issue['id'])])
        issue_data = {
            'name': issue['title'],
            'state': issue['state'],
            'gitlab_id': issue['id'],
            'gitlab_idd': issue['iid'],
            'project_id': project_idd,
            'user_id': self.create_user(cr, uid, issue['assignee']),
            'milestone_id': self.create_milestone(cr, uid, issue['milestone']),
            'label_ids': self.create_labels(cr, uid, issue['labels']),
            'stage_id': self.create_stage(cr, uid, issue['labels'])
        }
        if not len(issue_ids):
            issue_id = issue_model.create(cr, uid, issue_data)
        else:
            issue_id = issue_ids[0]
            issue_model.write(cr, uid, issue_id, issue_data)
        return issue_id

    def gitlab_walk_projects(self, cr, uid, projects, gitlab_conn):
        for project in projects:
            project_idd = self.create_project(cr, uid, project)
            issues = gitlab_conn.getprojectissues(project['id'])
            for issue in issues:
                self.create_issue(cr, uid, issue, project_idd)

gitlab_wizard_sync()
