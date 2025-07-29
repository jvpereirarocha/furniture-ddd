import abc

from aggregates import repository


class AbstractUnitOfWork(abc.ABC):
    products: repository.AbstractProductRepository