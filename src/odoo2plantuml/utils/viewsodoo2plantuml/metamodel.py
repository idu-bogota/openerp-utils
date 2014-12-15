from xml.dom import minidom

class Model():
    
    def __init__(self, model_of_view, file, detailed_model):
        self.model_of_view = model_of_view
        self.file = file
        self.detailed_model = detailed_model

    #grafica las entida
    def get_plantuml_relation_tags(self):
        for i in self.model_of_view:
            if(i.inherit_id):
                self.file.write("{0} <|-- {1}\n".format(i.inherit_id,i.name))
                self.file.write("\n")
    # graficar detalle
    def get_plantuml_entity_tags(self):
        for i in self.model_of_view:
            self.file.write("\nclass {0} << (V,#FF7700) >>{1}\n".format(i.name, "{"))
            self.file.write("    {0}:  {1}\n".format("Tipo de vista",i.type ))
            
            if(self.detailed_model  == "1"): # todo los campos
                self.file.write("    {0}:  {1}\n".format("Objeto",i.model ))
                self.file.write("    {0}:  {1}\n".format("Campo Hijo",i.field_parent ))
                self.file.write("    {0}:  {1}\n".format("ID externo",i.xml_id ))
            self.file.write("}\n")
    # fin    