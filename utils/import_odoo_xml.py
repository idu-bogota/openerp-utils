#!/usr/bin/python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import erppeek
import logging
import sys
import xml.etree.ElementTree as ET
import re

logging.basicConfig()
_logger = logging.getLogger('script')

def main():
    usage = "Script para carga de archivo XML en BD odoo\nusage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--filename", dest="filename", help='File to load')
    parser.add_option("-i", "--record_id", dest="record_id", help='Record ID to load', default=False)
    parser.add_option("-n", "--odoo_db_name", dest="odoo_db_name", help="Odoo database name")
    parser.add_option("-u", "--odoo_db_user",dest="odoo_db_user", help="Odoo database user", default='admin')
    parser.add_option("-p", "--odoo_db_password", dest="odoo_db_password", help="Odoo database password", default='admin')
    parser.add_option("-s", "--odoo_server", dest="odoo_server", help="Odoo server host", default="http://localhost:8069")
    parser.add_option("-m", "--module_name", dest="module_name", help="Module name")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Display debug messages", default=False)

    (options, args) = parser.parse_args()
    if not options:
        sys.exit(parser.print_help())

    if options.debug:
        _logger.setLevel(10)
    else:
        _logger.setLevel(20)

    check_obligatorios = ['odoo_db_name', 'odoo_db_user', 'odoo_db_password', 'module_name']
    for i in check_obligatorios:
        if not getattr(options, i):
            parser.error('{0} es obligatorio'.format(i))
    importar_xml(options)

def importar_xml(options):
    odoo = conectar_odoo_openerp(options.odoo_server, options.odoo_db_name, options.odoo_db_user, options.odoo_db_password)
    tree = ET.parse(options.filename)
    root = tree.getroot()
    elements = None
    if options.record_id:
        elements = root.findall(".//record[@id='{0}']".format(options.record_id))
    else:
        elements = root.iter('record')
    for record in elements:
        record_model = record.get('model')
        record_id = record.get('id')
        if record_model == 'ir.ui.view':
            view_id = odoo.model('ir.model.data').browse([
                'module = {0}'.format(options.module_name),
                'name = {0}'.format(record_id),
            ]).res_id
            if not view_id:
                _logger.error('No se encontró la vista a actualizar {1}.{2}'.format(options.module_name, record_id))

            view_arch = None
            for field in record.findall('field'):
                if field.get('name') == 'arch':
                    view_arch = ET.tostring(field)
                    view_arch = view_arch.strip()
                    view_arch = re.sub('^<field name="arch" type="xml">', '', view_arch)
                    view_arch = re.sub('</field>$', '', view_arch)
                    view_arch = view_arch.strip()
                    break
            if view_arch:
                _logger.info('Updating view {0} {1}.{2}'.format(view_id, options.module_name, record_id))
                _logger.debug("'{0}'".format(view_arch))
                try:
                    odoo.model('ir.ui.view').write(view_id, {
                        'arch': view_arch
                    })
                except Exception as e:
                    _logger.error('Updating view {0} {1}.{2}'.format(view_id, options.module_name, record_id))
                    _logger.error(e.faultCode)
                    _logger.debug(e.faultString)

def conectar_odoo_openerp(server, db_name, user, password):
    _logger.debug('Contectando a: {0} {1}'.format(server, db_name));

    client = erppeek.Client(
        server,
        db_name,
        user,
        password,
    )
    return client

if __name__ == '__main__':
    main()
