from typing import Type

from pydantic import create_model
from tortoise import Model

from fastgenerateapi.data_type.data_type import T
from fastgenerateapi.schemas_factory.common_function import get_dict_from_model_fields, get_dict_from_pydanticmeta


def update_schema_factory(model_class: Type[Model]) -> Type[T]:
    """
    Is used to create a UpdateSchema
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
        if hasattr(model_class.PydanticMeta, "update_include"):
            get_one_include_fields_dict = get_dict_from_pydanticmeta(model_class, model_class.PydanticMeta.update_include)
            all_fields_info.update(get_one_include_fields_dict)
            include_fields.update(get_one_include_fields_dict.keys())
        if hasattr(model_class.PydanticMeta, "exclude"):
            exclude_fields.update(model_class.PydanticMeta.exclude)
        if hasattr(model_class.PydanticMeta, "update_exclude"):
            exclude_fields.update(model_class.PydanticMeta.update_exclude)

    all_fields = include_fields.difference(exclude_fields)
    try:
        all_fields.remove(model_class._meta.pk_attr)
    except Exception:
        ...

    name = model_class.__name__ + "UpdateSchema"
    schema: Type[T] = create_model(__model_name=name, **{field: all_fields_info[field] for field in all_fields})
    return schema


