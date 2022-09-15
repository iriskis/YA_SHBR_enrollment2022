from aiohttp.web_response import Response
from aiohttp_apispec import docs, response_schema

from disk.api.schema import NodeSchema
from disk.db.schema import files_table
from disk.utils.pg import SelectQuery

from disk.api.handlers.base import BaseNodeView
from disk.api.handlers.query import NODES_QUERY


from sqlalchemy import and_, func, select
from disk.db.schema import files_table


class NodesView(BaseNodeView):
    URL_PATH = r'/nodes/{node_id}'

    @docs(summary='Получить информацию об элементе по id и о его вложенных')
    @response_schema(NodeSchema())
    async def get(self):
        await self.check_node_exists()

        nodes_query = select([
            files_table.c.id,
            files_table.c.type,
            files_table.c.url,
            files_table.c.size,
            files_table.c.parent_id,
            files_table.c.update_date
        ]).where(files_table.c.id == self.node_id).cte(recursive=True)

        nodes = nodes_query.alias()
        files = files_table.alias()

        nodes_query = nodes_query.union_all(
            select([
                files.c.id,
                files.c.type,
                files.c.url,
                files.c.size,
                files.c.parent_id,
                files.c.update_date
            ]).where(nodes.c.id == files.c.parent_id)
        )

        statement = select([
            nodes_query.c.id,
            nodes_query.c.type,
            nodes_query.c.url,
            nodes_query.c.size,
            nodes_query.c.parent_id,
            nodes_query.c.update_date
        ])

        body = SelectQuery(statement, self.pg.transaction())
        return Response(body=body)