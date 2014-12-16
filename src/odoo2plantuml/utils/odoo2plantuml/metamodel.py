'''
Created on 21/11/2014

@author: jota
'''
import re

class Model():

    def __init__(self, model, file, detailed_model, model_exclude):
        self.model = model
        self.file = file
        self.detailed_model = detailed_model
        self.model_exclude = model_exclude
    #excluir
    def exclude_of_graphic(self, relacion):
        retorno = True
        
        entity_to_exclude = self.model_exclude.split(',')
        
        for exclude in entity_to_exclude:
            if '*' in exclude:
                if re.match(exclude, relacion):
                    #print "esta en el exclude    {0}".format(relacion)
                    retorno = False
                    return retorno
            else:
                if relacion in entity_to_exclude:
                    #print "esta en el exclude    {0}".format(relacion)
                    retorno = False
                    return retorno
        return retorno
    
    #grafica las entida
    def get_plantuml_relation_tags(self):
        for i in self.model:
            campos = self.model[i]
            for key, campo in campos.iteritems():
                if campo['type'] == 'many2one':
                    #excluir 
                    if self.model_exclude:
                        if self.exclude_of_graphic(campo['relation']):
                            self.file.write("{0} \"*\" -- {1}\n".format(i, campo['relation']))
                    else:
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