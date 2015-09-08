#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import logging
import csv
from jinja2 import Environment, FileSystemLoader
from metamodel import Module
from cookiecutter.main import cookiecutter

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

def generate_metamodel(options, module):
    with open(options.filename, 'r') as handle:
        reader = csv.DictReader(handle)
        last_model_name = None
        for line in reader:
            line = dict_dot_access(trim_vals(line))
            _logger.debug(line)
            model = None
            if line.model_name:
                model = module.add_model(line.model_name)
                last_model_name = line.model_name
            elif last_model_name and not line.model_name:
                model = module.add_model(last_model_name)
            model.view_configuration = line.views
            model.description = line.description
            model.inherit = line.inherit
            model.inherits = line.inherits
            model.menu = line.menu
            model.overwrite_create = line.overwrite_create
            model.overwrite_write = line.overwrite_write
            field = model.add_field(line.name, line)


def generate_module_content(options, env, module):
    output = {}
    for namespace in module.namespaces():
        output[namespace] = {}
        template = env.get_template("model_py.tpl")
        output[namespace]['py'] = template.render( {'module': module, 'namespace': namespace} )

        template = env.get_template("view_xml.tpl")
        output[namespace]['view'] = template.render( {'module': module, 'namespace': namespace} )

    for model in module.models:
        output[model.name] = {}
        template = env.get_template("test_py.tpl")
        output[model.name]['test'] = template.render( {'model': model} )
        template = env.get_template("data_csv.tpl")
        output[model.name]['data'] = template.render( {'model': model} )

    template = env.get_template("openerp_py.tpl")
    openerp_py = template.render( {'module': module} )

    template = env.get_template("test_init_py.tpl")
    test_init_py = template.render( {'module': module} )

    template = env.get_template("model_init_py.tpl")
    model_init_py = template.render( {'module': module} )

    template = env.get_template("acl_csv.tpl")
    acl_csv = template.render( {'module': module} )

    # Crear estructura del módulo en archivos
    cookiecutter(
        options.templates_dir + '/cookiecutter_template/',
        no_input=True,
        extra_context={
            'name': module.name,
            'namespace': module.namespace,
            'acl_csv': acl_csv,
            'model_py': output[module.namespace]['py'],
            'view_xml': output[module.namespace]['view'],
            'openerp_py': openerp_py,
            'test_init_py': test_init_py,
            'model_init_py': model_init_py,
        },
    )

    for namespace in module.namespaces():
        fname_py = '{0}/models/{1}.py'.format(module.name, namespace)
        fname_view = '{0}/views/{1}_view.xml'.format(module.name, namespace)
        with open(fname_py, "w") as f:
            f.write(output[namespace]['py'])
        with open(fname_view, "w") as f:
            f.write(output[namespace]['view'])

    for model in module.models:
        if model.namespace == module.namespace and model.menu == 'conf' and not options.no_generate_csv_data:
            fname_csv = '{0}/data/{1}.csv'.format(module.name, model.name)
            with open(fname_csv, "w") as f:
                f.write(output[model.name]['data'])
        elif model.namespace == module.namespace and model.menu != 'conf':
            if not options.no_generate_csv_data:
                fname_csv = '{0}/demo/{1}.csv'.format(module.name, model.name)
                with open(fname_csv, "w") as f:
                    f.write(output[model.name]['data'])
            fname_test = '{0}/tests/test_{1}.py'.format(module.name, model.name.replace('.', '_'))
            with open(fname_test, "w") as f:
                f.write(output[model.name]['test'])

def generate_metamodel_security(options, module):
    with open(options.filename_security, 'r') as handle:
        reader = csv.DictReader(handle)
        last_group_name = None
        for line in reader:
            line = dict_dot_access(trim_vals(line))
            _logger.debug(line)
            group = None
            if line.group:
                group = module.add_group(line.group)
                last_group_name = line.group
            elif last_group_name and not line.group:
                group = module.add_group(last_group_name)

            group.add_acl(
                line.model_name,
                line.create,
                line.read,
                line.write,
                line.delete,
            )

