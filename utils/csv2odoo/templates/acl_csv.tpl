id,active,name,group_id/id,model_id/id,perm_create,perm_read,perm_write,perm_unlink
{%- for model in module.models if model.namespace == module.namespace %}
{{ model.short_name | replace('.', '_') }}_global,True,"{{ model.name}} global",,{{ module.name }}.model_{{ model.name | replace('.', '_') }},1,0,0,0
{%- endfor -%}
