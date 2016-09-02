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
"""Métodos helper para ser utilizados en la creación de campos field.binary en odoo que guarden el contenido como un
ir.attachment en lugar de un campo binario en la base de datos Esto permite tener bases de datos más pequeñas.

Se pueden usar de la siguiente manera:

import openerp.addons.binary_field_as_attachment as binary_field

class Ejemplo(models.Model):
    ...
    ...
    archivo = fields.Binary(
        string='Archivo digital',
        compute='_compute_archivo',
        inverse='_compute_archivo_inverse',
    )
    archivo_fname = fields.Char('Nombre Archivo')

    @api.one
    def _compute_archivo(self):
        self.archivo_acta = binary_field.get_attachment(self, 'archivo', self.env)

    def _compute_archivo_inverse(self):
        return binary_field.set_attachment(self, 'archivo', 'foo bar', self.archivo_fname, self.archivo, self.env)

"""

def get_attachment(record, field_name, env, return_object=False):
    """ Display the binary from ir.attachment, if already exist """
    res = False
    attachment_model = env['ir.attachment']
    attachment = attachment_model.with_context(active_test=False).search([
        ('res_model','=',record._name),('res_id','=',record.id),('binary_field','=',field_name),
    ])
    if attachment and return_object:
        return attachment
    if attachment:
        res = attachment.datas
    return res

def set_attachment(record, field_name, name, filename, binary, env):
    """ Create or update the binary in ir.attachment when we save the record """
    attachment_model = env['ir.attachment']

    attachment = get_attachment(record, field_name, env, True)
    if binary:
        if attachment:
            attachment_model.write({
                'name': name,
                'datas': binary,
                'datas_fname':filename,
                'active': False, # don't display it in the attachments list
            })
        else:
            attachment_model.create({
                'res_model': record._name, 
                'res_id': record.id,
                'binary_field': field_name,
                'name': name,
                'datas': binary,
                'datas_fname':filename,
                'active': False, # don't display it in the attachments list
            })
    else:
        record.with_context(force_unlink=True).unlink()
