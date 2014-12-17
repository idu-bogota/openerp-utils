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
    
    parser.add_option("-M", "--view_openERP", dest="view_openERP", help="view openERP to consult")
    parser.add_option("-D", "--detailed_view", dest="detailed_view", help="detailed model openERP to consult. value 1 yes, 0 not", default="0")
    parser.add_option("-L", "--view_levels", dest="view_levels", help="level of detail of the model between 1 to 3", default="1")
    
    parser.add_option("-I", "--view_include", dest="view_include", help="force models include but are not related")
    parser.add_option("-E", "--view_exclude", dest="view_exclude", help="not paint models although they are related")
    
    parser.add_option("-d", "--debug", dest="debug", help="Mostrar mensajes de debug utilize 10", default=0)

    (options, args) = parser.parse_args()
    _logger.setLevel(int(options.debug))

    if not options.db_name:
        parser.error('db_name not given')
    if not options.db_user:
        parser.error('db_user not given') 
    if not options.db_password:
        parser.error('db_password not given')
    if not options.view_openERP:
        parser.error('view_openERP not given')

    p = get_details_db(options)
    ## fin main
# *************** Método para UML ***************#  
def init_graph():
    out = open('./views_plantuml.txt', 'w+') 
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

def get_view_of_db(options, view_to_consult):
    end_record_view = []
    c = get_connection(options)
    view = c.model('ir.ui.view')
    record_view = view.browse([ "model = {0}".format(view_to_consult) ])
    for i in record_view:
        end_record_view.append(i)
    return end_record_view

# con expresiones regulares
def get_view_of_db_exr(options, view_to_consult):
    end_record_view = []
    c = get_connection(options)
    view = c.model('ir.ui.view')
    view_to_consult = view_to_consult.replace('*', '%')  #cambiar el * por el %
    
    record_view = view.browse([ "model like '{0}'".format(view_to_consult) ])
    
    for i in record_view:
        end_record_view.append(i)
    return end_record_view

def generate_model(model_of_view, options):
    #_logger.debug("*** generate_model ***")
    if len(model_of_view) == 0:
        #record_view = view.browse([ "model = {0}".format(options.view_openERP) ])
        record_view = get_view_of_db(options, options.view_openERP)
    else:
        record_view = increase_model(model_of_view)
        
    return record_view

def increase_model(model_of_view):
    _logger.debug("*** increase_model ***")
    fields_relations = []    
    end_model_of_view = model_of_view[:]
    
    for i in model_of_view:
        #relaciones
        if(i.inherit_id):
            fields_relations.append(i.inherit_id) 
    
    if(len(fields_relations) != 0):
        # limpiar campos de relaciones repetidas y el actual
        fields_relations = clean_relations_of_model(fields_relations)
        
        _logger.debug("relaciones")
        _logger.debug(fields_relations)
        
        # limpiar campos de relacion que esten en el modelo general
        fields_relations = clean_entity_of_model_general(fields_relations, model_of_view)
        _logger.debug("nuevos en la relacion ")
        _logger.debug(fields_relations)
        
        # asignar las nuevas relaciones al modelo general
        model_of_view = assign_new_entity(fields_relations, model_of_view)
    
    return model_of_view
    
def clean_relations_of_model(fields_relations):
    newlist = []
    # elimina repetidosw
    for i in fields_relations:
        if i not in newlist:
            newlist.append(i)
    return newlist

def clean_entity_of_model_general(fields_relations, model_of_view):
    end_fields_relations = fields_relations[:]
    # elimina los que ya existen en el modelo general
    for i in fields_relations:
        if i in model_of_view:
            end_fields_relations.remove(i)
    return end_fields_relations

def assign_new_entity(fields_relations, model_of_view):
    #_logger.debug( "\n*** assign_new_entity ***")
    for i in fields_relations:
        _logger.debug("{0} Campos agregado".format(i))
        model_of_view.append(i)
    return model_of_view
    
def exclude_entity_of_model_general(options, model):
    _logger.debug("\n*** exclude_entity_of_model_general ***\n")
    entity_to_exclude = options.view_exclude.split(',')
    list_model = []
    
    for i in model:
        list_model.append(i)
    
    end_list_model = list_model[:]
    
    for exclude in entity_to_exclude:
        if '*' in exclude:
            for entity in list_model:
                if re.match(exclude, entity.name):
                    end_list_model.remove(entity)
        else:
            for i in list_model:
                if i.name == exclude:
                    end_list_model.remove(i)
    return end_list_model

def include_entity_of_model_general(options, model):
    _logger.debug("\n***include_entity_of_model_general ***\n")
    entity_to_include = options.view_include.split(',')
    
    for include in entity_to_include:
        if '*' in include:
            entity = get_view_of_db_exr(options, include)
            # limpiar campos de relacion que esten en el modelo general
            entity = clean_entity_of_model_general(entity, model)
            # asignar las nuevas relaciones al modelo general
            model = assign_new_entity(entity, model)
        else:
            entity = get_view_of_db(options, include)
            # limpiar campos de relacion que esten en el modelo general
            entity = clean_entity_of_model_general(entity, model)
            # asignar las nuevas relaciones al modelo general
            model = assign_new_entity(entity, model)
    return model
    
def get_details_db(options):
    #_logger.debug("*** get_details_db ***")
    model_of_view = []
    profundidad = int(options.view_levels)
    
    for i in range(profundidad):
        _logger.debug("iteracion numero  {0}\n".format(i))
        model_of_view = generate_model(model_of_view, options)
    
    _logger.debug("\n** modelo Generado **\n")
    for i in model_of_view:
        _logger.debug(i)
    
    # include
    if(options.view_include):
        model_of_view = include_entity_of_model_general(options, model_of_view)
        _logger.debug("\n*** retorno despues del include ***\n")
        for i in model_of_view:
            _logger.debug(i)
    
    # exclude
    if(options.view_exclude):
        model_of_view = exclude_entity_of_model_general(options, model_of_view)
        _logger.debug("\n*** retorno despues del exclude ***\n")
        for i in model_of_view:
            _logger.debug(i)
    
    file = init_graph()
    pintar = Model(model_of_view, file, options)
    pintar.get_plantuml_relation_tags()
    pintar.get_plantuml_entity_tags()
    fin_graph(file)

# *************** Fin Método para UML ***************#  
if __name__ == '__main__':
    main()