#!/usr/bin/python
# -*- coding: utf-8 -*-

import ldap
import logging
from ldap.filter import filter_format
import erppeek
import re
from optparse import OptionParser

from metamodel import Model

logging.basicConfig()
_logger = logging.getLogger('script')

def main():
    
    usage = "Connection to Active Directory by LDAP\nusage: %prog [options]"
    parser = OptionParser(usage)
    
    parser.add_option("-N", "--db_name", dest="db_name", help="OpenERP database name")
    parser.add_option("-U", "--db_user",dest="db_user",help="OpenERP database user")
    parser.add_option("-P", "--db_password", dest="db_password", help="OpenERP database password")
    parser.add_option("-H", "--host_openERP", dest="host_openERP", help="OpenERP server host", default="http://localhost")
    parser.add_option("-J", "--port_openERP", dest="port_openERP", help="OpenERP server port", default="8069")
    
    parser.add_option("-M", "--model_openERP", dest="model_openERP", help="Model openERP to consult")
    parser.add_option("-D", "--detailed_model", dest="detailed_model", help="detailed model openERP to consult. value 1 yes, 0 not", default="0")
    parser.add_option("-L", "--model_levels", dest="model_levels", help="level of detail of the model between 1 to 3", default="1")
    
    parser.add_option("-I", "--model_include", dest="model_include", help="force models include but are not related")
    parser.add_option("-E", "--model_exclude", dest="model_exclude", help="not paint models although they are related")
    
    parser.add_option("-d", "--debug", dest="debug", help="Mostrar mensajes de debug utilize 10", default=0)

    (options, args) = parser.parse_args()
    _logger.setLevel(int(options.debug))

    if not options.db_name:
        parser.error('db_name not given')
    if not options.db_user:
        parser.error('db_user not given') 
    if not options.db_password:
        parser.error('db_password not given')
    if not options.model_openERP:
        parser.error('model_openERP not given')
    '''
    if int(options.model_levels) > 3:    #int(float(a))
        parser.error('model_levels must be less than 3')
    if int(options.model_levels) <= 0:    #int(float(a))
        parser.error('model_levels must be greater than 0')    
    '''    
        
    p = get_details_db(options) 

    ## fin main
    
# *************** Método para UML ***************#  
def init_graph():
    out = open('./plantuml.txt', 'w+') 
    out.write('@startuml\n')
    return out

def fin_graph(out):
    out.write('@enduml')
    out.close()

def get_connection(options):
    server = options.host_openERP + ':' +  options.port_openERP
    database = options.db_name
    user = options.db_user
    password = options.db_password
    insert_employee_id = False
    c = erppeek.Client(server, database, user, password)
    return c

def generate_model(entity, model, options):
    c = get_connection(options)
    
    if len(model) == 0:
        campos = c.model(entity).fields()
        model[entity] = campos
    
    modelo2 = increase_model(c,model)
    return modelo2
        
def increase_model(connect, model):
    _logger.debug("*** increase_model ***")
    entity_relations = []
    end_model = model.copy()
    
    #print "modelo inicial"
    _logger.debug("modelo que ingresa ")
    for i in model: 
        _logger.debug(i)
    
    for i in model:
        campos = model[i] 
        _logger.debug("\n{0} Campos a iterar\n".format(i))
        
        for key, campo in campos.iteritems():
            if campo['type'] == 'many2one':
                entity_relations.append(campo['relation'])

        if len(entity_relations) != 0:
            _logger.debug("tiene relaciones")
            # limpiar campos de relaciones repetidas y el actual
            entity_relations = clean_relations_of_entity(entity_relations, i)
            
            # limpiar entidades del modelo general
            entity_relations = clean_entity_of_model_general(entity_relations, end_model)
            
            # asignar las nuevas relaciones al modelo general
            end_model = assign_new_entity(connect, entity_relations, end_model)

    return end_model

