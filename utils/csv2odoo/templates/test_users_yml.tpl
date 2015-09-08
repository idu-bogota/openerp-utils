-
  CREAR USUARIOS y ASIGNAR GRUPO
{% for group in module.groups %}
-
  !record { model: res.users, id: {{ group.short_name }}_user_01 }:
    name: '{{ group.short_name }}_user_01'
    login: '{{ group.short_name }}_user_01'
    new_password: 'testing'
-
  !record { model: res.users, id: {{ group.short_name }}_user_02 }:
    name: '{{ group.short_name }}_user_02'
    login: '{{ group.short_name }}_user_02'
    new_password: 'testing'
-
  !python { model: res.groups }: |
    self.write(cr, uid, ref("{{ group.name }}"), {
        'users':[
            (4, ref('{{ group.short_name }}_user_01')),
            (4, ref('{{ group.short_name }}_user_02')),
        ]
    })
{% endfor %}
