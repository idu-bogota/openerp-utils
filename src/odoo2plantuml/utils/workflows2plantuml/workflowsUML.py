#!/usr/bin/python
# -*- coding: utf-8 -*-

import ldap
import logging
from ldap.filter import filter_format
import erppeek
import re
from optparse import OptionParser

from metamodel_workflows import Model
from erppeek_connection import Connection

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
    
    parser.add_option("-M", "--workflow_openERP", dest="workflow_openERP", help="workflow openERP to consult")
    parser.add_option("-D", "--workflow_view", dest="workflow_view", help="detailed workflow openERP to consult. value 1 yes, 0 not", default="0")
    
    parser.add_option("-d", "--debug", dest="debug", help="Mostrar mensajes de debug utilize 10", default=0)

    (options, args) = parser.parse_args()
    _logger.setLevel(int(options.debug))

    if not options.db_name:
        parser.error('db_name not given')
    if not options.db_user:
        parser.error('db_user not given') 
    if not options.db_password:
        parser.error('db_password not given')
    if not options.workflow_openERP:
        parser.error('workflow_openERP not given')

    p = get_details_db(options)
    ## fin main

def init_graph():
    out = open('./workflows_plantuml.txt', 'w+') 
    out.write('@startuml\n')
    return out

def fin_graph(out):
    out.write('@enduml')
    out.close()

def get_wkf_activity(options, connect):
    c = connect.get_connection()
    model = c.model('workflow.activity')
    record_wkf_activity = model.browse([ "wkf_id = {0}".format(options.workflow_openERP) ])
    return record_wkf_activity
    
def get_wkf_transition(options, connect, wkf_activity):
    wkf_acti_tras = {}
    c = connect.get_connection()
    model = c.model('workflow.transition')
    for i in wkf_activity:
        record_wkf_transition = model.browse([ "act_from = {0}".format(i.id) ])
        wkf_acti_tras[i.name] = record_wkf_transition
    return wkf_acti_tras

def get_flow_start(wkf_activity):
    for i in wkf_activity:
        if i.flow_start:
            return i

def get_details_db(options):
    #_logger.debug("*** get_details_db ***")
    connect = Connection(options)
    #c = connect.get_connection()
    wkf_activity = get_wkf_activity(options, connect)
    flow_start = get_flow_start(wkf_activity)
    wkf_acti_tras = get_wkf_transition(options, connect, wkf_activity)
    
    #graficar
    file = init_graph()
    pintar = Model(wkf_acti_tras, file, options, flow_start)
    pintar.get_plantuml_relation_tags()
    fin_graph(file)
    _logger.debug("***Fin workflows UML ***")
# *************** Fin Método para UML ***************#  
if __name__ == '__main__':
    main()