# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Instituto de Desarrollo Urbano (<http://www.idu.gov.co>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from osv import fields, osv
import gitlab
from openerp import SUPERUSER_ID

def get_connection_gitlab(param_model, cr):
    token = param_model.get_param(cr, SUPERUSER_ID, 'gitlab.token2', default=False)
    host = param_model.get_param(cr, SUPERUSER_ID, 'gitlab.host', default=False)
    c = gitlab.Gitlab(host, token)
    return c

class res_users(osv.osv):
    _inherit = "res.users"
    _name = "res.users"

    _columns = {
        'gitlab_id': fields.integer('GitLab ID'),
    }


class gitlab_issue(osv.osv):
    _name = "gitlab.issue"
    _columns = {
        'name': fields.char('Name', size=255, required=True, select=1),
        'state': fields.selection([('opened','Abierto'), ('closed','Cerrado'), ('reopened','Re-Abierto')], 'Estado',required=True),
        'gitlab_id': fields.integer('GitLab ID'),
        'gitlab_idd': fields.integer('GitLab idd'),
        'stage_id': fields.many2one('gitlab.stage', 'Stage'),
        'milestone_id': fields.many2one('gitlab.milestone', 'Milestone'),
        'project_id': fields.many2one('gitlab.project', 'Project'),
        'label_ids': fields.many2many('gitlab.label', 'gitlab_issue_label', 'issue_id', 'label_ids', 'Labels'),
        'user_id': fields.many2one('res.users', 'User'),
        'task_id': fields.many2one('project.task', 'Task'),
    }

    def write(self, cr, uid, ids, vals, context=None):
        if len(vals) == 1 and vals.get('stage_id'):
            gitlab_conn = get_connection_gitlab(self.pool.get('ir.config_parameter'), cr)
            if vals.get('stage_id'):
                stage = self.pool.get('gitlab.stage').browse(cr, uid, vals.get('stage_id'), context=context)
                for issue in self.browse(cr, uid, ids, context=context):
                    labels = 'col:' + stage.name
                    for label in issue.label_ids:
                        labels = labels + ',' + label.name
                    res = gitlab_conn.editissue(issue.project_id.gitlab_id, issue.gitlab_id, labels = labels)
        return super(gitlab_issue, self).write(cr, uid, ids, vals, context)


class gitlab_stage(osv.osv):
    _name = "gitlab.stage"
    _columns = {
        'name': fields.char('Name', size=255, required=True, select=1),
        'sequence': fields.integer('Sequence', help="Gives the sequence order when displaying a list."),
        'issue_ids': fields.one2many('gitlab.issue', 'stage_id', 'Issues'),
    }


class gitlab_project(osv.osv):
    _name = "gitlab.project"
    _columns = {
        'name': fields.char('Name', size=255, required=True, select=1),
        'namespace_id': fields.char('Namespace', size=255, required=True, select=1),
        'gitlab_id': fields.integer('GitLab ID'),
        'issue_ids': fields.one2many(
            'gitlab.issue',
            'project_id',
            'Issues',
       ),
    }


class gitlab_milestone(osv.osv):
    _name = "gitlab.milestone"
    _columns = {
        'name': fields.char('Name', size=255, required=True, select=1),
        'gitlab_id': fields.integer('GitLab ID'),
        'gitlab_idd': fields.integer('GitLab idd'),
        'issue_ids': fields.one2many(
            'gitlab.issue', 
            'milestone_id',
            'Issues',
       ),
    }


class gitlab_label(osv.osv):
    _name = "gitlab.label"
    _columns = {
        'name': fields.char('Name', size=255, required=True, select=1),
        'issue_ids': fields.many2many('gitlab.issue', 'gitlab_issue_label', 'label_ids','issue_id','Issues'),
    }








"""
@startuml
Title gitlab integración openerp
class gitlab.issue
class gitlab.milestone
class gitlab.project

class project.task
class project.project

class res.user

gitlab.issue "*" -up- res.user
gitlab.issue "*" -- project.task
gitlab.milestone -- "*" gitlab.issue
gitlab.project -- "*" gitlab.issue
gitlab.issue "*" -- "*" gitlab.label

@enduml


"""
