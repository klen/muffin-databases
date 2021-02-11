Muffin-Databases
################

.. _description:

**Muffin-Databases** -- Async support for a range of databases for Muffin_ Framework

.. _badges:

.. image:: https://github.com/klen/muffin-databases/workflows/tests/badge.svg
    :target: https://github.com/klen/muffin-databases/actions
    :alt: Tests Status

.. image:: https://img.shields.io/pypi/v/muffin-databases
    :target: https://pypi.org/project/muffin-databases/
    :alt: PYPI Version

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 3.7

.. note:: The plugin supports only asyncio evenloop (not trio)

.. _installation:

Installation
=============

**Muffin-Databases** should be installed using pip: ::

    $ pip install muffin-databases

Optionally you can install the required database drivers with: ::

    $ pip install muffin-databases[sqlite]
    $ pip install muffin-databases[postgres]
    $ pip install muffin-databases[mysql]

Driver support is provided using one of asyncpg_, aiomysql_, or aiosqlite_.

.. _usage:

Usage
=====

Setup the plugin and connect it into your app:

.. code-block:: python

    from muffin import Application
    from muffin_databases import Plugin as DB

    # Create Muffin Application
    app = Application('example')

    # Initialize the plugin
    # As alternative: db = DB(app, **options)
    db = DB(url='sqlite:///db.sqlite')
    db.setup(app)


That's it now you are able to use the plugin inside your views:

.. code-block:: python

    @app.route('/items', methods=['GET'])
    async def get_items(request):
        """Return a JSON with items from database."""
        rows = await db.fetch_all('SELECT * from items')
        return [dict(row.items()) for row in rows]

    @app.route('/items', methods=['POST'])
    async def insert_item(request):
        """Store an item into database."""
        data = await request.data()  # parse formdata/json from the request
        await db.execute_many('INSERT INTO items (name, value) VALUES (:name, :value)', values=data)
        return 'OK'

The Muffin-Databases plugin is based on databases_. See the databases_'s docs for further references.


Options
-------

=========================== ======================================= =========================== 
Name                        Default value                           Desctiption
--------------------------- --------------------------------------- ---------------------------
**url**                     ``"sqlite:///db.sqlite"``               A database connection URL
**params**                  ``{}``                                  A database connection params
=========================== ======================================= =========================== 


You are able to provide the options when you are initiliazing the plugin:

.. code-block:: python

    db.setup(app, url='postgresql://localhost/example', params={'ssl': True, 'min_size': 5, 'max_size': 20})

Or setup it from ``Muffin.Application`` configuration using the ``DATABASES_`` prefix:

.. code-block:: python

   DATABASES_URL = 'postgresql://localhost/example'

``Muffin.Application`` configuration options are case insensitive

.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/muffin-databases/issues

.. _contributing:

Contributing
============

Development of Muffin-Databases happens at: https://github.com/klen/muffin-databases


Contributors
=============

* klen_ (Kirill Klenov)

.. _license:

License
========

Licensed under a `MIT license`_.

.. _links:


.. _klen: https://github.com/klen
.. _Muffin: https://github.com/klen/muffin

.. _asyncpg: https://github.com/MagicStack/asyncpg 
.. _aiomysql: https://aiomysql.readthedocs.io/en/latest/
.. _aiosqlite: https://github.com/omnilib/aiosqlite
.. _databases: https://www.encode.io/databases/

.. _MIT license: http://opensource.org/licenses/MIT
