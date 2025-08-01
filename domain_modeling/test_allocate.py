from domain_modeling.model import Batch, OrderLine, OutOfStockException, allocate
from datetime import date, timedelta
import pytest


def test_prefers_current_stock_batches_to_shipments():
    tomorrow = date.today() + timedelta(days=1)
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)

    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    later = date.today() + timedelta(days=7)
    
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)

    line = OrderLine("order1", "MINIMALIST-SPOON", 10)

    allocate(line, [medium, earliest, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    tomorrow = date.today() + timedelta(days=1)
    in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=tomorrow)

    line = OrderLine("oref", "HIGHBROW-POSTER", 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


def test_raise_out_of_stock_exception_if_cannot_allocate():
    today = date.today()
    batch = Batch("batch1", "SMALL-FORK", 10, eta=today)
    first_order_line = OrderLine("order1", "SMALL-FORK", 10)
    
    allocate(line=first_order_line, batches=[batch])

    with pytest.raises(OutOfStockException, match="SMALL-FORK"):
        second_order_line = OrderLine(
            "order2",
            "SMALL-FORK",
            1
        )
        allocate(line=second_order_line, batches=[batch])