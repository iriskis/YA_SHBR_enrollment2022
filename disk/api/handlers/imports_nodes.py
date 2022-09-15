from http import HTTPStatus
from typing import Generator

from aiohttp.web_response import Response
from aiohttp_apispec import docs, request_schema, response_schema
from aiomisc import chunk_list

from disk.api.schema import ImportSchema
from disk.db.schema import files_table
from disk.utils.pg import MAX_QUERY_ARGS

from .base import BaseView


class ImportsView(BaseView):
    URL_PATH = '/imports'

    @classmethod
    def make_files_table_rows(cls, items, update_date) -> Generator:
        """
        Генерирует данные готовые для вставки в таблицу files.
        """
        for item in items:
            yield {
                'update_date': update_date,
                'url': item['url'],
                'id': item['id'],
                'parent_id': item['parentId'],
                'size': item['size'],
                'type': item['type'],
            }


    @docs(summary='Импортирует элементы файловой системы')
    @request_schema(ImportSchema())
    async def post(self):
        # Транзакция требуется чтобы в случае ошибки (или отключения клиента,
        # не дождавшегося ответа) откатить частично добавленные изменения.
        async with self.pg.transaction() as conn:
            items = self.request['data']['items']
            update_date = self.request['data']['updateDate']
            files_rows = self.make_files_table_rows(items, update_date)

            query = files_table.insert()
            await conn.execute(query.values(list(files_rows)))

        return Response(status=HTTPStatus.OK)
