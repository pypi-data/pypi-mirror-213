from typing import Optional, Type, Union, Any

from fastapi.types import DecoratedCallable
from starlette.requests import Request
from starlette.responses import JSONResponse
from tortoise import Model
from tortoise.transactions import atomic

from fastgenerateapi.api_view.base_view import BaseView
from fastgenerateapi.api_view.mixin.save_mixin import SaveMixin
from fastgenerateapi.data_type.data_type import DEPENDENCIES, CALLABLE
from fastgenerateapi.pydantic_utils.base_model import BaseModel
from fastgenerateapi.schemas_factory import update_schema_factory, get_one_schema_factory, response_factory
from fastgenerateapi.settings.register_settings import settings
from fastgenerateapi.utils.exception import NOT_FOUND


class UpdateView(BaseView, SaveMixin):

    update_schema: Optional[Type[BaseModel]] = None
    update_route: Union[bool, DEPENDENCIES] = True
    """
    update_schema: 修改请求模型
    update_route: 修改路由开关，可以放依赖函数列表
    """

    @atomic()
    async def update(self, pk: str, request_data, *args, **kwargs):
        queryset = self.model_class.filter(
            eval(f"Q({settings.app_settings.WHETHER_DELETE_FIELD}='{settings.app_settings.ACTIVE_DEFAULT_VALUE}')"))
        model = await queryset.filter(id=pk).first()
        if not model:
            raise NOT_FOUND

        request_data = await self.set_update_fields(request_data=request_data, *args, **kwargs)

        await self.check_unique_field(request_data, model_class=self.model_class, model=model)

        model = await self.set_save_model(model=model, request_data=request_data, *args, **kwargs)

        model = await self.set_update_model(model=model, request_data=request_data, *args, **kwargs)

        await model.update_from_dict(request_data.dict(exclude_none=True)).save()

        await self.setattr_model(model, prefetch_related_fields=self.prefetch_related_fields, *args, **kwargs)

        await self.setattr_model_rpc(self.rpc_class, model, self.rpc_param)

        return await self.schema.from_tortoise_orm(model)

    @staticmethod
    async def set_update_fields(request_data, *args, **kwargs):
        """
        修改属性: request_data.user_id = current_user.id
        """
        return request_data

    async def set_update_model(self, model: Model, request_data, *args, **kwargs) -> Model:
        """
        修改属性: model.user_id = current_user.id
        """
        return model

    def _update_decorator(self, *args: Any, **kwargs: Any) -> DecoratedCallable:
        async def route(
                pk: str,
                request_data: self.update_schema,  # type: ignore
                request: Request,
        ) -> JSONResponse:
            data = await self.update(
                pk=pk,
                request_data=request_data,
                request=request,
                *args, **kwargs
            )
            return self.success(data=data)
        return route

    def _handler_update_settings(self):
        self.update_schema = self.update_schema or update_schema_factory(self.model_class)
        if not hasattr(self, "get_one_schema"):
            self.get_one_schema = get_one_schema_factory(model_class=self.model_class)
        if not hasattr(self, "get_one_response_schema"):
            self.get_one_response_schema = response_factory(self.get_one_schema, name="GetOne")

        if self.update_route:
            doc = self.update.__doc__
            summary = doc.strip().split("\n")[0] if doc else f"Update {self.model_class.__name__.title()}"
            path = f"/{settings.app_settings.ROUTER_UPDATE_SUFFIX_FIELD}/{'{pk}'}" if settings.app_settings.ROUTER_WHETHER_ADD_SUFFIX else "/{pk}"
            self._add_api_route(
                path=path,
                endpoint=self._update_decorator(),
                methods=["PUT"],
                response_model=self.get_one_response_schema,
                summary=summary,
                dependencies=self.update_route,
                error_responses=[NOT_FOUND],
            )



