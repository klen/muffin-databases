"""Support databases for Muffin framework."""

from typing import Any, ClassVar

from databases import Database
from muffin import Application
from muffin.plugins import BasePlugin


class Plugin(BasePlugin):
    """Manage databases connections for Muffin."""

    name = "databases"
    defaults: ClassVar = {
        "params": {},
        "url": "sqlite:///:memory:",
    }

    def __init__(self, *args, **kwargs):
        """Initialize a database."""
        self.__database__: Database | None = None
        super(Plugin, self).__init__(*args, **kwargs)

    def setup(self, app: Application, *, name: str | None = None, **options) -> bool:
        """Initialize a database."""
        res = super(Plugin, self).setup(app, name=name, **options)

        self.__database__ = Database(self.cfg.url, **self.cfg.params)
        return res

    @property
    def database(self):
        """The database property."""
        if self.__database__ is None:
            raise RuntimeError("Plugin is not initialized.")

        return self.__database__

    def __getattr__(self, name: str) -> Any:
        """Proxy attributes to self database."""
        if name == "middleware":
            return object.__getattribute__(self, name)

        return getattr(self.database, name)

    async def startup(self):
        """Disconnect the database."""
        await self.database.connect()

    async def shutdown(self):
        """Disconnect the database."""
        await self.database.disconnect()
