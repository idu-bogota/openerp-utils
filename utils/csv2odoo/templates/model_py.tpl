{% import "field_macros.tpl" as macro_fields -%}
# -*- coding: utf-8 -*-
##############################################################################
#
#    Grupo de Investigación, Desarrollo e Innovación I+D+I
#    Subdirección de Recursos Tecnológicos - STRT
#    INSTITUTO DE DESARROLLO URBANO - BOGOTA (COLOMBIA)
#    Copyright (C) 2015 IDU STRT I+D+I (http://www.idu.gov.co/)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
from openerp.exceptions import ValidationError

{% for model in module.models if model.namespace == namespace %}
class {{ model.name | replace('.', '_')}}(models.Model):
    _name = '{{ model.name }}'
    _description = '{% if model.description %}{{ model.description }}{% else %}{{ model.name + ' DESCRIPTION PENDING' }}{% endif %}'{{ macro_fields.inheritance(model) }}

    # Fields
    {%- for field in model.fields %}
    {#-
        Llama al macro que tiene el mismo nombre del field.type
        y pasa el field como argumento
    #}
    {{ macro_fields|attr(field.type)(field) }}
    {%- endfor -%}
{%- if model.inherits %}
  {%- for k,v in model.inherits.iteritems() %}
    {{ v }} = fields.Many2one(
        comodel_name="{{ k }}",
        ondelete='restrict',
        required=True,
    )
  {%- endfor %}
{%- endif -%}
    {%- if model.get_unique_fields() %}

    {{ macro_fields.sql_constraints(model) }}
    {%- endif %}
    {%- if model.overwrite_create %}
{{ macro_fields.overwrite_create(model) }}
    {%- endif %}
    {%- if model.overwrite_write %}
{{ macro_fields.overwrite_write(model) }}
    {%- endif %}
    {%- for field in model.fields if field.arguments['compute'] -%}
    {{  macro_fields | attr('compute_method')(field) }}
    {%- endfor %}
    {%- for field in model.fields if field.arguments['constrains'] -%}
    {{  macro_fields | attr('constrains_method')(field) }}
    {%- endfor %}
    {%- for field in model.fields if field.arguments['onchange'] -%}
    {{  macro_fields | attr('onchange_method')(field) }}
    {%- endfor %}
    {%- if model.activities %}

    # Workflow{% endif %}
{%- for activity in model.activities %}
    def wkf_{{ activity.name }}(self):
        self.state = '{{ activity.name }}'
{% endfor %}
{% endfor %}