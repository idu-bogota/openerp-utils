# -*- coding: utf-8 -*-
##############################################################################
#
#    Grupo I+D+I
#    Subdirección Técnica de Recursos Tecnológicos
#    Instituto de Desarrollo Urbano - IDU - Bogotá - Colombia
#    Copyright (C) IDU (<http://www.idu.gov.co>)
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

from openerp import models, fields, api, exceptions
from openerp.exceptions import Warning, AccessError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

TIPO_TRANSPORTE = [
    ('carro', 'Carro'),
    ('moto', 'Moto'),
    ('taxi', 'Táxi'),
    ('bici', 'Bicicleta'),
]

class mi_carro_tu_carro_oferta(models.Model):
    _name = 'mi_carro_tu_carro.oferta'
    _description = 'Mi carro tu carro Oferta'

    #Fields
    descripcion = fields.Char('Descripcion')  # minimo de ruta 
    origen = fields.Char('Origen')  # minimo de ruta
    destino = fields.Char('Destino') # max de ruta
    hora_viaje = fields.Datetime('Hora inicio de viaje')
    tipo_transporte = fields.Selection(
        TIPO_TRANSPORTE,
        'Tipo de Trasporte',
        default="carro",
        required=True,
    )
    vacantes = fields.Integer('Vacantes')
    integrantes = fields.Integer('Integrantes')
    pasajeros_ids = fields.One2many(
        string='Pasajeros',
        comodel_name='res.users',
        inverse_name='ruta_oferta_id',
        default=lambda self: [self._context.get('uid', False)],
        help='Usuarios integrantes.',
    )
    costo = fields.Integer('Costo')
    comentario = fields.Text('Comentario')
    user_id = fields.Many2one(
        'res.users',
        'Usuario',
        default=lambda self: self._context.get('uid', False)
    )
    state = fields.Selection(
        [
           ('inactivo', 'Desactivar Oferta'),
           ('activo', 'Activar Oferta'),
        ],
        default="inactivo",
    )
    route = fields.Char('Ruta Completa',default="",)
    # Campo det tipo ruta

    @api.multi
    def compute_vacantes(self):
        usuario = self._context.get('uid', False)
        if usuario in self.pasajeros_ids:
            raise exceptions.Warning('Usted ya esta en esta ruta')
        if self.vacantes > 0:
            self.pasajeros_ids = usuario    #[(4, usuario, 0)]
            self.vacantes = self.vacantes - 1
            return True
        else:
            res = {'value':{}}
            res.update({'warning': {'title': _('Warning !'), 'message': _('No hay Vacantes en esta Ruta.')}})
            return res

    @api.multi
    def compute_integrantes(self):
        usuario = self._context.get('uid', False)
        if usuario in self.pasajeros_ids:
            raise exceptions.Warning('Usted ya esta en esta ruta')
        self.pasajeros_ids = usuario    #[(4, usuario, 0)]
        self.integrantes = self.integrantes + 1
        return True

#     @api.model
#     def create(self,vals):
# #         if self.search([('user_id','=',self._context.get('uid', False))]):
# #             raise exceptions.Warning('Este Usuario ya esta dentro de una oferta.')
#         vals['pasajeros_ids'] = [self._context.get('uid', False)]
#         return super(mi_carro_tu_carro_oferta, self).create(vals)