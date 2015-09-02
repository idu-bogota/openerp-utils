import random
from faker import Factory #pip install fake-factory

class Module(object):
    def __init__(self, name, namespace, string):
        self.name = name
        self.string = string or name
        self._models = {}
        self._groups = {}
        self.namespace = namespace or name

    @property
    def models(self):
        return self._models.values()

    def add_model(self, name):
        if not name in self._models:
            self._models[name] = Model(name, self)
        return self._models[name]

    @property
    def groups(self):
        return self._groups.values()

    def add_group(self, name):
        if not name in self._groups:
            self._groups[name] = Group(name, self)
        return self._groups[name]

    def namespaces(self):
        namespaces = [ m.namespace for m in self.models if m.namespace ]
        return list(set(namespaces))


class Model(object):
    sequence = 0
    def __init__(self, name, module):
        self.name = name
        parts = name.split('.')
        self.namespace = parts[0]
        self._module = module
        self.short_name = '_'.join(parts[1:])
        self._description = None
        self._inherit = None
        self._inherits = None
        self._menu = None
        self._overwrite_create = None
        self._overwrite_write = None
        self._fields = {}
        self._view_configuration = {}

    @property
    def view_configuration(self):
        if not self._view_configuration:
            conf = {
                'create_view': None,
                'extend_view': {},
            }
            if self.namespace == self._module.namespace:
                conf['create_view'] = 'new'
            else:
                conf['create_view'] = 'extend'
                conf['extend_view'] = {
                    'form': [ self.name + '_FORM_ID_CHANGEME', 'name'],
                    'tree': [ self.name + '_TREE_ID_CHANGEME', 'name'],
                    'search': [ self.name + '_SEARCH_ID_CHANGEME', 'name'],
                }
        return self._view_configuration

    @view_configuration.setter
    def view_configuration(self, v):
        """ Process a lines like:
        new # Create new views
        none # Don't create views
        extend # Extend view using defaults
        extend:form=view_id_f|fieldname,tree=view_id_t|fieldname,search=view_id_s|fieldname
        extend:form=view_id_f,tree=view_id_t,search=view_id_s # create just tree and search view
        extend:form=view_id_f # Create just form view
        """
        conf = {
            'create_view': 'new',
            'extend_view': {
                'form': [ self.name.replace('.', '_') + '_FORM_ID_CHANGEME', 'name'],
                'tree': [ self.name.replace('.', '_') + '_TREE_ID_CHANGEME', 'name'],
                'search': [ self.name.replace('.', '_') + '_SEARCH_ID_CHANGEME', 'name'],
            },
        }
        if not self._view_configuration and len(v):
            parts = v.split(':')
            if parts[0].strip().lower() == 'none':
                conf['create_view'] = 'none'
            if parts[0].strip().lower() == 'extend':
                conf['create_view'] = 'extend'
                if len(parts) == 2:
                    extend_parts = parts[1].split(',')
                    extend_view = {}
                    for extend_part in extend_parts:
                        key, values = extend_part.split('=')
                        extend_view[key] = values.split('|')
                        if len(extend_view[key]) == 1:
                            extend_view[key].append('name') #Set field 'name' to extend by default

                    conf['extend_view'] = extend_view
            print conf
            self._view_configuration = conf

    @property
    def description(self):
        if not self._description:
            return self.name
        return self._description

    @description.setter
    def description(self, v):
        if not self._description and len(v):
            self._description = v

    @property
    def module(self):
        return self._module

    @property
    def menu(self):
        if not self._menu:
            return False
        return self._menu

    @menu.setter
    def menu(self, v):
        if not self._menu and v in ['main', 'conf']:
            self._menu = v

    @property
    def inherit(self):
        if not self._inherit:
            return False
        return self._inherit

    @inherit.setter
    def inherit(self, v):
        if not self._inherit and v:
            self._inherit = v.split(',')

    @property
    def inherits(self):
        if not self._inherits:
            return False
        inherits = {}
        for i in self._inherits:
            model_name = i
            field_name = i.replace('.', '_') + '_id'
            inherits[model_name] = field_name
        return inherits

    @inherits.setter
    def inherits(self, v):
        if not self._inherits and v:
            self._inherits = v.split(',')

    @property
    def fields(self):
        return sorted(self._fields.values(), key=lambda x: x.sequence)

    def add_field(self, name, line):
        if not name in self._fields:
            Model.sequence += 1
            self._fields[name] = Field(name, self, Model.sequence)
        field = self._fields[name]
        field.arguments = line
        return field

    def get_view_fields(self, filter_by):
        key = '{0}_enabled'.format(filter_by)
        res = []
        for f in self._fields.values():
            if f.view_arguments[key]:
                res.append(f)
        return sorted(res, key=lambda x: x.sequence)

    def get_unique_fields(self):
        res = []
        for f in self._fields.values():
            if f.arguments['unique']:
                res.append(f)
        return res

    def get_form_tabs(self):
        res = []
        for f in self._fields.values():
            if f.view_arguments['form_tab_enabled']:
                res.append(f.view_arguments['form_tab_param'])
        return list(set(res))

    @property
    def overwrite_create(self):
        return self._overwrite_create

    @overwrite_create.setter
    def overwrite_create(self, v):
        if not self._overwrite_create and v:
            self._overwrite_create = bool(eval(v)) # Convierte 1/0 en True/False

    @property
    def overwrite_write(self):
        return self._overwrite_write

    @overwrite_write.setter
    def overwrite_write(self, v):
        if not self._overwrite_write and v:
            self._overwrite_write = bool(eval(v)) # Convierte 1/0 en True/False

