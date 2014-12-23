#!/usr/bin/python
# -*- coding: utf-8 -*-
class Model():
    
    def __init__(self, wkf_acti_tras, file, options, flow_start, flow_stop):
        self.wkf_acti_tras = wkf_acti_tras
        self.file = file
        self.options = options
        self.flow_start = flow_start
        self.flow_stop = flow_stop

    def get_plantuml_relation_tags_flow_stop(self):
        for i in self.flow_stop:
            self.file.write("{0} --> [*]\n".format(i))
    #grafica las transiciones
    def get_plantuml_relation_tags(self):
        self.file.write("[*] --> {0}\n".format(self.flow_start))
        for key, transiciones in self.wkf_acti_tras.iteritems():
            for p in transiciones:
                self.file.write("{0} -->  {1} : ({2})\n".format(p.act_from, p.act_to, p.id))
        self.get_plantuml_relation_tags_flow_stop()
                
    def get_plantuml_entity_tags(self, wkf_activity):
        self.file.write("\n")
        for i in wkf_activity:
            if i.action_id:
                self.file.write("{0}: action_id : {1}\n".format(i.name, i.action_id))
                self.file.write("{0}: action : {1}\n".format(i.name, i.action))
            else:
                self.file.write("{0}: action : {1}\n".format(i.name, i.action))
    
    def get_plantuml_note_tags(self):
        self.file.write("\n")
        list = []
        self.file.write("note as AA\n")
        for key, transiciones in self.wkf_acti_tras.iteritems():
            #print "key: {0}    transiciones: {1}\n".format(key, transiciones)
            for p in transiciones:
                list.append([p.id, p.group_id, p.condition, p.signal])
        #ordenar
        orden = sorted(list)
        for p in orden:
            self.file.write("    ({0}) Señal : {1}\n".format(p[0], p[3]))
            self.file.write("          Grupo de seguridad : {0}\n".format(p[1]))
            self.file.write("          Condición : {0}\n".format(p[2]))
        self.file.write("end note\n")
        
    # fin    