def generate_module_security(options, env, module):

    template = env.get_template("security_xml.tpl")
    content = template.render( {'module': module} )
    fname = '{0}/security/security.xml'.format(module.name)
    with open(fname, "w") as f:
        f.write(content)

    template = env.get_template("acl_csv.tpl")
    content = template.render( {'module': module} )
    fname = '{0}/security/ir.model.access.csv'.format(module.name)
    with open(fname, "w") as f:
        f.write(content)

    template = env.get_template("test_domain_py.tpl")
    for group in module.groups:
        fname_test = '{0}/tests/test_domain_{1}.py'.format(module.name, group.name.replace('.', '_'))
        content = template.render( {'group': group, 'module': module} )
        with open(fname_test, "w") as f:
            f.write(content)

    template = env.get_template("test_users_yml.tpl")
    fname_test = '{0}/tests/001_users.yml'.format(module.name)
    content = template.render( {'module': module} )
    with open(fname_test, "w") as f:
        f.write(content)

    template = env.get_template("openerp_py.tpl")
    openerp_py = template.render( {'module': module} )
    fname_test = '{0}/__openerp__.py'.format(module.name)
    with open(fname_test, "w") as f:
        f.write(openerp_py)

    template = env.get_template("test_init_py.tpl")
    test_init_py = template.render( {'module': module} )
    fname_test = '{0}/tests/__init__.py'.format(module.name)
    with open(fname_test, "w") as f:
        f.write(test_init_py)


def generate_metamodel_workflow(options, module):
    with open(options.filename_workflow, 'r') as handle:
        reader = csv.DictReader(handle)
        last_model_name = None
        for line in reader:
            line = dict_dot_access(trim_vals(line))
            _logger.debug(line)
            model = None
            if line.model_name:
                model = module.add_model(line.model_name)
                last_model_name = line.model_name
            elif last_model_name and not line.model_name:
                model = module.add_model(last_model_name)
            model.add_transition(line)

def generate_module_workflow(options, env, module):
    template = env.get_template("workflow_xml.tpl")
    for model in module.models:
        if model.transitions:
            fname_xml = '{0}/workflow/{1}_workflow.xml'.format(module.name, model.short_name)
            content = template.render( {'model': model} )
            with open(fname_xml, "w") as f:
                f.write(content)

