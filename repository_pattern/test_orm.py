from repository_pattern import model

def test_orderline_mapper_can_load_lines(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES "
        '("order1", "RED-CHAIR", 12),'
        '("order1", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14),'
    )

    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-TABLE", 13),
        model.OrderLine("order2", "BLUE-LIPSTICK", 14)
    ]

    assert session.query(model.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = model.OrderLine(
        orderid="order1",
        sku="DECORATIVE-WIDGET",
        qty=12
    )
    session.add(new_line)
    session.commit()

    rows = list(
        session.execute('SELECT orderid, sku, qty FROM "order_lines"')
    )
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]