class Field(object):
    def __init__(self, name, model, sequence):
        self.sequence = sequence
        self.name = name
        self.model = model
        self.type = None
        self._arguments = {}
        self._view_arguments = {}

    def report_error(self, error):
        message = '[{0}] {1}'.format(
            self.name,
            error,
        )
        raise ValueError(message)

    @property
    def view_arguments(self):
        return self._view_arguments

    @property
    def arguments(self):
        return self._arguments

    @arguments.setter
    def arguments(self, v):
        params = self._process_generic_parameters(v)
        self._process_arguments_by_type(v, params)
        self._process_view_arguments(v, params)

    _PARAMS_ALLOWED = ['store', 'related', 'size', 'compute', 'domain', 'readonly', 'depends', 'selection', 'default', 'ondelete']
    def _process_generic_parameters(self, v):
        ############################################
        # Process CSV 'params' column
        params = {}
        for i in v.params.split(';'):
            parts = i.split(':')
            if len(parts) == 2:
              params[parts[0]] = parts[1]

        params_allowed = set(self._PARAMS_ALLOWED)
        params_used = set(params.keys())
        if not params_used.issubset(params_allowed):
            self.report_error('Parameters not recognized: {0}'.format(
                params_used - params_allowed,
            ))
        for k in list(params_used):
            if not k in ['size', 'domain', 'selection', 'ondelete']: #params allowed, used but not to be included by default in all fields
                self._arguments[k] = params[k]

        for i in ['depends']:
            self._arguments[i] = params[i].split('|') if i in params and params[i] else None

        ############################################
        # Process parameters with its own CSV column
        self.type = v.type
        self._arguments['type'] = v.type
        for i in ['required', 'onchange', 'unique', 'constrains']:
            if i in v and getattr(v, i):
                self._arguments[i] = bool(eval(getattr(v, i))) # Convierte 1/0 en True/False

        for i in ['help', 'string']:
            self._arguments[i] = getattr(v, i) if i in v and getattr(v, i) else None

        return params

    def _process_arguments_by_type(self, v, params):
        if v.type in ['text', 'integer', 'float', 'html', 'date', 'datetime', 'boolean']:
            pass
        elif v.type == 'selection':
            if 'selection' in params:
                parts = params['selection'].split('|')
                self._arguments['selection'] = [('{}'.format(i).lower().replace(' ','_'), '{}'.format(i)) for i in parts]
            else:
                self._arguments['selection'] = None
        elif v.type == 'char':
            self._arguments['size'] = params['size'] if 'size' in params else 255
        elif v.type in ['many2one', 'many2many']:
            if 'comodel' in v:
                self._arguments['comodel'] = v.comodel
            else:
                self.report_error('"comodel" required on "{0}" field'.format(v.type))

            if len(self._arguments['comodel'].split(',')) > 1:
                self.report_error('No extra params taken on "{0}" comodel:{1}'.format(
                    v.type,
                    v.comodel,
                ))
            self._arguments['domain'] = params['domain'] if 'domain' in params and params['domain'] else None
            self._arguments['ondelete'] = params['ondelete'] if 'ondelete' in params and params['ondelete'] else 'restrict'
        elif v.type == 'one2many':
            if not 'comodel' in v or not v.comodel:
                self.report_error('"comodel" required on "one2many" field')
            self._arguments['comodel'] = v.comodel
            parts = self._arguments['comodel'].split(',')
            if len(parts) > 1:
                self._arguments['comodel'] = parts[0]
                self._arguments['fk_field'] = parts[1]
            else:
                self.report_error('No extra params accepted on "one2many" comodel:{0}'.format(
                    v.comodel
                ))
            self._arguments['domain'] = params['domain'] if 'domain' in params and params['domain'] else None
            self._arguments['ondelete'] = params['ondelete'] if 'ondelete' in params and params['ondelete'] else 'restrict'

    def _process_view_arguments(self, v, params):
        self._set_view_arguments(v, 'tree')
        self._set_view_arguments(v, 'form')
        self._set_view_arguments(v, 'search')
        self._set_view_arguments(v, 'search_group_by')
        self._set_view_arguments(v, 'form_tab')

    def _set_view_arguments(self, v, type):
        enabled = '{0}_enabled'.format(type)
        param = '{0}_param'.format(type)
        key = 'view_{0}'.format(type)
        self._view_arguments[enabled] = None
        self._view_arguments[param] = None
        if key in v and v[key]:
            try:
                self._view_arguments[enabled] = bool(int(v[key]))
            except ValueError, e:
                self._view_arguments[enabled] = True
                self._view_arguments[param] = v[key]

    def generate_value(self):
        fake = Factory.create()
        if self.type in ['integer']:
            return random.randint(0, 100000000)
        elif self.type in ['float']:
            return random.uniform(0, 100000000)
        elif self.type in ['date']:
            return '"{0}"'.format(fake.date())
        elif self.type in ['datetime']:
            return '"{0}"'.format(fake.date_time())
        elif self.type in ['selection']:
            return '"{}"'.format(random.choice(self.arguments['selection'])[0])
        elif self.type in ['many2one', 'one2many', 'many2many']:
            return ''
        else:
            return '"{0}"'.format(fake.sentence())

    def generate_default(self):
        default = self.arguments['default']
        if default == '_CURRENT_USER_':
            return "lambda self: self._context.get('uid', False)"
        elif default == '_CONTEXT_':
            return "lambda self: self._context.get('{0}', None)".format(self.name)
        elif default == '_NOW_' and self.type == 'date':
            return "fields.Date.today"
        elif default == '_NOW_' and self.type == 'datetime':
            return "fields.Datetime.now"
        else:
            return default

