from typing import Union

from fastgenerateapi.api_view.mixin.response_mixin import ResponseMixin
from fastgenerateapi.data_type.data_type import DEPENDENCIES


class BaseRouter(ResponseMixin):
    def __init__(
            self,
            router_class,
            func_name: str,
            method: str = "POST",
            prefix: str = None,
            dependencies: DEPENDENCIES = None,
            summary: str = None,
    ):
        self.func_name = func_name
        if method.upper() in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            self.method = method.upper()
        else:
            self.error(msg=f"方法 {func_name} 中 {method} 不符合规范")

        if self.method == "GET" and not prefix.endswith("/") and not prefix.endswith("{pk}"):
            prefix += "/"
        self.prefix = prefix

        # if function in ["get_one", "get_all", "create", "update", "update_optional", "destroy", "switch"]:
        #     self.is_new = False
        # else:
        #     self.is_new = True

        self.dependencies = dependencies if dependencies else []
        if summary is None:
            doc = getattr(router_class, func_name).__doc__
            summary = doc.strip().split("\n")[0] if doc else func_name.lstrip("view_").rstrip("_pk").replace("_", " ").title()
        self.summary = summary


class RouterController:

    def __init__(self, router_class, func_name_list):
        self.router_data = []
        for func_name in func_name_list:
            prefix_list = func_name.replace("__", "/").split("_")
            method = prefix_list[1]
            if prefix_list[-1] == "pk":
                prefix = "-".join(prefix_list[2:-1]) + "/{pk}"
            else:
                prefix = "-".join(prefix_list[2:])
            self.router_data.append(BaseRouter(router_class, func_name, method, prefix))
            # self.router_data.setdefault(func_name, BaseRouter(router_class, func_name, method, prefix))

    # def get_summary(self, func_name):
    #
    #     return self.router_data.get(func_name).summary
    #
    # def get_dependencies(self, func_name, default: Union[bool, DEPENDENCIES] = None):
    #     dependencies = [] if default is None or isinstance(default, bool) else default
    #
    #     return dependencies | self.router_data.get(func_name).dependencies

