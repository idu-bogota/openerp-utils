import re

class Model():
    
    def __init__(self, model_of_view, file, options):
        self.model_of_view = model_of_view
        self.file = file
        self.options = options
        
    #excluir del grafico 
    def exclude_of_graphic(self, relacion):
        retorno = True
        entity_to_exclude = self.options.view_exclude.split(',')
        #print entity_to_exclude
        
        for exclude in entity_to_exclude:
            if '*' in exclude:
                #print "{0} {1}".format(relacion, exclude)
                if re.match(exclude, relacion.name):
                    #print "esta en el exclude    {0}".format(relacion)
                    retorno = False
                    return retorno
            else:
                if relacion.name in entity_to_exclude:
                    #print "esta en el exclude    {0}".format(relacion)
                    retorno = False
                    return retorno
        return retorno
        
    #grafica las entida
    def get_plantuml_relation_tags(self):
        for i in self.model_of_view:
            if(i.inherit_id):
                #excluir
                if self.options.view_exclude:
                    if self.exclude_of_graphic(i.inherit_id):
                        self.file.write("{0} <|-- {1}\n".format(i.inherit_id,i.name))
                #fin excluir 
                else:
                    self.file.write("{0} <|-- {1}\n".format(i.inherit_id,i.name))
                    self.file.write("\n")
    # graficar detalle
    def get_plantuml_entity_tags(self):
        for i in self.model_of_view:
            self.file.write("\nclass \"{0}\" << (V,#FF7700) >>{1}\n".format(i.name, "{"))
            self.file.write("    {0}:  {1}\n".format("Tipo de vista",i.type ))
            
            if(self.options.detailed_view  == "1"): # todo los campos
                self.file.write("    {0}:  {1}\n".format("Objeto",i.model ))
                self.file.write("    {0}:  {1}\n".format("Campo Hijo",i.field_parent ))
                self.file.write("    {0}:  {1}\n".format("ID externo",i.xml_id ))
            self.file.write("}\n")
    # fin    