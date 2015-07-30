class Module(object):
    def __init__(self, name, namespace):
        self.name = name
        self._models = {}
        self.namespace = namespace or name

    @property
    def models(self):
        return self._models.values()

    def add_model(self, name):
        if not name in self._models:
            self._models[name] = Model(name, self)
        return self._models[name]

    def namespaces(self):
        namespaces = [ m.namespace for m in self.models ]
        return list(set(namespaces))


class Model(object):
    def __init__(self, name, module):
        self.name = name
        parts = name.split('.')
        self.namespace = parts[0]
        self._module = module
        self.short_name = '_'.join(parts[1:])
        self.description = name
        self._inherit = None
        self._inherits = None
        self._menu = None
        self._fields = {}

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
        return self._fields.values()

    def add_field(self, name, line):
        if not name in self._fields:
            self._fields[name] = Field(name)
        field = self._fields[name]
        field.arguments = line
        return field

    def get_view_fields(self, filter_by):
        key = '{0}_enabled'.format(filter_by)
        res = []
        for f in self._fields.values():
            if f.view_arguments[key]:
                res.append(f)
        return res


class Field(object):
    def __init__(self, name):
        self.name = name
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

    _PARAMS_ALLOWED = ['store', 'related', 'size', 'compute', 'domain', 'readonly', 'depends']
    def _process_generic_parameters(self, v):
        # Process CSV 'params' column
        params = {}
        for i in v.params.split(','):
            parts = i.split('=')
            if len(parts) == 2:
              params[parts[0]] = parts[1]
        params_allowed = set(self._PARAMS_ALLOWED)
        params_used = set(params.keys())

        if not params_used.issubset(params_allowed):
            self.report_error('Parameters not recognized: {0}'.format(
                params_used - params_allowed,
            ))
        for k in list(params_used):
            if not k in ['size', 'domain']: #params allowed, used but not to be included by default in all fields
                self._arguments[k] = params[k]

        # Process parameters with its own CSV column
        self.type = v.type
        self._arguments['type'] = v.type
        for i in ['required', 'onchange', 'unique', 'constrains']:
            if i in v and getattr(v, i):
                self._arguments[i] = bool(eval(getattr(v, i))) # Convierte 1/0 en True/False

        for i in ['help', 'string']:
            self._arguments[i] = getattr(v, i) if i in v and getattr(v, i) else None

        for i in ['depends']:
            self._arguments[i] = params[i].split('|') if i in params and params[i] else None

        return params

    def _process_arguments_by_type(self, v, params):
        if v.type in ['text', 'integer', 'float', 'html', 'date', 'datetime']:
            pass
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
