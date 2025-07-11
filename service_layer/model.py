from dataclasses import dataclass
from datetime import date
from typing import Optional, Set, NewType


Quantity = NewType("Quantity", int)
Sku = NewType("Sku", str)
Reference = NewType("Reference", str)


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(
        self,
        ref: Reference,
        sku: Sku,
        qty: Quantity,
        eta: Optional[date]
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        # self.available_quantity = qty
        self._purchased_quantity = qty
        self._allocations = set() # type: Set[OrderLine]

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference
    
    def __hash__(self):
        return hash(self.reference)
    
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        if self.can_allocate(line=line):
            self._allocations.add(line)
        # self.available_quantity -= line.qty

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)
    
    @property
    def available_quantity(self) -> int:
        self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine):
        return self.sku == line.sku and self.available_quantity >= line.qty
    

class OutOfStockException(Exception):
    pass


# standalone function for our domain service
def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStockException(
            f"Out of stock for SKU {line.sku}"
        )