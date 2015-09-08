{% import "test_macros.tpl" as macro_fields -%}
# -*- encoding: utf-8 -*-
import unittest2
import logging
from openerp.tests import common

logging.basicConfig()
_logger = logging.getLogger('TEST')

class Test_security_{{ group.name | replace('.','_') }}(common.TransactionCase):
    def test_{{ group.name | replace('.', '_') }}_search(self):
        {%- set user = "user_" + group.short_name | replace('.', '_') %}
        {{ user }}_01 = self.ref('{{ group.name }}_user_01')
        {{ user }}_02 = self.ref('{{ group.name }}_user_02')
    {%- for model in module.models %}

        {{ model.short_name }}_model = self.env['{{ model.name }}']
        self.assertEqual(1000, {{ model.short_name }}_model.sudo({{ user }}_01).search_count([]))
        self.assertEqual(1000, {{ model.short_name }}_model.sudo({{ user }}_02).search_count([]))
    {%- endfor %}

    def test_{{ group.name | replace('.', '_') }}_create(self):
        {%- set user = "user_" + group.short_name | replace('.', '_') %}
        {{ user }}_01 = self.ref('{{ group.name }}_user_01')
        {{ user }}_02 = self.ref('{{ group.name }}_user_02')

    {%- for model in module.models %}

        {{ model.short_name }}_model = self.env['{{ model.name }}']
        #### Creación permitida
        vals = {{ '{' }}{% for field in model.fields if not field.arguments['compute'] and not field.arguments['related'] %}
            {{  macro_fields|attr(field.type)(field) }}
        {%- endfor %}
        }
        {{ model.short_name }} = {{ model.short_name }}_model.sudo({{ user }}_01).create(vals)

        #### Creación NO permitida
        vals = {{ '{' }}{% for field in model.fields if not field.arguments['compute'] and not field.arguments['related'] %}
            {{  macro_fields|attr(field.type)(field) }}
        {%- endfor %}
        }
        try:
            {{ model.short_name }} = {{ model.short_name }}_model.sudo({{ user }}_01).create(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad creando {}'.format({{ model.short_name }}_model))
    {%- endfor %}

    def test_{{ group.name | replace('.', '_') }}_write(self):
        {%- set user = "user_" + group.short_name | replace('.', '_') %}
        {{ user }}_01 = self.ref('{{ group.name }}_user_01')
        {{ user }}_02 = self.ref('{{ group.name }}_user_02')

    {%- for model in module.models %}

        {{ model.short_name }}_model = self.env['{{ model.name }}']
        #### Actualización permitida
        vals = {{ '{' }}{% for field in model.fields if not field.arguments['compute'] and not field.arguments['related'] %}
            {{  macro_fields|attr(field.type)(field) }}
        {%- endfor %}
        }
        {{ model.short_name }} = self.env[{{ model.short_name }}_model].sudo({{ user }}_01).search([], limit=1)
        {{ model.short_name }}.sudo({{ user }}_01).write(vals)

        #### Actualización NO permitida
        vals = {{ '{' }}{% for field in model.fields if not field.arguments['compute'] and not field.arguments['related'] %}
            {{  macro_fields|attr(field.type)(field) }}
        {%- endfor %}
        }
        {{ model.short_name }} = self.env[{{ model.short_name }}_model].sudo({{ user }}_01).search([], limit=1)
        try:
            {{ model.short_name }}.sudo({{ user }}_01).write(vals)
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad actualizando {}'.format({{ model.short_name }}_model))
    {%- endfor %}

    def test_{{ group.name | replace('.', '_') }}_unlink(self):
        {%- set user = "user_" + group.short_name | replace('.', '_') %}
        {{ user }}_01 = self.ref('{{ group.name }}_user_01')
        {{ user }}_02 = self.ref('{{ group.name }}_user_02')

    {%- for model in module.models %}

        {{ model.short_name }}_model = self.env['{{ model.name }}']
        #### Eliminación permitida
        {{ model.short_name }} = self.env[{{ model.short_name }}_model].sudo({{ user }}_01).search([], limit=1)
        {{ model.short_name }}.sudo({{ user }}_01).unlink()

        #### Eliminación NO permitida
        {{ model.short_name }} = self.env[{{ model.short_name }}_model].sudo({{ user }}_01).search([], limit=1)
        try:
            {{ model.short_name }}.sudo({{ user }}_01).unlink()
        except AccessError:
            pass
        else:
            self.fail('No se generó Exception de seguridad Eliminando {}'.format({{ model.short_name }}_model))
    {%- endfor %}


if __name__ == '__main__':
    unittest2.main()