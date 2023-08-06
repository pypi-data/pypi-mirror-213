from typing import Type, Optional, Union, List

from pydantic.fields import FieldInfo
from tortoise import Model
from pydantic import create_model

from fastgenerateapi.data_type.data_type import T
from fastgenerateapi.pydantic_utils.base_model import Config
from fastgenerateapi.schemas_factory.common_function import get_dict_from_model_fields, get_dict_from_pydanticmeta
from fastgenerateapi.settings.register_settings import settings


def get_all_schema_factory(model_class: Type[Model]) -> Optional[Type[T]]:
    """
    Is used to create a GetAllSchema
    """
    if not hasattr(model_class, "PydanticMeta"):
        return None
    if not hasattr(model_class.PydanticMeta, "get_all_include") and not hasattr(model_class.PydanticMeta, "get_all_exclude"):
        return None

    all_fields_info = get_dict_from_model_fields(model_class)

    include_fields = set()
    exclude_fields = set()

    get_all_include_fields_dict = get_dict_from_pydanticmeta(model_class, model_class.PydanticMeta.get_all_include)
    all_fields_info = get_all_include_fields_dict.update(all_fields_info)
    include_fields.update(get_all_include_fields_dict.keys())
    if hasattr(model_class.PydanticMeta, "include"):
        include_fields_dict = get_dict_from_pydanticmeta(model_class, model_class.PydanticMeta.include)
        all_fields_info = include_fields_dict.update(all_fields_info)
        include_fields.update(include_fields_dict.keys())
    else:
        include_fields.update(all_fields_info.keys())

    exclude_fields.update(model_class.PydanticMeta.get_all_exclude)
    if hasattr(model_class.PydanticMeta, "exclude"):
        exclude_fields.update(model_class.PydanticMeta.exclude)

    all_fields = include_fields.difference(exclude_fields)

    name = model_class.__name__ + "GetAllSchema"
    schema: Type[T] = create_model(__model_name=name, **{field: all_fields_info[field] for field in all_fields}, __config__=Config)
    return schema


def get_list_schema_factory(schema_cls: Type[T]) -> Type[T]:
    fields = {
        settings.app_settings.LIST_RESPONSE_FIELD: (Optional[List[schema_cls]], FieldInfo(default=[], description="数据返回")),
    }
    name = schema_cls.__name__ + "GetListSchema"
    schema: Type[T] = create_model(__model_name=name, **fields)
    return schema


def get_page_schema_factory(schema_cls: Type[T]) -> Type[T]:
    fields = {
        settings.app_settings.CURRENT_PAGE_FIELD: (Optional[int], FieldInfo(default=1, description="当前页")),
        settings.app_settings.PAGE_SIZE_FIELD: (Optional[int], FieldInfo(default=settings.app_settings.DEFAULT_PAGE_SIZE, description="每页数量")),
        settings.app_settings.TOTAL_SIZE_FIELD: (Optional[int], FieldInfo(default=0, description="数量总计")),
        settings.app_settings.LIST_RESPONSE_FIELD: (Optional[List[schema_cls]], FieldInfo(default=[], description="数据返回")),
    }
    name = schema_cls.__name__ + "GetPageSchema"
    schema: Type[T] = create_model(__model_name=name, **fields)
    return schema






