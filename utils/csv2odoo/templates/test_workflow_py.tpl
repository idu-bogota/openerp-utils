{% import "test_macros.tpl" as macro_fields -%}
# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common
from openerp.exceptions import AccessError

logging.basicConfig()
_logger = logging.getLogger('TEST')

class test_workflow_{{ model.short_name | replace('.','_') }}(common.TransactionCase):
    def test_000_{{ model.short_name | replace('.', '_') }}_01(self):
        """ {{ model.short_name }} verifica flujo de trabajo"""
    {%- for group in model.module.groups %}
        {%- set user = "user_" + group.name | replace('.', '_') %}
        {{ user }} = self.ref('{{ model.module.name }}.{{ group.short_name }}_user_01')
    {%- endfor %}
        {{ model.short_name }}_model = self.env['{{ model.name }}']
        {{ model.short_name }} = {{ model.short_name }}_model.search([], limit=1)
  {%- for tr in model.transitions %}

        # ----------------------------
        # [{{ tr.act_from.name }}] -> [{{ tr.act_to.name }}]
        # ----------------------------
        self.assertEqual({{ model.short_name }}.state, '{{ tr.act_from.name }}')
    {%- if tr.group_name %}
      {%- set group_valid = "user_" + tr.group_name | replace('.', '_') %}
      {%- if tr.condition == 'True' %}
        {{ model.short_name }}.sudo(GRUPO_SIN_PERMISO).signal_workflow('{{ tr.signal }}')
        self.assertEqual({{ model.short_name }}.state, '{{ tr.act_from.name }}')
        {{ model.short_name }}.sudo({{ group_valid }}).signal_workflow('{{ tr.signal }}')
        self.assertEqual({{ model.short_name }}.state, '{{ tr.act_to.name }}')
      {%- else %}

        # No se cumple la condicion {{ tr.condition }}
        {{ model.short_name }}.sudo(GRUPO_SIN_PERMISO).signal_workflow('{{ tr.signal }}')
        self.assertEqual({{ model.short_name }}.state, '{{ tr.act_from.name }}')
        {{ model.short_name }}.sudo({{ group_valid }}).signal_workflow('{{ tr.signal }}')
        self.assertEqual({{ model.short_name }}.state, '{{ tr.act_from.name }}')

        # Si se cumple la condicion {{ tr.condition }}
        {{ model.short_name }}.write({'campo': 'valor_valido'})
        {{ model.short_name }}.sudo(GRUPO_SIN_PERMISO).signal_workflow('{{ tr.signal }}')
        self.assertEqual({{ model.short_name }}.state, '{{ tr.act_from.name }}')
        {{ model.short_name }}.sudo({{ group_valid }}).signal_workflow('{{ tr.signal }}')
        self.assertEqual({{ model.short_name }}.state, '{{ tr.act_to.name }}')
      {%- endif -%}
    {%- else -%}
      {%- if tr.condition == 'True' %}
        {{ model.short_name }}.signal_workflow('{{ tr.signal }}')
        self.assertEqual({{ model.short_name }}.state, '{{ tr.act_to.name }}')
      {%- else %}

        # No se cumple la condicion {{ tr.condition }}
        {{ model.short_name }}.signal_workflow('{{ tr.signal }}')
        self.assertEqual({{ model.short_name }}.state, '{{ tr.act_from.name }}')

        # Si se cumple la condicion {{ tr.condition }}
        {{ model.short_name }}.write({'campo': 'valor_valido'})
        {{ model.short_name }}.signal_workflow('{{ tr.signal }}')
        self.assertEqual({{ model.short_name }}.state, '{{ tr.act_to.name }}')
      {%- endif -%}
    {%- endif -%}
  {%- endfor %}


if __name__ == '__main__':
    unittest2.main()