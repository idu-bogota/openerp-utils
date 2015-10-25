'''
Created on Jul 6, 2015

@author: camoncal1
'''
from openerp import http
from openerp.http import request
from openerp import fields
import json
import pyproj

class Rutas(http.Controller):
    @http.route('/rutas/', auth='public', website=True)
    def index(self):
        Oferta = http.request.env['mi_carro_tu_carro.oferta']
        return http.request.render('mi_carro_tu_carro_idu.index', {
            'ofertas': Oferta.search([]),
        })
        
    @http.route('/rutas/<model("mi_carro_tu_carro.oferta"):offer>/', auth='public', website=True)
    def offer(self, offer,**kwargs):
        values = {}
        for field in ['rutas_id', 'rutas_wp']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return http.request.render('mi_carro_tu_carro_idu.descripcion', {
            'person': offer,
            'kwargs': values
        })

    @http.route(['/rutas/info_extended'], type='http', auth="public", website=True)
    def info_extended(self, **kwargs):
        #import pudb; pu.db
        rutas_ids = request.env['mi_carro_tu_carro.oferta']
        rutas = rutas_ids.search([('id','=',kwargs['rutas_id'])])
        date_comment = fields.Datetime.now()
        if kwargs['rutas_wp']:
            the_dict = json.loads(kwargs['rutas_wp'])
            gmap = pyproj.Proj("+init=EPSG:3857")
            google = pyproj.Proj("+init=EPSG:4326")
            steps_google = []
            for step in the_dict['steps']:
                steps_google.append(
                    pyproj.transform(gmap, google, step[0], step[1]),
                )
            shape = {
                "type": "LineString",
                "coordinates": steps_google, #the_dict['steps'],
            }
            rutas.write({
                'route': kwargs['rutas_wp'],
                'shape': json.dumps(shape),
            })

        return request.website.render("mi_carro_tu_carro_idu.rutas_update")
#        else:
#            return request.website.render("pqrs_idu.pqrs_not_update")