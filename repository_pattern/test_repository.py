from repository_pattern import model, repository


def insert_order_line(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty)"
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    )
    [[ orderline_id ]] = session.execute(
        "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku",
        dict(orderid="order1", sku="GENERIC-SOFA"),
    )
    return orderline_id


def test_repository_can_save_a_batch(session):
    batch = model.Batch(
        ref="batch1",
        sku="RUSTY-SOAPDISH",
        qty=100,
        eta=None
    )

    repo = repository.SqlAlchemyRepository(session=session)
    repo.add(batch)
    session.commit()

    rows = session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    )
    assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]


def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session=session)
    batch1_id = insert_batch(session=session, ref="batch1")
    insert_batch(session=session, ref="batch2")
    insert_allocation(session=session, order_id=orderline_id, batch_id=batch1_id)

    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = model.Batch(
        ref="batch1",
        sku="GENERIC-SOFA",
        qty=100,
        eta=None
    )
    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        model.OrderLine("order1", "GENERIC-SOFA", 12)
    }