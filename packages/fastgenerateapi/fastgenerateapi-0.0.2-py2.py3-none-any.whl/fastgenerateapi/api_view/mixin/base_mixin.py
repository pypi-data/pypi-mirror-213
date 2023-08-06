import inspect
from abc import ABC
from typing import List, Callable, Any, Union, Optional, Generic, Type

from fastapi import APIRouter
from fastapi.types import DecoratedCallable
from starlette.exceptions import HTTPException
from tortoise import Model

from fastgenerateapi.data_type.data_type import DEPENDENCIES, T


class BaseMixin(Generic[T], APIRouter, ABC):

    @staticmethod
    def _get_routes(is_controller_field: bool = False) -> List[str]:
        if is_controller_field:
            return ["get_one_route", "get_all_route", "create_route",
                    "update_route", "delete_route", "switch_route_fields"]
        return ["get_one", "get_all", "create",  "update", "destroy", "switch"]

    @classmethod
    def _get_field_description(cls, model_class: Type[Model], fields: Union[str, list, tuple, set]) -> str:
        if type(fields) == str:
            try:
                if field_info := model_class._meta.fields_map.get(fields):
                    return field_info.description
                elif "__" in fields:
                    field_list = fields.split("__", maxsplit=1)
                    description = ""
                    description += cls._get_field_description(model_class=model_class, fields=field_list[0])
                    description += cls._get_field_description(
                        model_class=cls._get_foreign_key_relation_class(model_class=model_class, field=field_list[0]),
                        fields=field_list[1]
                    )
                    return description
                else:
                    others_description = {
                        "gt": "大于",
                        "gte": "大于等于",
                        "lt": "小于",
                        "lte": "小于等于",
                        "contains": "模糊搜索",
                        "in": "范围"
                    }
                    return others_description.get(fields, "")

            except Exception:
                return fields
        else:
            try:
                description_list = []
                for field in fields:
                    description_list.append(cls._get_field_description(model_class=model_class, fields=field))
                return ",".join(description_list)

            except Exception:
                return ",".join(list(fields))

    @staticmethod
    def _get_foreign_key_relation_class(model_class: Type[Model], field: str) -> Type[Model]:
        module = inspect.getmodule(model_class, inspect.getfile(model_class))
        res_class = getattr(module, model_class._meta.fields_map.get(field).model_name.split(".")[1])
        return res_class

    @staticmethod
    def _get_pk_field(model_class: Type[Model]) -> str:
        try:
            return model_class.describe()["pk_field"]["db_column"]
        except:
            return "id"

    def _get_unique_fields(self, model_class: Type[Model] = None, exclude_pk: bool = True) -> List[str]:
        model_class = model_class or self.model_class
        try:
            if exclude_pk:
                _pk = self._get_pk_field(model_class=model_class)
                return [key for key, value in model_class._meta.fields_map.items() if value.unique and key != _pk]
            return [key for key, value in model_class._meta.fields_map.items() if value.unique]
        except:
            return []

    def _get_unique_together_fields(self, model_class: Model = None) -> tuple:
        model_class = model_class or self.model_class
        try:
            return model_class._meta.unique_together
        except:
            return tuple()

    @classmethod
    def _get_cls_func(cls):
        func_list = inspect.getmembers(cls, inspect.isfunction)
        return [func[0] for func in func_list if func[0].startswith("view_")]

    def _add_api_route(
            self,
            path: str,
            endpoint: Callable[..., Any],
            dependencies: Union[bool, DEPENDENCIES],
            error_responses: Optional[List[HTTPException]] = None,
            **kwargs: Any,
    ) -> None:
        dependencies = [] if isinstance(dependencies, bool) else dependencies
        responses: Any = (
            {err.status_code: {"detail": err.detail} for err in error_responses}
            if error_responses
            else None
        )

        self.add_api_route(
            path, endpoint, dependencies=dependencies, responses=responses, **kwargs
        )

    def api_route(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """Overrides and exiting route if it exists"""
        methods = kwargs["methods"] if "methods" in kwargs else ["GET"]
        self._remove_api_route(path, methods)
        return super().api_route(path, *args, **kwargs)

    def get(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_api_route(path, ["Get"])
        return super().get(path, *args, **kwargs)

    def post(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_api_route(path, ["POST"])
        return super().post(path, *args, **kwargs)

    def put(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_api_route(path, ["PUT"])
        return super().put(path, *args, **kwargs)

    def patch(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_api_route(path, ["PATCH"])
        return super().put(path, *args, **kwargs)

    def delete(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_api_route(path, ["DELETE"])
        return super().delete(path, *args, **kwargs)

    def _remove_api_route(self, path: str, methods: List[str]) -> None:
        methods_ = set(methods)

        for route in self.routes:
            if (
                    route.path == f"{self.prefix}{path}"  # type: ignore
                    and route.methods == methods_  # type: ignore
            ):
                self.routes.remove(route)



