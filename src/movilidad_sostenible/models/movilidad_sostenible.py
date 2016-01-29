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

class movilidad_sostenible_oferta(geo_model.GeoModel):
    _name = 'movilidad_sostenible.oferta'
    _description = 'Movilidad SostenibleOferta'

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
        compute="compute_integrantes",
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

    # -------------------
    # methods
    # -------------------
    @api.one
    def compute_integrantes(self):
        self.integrantes = len(self.pasajeros_ids)

    # -------------------
    # methods website
    # -------------------
    @api.multi
    def validar_hay_vacantes(self):
        vacantes = self.vacantes
        integrante_actuales = len(self.pasajeros_ids)
        diferencia = vacantes - integrante_actuales
        if diferencia > 0:
            return True
        else:
            return False

    @api.multi
    def existe_usuario_en_ruta(self):
        usuario = self.env.user
        if usuario in self.pasajeros_ids:
            return True
        else:
            return False

    @api.multi
    def add_user_a_ruta(self):
        usuario = self.env.user
        self.pasajeros_ids = [(4, usuario.id, 0)]

    @api.one
    def mobile_update(self, celular):
        usuario = self.env.user
        partner = usuario.partner_id
        partner.mobile = celular

    @api.multi
    def es_usuario_creador_de_ruta(self):
        usuario = self.env.user
        if usuario == self.user_id:
            return True
        else:
            return False