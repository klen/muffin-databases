"""Support databases for Muffin framework."""

import typing as t

from databases import Database
from muffin.plugins import BasePlugin


__version__ = "0.3.3"
__project__ = "muffin-databases"
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "MIT"


class Plugin(BasePlugin):

    """Manage databases connections for Muffin."""

    name = 'databases'
    defaults: t.Dict = {
        'params': {},
        'url': 'sqlite:///:memory:',
    }

    def __getattr__(self, name) -> t.Any:
        """Proxy attributes to self database."""
        if not self.installed:
            raise AttributeError(name)

        return getattr(self.__database__, name)

    def setup(self, *args, **options):
        """Initialize a database."""
        super(Plugin, self).setup(*args, **options)

        self.__database__ = Database(self.cfg.url, **self.cfg.params)

    async def startup(self):
        """Disconnect the database."""
        await self.__database__.connect()

    async def shutdown(self):
        """Disconnect the database."""
        await self.__database__.disconnect()
