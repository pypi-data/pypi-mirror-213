from typing import Optional

from pydantic import BaseSettings as PydanticSettings, Field, BaseModel


class AppSettings(PydanticSettings):
    # 分页对应字段以及配置默认值
    CURRENT_PAGE_FIELD: Optional[str] = Field(default='page', description="当前页字段")
    PAGE_SIZE_FIELD: Optional[str] = Field(default='page_size', description="每页数量字段")
    TOTAL_SIZE_FIELD: Optional[str] = Field(default='total', description="统计数量字段")
    DETERMINE_WHETHER_PAGE_FIELD: Optional[str] = Field(default='no_page', description="判断是否分页字段")
    DEFAULT_PAGE_SIZE: Optional[int] = Field(default=10, description="默认每页数量")
    DEFAULT_WHETHER_PAGE: Optional[bool] = Field(default=False, description="默认是否分页")
    DEFAULT_MAX_PAGE_SIZE: Optional[int] = Field(default=200, description="默认最大每页数量")

    # 路由后缀字段是否添加以及配置默认值
    ROUTER_WHETHER_ADD_SUFFIX: Optional[bool] = Field(default=True, description="增删改查路由是否添加后缀")
    ROUTER_CREATE_SUFFIX_FIELD: Optional[str] = Field(default='create', description="创建后缀字段")
    ROUTER_GET_ONE_SUFFIX_FIELD: Optional[str] = Field(default='get-one', description="获取一个后缀字段")
    ROUTER_GET_ALL_SUFFIX_FIELD: Optional[str] = Field(default='get-all', description="获取列表后缀字段")
    ROUTER_UPDATE_SUFFIX_FIELD: Optional[str] = Field(default='update', description="修改后缀字段")
    ROUTER_DELETE_SUFFIX_FIELD: Optional[str] = Field(default='delete', description="删除后缀字段")

    # 数据库字段默认值
    WHETHER_DELETE_FIELD: Optional[str] = Field(default="is_active", description="是否删除字段")
    ACTIVE_DEFAULT_VALUE: Optional[bool] = Field(default=True, description="有效的默认值值")

    # 返回格式字段配置默认值
    CODE_RESPONSE_FIELD: Optional[bool] = Field(default=True, description="code返回字段")
    SUCCESS_RESPONSE_FIELD: Optional[bool] = Field(default=True, description="success返回字段")
    MESSAGE_RESPONSE_FIELD: Optional[str] = Field(default="message", description="消息返回字段")
    DATA_RESPONSE_FIELD: Optional[str] = Field(default="data", description="数据返回字段")
    LIST_RESPONSE_FIELD: Optional[str] = Field(default='list', description="列表页返回字段")

    # GetAll 筛选是否双下划线转单下划线
    FILTER_UNDERLINE_WHETHER_DOUBLE_TO_SINGLE: Optional[bool] = Field(default=True, description="筛选是否双下划线转单下划线")
    SCHEMAS_UNDERLINE_WHETHER_DOUBLE_TO_SINGLE: Optional[bool] = Field(default=True, description="序列化字段是否双下划线转单下划线")

    class Config:
        env_prefix = 'APP_'
        case_sensitive = True


class SettingsModel(BaseModel):
    # 系统配置
    app_settings: AppSettings = AppSettings()









