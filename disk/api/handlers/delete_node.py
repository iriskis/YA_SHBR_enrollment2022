from aiohttp.web_response import Response
from aiohttp_apispec import docs, response_schema

from disk.api.schema import NodeSchema
from disk.db.schema import files_table
from disk.utils.pg import SelectQuery

from disk.api.handlers.base import BaseNodeView
from disk.api.handlers.query import NODES_QUERY


from sqlalchemy import and_, func, select, delete
from disk.db.schema import files_table
from http import HTTPStatus


class DeleteNodeView(BaseNodeView):
    URL_PATH = r'/delete/{node_id}'

    @docs(summary='Удалить элемент по идентификатору')
    async def delete(self):
        await self.check_node_exists()
        # Транзакция требуется чтобы в случае ошибки (или отключения клиента,
        # не дождавшегося ответа) откатить частично добавленные изменения.
        async with self.pg.transaction() as conn:
            query = files_table.delete().where(files_table.c.id==self.node_id)
            await conn.execute(query)

        return Response(status=HTTPStatus.OK)