'''
Created on Jul 6, 2015

@author: camoncal1
'''
from openerp import http

class Rutas(http.Controller):
    @http.route('/rutas/', auth='public', website=True)
    def index(self):
        Oferta = http.request.env['mi_carro_tu_carro.oferta']
        return http.request.render('mi_carro_tu_carro_idu.index', {
            'ofertas': Oferta.search([]),
        })
        
    @http.route('/rutas/<model("mi_carro_tu_carro.oferta"):offer>/', auth='public', website=True)
    def offer(self, offer):
        return http.request.render('mi_carro_tu_carro_idu.descripcion', {
            'person': offer
        })