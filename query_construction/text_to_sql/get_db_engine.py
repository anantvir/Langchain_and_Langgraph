from langchain_community.utilities import SQLDatabase
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import requests

def get_engine_for_chinook_db():
    """Pull sql file, populate in-memory database, and create engine."""
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text

    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

# engine = get_engine_for_chinook_db()

# db = SQLDatabase(engine)

# print(db.dialect)
# print(db.get_usable_table_names())

# #print(db.run("SELECT * FROM Artist LIMIT 10;"))