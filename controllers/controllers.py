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

    @http.route(['/rutas/info_extended/'], type='http', auth="public", website=True)
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

    @http.route('/crear/', auth='public', website=True)
    def get_crear(self, **kwargs):
        values = {}
        for field in ['ruta_number']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return request.website.render("mi_carro_tu_carro_idu.crear_ruta_form", values)

    @http.route(['/crear_ruta/'], type='http', auth="public", website=True)
    def get_crear_ruta(self, **kwargs):
        ruta_created = request.env['mi_carro_tu_carro.oferta'].create(
                                       {'descripcion' : kwargs['descripcion'],
                                        'hora_viaje': kwargs['fecha_viaje'],
                                        'tipo_transporte': kwargs['transporteselect'],
                                        'vacantes': kwargs['vacantes'],
                                        'comentario' : kwargs['comentarios'],
                                        'state' : kwargs['stateselect'],
                                        'route': kwargs['rutas_wp'],
                                        }) #Agradecimientos a JJ.

        values = ruta_created
        
        return request.website.render("mi_carro_tu_carro_idu.ruta_creada", {
                            'person': values
                            })


    @http.route('/buscar/', auth='public', website=True)
    def get_buscar(self, **kwargs):
        values = {}
        for field in ['ruta_number']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return request.website.render("mi_carro_tu_carro_idu.buscar_ruta_form", values)

    @http.route('/buscar_ruta/', auth='public', website=True)
    def get_buscar_ruta(self, **kwargs):
        values = {}
        wp = kwargs['rutas_wp']
#         Oferta = http.request.env['mi_carro_tu_carro.oferta']
#         return http.request.render('mi_carro_tu_carro_idu.index', {
#             'ofertas': Oferta.search([]),
#         })
        for field in ['ruta_number']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return request.website.render("mi_carro_tu_carro_idu.buscar_ruta_form", values)
