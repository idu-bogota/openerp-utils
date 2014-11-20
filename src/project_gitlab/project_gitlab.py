"""
@startuml
Title gitlab integración openerp
class gitlab.issue
class gitlab.milestone
class gitlab.project

class project.task
class project.project

class res.user

gitlab.issue "*" -up- res.user
gitlab.issue "*" -- project.task
gitlab.milestone -- "*" gitlab.issue
gitlab.project -- "*" gitlab.issue
gitlab.issue "*" -- "*" gitlab.label

@enduml


"""
