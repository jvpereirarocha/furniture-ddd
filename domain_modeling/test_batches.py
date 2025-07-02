from datetime import date

from domain_modeling.model import Batch, OrderLine


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch(ref="batch-001", sku=sku, qty=batch_qty, eta=date.today()),
        OrderLine(orderid="order-123", sku=sku, qty=line_qty)
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line(
        sku="ELEGANT-LAMP",
        batch_qty=20,
        line_qty=2
    )

    assert large_batch.can_allocate(line=small_line)


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line(
        sku="ELEGANT-LAMP",
        batch_qty=2,
        line_qty=20
    )

    assert small_batch.can_allocate(line=large_line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line(
        sku="ELEGANT-LAMP",
        batch_qty=2,
        line_qty=2
    )
    assert batch.can_allocate(line=line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch(
        ref="batch-001",
        sku="UNCOMFORTABLE-CHAIR",
        qty=100,
        eta=None
    )
    different_sku_line = OrderLine(
        orderid="order-123",
        sku="EXPENSIVE-TOASTER",
        qty=10
    )
    assert batch.can_allocate(line=different_sku_line) is False

def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line(
        sku="DECORATIVE-TRINKET",
        batch_qty=20,
        line_qty=2
    )
    batch.deallocate(line=unallocated_line)
    assert batch.available_quantity == 20

def test_allocation_is_idempotent():
    batch, line = make_batch_and_line(
        sku="ANGULAR-DESK",
        batch_qty=20,
        line_qty=2
    )
    batch.allocate(line=line)
    assert batch.available_quantity == 18
    # now, let's try to allocate the same line
    batch.allocate(line=line)
    # the line is already allocated so the batch must have 18 in
    # available_quantity
    assert batch.available_quantity == 18

