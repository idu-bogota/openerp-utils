class Module(object):
    def __init__(self, name):
        self.name = name
        self.models = {}

    def add_model(self, name):
        if not name in self.models:
            self.models[name] = Model(name)
        return self.models[name]

class Model(object):
    def __init__(self, name):
        self.name = name
        self.description = name
        self._inherit = None
        self._inherits = None
        self._attributes = {}

    @property
    def inherit(self):
        return self._inherit

    @inherit.setter
    def inherit(self, v):
        if not self._inherit and v:
            self._inherit = v.split(',')

    @property
    def inherits(self):
        return self._inherits

    @inherits.setter
    def inherits(self, v):
        if not self._inherits and v:
            self._inherits = v.split(',')

    @property
    def attributes(self):
        return self._attributes

    def add_attribute(self, name, line):
        if not name in self._attributes:
            self._attributes[name] = Attribute(name)
        attribute = self._attributes[name]
        attribute.arguments = line
        return attribute


class Attribute(object):
    def __init__(self, name):
        self.name = name
        self._arguments = {}
        self._view_arguments = {}

    def report_error(self, error):
        message = '[{0}] {1}'.format(
            self.name,
            error,
        )
        raise ValueError(message)

    @property
    def arguments(self):
        return self._arguments

    @arguments.setter
    def arguments(self, v):
        params = self._process_generic_parameters(v)
        self._process_arguments_by_type(v, params)
        self._process_view_arguments(v, params)

    _PARAMS_ALLOWED = ['store','related','size','compute']
    def _process_generic_parameters(self, v):
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
            self._arguments[k] = params[k]

        self._arguments['string'] = v.string if 'string' in v and v.string else None
        self._arguments['required'] = True if 'required' in v and v.required else False
        self._arguments['help'] = v.help if 'help' in v and v.help else None
        self._arguments['type'] = v.type
        return params

    def _process_arguments_by_type(self, v, params):
        if v.type in ['text', 'integer', 'float', 'html']:
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
            except ValueError,e:
                self._view_arguments[enabled] = True
                self._view_arguments[param] = v[key]
