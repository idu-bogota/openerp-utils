import re

class Model():
    
    def __init__(self, wkf_acti_tras, file, options, flow_start):
        self.wkf_acti_tras = wkf_acti_tras
        self.file = file
        self.options = options
        self.flow_start = flow_start

    #grafica las transiciones
    def get_plantuml_relation_tags(self):
        self.file.write("[*] --> {0}\n".format(self.flow_start))
        for key, transiciones in self.wkf_acti_tras.iteritems():
            for p in transiciones:
                if self.options.workflow_view == '1':
                    self.file.write("{0} -->  {1} : Signal_{2}_Condition{3}\n".format(p.act_from, p.act_to, p.signal, p.condition))
                else:
                    self.file.write("{0} -->  {1}\n".format(p.act_from, p.act_to))
    # fin    