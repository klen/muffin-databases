"""Support databases for Muffin framework."""

from typing import Any, Mapping

from muffin.plugins import BasePlugin

from databases import Database

__version__ = "0.4.0"
__project__ = "muffin-databases"
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "MIT"


class Plugin(BasePlugin):

    """Manage databases connections for Muffin."""

    name = "databases"
    defaults: Mapping[str, Any] = {
        "params": {},
        "url": "sqlite:///:memory:",
    }

    def __init__(self, *args, **kwargs):
        """Initialize a database."""
        self.__database__ = None
        super(Plugin, self).__init__(*args, **kwargs)

    def setup(self, *args, **options):
        """Initialize a database."""
        super(Plugin, self).setup(*args, **options)

        self.__database__ = Database(self.cfg.url, **self.cfg.params)

    @property
    def database(self):
        """The database property."""
        if self.__database__ is None:
            raise RuntimeError("Plugin is not initialized.")

        return self.__database__

    def __getattr__(self, name: str) -> Any:
        """Proxy attributes to self database."""
        return getattr(self.database, name)

    async def startup(self):
        """Disconnect the database."""
        await self.database.connect()

    async def shutdown(self):
        """Disconnect the database."""
        await self.database.disconnect()
