"""
Модуль содержит схемы для валидации данных в запросах и ответах.

Схемы валидации запросов используются в бою для валидации данных отправленных
клиентами.

Схемы валидации ответов *ResponseSchema используются только при тестировании,
чтобы убедиться что обработчики возвращают данные в корректном формате.
"""
from datetime import date

from marshmallow import Schema, ValidationError, validates, validates_schema
from marshmallow.fields import DateTime, Dict, Int, List, Nested, Str, UUID, Url
from marshmallow.validate import Length, OneOf, Range

from disk.db.schema import FileType

DATE_FORMAT = ''

class ImportNodeSchema(Schema):

    type = Str(
        validate=OneOf([type.value for type in FileType]),
        required=True
    )
    url = Str(validate=Length(min=0, max=256))
    id = UUID(strict=True, required=True)
    parentId = UUID(allow_none=True, required=True)
    size = Int(validate=Range(min=1))


class ImportSchema(Schema):
    items = Nested(ImportNodeSchema, many=True, required=True,
                      validate=Length(max=10000))
    updateDate = DateTime(required=True)


class NodeSchema(Schema):

    id = UUID(strict=True, required=True)
    url = Str(validate=Length(min=0, max=256))
    type = Str(
        validate=OneOf([type.value for type in FileType]),
        required=True
    )
    parentId = UUID(required=False)
    update_date = DateTime()
    size = Int(validate=Range(min=0), required=True)


class NodeResponseSchema(Schema):
    data = Nested(NodeSchema(), required=True)


class ErrorSchema(Schema):
    code = Str(required=True)
    message = Str(required=True)
    fields = Dict()


class ErrorResponseSchema(Schema):
    error = Nested(ErrorSchema(), required=True)
