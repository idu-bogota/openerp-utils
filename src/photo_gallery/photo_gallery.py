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


from openerp.osv import fields, osv
import tempfile
import logging
_logger = logging.getLogger(__name__)

class photo_gallery_photo(osv.osv):
    _name = "photo_gallery.photo"
    _order = "sequence, id"

    def _get_binary_filesystem(self, cr, uid, ids, name, arg, context=None):
        """ Display the binary from ir.attachment, if already exist """
        res = {}
        attachment_model = self.pool.get('ir.attachment')

        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = False
            attachment_ids = attachment_model.search(cr, uid,
                [('res_model','=',self._name),('res_id','=',record.id),('binary_field','=',name)],
                context=context
            )
            if attachment_ids:
                img  = attachment_model.browse(cr, uid, attachment_ids, context=context)[0].datas
                res[record.id] = img
        return res

    def _set_binary_filesystem(self, cr, uid, id_, name, value, arg, context=None):
        """ Create or update the binary in ir.attachment when we save the record """
        attachment_model = self.pool.get('ir.attachment')

        attachment_ids = attachment_model.search(cr, uid, [('res_model','=',self._name),('res_id','=',id_),('binary_field','=',name)], context=context)
        if value:
            if attachment_ids:
                attachment_model.write(cr, uid, attachment_ids, {'datas': value}, context=context)
            else:
                photo_name = 'Photo_{0}_{1}'.format(self._name, id_)
                _datas_fname = 'Photo_{0}_{1}.jpg'.format(self._name,id_)
                attachment_model.create(cr, uid,
                    {'res_model': self._name, 'res_id': id_, 'name': photo_name, 'binary_field': name, 'datas': value, 'datas_fname':_datas_fname},
                    context=context
                )
        else:
            attachment_model.unlink(cr, uid, attachment_ids, context=context)

    _columns={
        'name': fields.char('Caption',size=255, required=True),
        'active':fields.boolean('Active',),
        'sequence': fields.integer('Sequence', help="Gives the sequence order when displaying a list."),
        'photo': fields.function(_get_binary_filesystem,
            fnct_inv=_set_binary_filesystem,
            type='binary',
            string='File',
        ),
        'description': fields.text('Description', size=255),
        'location': fields.text('Location', size=255),
        'photographer': fields.text('Photographer', size=255),
        'datetime': fields.datetime('Date and time'),
        'url': fields.char('URL', size=255),
    }
    
    _defaults = {
        'active': True,
        'datetime': fields.datetime.now,
        'sequence': 10,
    }

    def flickr_publish_photos(self, cr, uid, ids, context=None):
        try:
            api_key = self.pool.get('ir.config_parameter').get_param(cr, uid, 'flickr.api.key', default='', context=context)
            api_secret = self.pool.get('ir.config_parameter').get_param(cr, uid, 'flickr.api.secret', default='', context=context)
            api_login = self.pool.get('ir.config_parameter').get_param(cr, uid, 'flickr.api.login', default='', context=context)
        except Exception as e:
            raise osv.except_osv('ERROR',
                """Please configure flickr.api.key, flickr.api.secret, flickr.api.login: {0}
                """.format(e))
        try:
            flicker = flickr_uploader.flickr_uploader(api_key, api_secret, api_login)
        except Exception as e:
            raise osv.except_osv('ERROR', 'Flickr: {0} Please try again later'.format(e))

        records = self.browse(cr, uid, ids, context=context)
        for record in records:
            if record.photo:
                _today = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
                tag = 'photo_{0}_{1}'.format(
                    uid,
                    record.id,
                    _today
                )
                title = record.name
                image = base64.decodestring(record.photo)
                try:
                    f = tempfile.NamedTemporaryFile(
                        prefix='flickr_uploader_', 
                        dir='/tmp',
                    )
                    f.write(image)
                    url = flicker.upload(f.name, title, tag)
                    self.log(cr, uid, record.id, 'Imagen almacenada en flickr con URL {0}'.format(url))
                    self.write(cr, uid, [record.id], {'url': url}, context=context)
                except Exception as e:
                    raise osv.except_osv('ERROR', 'Hubo un error cargando la foto a Flickr: {0}, por favor intentelo mas tarde.'.format(e))
                finally:
                    f.close()


photo_gallery_photo()

class ir_attachment(osv.osv):
    "Extends the ir.attachment model to support photo_gallery.photo storage"
    _name = 'ir.attachment'
    _inherit = 'ir.attachment'

    _columns = {
        'binary_field': fields.char('Binary field', size=128)
    }
