from openerp import http
from openerp.http import request
from openerp import fields
import json
import pyproj



class Rutas(http.Controller):

    @http.route('/movilidad_sostenible/', auth='user', website=True)
    def movilidad_sostenible(self):
        return request.website.render(
                "movilidad_sostenible.index"
                )

    @http.route('/movilidad_sostenible/rutas/ofertadas/', auth='user', website=True)
    def rutas(self):
        Oferta = http.request.env['movilidad_sostenible.oferta']
        return http.request.render('movilidad_sostenible.rutas_ofertadas', {
            'ofertas': Oferta.search([('state', '=', 'activo'),]),
        })

    @http.route('/movilidad_sostenible/misrutas/', auth='user', website=True)
    def misrutas(self):
        Oferta = http.request.env['movilidad_sostenible.oferta']
        return http.request.render('movilidad_sostenible.misrutas', {
            'ofertas': Oferta.search([('user_id','=', http.request.uid)]),
            'solicitadas': Oferta.search([('pasajeros_ids','in', http.request.uid)]),
        })

    @http.route('/movilidad_sostenible/misrutas/<model("movilidad_sostenible.oferta"):offer>/', auth='user', website=True)
    def showrutas(self, offer,**kwargs):
        values = {}
        for field in ['rutas_id', 'rutas_wp']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return http.request.render('movilidad_sostenible.showrutas', {
            'person': offer,
            'kwargs': values
        })

    @http.route('/movilidad_sostenible/misrutas/solicitadas/<model("movilidad_sostenible.oferta"):offer>/', auth='user', website=True)
    def offer(self, offer,**kwargs):
        return http.request.render('movilidad_sostenible.mis_rutas_solicitadas', {
            'mis_rutas_solicitadas': offer,
        })

    @http.route(['/movilidad_sostenible/misrutas/info_extended/'], type='http', auth='user', website=True)
    def info_extended(self, **kwargs):
        rutas_model = request.env['movilidad_sostenible.oferta']
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

        return request.website.render("movilidad_sostenible.rutas_update")
#        else:
#            return request.website.render("pqrs_idu.pqrs_not_update")


    @http.route('/movilidad_sostenible/rutas/crear/', auth='user', website=True)
    def get_crear(self, **kwargs):
        values = {}
        for field in ['ruta_number']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return request.website.render("movilidad_sostenible.crear_ruta_form", values)

    @http.route(['/movilidad_sostenible/rutas/crear_ruta/'], type='http', auth='user', website=True)
    def get_crear_ruta(self, **kwargs):
        rutas = request.env['movilidad_sostenible.oferta']
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
            ruta_created = rutas.create(
                                       {'descripcion' : kwargs['descripcion'],
                                        'hora_viaje': kwargs['fecha_viaje'],
                                        'tipo_transporte': kwargs['transporteselect'],
                                        'vacantes': kwargs['vacantes'],
                                        'comentario' : kwargs['comentarios'],
                                        'state' : kwargs['stateselect'],
                                        'route' : kwargs['rutas_wp'],
                                        }) #Agradecimientos a JJ.
            ruta_created.write({
                'route': json.dumps(the_dict),
                'shape': json.dumps(shape),
            })
        
        


        values = ruta_created
        return request.website.render("movilidad_sostenible.ruta_creada", {
                            'person': values
                            })


    @http.route('/movilidad_sostenible/rutas/buscar/', auth='user', website=True)
    def get_buscar(self, **kwargs):
        values = {}
        for field in ['ruta_number']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return request.website.render("movilidad_sostenible.buscar_ruta_form", values)

    @http.route('/movilidad_sostenible/rutas/buscar_ruta/', auth='user', website=True)
    def get_buscar_ruta(self, **kwargs):
        values = json.loads(kwargs['rutas_wp'])
        google = pyproj.Proj("+init=EPSG:3857")
        gps = pyproj.Proj("+init=EPSG:4326")
        start = pyproj.transform(gps, google, values['start']['lng'], values['start']['lat'])
        finish = pyproj.transform(gps, google, values['end']['lng'], values['end']['lat'])
        sql = """SELECT id
            FROM movilidad_sostenible_oferta o
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
        rutas_model = request.env['movilidad_sostenible.oferta']
        rutas = rutas_model.browse(rutas_ids)
        #print rutas
        values.update(kwargs=kwargs.items())
        return http.request.render('movilidad_sostenible.lista_rutas_ofertar', {
            'lista_ofertas': rutas,
        })
        #return request.website.render("movilidad_sostenible.buscar_ruta_form", values)

    @http.route('/movilidad_sostenible/rutas/ofertar/<model("movilidad_sostenible.oferta"):oferta>/', auth='user', website=True)
    def ruta_ofertar_form(self, oferta,**kwargs):
        values = {}
        for field in ['rutas_id', 'rutas_wp']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return http.request.render('movilidad_sostenible.ruta_ofertar_form', {
            'person': oferta,
            'kwargs': values
        })

    @http.route(['/movilidad_sostenible/rutas/ofertar/info_extended/'], type='http', auth='user', website=True)
    def ofertar(self, **kwargs):
        values = {}
        rutas_ids = request.env['movilidad_sostenible.oferta']
        rutas = rutas_ids.search([('id','=',kwargs['rutas_id'])])
        celular = kwargs['celular']
        rutas.mobile_update(celular)
        esta = rutas.existe_usuario_en_ruta()

        if esta:
            return request.website.render("movilidad_sostenible.ruta_no_solicitada")
        else:
            if rutas.tipo_transporte == 'bici':
                rutas.add_user_a_ruta()
                return request.website.render("movilidad_sostenible.ruta_solicitada_success")
            else:
                if rutas.validar_hay_vacantes():
                    rutas.add_user_a_ruta()
                    return request.website.render("movilidad_sostenible.ruta_solicitada_success")
                else:
                    return request.website.render("movilidad_sostenible.ruta_no_solicitada")
