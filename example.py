"""Example app."""

import muffin

from muffin_databases import Plugin

app = muffin.Application("example", DATABASES_URL="sqlite:///example.sqlite")
db = Plugin(app)


@app.on_startup
async def init_db():
    """Create a table for the example."""
    await db.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name VARCHAR(100))")


@app.route("/", methods=["GET"])
async def get_items(request):
    """Return a JSON with items from database."""
    rows = await db.fetch_all("SELECT * FROM items")
    return [dict(row) for row in rows]


@app.route("/", methods=["POST"])
async def insert_item(request):
    """Store an item into database."""
    data = await request.data()
    await db.execute_many("INSERT INTO items (name) VALUES (:name)", values=data)
    return "OK"