class Group(object):
    def __init__(self, name, module):
        self.name = name
        parts = name.split('.')
        self.namespace = parts[0]
        self.short_name = parts[1]
        self.module = module
        self._acls = {}

    @property
    def acls(self):
        return self._acls

    def add_acl(self, model_name, create, read, update, delete):
        if not model_name in self._acls:
            self._acls[model_name] = Acl(self, model_name, create, read, update, delete)
        return self._acls[model_name]

class Acl(object):
    def __init__(self, group, model, create, read, write, delete):
        self._params = {}
        self._model = None
        self.group = group
        self.model = model
        self.create = create
        self.read = read
        self.write = write
        self.delete = delete

    def _set_params(self, operation, v):
        self._params[operation] = {
            'enabled': False,
            'param': None,
        }
        try:
            self._params[operation]['enabled'] = bool(int(v))
        except ValueError, e:
            self._params[operation]['enabled'] = True
            self._params[operation]['param'] = v

    @property
    def params(self):
        return self._params

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, v):
        self._model = self.group.module.add_model(v)

    @property
    def create(self):
        if 'create' in self._params:
            return self._params['create']
        return {'enabled': False, 'param': None}

    @create.setter
    def create(self, v):
        self._set_params('create', v)

    @property
    def read(self):
        if 'read' in self._params:
            return self._params['read']
        return {'enabled': False, 'param': None}

    @read.setter
    def read(self, v):
        self._set_params('read', v)

    @property
    def write(self):
        if 'write' in self._params:
            return self._params['write']
        return {'enabled': False, 'param': None}

    @write.setter
    def write(self, v):
        self._set_params('write', v)

    @property
    def delete(self):
        if 'delete' in self._params:
            return self._params['delete']
        return {'enabled': False, 'param': None}

    @delete.setter
    def delete(self, v):
        self._set_params('delete', v)


    def group_name(self):
        return "{0}.group_{1}".format(
            self.group.namespace,
            self.group.short_name.replace('.', '_'),
        )

    def domain_force(self, action):
        domain = getattr(self, action)['param']
        if domain == '_OWN_':
            return "(['user_id', '=', user.id])"
        elif domain == '_ALL_':
            return "([1, '=', 1])"
        else:
            return "[{0}]".format(domain)