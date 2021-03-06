-
  CREAR USUARIOS y ASIGNAR GRUPO
{% for group in module.groups %}
-
  !record { model: res.partner, id: {{ group.short_name }}_partner_01 }:
    name: 'u01_{{ group.short_name }}_{{ module.name }}'
    email: '{{ group.short_name }}_user_01@{{ module.name }}.test.com'
-
  !record { model: res.users, id: {{ group.short_name }}_user_01 }:
    name: 'u01_{{ group.short_name }}_{{ module.name }}'
    login: 'u01_{{ group.short_name }}_{{ module.name }}'
    new_password: 'testing'
    partner_id: {{ group.short_name }}_partner_01
    email: '{{ group.short_name }}_user_01@{{ module.name }}.test.com'
-
  !record { model: res.partner, id: {{ group.short_name }}_partner_02 }:
    name: 'u02_{{ group.short_name }}_{{ module.name }}'
    email: '{{ group.short_name }}_user_02@{{ module.name }}.test.com'
-
  !record { model: res.users, id: {{ group.short_name }}_user_02 }:
    name: 'u02_{{ group.short_name }}_{{ module.name }}'
    login: 'u02_{{ group.short_name }}_{{ module.name }}'
    new_password: 'testing'
    partner_id: {{ group.short_name }}_partner_02
    email: '{{ group.short_name }}_user_02@{{ module.name }}.test.com'
-
  !python { model: res.groups }: |
    self.write(cr, uid, ref("{{ group.name }}"), {
        'users':[
            (4, ref('{{ group.short_name }}_user_01')),
            (4, ref('{{ group.short_name }}_user_02')),
        ]
    })
    # All users are employee by default - delete for portal users
    self.write(cr, uid, ref("base.group_user"), {
        'users':[
            (4, ref('{{ group.short_name }}_user_01')),
            (4, ref('{{ group.short_name }}_user_02')),
        ]
    })
{% endfor %}