def main():
    usage = "Takes a CSV and creates a Odoo Module: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--filename", dest="filename", help="CSV file")
    parser.add_option("-S", "--filename_security", dest="filename_security", help="CSV file security", default=False)
    parser.add_option("-w", "--filename_workflow", dest="filename_workflow", help="CSV file workflow", default=False)
    parser.add_option("-n", "--module_namespace", dest="module_namespace", help="Module namespace", default=False)
    parser.add_option("-m", "--module_name", dest="module_name", help="Module technical name", default='')
    parser.add_option("-s", "--module_string", dest="module_string", help="Module human name", default=False)
    parser.add_option("-g", "--generate", action="store_true", dest="generate_file", default=False, help="Generate CSV Template")
    parser.add_option("-G", "--generate_security_file", action="store_true", dest="generate_security_file", default=False, help="Generate CSV Template for Security")
    parser.add_option("-W", "--generate_workflow_file", action="store_true", dest="generate_workflow_file", default=False, help="Generate CSV Template for Workflow")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Display debug message", default=False)
    parser.add_option("-c", "--no_generate_csv_data", action="store_true", dest='no_generate_csv_data', help='Don\'t generate csv files on demo and data', default=False)
    parser.add_option("-t", "--templates", dest="templates_dir", help="Templates folder",
        default=os.path.dirname(os.path.realpath(__file__)) + '/templates'
    )

    (options, args) = parser.parse_args()
    _logger.setLevel(0)

    if options.debug:
        _logger.setLevel(10)

    if options.generate_file:
        print """model_name,name,type,params,comodel,string,help,required,unique,tracking,constrains,onchange,view_tree,view_form,view_search,view_search_group_by,view_form_tab,menu,description,inherits,inherit,overwrite_write,overwrite_create,views
petstore.pet,name,char,size:50,,Nombre,Nombre de la mascota,1,0,1,0,0,1,1,1,0,0,main,Pet,,mail.thread,1,1,new
,state,selection,selection:Draft|Open|Closed|Pending;default:'draft',,Estado,Estados de la mascota,1,0,1,0,0,1,1,1,1,0,,,,,,,
,user_id,many2one,readonly:True;default:_CURRENT_USER_,res.users,Usuario,Usuario asignado,0,0,1,0,0,1,_ATTRS_,"[('user_id','=',uid)]",1,0,,,,,,,
,age,float,compute:True;depends:birth_date,,Edad,Edad en Años,0,0,1,0,0,1,1,1,0,0,,,,,,,
,birth_date,date,default:_NOW_,,Fecha de nacimiento,Fecha de nacimiento,0,0,1,0,0,1,1,1,0,0,,,,,,,
,breed_id,many2one,,petstore.breed,Raza,Raza de la mascota,1,0,1,0,0,1,1,1,1,Raza,,,,,,,
,partner_id,many2one,"domain:[('is_company','=',False)]",res.partner,Dueño,Dueño de la mascota,1,0,1,0,0,1,1,1,1,Dueño,,,,,,,
petstore.breed,name,char,size:100,,Nombre,Nombre de la raza,1,1,1,0,0,1,1,1,0,0,conf,Raza de Mascotas,,,,,new
,pet_ids,one2many,readonly:True,"petstore.pet,breed_id",Mascotas,Mascotas registradas para esta raza,0,0,0,0,0,0,1,0,0,0,,,,,,,
res.partner,pet_ids,one2many,,"petstore.pet,partner_id",Mascotas,Mascotas registradas a este Partner,0,0,0,0,0,0,1,0,0,0,main,,,res.partner,,,"extend:form=base.view_partner_form|category_id,tree=base.view_partner_tree|email,search=base.view_res_partner_filter|parent_id"
res.users,pet_ids,one2many,,"petstore.pet,user_id",Mascotas a cargo,,0,0,0,0,0,0,0,0,0,0,main,,,res.users,,,none"""
        return

    if options.generate_security_file:
        print """model_name,group,create,read,write,delete
petstore.pet,base.group_user,0,"('partner_id','=', user.partner_id.id)",0,0
petstore.pet,petstore.vet,_OWN_,_ALL_,_OWN_,0
petstore.pet,petstore.admin,1,1,1,1
petstore.breed,petstore.admin,1,_ALL_,1,1"""
        return

    if options.generate_workflow_file:
        print """model_name,act_from,act_to,condition,group,button_label,type
petstore.pet,draft,open,True,petstore.group_vet,Abrir,start
,open,pending,True,petstore.group_vet,Pendiente,
,open,closed,True,petstore.group_vet,Cerrar,stop
,pending,open,True,petstore.group_admin,Abrir,
,pending,closed,age > 10,,,
petstore.breed,nuevo,en_progreso,True,petstore.group_admin,Abrir,start
,en_progreso,terminado,True,petstore.group_admin,Cerrar,stop"""
        return

    if not options.filename:
        parser.error('CSV filename not given')

    env = Environment(loader=FileSystemLoader(options.templates_dir))

    module = Module(options.module_name, options.module_namespace, options.module_string)
    generate_metamodel(options, module)
    if options.filename_workflow:
        generate_metamodel_workflow(options, module)
    generate_module_content(options, env, module)
    if options.filename_workflow:
        generate_module_workflow(options, env, module)

    if options.filename_security:
        generate_metamodel_security(options, module)
        generate_module_security(options, env, module)



if __name__ == '__main__':
    main()
