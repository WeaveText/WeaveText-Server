"""Pydantic 请求/响应模型。"""

from typing import Any

from pydantic import BaseModel, Field


class PlaceholderParseResponse(BaseModel):
    """模板解析响应。"""

    placeholders: list[str] = Field(default_factory=list, description="模板中提取出的占位符列表")


class PlaceholderAnalyzeRequest(BaseModel):
    """占位符分析请求。"""

    placeholders: list[str] = Field(default_factory=list, description="待分析的占位符列表")


class PlaceholderAnalyzeResponse(BaseModel):
    """占位符分析响应。"""

    descriptions: dict[str, str] = Field(
        default_factory=dict,
        description="占位符名称到描述文案的映射",
    )


class RenderRequest(BaseModel):
    """文档渲染请求。"""

    data: dict[str, Any] = Field(default_factory=dict, description="渲染模板所需键值对")
