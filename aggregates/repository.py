import abc
from aggregates import model


class AbstractProductRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, product):
        pass

    @abc.abstractmethod
    def get(self, sku) -> model.Product:
        pass