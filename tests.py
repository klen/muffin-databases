import muffin
import pytest


@pytest.fixture
def app():
    return muffin.Application('example', debug=True)


@pytest.mark.asyncio
async def test_db_sqlite(app, client):
    from muffin_databases import Plugin as DB

    db = DB(app, url='sqlite:///:memory:', params={'force_rollback': True})
    assert db

    await db.connect()
    await db.execute('create table nums (id integer primary key, value integer)')

    @app.route(r'/value/<num:int>')
    async def value(request):
        num = request.path_params['num']
        return await db.fetch_val(f'SELECT {num}')

    res = await client.get('/value/42')
    assert res.status_code == 200
    assert await res.json() == 42

    @app.route(r'/insert/<num:int>')
    async def insert(request):
        num = request.path_params['num']
        return await db.execute(f'insert into nums (value) values ({num})')

    res = await client.get('/insert/10')
    assert res.status_code == 200
    assert await res.json() == 1

    res = await client.get('/insert/20')
    assert res.status_code == 200
    assert await res.json() == 2

    @app.route(r'/select')
    async def select(request):
        rows = await db.fetch_all('SELECT * from nums')
        return [dict(row.items()) for row in rows]

    res = await client.get('/select')
    assert res.status_code == 200
    assert await res.json() == [{'id': 1, 'value': 10}, {'id': 2, 'value': 20}]

    await db.disconnect()


@pytest.mark.asyncio
async def test_example_from_readme(app, client):
    from muffin_databases import Plugin as DB

    db = DB(app, url='sqlite:///:memory:', params={'force_rollback': True})

    await db.connect()
    await db.execute(
        'create table items (id integer primary key, name varchar(100), value integer)')

    @app.route('/items', methods=['GET'])
    async def get_items(request):
        """Return a JSON with items from database."""
        rows = await db.fetch_all('SELECT * from items')
        return [dict(row.items()) for row in rows]

    @app.route('/items', methods=['POST'])
    async def insert_item(request):
        """Store an item into database."""
        data = await request.data()  # parse formdata/json from the request
        await db.execute_many(
            'INSERT INTO items (name, value) VALUES (:name, :value)', values=data)
        return 'OK'

    res = await client.post('/items', json=[
        {'name': 'test1', 'value': 11}, {'name': 'test2', 'value': 22}])
    assert res.status_code == 200

    res = await client.get('/items')
    assert res.status_code == 200
    json = await res.json()
    assert json == [
        {'id': 1, 'name': 'test1', 'value': 11}, {'id': 2, 'name': 'test2', 'value': 22}
    ]

    await db.disconnect()
