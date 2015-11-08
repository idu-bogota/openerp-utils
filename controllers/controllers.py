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
        rutas_model = request.env['mi_carro_tu_carro.oferta']
        rutas = rutas_model.search([('id','=',kwargs['rutas_id'])])
        date_comment = fields.Datetime.now()
        if kwargs['rutas_wp']:
            the_dict = json.loads(kwargs['rutas_wp'])
            google = pyproj.Proj("+init=EPSG:3857")
            gps = pyproj.Proj("+init=EPSG:4326")
            steps_google = []
            for step in the_dict['steps']:
                steps_google.append(
                    pyproj.transform(gps, google, step[0], step[1]),
                )
            shape = {
                "type": "LineString",
                "coordinates": steps_google,
                #"coordinates": the_dict['steps'],
            }
            the_dict.pop('steps', None) # Eliminando
            rutas.write({
                'route': json.dumps(the_dict),
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
        values = json.loads(kwargs['rutas_wp'])
        google = pyproj.Proj("+init=EPSG:3857")
        gps = pyproj.Proj("+init=EPSG:4326")
        start = pyproj.transform(gps, google, values['start']['lng'], values['start']['lat'])
        finish = pyproj.transform(gps, google, values['end']['lng'], values['end']['lat'])
        sql = """SELECT id
            FROM mi_carro_tu_carro_oferta o
            WHERE ST_DWithin(o.shape, ST_SetSRID(ST_MakePoint(%s, %s), 900913), 500) AND
            ST_DWithin(o.shape, ST_SetSRID(ST_MakePoint(%s, %s), 900913), 500)
        """ # Busca rutas que esten a 500 metros de los puntos origen y destino seleccionados
        params = (start[0], start[1], finish[0], finish[1])
        request.env.cr.execute(sql, params)
        res = request.env.cr.fetchall()
        #print values['start']['lng'], values['start']['lat']
        #print values['end']['lng'], values['end']['lat']
        #print sql
        #print params
        #print res
        rutas_ids = [ i[0] for i in res ]
        rutas_model = request.env['mi_carro_tu_carro.oferta']
        rutas = rutas_model.browse(rutas_ids)
        #print rutas
        values.update(kwargs=kwargs.items())
        return request.website.render("mi_carro_tu_carro_idu.buscar_ruta_form", values)
