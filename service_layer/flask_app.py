import os
from flask import Flask, request
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import model
import orm
import repository


load_dotenv()

SQL_ALCHEMY_URI = os.getenv("DB_URI", None)

if SQL_ALCHEMY_URI is None:
    raise ValueError("Database URI must have a value")


orm.start_mappers()
get_session = sessionmaker(bind=create_engine(url=SQL_ALCHEMY_URI))

app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    batches = repository.SqlAlchemyRepository(session=session).list()
    line = model.OrderLine(
        orderid=request.json["orderid"],
        sku=request.json["sku"],
        qty=request.json["qty"],
    )
    batchref = model.allocate(line=line, batches=batches)

    return {"batchref": batchref}, 201