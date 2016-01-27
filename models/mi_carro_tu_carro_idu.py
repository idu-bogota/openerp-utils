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
from openerp.addons.base_geoengine import geo_model
from openerp.addons.base_geoengine import fields as geo_fields

TIPO_TRANSPORTE = [
    ('carro', 'Carro'),
    ('moto', 'Moto'),
    ('taxi', 'Táxi'),
    ('bici', 'Bicicleta'),
]

class mi_carro_tu_carro_oferta(geo_model.GeoModel):
    _name = 'mi_carro_tu_carro.oferta'
    _description = 'Mi carro tu carro Oferta'

    #Fields
    descripcion = fields.Char('Descripcion')
    origen = fields.Char('Origen')
    destino = fields.Char('Destino')
    hora_viaje = fields.Datetime('Hora inicio de viaje')
    tipo_transporte = fields.Selection(
        TIPO_TRANSPORTE,
        'Tipo de Trasporte',
        default="carro",
        required=True,
    )
    vacantes = fields.Integer(
        'Vacantes',
        default=0,
    )
    integrantes = fields.Integer(
        'Integrantes',
        default=0,
    )
    pasajeros_ids = fields.One2many(
        string='Pasajeros',
        comodel_name='res.users',
        inverse_name='ruta_oferta_id',
        help='Usuarios integrantes.',
        ondelete = 'SET DEFAULT',
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
           ('inactivo', 'Inactivo'),
           ('activo', 'Activo'),
        ],
        default="inactivo",
    )
    route = fields.Char(
        'Ruta Completa',
        default="",
    )
    # Campo det tipo ruta
    shape = geo_fields.GeoLine(
        string='Ruta',
    )

    @api.multi
    def compute_vacantes(self):
        usuario = self._context.get('uid', False)
        usuario = self.env['res.users'].browse(usuario)
        if usuario in self.pasajeros_ids:
            return False
#            raise exceptions.Warning('Usted ya esta en esta ruta')
        if self.vacantes > 0:
            self.pasajeros_ids = [(4, usuario.id, 0)]#usuario.id    #[(4, usuario, 0)]
            self.vacantes = self.vacantes - 1
            return True
        else:
            res = {'value':{}}
            res.update({'warning': {'title': _('Warning !'), 'message': _('No hay Vacantes en esta Ruta.')}})
            return res

    @api.multi
    def compute_integrantes(self):
        usuario = self._context.get('uid', False)
        usuario = self.env['res.users'].browse(usuario)
        if usuario in self.pasajeros_ids:
            raise exceptions.Warning('Usted ya esta en esta ruta')
        self.pasajeros_ids = [(4, usuario.id, 0)]    #[(4, usuario, 0)]
        self.integrantes = self.integrantes + 1
        return True

#     @api.model
#     def create(self,vals):
# #         if self.search([('user_id','=',self._context.get('uid', False))]):
# #             raise exceptions.Warning('Este Usuario ya esta dentro de una oferta.')
#         vals['pasajeros_ids'] = [self._context.get('uid', False)]
#         return super(mi_carro_tu_carro_oferta, self).create(vals)