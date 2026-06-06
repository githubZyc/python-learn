"""
结构化输出
可以请求模型以匹配给定架构的格式提供其响应。
这对于确保输出易于解析并用于后续处理非常有用。
LangChain 支持多种架构类型和强制执行结构化输出的方法。


"""
from agent.learn_01.learn_chat_model_1 import model

"""
Pydantic
Pydantic 模型 提供最丰富的功能集，包括字段验证、描述和嵌套结构。
"""
from pydantic import BaseModel, Field

# class Movie(BaseModel):
#     """一部带有详细信息的电影。"""
#     title: str = Field(..., description="电影标题")
#     year: int = Field(..., description="电影上映年份")
#     director: str = Field(..., description="电影导演")
#     rating: float = Field(..., description="电影评分，满分 10 分")
#
# model_with_structure = model.with_structured_output(Movie)
# print("f model_with_structure {model_with_structure} ",model_with_structure)
# response = model_with_structure.invoke("提供关于电影《盗梦空间》的详细信息")
# print(response)
# Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8.8)

"""
TypedDict
TypedDict 提供使用 Python 内置类型的更简单替代方案，适用于不需要运行时验证的情况。
"""
# from typing_extensions import TypedDict,Annotated
# class MovieDict(TypedDict):
#     """一部带有详细信息的电影。"""
#     title: Annotated[str, ..., "电影标题"]
#     year: Annotated[int, ..., "电影上映年份"]
#     director: Annotated[str, ..., "电影导演"]
#     rating: Annotated[float, ..., "电影评分，满分 10 分"]
#
# model_with_structure = model.with_structured_output(MovieDict)
# response = model_with_structure.invoke("提供关于电影《盗梦空间》的详细信息")
# print(response)

"""
JSON Schema
为了获得最大控制或互操作性，您可以提供原始 JSON 架构。
"""

import json

json_schema = {
    "title": "Movie",
    "description": "一部带有详细信息的电影",
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "电影标题"
        },
        "year": {
            "type": "integer",
            "description": "电影上映年份"
        },
        "director": {
            "type": "string",
            "description": "电影导演"
        },
        "rating": {
            "type": "number",
            "description": "电影评分，满分 10 分"
        }
    },
    "required": ["title", "year", "director", "rating"]
}

model_with_structure = model.with_structured_output(
    json_schema,
    method="json_schema",
)
response = model_with_structure.invoke("提供关于电影《盗梦空间》的详细信息")
print(response)  # {'title': 'Inception', 'year': 2010, ...}
