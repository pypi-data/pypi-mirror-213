from typing import Type, Union, Optional

from pydantic import create_model
from pydantic.fields import FieldInfo

from fastgenerateapi.data_type.data_type import T
from fastgenerateapi.pydantic_utils.base_model import BaseModel
from fastgenerateapi.settings.register_settings import settings


def response_factory(schema_cls: Union[Type[T], BaseModel, None], name: str = "") -> Type[T]:
    fields = {
        settings.app_settings.MESSAGE_RESPONSE_FIELD: (str, FieldInfo(default="请求成功", description="返回消息")),
        settings.app_settings.DATA_RESPONSE_FIELD: (schema_cls or dict, FieldInfo(default={}, description="数据内容")),
    }
    if settings.app_settings.CODE_RESPONSE_FIELD:
        default_code_field = FieldInfo(default=200, description="编码")
        fields.setdefault("code", (Optional[int], default_code_field))
    if settings.app_settings.SUCCESS_RESPONSE_FIELD:
        default_success_field = FieldInfo(default=True, description="是否请求成功")
        fields.setdefault("success", (Optional[bool], default_success_field))

    name = schema_cls.__name__ + name + "Response"
    schema: Type[T] = create_model(__model_name=name, **fields)

    return schema








