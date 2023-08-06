from viggocore.common.subsystem import operation
from viggocore.common.subsystem.pagination import Pagination
from viggocore.common import manager

from viggofiscal.subsystem.financeiro.portador.resource import Portador


class List(operation.List):

    def do(self, session, **kwargs):

        query = session.query(Portador)

        query = self.manager.apply_filters(query, Portador, **kwargs)
        query = query.distinct()

        total_rows = None
        if self.manager.with_pagination(**kwargs):
            total_rows = query.count()

        pagination = Pagination.get_pagination(Portador, **kwargs)
        if pagination.order_by is not None:
            pagination.adjust_order_by(Portador)
        query = self.driver.apply_pagination(query, pagination)
        result = query.all()

        return (result, total_rows)


class Manager(manager.CommonManager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.list = List(self)
