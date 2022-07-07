from marshmallow import validate, Schema
from webargs import fields as webargs_fields
from dynaconf import settings


class PaginateSchema(Schema):
    page = webargs_fields.Integer(default=1,
                                  missing=1,
                                  validate=validate.Range(min=1),
                                  location='query', description='requested page number',
                                  data_key='page_num')
    per_page = webargs_fields.Integer(default=settings.API_DEFAULT_PAGE_SIZE,
                                      missing=settings.API_DEFAULT_PAGE_SIZE,
                                      validate=validate.Range(
                                          min=1,
                                          max=settings.API_MAX_PAGE_SIZE),
                                      location='query', description='number of items per page',
                                      data_key='page_size')
