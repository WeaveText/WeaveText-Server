"""模板相关 API 端点。"""

import json
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, Form, UploadFile
from fastapi.responses import FileResponse
from pydantic import ValidationError

from app.core.config import get_settings
from app.core.exceptions import AppException
from app.models.schemas import (
    PlaceholderAnalyzeRequest,
    PlaceholderAnalyzeResponse,
    PlaceholderParseResponse,
    RenderRequest,
)
from app.services.docx_service import DocxService
from app.utils.file_helper import FileHelper

router = APIRouter()
docx_service = DocxService()
settings = get_settings()


@router.post("/template/parse", response_model=PlaceholderParseResponse)
async def parse_template(template_file: UploadFile = File(...)) -> PlaceholderParseResponse:
    """
    解析上传的 DOCX 模板并提取占位符。
    """
    if not template_file.filename or not template_file.filename.endswith(".docx"):
        raise AppException("仅支持上传 .docx 模板文件", status_code=400)

    input_path: Path = await FileHelper.save_upload_file(template_file, settings.temp_dir)
    try:
        placeholders = docx_service.extract_placeholders_from_docx(input_path)
        return PlaceholderParseResponse(placeholders=placeholders)
    finally:
        FileHelper.remove_file(input_path)


@router.post("/template/analyze", response_model=PlaceholderAnalyzeResponse)
async def analyze_placeholders(
    payload: PlaceholderAnalyzeRequest,
) -> PlaceholderAnalyzeResponse:
    """
    根据占位符列表生成描述（当前为 Mock 逻辑）。
    """
    descriptions = docx_service.generate_placeholder_descriptions(payload.placeholders)
    return PlaceholderAnalyzeResponse(descriptions=descriptions)


@router.post("/document/render")
async def render_document(
    background_tasks: BackgroundTasks,
    template_file: UploadFile = File(...),
    data_json: str = Form(..., description="JSON 字符串，示例：{\"name\":\"Alice\"}"),
) -> FileResponse:
    """
    接收模板文件和 JSON 数据并渲染输出 DOCX。

    说明：文件上传与 JSON 同时传递时，使用 multipart/form-data，
    因此 JSON 数据以字符串表单字段传入后再进行校验。
    """
    if not template_file.filename or not template_file.filename.endswith(".docx"):
        raise AppException("仅支持上传 .docx 模板文件", status_code=400)

    try:
        parsed_data = json.loads(data_json)
        render_request = RenderRequest(data=parsed_data)
    except json.JSONDecodeError as exc:
        raise AppException("data_json 不是合法的 JSON 字符串", status_code=400) from exc
    except ValidationError as exc:
        raise AppException(f"渲染数据校验失败: {exc}", status_code=422) from exc

    input_path: Path = await FileHelper.save_upload_file(template_file, settings.temp_dir)
    output_path: Path = FileHelper.build_output_path(settings.temp_dir, template_file.filename)
    try:
        docx_service.render_docx_template(input_path, render_request.data, output_path)
    finally:
        FileHelper.remove_file(input_path)

    background_tasks.add_task(FileHelper.remove_file, output_path)

    return FileResponse(
        path=str(output_path),
        media_type=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
        filename=f"rendered_{template_file.filename}",
    )
