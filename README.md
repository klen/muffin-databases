# Muffin-Databases

Async support for a range of databases in the [Muffin](https://github.com/klen/muffin) framework.

[![Tests](https://github.com/klen/muffin-databases/workflows/tests/badge.svg)](https://github.com/klen/muffin-databases/actions)
[![PyPI](https://img.shields.io/pypi/v/muffin-databases)](https://pypi.org/project/muffin-databases/)
[![Python versions](https://img.shields.io/pypi/pyversions/muffin-databases)](https://pypi.org/project/muffin-databases/)

<a id="requirements"></a>
## Requirements

- Python >= 3.11

> **Note:** the plugin supports only the asyncio event loop (not trio).

<a id="installation"></a>
## Installation

```console
$ pip install muffin-databases
```

Optionally install the database drivers:

```console
$ pip install muffin-databases[sqlite]
$ pip install muffin-databases[postgres]
$ pip install muffin-databases[mysql]
```

Driver support comes from one of [asyncpg](https://github.com/MagicStack/asyncpg),
[aiomysql](https://aiomysql.readthedocs.io/en/latest/) or
[aiosqlite](https://github.com/omnilib/aiosqlite).

<a id="usage"></a>
## Usage

Set up the plugin and connect it to your app:

```python
from muffin import Application
from muffin_databases import Plugin as DB

# Create Muffin Application
app = Application("example")

# Initialize the plugin
# As alternative: db = DB(app, **options)
db = DB(url="sqlite:///db.sqlite")
db.setup(app)
```

That's it. Now you can use the plugin inside your views:

```python
@app.route("/items", methods=["GET"])
async def get_items(request):
    """Return a JSON with items from database."""
    rows = await db.fetch_all("SELECT * from items")
    return [dict(row) for row in rows]


@app.route("/items", methods=["POST"])
async def insert_item(request):
    """Store an item into database."""
    data = await request.data()  # parse formdata/json from the request
    await db.execute_many("INSERT INTO items (name, value) VALUES (:name, :value)", values=data)
    return "OK"
```

The plugin is based on [databases](https://www.encode.io/databases/); see its docs for further
references.

## Public API

**`db.database`**: the underlying `databases.Database` instance. Raises `RuntimeError` if the
plugin is not initialized.

Any unknown attribute is proxied to `db.database`, so the whole databases API is available
directly on the plugin: `await db.fetch_all(...)`, `await db.fetch_one(...)`, `db.transaction()`,
`await db.execute_many(...)` and so on.

The plugin manages the connection for you: on application startup it calls `database.connect()`,
on shutdown it calls `database.disconnect()`.

## Options

| Name       | Default value            | Description                 |
| ---------- | ------------------------ | --------------------------- |
| **url**    | `"sqlite:///:memory:"`   | A database connection URL   |
| **params** | `{}`                     | A database connection params |

Unknown options are ignored.

You can provide the options when initializing the plugin:

```python
db.setup(
    app,
    url="postgresql://localhost/example",
    params={"ssl": True, "min_size": 5, "max_size": 20},
)
```

Or set them from the `Muffin.Application` configuration with the `DATABASES_` prefix:

```python
DATABASES_URL = "postgresql://localhost/example"
```

Application configuration options are case insensitive.

Environment variables use the `{APP_NAME}_DATABASES_` prefix (the default application name is
`muffin`):

```console
$ export MUFFIN_DATABASES_URL='postgresql://localhost/example'
```

## Bug tracker

If you have any suggestions, bug reports or annoyances, please report them to the issue tracker
at https://github.com/klen/muffin-databases/issues.

## License

Licensed under the [MIT license](http://opensource.org/licenses/MIT). Development happens at
https://github.com/klen/muffin-databases.
