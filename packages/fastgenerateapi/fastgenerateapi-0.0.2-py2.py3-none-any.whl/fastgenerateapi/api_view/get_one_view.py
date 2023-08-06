from typing import Any, Union, Optional, Type

from fastapi.types import DecoratedCallable
from starlette.requests import Request
from starlette.responses import JSONResponse
from tortoise import Model

from fastgenerateapi.api_view.base_view import BaseView
from fastgenerateapi.api_view.mixin.get_mixin import GetMixin
from fastgenerateapi.data_type.data_type import CALLABLE, DEPENDENCIES
from fastgenerateapi.pydantic_utils.base_model import BaseModel
from fastgenerateapi.schemas_factory import get_one_schema_factory, response_factory
from fastgenerateapi.settings.register_settings import settings
from fastgenerateapi.utils.exception import NOT_FOUND


class GetOneView(BaseView, GetMixin):

    get_one_route: Union[bool, DEPENDENCIES] = True
    get_one_schema: Optional[Type[BaseModel]] = None
    """
    get_one_route: 获取详情路由开关，可以放依赖函数列表
    get_one_schema: 返回序列化
        优先级：  
            - get_one_schema：参数传入
            - get_one_schema_factory：数据库模型自动生成
                - 优选模型层get_one_include和get_one_exclude(同时存在交集)
                - 合并模型层include和exclude(同时存在交集)
                - 模型层所有字段
    """

    async def get_one(self, pk: str, *args, **kwargs) -> Union[BaseModel, dict, None]:
        model = await self.get_object(pk)

        await self.setattr_model(model, prefetch_related_fields=self.prefetch_related_fields, *args, **kwargs)

        # await self.setattr_model_rpc(self.rpc_class, model, self.rpc_param)
        await self.set_get_model(model)

        return await self.get_one_schema.from_tortoise_orm(model)

    def _get_one_decorator(self, *args: Any, **kwargs: Any) -> DecoratedCallable:
        async def route(
                pk: str,
                request: Request,
        ) -> JSONResponse:
            data = await self.get_one(
                pk=pk,
                request=request,
                *args, **kwargs
            )
            return self.success(data=data)
        return route

    def _handler_get_one_settings(self):

        self.get_one_schema = self.get_one_schema or get_one_schema_factory(model_class=self.model_class)
        self.get_one_response_schema = response_factory(self.get_one_schema, name="GetOne")

        if self.get_one_route:
            doc = self.get_one.__doc__
            summary = doc.strip().split("\n")[0] if self.get_one.__doc__ else "Get One"
            path = f"/{settings.app_settings.ROUTER_GET_ONE_SUFFIX_FIELD}/{'{pk}'}" if settings.app_settings.ROUTER_WHETHER_ADD_SUFFIX else "/{pk}"
            self._add_api_route(
                path=path,
                endpoint=self._get_one_decorator(),
                methods=["GET"],
                response_model=self.get_one_response_schema,
                summary=summary,
                dependencies=self.get_one_route,
                error_responses=[NOT_FOUND],
            )










