'''
Created on 21/11/2014

@author: jota
'''
import re
import erppeek

class Model():

    def __init__(self, model, file, options, connection):
        self.model = model
        self.file = file
        self.options = options
        self.connection = connection
    #excluir
    def exclude_of_graphic(self, relacion):
        retorno = True
        
        entity_to_exclude = self.options.model_exclude.split(',')
        
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
    
    #identificar clases wizard
    def is_wizard(self, clase):
        model = self.connection.model('ir.model')
        record_view = model.browse([ "model = {0}".format(clase) ]).osv_memory
        return record_view[0]
    
    #grafica las entida
    def get_plantuml_relation_tags(self):
        for i in self.model:
            campos = self.model[i]
            for key, campo in campos.iteritems():
                
                if campo['type'] == 'many2one':
                    #excluir 
                    if self.options.model_exclude:
                        if self.exclude_of_graphic(campo['relation']):
                            self.file.write("{0} \"*\" -- {1}\n".format(i, campo['relation']))
                    else:
                        self.file.write("{0} \"*\" -- {1}\n".format(i, campo['relation']))
                    #fin excluir
                
                if campo['type'] == 'many2many':
                    try:
                        if campo['m2m_join_table']:
                            self.file.write("{0} \"0..*\" -- \"0..*\" {1}\n".format(i, campo['relation']))
                            self.file.write("({0}, {1}) .. {2} \n".format(i, campo['relation'], campo['m2m_join_table']))
                    except:
                        #print "los que no tienen tabla de cruce"
                        #print "{0}     modelo: {1}".format(key, i)
                        #print campo
                        pass
            self.file.write("\n")
    
    def get_plantuml_entity_tags(self):
        for i in self.model:
            #pintar wizard
            if self.is_wizard(i):
                self.file.write("\nclass {0} << (W,#0ACEB7) >> {1}\n".format(i, "{"))
            else:
                self.file.write("\nclass {0}{1}\n".format(i, "{"))
            # fin pintar wizard
            campos = self.model[i]
            for key, campo in campos.iteritems():
                if campo['type'] == 'many2one':
                    self.file.write("    {0} {1}\n".format(campo['type'], campo['string']))
                 
                if campo['type'] == 'many2many':
                    try:
                        if campo['m2m_join_table']:
                            self.file.write("    {0} {1}\n".format(campo['type'], campo['string']))
                    except:
                        pass
            
            if(self.options.detailed_model  == "1"): # todo los campos
                for key, campo in campos.iteritems():
                    if campo['type'] != 'many2one' and campo['type'] != 'many2many':
                        self.file.write("    {0} {1}\n".format(campo['type'], campo['string']))
            
            self.file.write("}\n")
    # fin        