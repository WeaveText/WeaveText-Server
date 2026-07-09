# WeaveText-Server

基于 FastAPI 的无状态服务端骨架，提供 `.docx` 模板解析、占位符分析与文档渲染能力。

## 1) 项目目录结构与职责

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py                        # FastAPI 应用入口与实例初始化
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # v1 路由聚合
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       └── template.py        # 核心路由 (parse, analyze, render)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                  # 环境变量与应用配置
│   │   └── exceptions.py              # 全局异常处理
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py                 # Pydantic 数据模型定义
│   ├── services/
│   │   ├── __init__.py
│   │   └── docx_service.py            # docx 解析与渲染业务逻辑层
│   └── utils/
│       ├── __init__.py
│       └── file_helper.py             # 临时文件读写与清理工具
├── requirements.txt
└── .gitignore
```

## 2) requirements.txt 核心依赖

- `fastapi`: Web API 框架
- `uvicorn[standard]`: ASGI 服务启动
- `python-multipart`: 处理文件上传
- `pydantic` / `pydantic-settings`: 数据校验与配置管理
- `docxtpl`: 按模板渲染 DOCX
- `python-docx`: 读取 DOCX 内容并提取占位符

## 3) 核心接口

- `POST /api/v1/template/parse`：上传模板并提取占位符
- `POST /api/v1/template/analyze`：输入占位符列表并返回描述（当前为 Mock）
- `POST /api/v1/document/render`：上传模板 + JSON 数据并返回渲染后的 docx 文件
