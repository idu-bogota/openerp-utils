{%- macro one_or_zero(value) -%}
    {%- if value['enabled'] -%}
      1
    {%- else -%}
      0
    {%- endif -%}
{%- endmacro -%}
id,active,name,group_id/id,model_id/id,perm_create,perm_read,perm_write,perm_unlink
{%- for model in module.models if model.namespace == module.namespace %}
{{ model.short_name | replace('.', '_') }}_global,True,"{{ model.name}} global",,{{ module.name }}.model_{{ model.name | replace('.', '_') }},1,0,0,0
{%- endfor -%}
{%- for group in module.groups -%}
{%- for model_name, acl in group.acls.iteritems() %}
{{ acl.model.short_name | replace('.', '_') }}_{{ group.name | replace('.', '_') }},True,"{{ acl.model.name}} {{ group.name }}",,{{ module.name }}.model_{{ acl.model.name | replace('.', '_') }},{{ one_or_zero(acl.create) }},{{ one_or_zero(acl.read) }},{{ one_or_zero(acl.write) }},{{ one_or_zero(acl.delete) }}
{%- endfor -%}
{%- endfor -%}

