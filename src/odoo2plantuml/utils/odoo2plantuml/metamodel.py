'''
Created on 21/11/2014

@author: jota
'''

class Model():

    def __init__(self, model, file, detailed_model):
        self.model = model
        self.file = file
        self.detailed_model = detailed_model
    #grafica las entida
    def get_plantuml_relation_tags(self):
        for i in self.model:
            # print i
            # print self.model[i]
            campos = self.model[i]
            for key, campo in campos.iteritems():
                if campo['type'] == 'many2one':
                    self.file.write("{0} \"*\" -- {1}\n".format(i, campo['relation']))
            self.file.write("\n")
    
    def get_plantuml_entity_tags(self):
        for i in self.model:
            # print i
            # print self.model[i]
            self.file.write("\nclass {0}{1}\n".format(i, "{"))
            campos = self.model[i]
            for key, campo in campos.iteritems():
                if campo['type'] == 'many2one':
                    self.file.write("    {0} {1}\n".format(campo['type'], campo['string']))
            
            if(self.detailed_model  == "1"): # todo los campos
                for key, campo in campos.iteritems():
                    if campo['type'] != 'many2one':
                        self.file.write("    {0} {1}\n".format(campo['type'], campo['string']))
            
            self.file.write("}\n")
    # fin        