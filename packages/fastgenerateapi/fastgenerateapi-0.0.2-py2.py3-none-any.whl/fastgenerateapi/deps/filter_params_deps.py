from typing import Type, Union, Any

from fastapi import Query, Depends
from pydantic import create_model
from pydantic.fields import FieldInfo
from tortoise import Model

from fastgenerateapi.api_view.mixin.base_mixin import BaseMixin
from fastgenerateapi.controller.filter_controller import BaseFilter
from fastgenerateapi.pydantic_utils.base_model import BaseModel, QueryConfig


def filter_params_deps(model_class: Type[Model], fields: list[str, tuple[str, Type], BaseFilter] = None):
    """
        生成filter依赖
    """
    model_fields = {}

    for field_info in fields or []:
        if not isinstance(field_info, BaseFilter):
            field_info = BaseFilter(field_info)
        f = field_info.filter_field
        t = field_info.field_type

        model_fields.update({
            f: (
                Union[t, str],
                FieldInfo(
                    title=f"{f}",
                    default=Query(""),
                    description=f"{BaseMixin._get_field_description(model_class, field_info.model_field)}"
                ))
        })

    filter_params_model: Type[BaseModel] = create_model(__model_name="CommonFilterParams", **model_fields, __config__=QueryConfig)

    def filter_query(filter_params: filter_params_model = Depends(filter_params_model)) -> dict[str, Any]:
        """
            filter 筛选字段依赖
        :param filter_params:
        :return:
        """
        result = filter_params.dict(exclude_none=True)
        return result

    return filter_query
