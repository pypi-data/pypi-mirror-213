from typing import Type

from pydantic import create_model
from tortoise import Model

from fastgenerateapi.data_type.data_type import T
from fastgenerateapi.schemas_factory.common_function import get_dict_from_model_fields, get_dict_from_pydanticmeta


def get_one_schema_factory(model_class: Type[Model]) -> Type[T]:
    """
    Is used to create a GetOneSchema
    """
    all_fields_info = get_dict_from_model_fields(model_class)

    include_fields = set()
    exclude_fields = set()
    if hasattr(model_class, "PydanticMeta"):
        if hasattr(model_class.PydanticMeta, "include"):
            include_fields_dict = get_dict_from_pydanticmeta(model_class, model_class.PydanticMeta.include)
            all_fields_info.update(include_fields_dict)
            include_fields.update(include_fields_dict.keys())
        else:
            include_fields.update(all_fields_info.keys())
        if hasattr(model_class.PydanticMeta, "get_one_include"):
            get_one_include_fields_dict = get_dict_from_pydanticmeta(model_class, model_class.PydanticMeta.get_one_include)
            all_fields_info.update(get_one_include_fields_dict)
            include_fields.update(get_one_include_fields_dict.keys())
        if hasattr(model_class.PydanticMeta, "exclude"):
            exclude_fields.update(model_class.PydanticMeta.exclude)
        if hasattr(model_class.PydanticMeta, "get_one_exclude"):
            exclude_fields.update(model_class.PydanticMeta.get_one_exclude)

    all_fields = include_fields.difference(exclude_fields)

    name = model_class.__name__ + "GetOneSchema"
    schema: Type[T] = create_model(__model_name=name, **{field: all_fields_info[field] for field in all_fields})
    return schema



