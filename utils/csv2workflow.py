#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import re
import csv

from optparse import OptionParser

logging.basicConfig()
_logger = logging.getLogger('script')

def trim_vals(vals):
    for key, value in vals.items():
        if type(value) == str:
            vals[key] = value.strip()
    return vals

TMPL_XML_HEADER = """<?xml version="1.0" encoding="utf-8"?>
<openerp>
<data>
"""
TMPL_XML_FOOTER = "</data>\n</openerp>"
TMPL_WORKFLOW = """    <record id="{prefix}workflow" model="workflow">
        <field name="name">{model}.workflow</field>
        <field name="osv">{model}</field>
        <field name="on_create">True</field>
    </record>"""
TMPL_ACTIVITY = """    <record id="{prefix}{act}_activity" model="workflow.activity">
            <field name="wkf_id" ref="{wkf_id}"/>
            <field name="name">{act}</field>
            <field name="kind">function</field>
            <field name="action">wkf_{act}()</field>
            <field name="flow_start" eval="False"/>
            <field name="flow_stop" eval="False"/>
    </record>"""
TMPL_TRANSITION =  """    <record id="{prefix}{act_from}__{act_to}_transition" model="workflow.transition">
                    <field name="act_from" ref="{prefix}{act_from}_activity"/>
                    <field name="act_to" ref="{prefix}{act_to}_activity"/>
                    <field name="condition">{condition}</field>
                    <field name="group_id" ref="{group}"/>
                    <field name="signal">wkf_{act_from}__{act_to}</field>
    </record>"""
TMPL_BUTTON = """                    <button string="{label}" name="{signal}" type="workflow" class="oe_highlight"
                        groups="{group}"
                        states="{state}"
                    />"""
TMPL_WORKFLOW_METHOD = """    def wkf_{state}(self):
        self.state = '{state}'
"""

def main():
    usage = "Takes a CSV and creates a Odoo XML Workflow document: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--filename", dest="filename", help="CSV file")
    parser.add_option("-p", "--prefix", dest="prefix", help="External ID prefix to use", default='')
    parser.add_option("-m", "--model", dest="model", help="Model Name", default='module.model_name')
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
    model = options.model
    wkf_id = '{0}workflow'.format(prefix)
    activities = set()
    buttons = set()

    print TMPL_XML_HEADER
    print TMPL_WORKFLOW.format(model=model, prefix=prefix)
    with open(options.filename, 'r') as handle:
        print """    <!--
    ===================================================================================
    Activities
    ===================================================================================
     -->"""
        reader = csv.DictReader(handle)
        for line in reader:
            _logger.debug(line)
            line = trim_vals(line)
            activities.add(line['act_from'])
            activities.add(line['act_to'])
            signal = "wkf_{act_from}__{act_to}".format(act_from=line['act_from'], act_to=line['act_to'])
            buttons.add((line['group'], signal, line['label'], line['act_from']))
        ## Worflow - Activities
        for act in list(activities):
            print TMPL_ACTIVITY.format(prefix=prefix, act=act, wkf_id=wkf_id)
        print """    <!--
    ===================================================================================
    Transitions
    ===================================================================================
     -->"""
        handle.seek(0)
        reader = csv.DictReader(handle)
        for line in reader:
            _logger.debug(line)
            print TMPL_TRANSITION.format(
            prefix=prefix,
            act_from=line['act_from'],
            act_to=line['act_to'],
            condition=line['condition'],
            group=line['group'],
        )
        print TMPL_XML_FOOTER
        print """    <!--
    ===================================================================================
    Form Workflow Buttons
    ===================================================================================
     -->"""
        for button in list(buttons):
            print TMPL_BUTTON.format(
                label=button[2],
                signal=button[1],
                group=button[0],
                state=button[3],
            )
        print """
    # ===================================================================================
    # Workflow Methods
    # ===================================================================================
"""
        for act in list(activities):
            print TMPL_WORKFLOW_METHOD.format(state=act)


if __name__ == '__main__':
    main()