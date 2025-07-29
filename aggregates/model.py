from typing import List

from aggregates.batch import Batch, OrderLine


class OutOfStockException(Exception):
    pass


class Product:
    def __init__(self, sku: str, batches: List[Batch]):
        self.sku = sku
        self.batches = batches

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line=line)
            return batch.reference
        except StopIteration:
            raise OutOfStockException(f"Out of stock for SKU {line.sku}")