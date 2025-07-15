from __future__ import annotations


import model
from model import Batch, OrderLine
from repository import AbstractRepository


class InvalidSkuException(Exception):
    pass


def is_valid_sku(sku: str, batches: list[Batch]):
    return sku in {b.sku for b in batches}


def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    sku_is_valid = is_valid_sku(
        sku=line.sku,
        batches=batches,
    )
    if not sku_is_valid:
        raise InvalidSkuException(
            f"Invalid sku {line.sku}"
        )
    batchref = model.allocate(line=line, batches=batches)
    session.commit()
    return batchref