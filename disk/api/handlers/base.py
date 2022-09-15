from aiohttp.web_exceptions import HTTPNotFound
from aiohttp.web_urldispatcher import View
from asyncpgsa import PG
from sqlalchemy import exists, select

from disk.db.schema import files_table


class BaseView(View):
    URL_PATH: str

    @property
    def pg(self) -> PG:
        return self.request.app['pg']


class BaseNodeView(BaseView):
    @property
    def node_id(self):
        return self.request.match_info.get('node_id')

    async def check_node_exists(self):
        query = select([
            exists().where(files_table.c.id == self.node_id)
        ])
        if not await self.pg.fetchval(query):
            raise HTTPNotFound()
