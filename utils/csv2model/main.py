#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import re
import csv

from optparse import OptionParser

logging.basicConfig()
_logger = logging.getLogger('csv2model')

class dict_dot_access(dict):
    """Extension to make dict attributes be accesible with dot notation
    """
    __getattr__ = dict.__getitem__

def trim_vals(vals):
    for key, value in vals.items():
        if type(value) == str:
            vals[key] = value.strip()
    return vals

def main():
    usage = "Takes a CSV and creates a Odoo Module: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--filename", dest="filename", help="CSV file")
    parser.add_option("-p", "--prefix", dest="prefix", help="External ID prefix to use", default='')
    parser.add_option("-m", "--module_name", dest="module", help="Module name", default='')
    parser.add_option("-g", "--generate", action="store_true", dest="generate_file", default=False, help="Generate CSV Template")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Display debug message", default=False)

    (options, args) = parser.parse_args()
    _logger.setLevel(0)
    if options.debug:
        _logger.setLevel(10)

    if options.generate_file:
        print "act_from,act_to,condition,group,label"
        print 'nuevo,en_progreso,True,pqrs_idu.group_responsable,"Abrir"'
        print 'en_progreso,cancelado,True,pqrs_idu.group_administrador,"Cancelar"'
        print 'en_progreso,terminado,tipo==\'canales\',pqrs_idu.group_responsable,"Cerrar"'
        return

    if not options.filename:
        parser.error('filename not given')
    if not options.prefix:
        parser.error('prefix not given')

    prefix = options.prefix

    module = Module(options.module_name)

    with open(options.filename, 'r') as handle:
        reader = csv.DictReader(handle)
        for line in reader:
            _logger.debug(line)
            line = dict_dot_access(trim_vals(line))
            model = module.add_model(line.model_name)
            model.description = line.description
            model.inherit = line.inherit
            model.inherits = line.inherits
            attribute = model.add_attribute(line.name, line)


if __name__ == '__main__':
    main()