def clean_relations_of_entity(entity_relations, entity):
    _logger.debug("*** clean_relations_of_entity  ***")
    
    # elimina repetidosw
    entity_relations = list(set(entity_relations))
    #_logger.debug("entidades relacionadas sin repetidos")
    #_logger.debug(entity_relations)
    
    if entity in entity_relations:
        # eliminar actula modelo a la lista
        entity_relations.remove(entity)
        #_logger.debug("entidades relacionadas sin repetidos y sin el actual ")entity_relations
        #_logger.debug(entity_relations)
    
    _logger.debug(entity_relations)
    return entity_relations

def clean_entity_of_model_general(entity_relations, model):
    _logger.debug( "\n**** clean_entity_of_model_general ***")
    end_entity_relations = entity_relations[:]
    
    for i in entity_relations:
        if i in model:
            #_logger.debug("la entityu {0} esta en el modelo general {1}".format(i, model))
            end_entity_relations.remove(i)
            
    _logger.debug("\n{0} Campos que no existen en el modelo original\n".format(end_entity_relations))        
    return end_entity_relations 

def assign_new_entity(connect, entity_relations, model):
    _logger.debug( "\n*** assign_new_entity ***")
    
    for i in entity_relations:
        _logger.debug("{0} Campos agregado".format(i))
        campos = connect.model(i).fields()
        model[i] = campos
    return model

def exclude_entity_of_model_general(options, model):
    _logger.debug("exclude_entity_of_model_general")
    
    entity_to_exclude = options.model_exclude.split(',')
    
    end_model = model.copy()
    
    for exclude in entity_to_exclude:
        if '*' in exclude:
            for entity in model:
                if re.match(exclude, entity):
                    del end_model[entity]
        else:
            del end_model[exclude]
            
    return end_model
    
def include_entity_of_model_general(options, model):
    _logger.debug("include_entity_of_model_general")
    c = get_connection(options)
    # separar por comas
    entity_to_include = options.model_include.split(',')
    
    for include in entity_to_include:
        if '*' in include:
            print '\n***** consultar en ir model ******\n'
            end_entity_to_include = get_model_of_db_exr(options, include, c)
            
            end_entity_to_include = clean_entity_of_model_general(end_entity_to_include, model)
            
            end_model = assign_new_entity(c, end_entity_to_include, model)
        else:
            lista = []
            lista.insert(0,include) # se convierte en lista porque las funciones esperan listas

            end_entity_to_include = clean_entity_of_model_general(lista, model)
            
            end_model = assign_new_entity(c, end_entity_to_include, model)
    
    return end_model

def get_model_of_db_exr(options, models_to_consult, connect):
    end_record_model = []
    models = connect.model('ir.model')
    models_to_consult = models_to_consult.replace('*', '%')  #cambiar el * por el %
    
    record_model = models.browse([ "model like '{0}'".format(models_to_consult) ])
    
    for i in record_model:
        end_record_model.append(i.model)
    
    return end_record_model


def get_details_db(options):
    
    profundidad = int(options.model_levels)
    a = {}
    
    for i in range(profundidad):
        print "{0}  {1}\n".format("Iteracion numero :", i)
        a = generate_model(options.model_openERP, a, options)
    # ***
    _logger.debug("\n*** retorno generate_model ***")
    for i in a:
        print i
        
        
    # include
    if(options.model_include):
        a = include_entity_of_model_general(options, a)

        _logger.debug("\n*** retorno despues del include ***")
        for i in a:
            print i

    # exclude
    if(options.model_exclude):
        a = exclude_entity_of_model_general(options, a)
    
        _logger.debug("\n*** retorno despues del exclude ***")
        for i in a:
            print i
    
    file = init_graph()
    pintar = Model(a, file, options.detailed_model)
    pintar.get_plantuml_relation_tags()
    pintar.get_plantuml_entity_tags()
    
    fin_graph(file)
    
# *************** Fin Método para UML ***************#  
if __name__ == '__main__':
    main()