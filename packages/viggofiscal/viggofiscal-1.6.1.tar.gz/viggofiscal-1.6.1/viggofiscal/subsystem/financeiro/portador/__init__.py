from viggocore.common import subsystem, controller
from viggofiscal.subsystem.financeiro.portador \
    import resource, manager

subsystem = subsystem.Subsystem(resource=resource.Portador,
                                manager=manager.Manager,
                                controller=controller.CommonController)
