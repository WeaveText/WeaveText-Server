"""文件辅助工具。"""

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class FileHelper:
    """负责上传文件落盘与临时文件清理。"""

    @staticmethod
    async def save_upload_file(upload_file: UploadFile, temp_dir: Path) -> Path:
        """将上传文件保存到临时目录。"""
        temp_dir.mkdir(parents=True, exist_ok=True)
        suffix = Path(upload_file.filename or "template.docx").suffix
        file_path = temp_dir / f"{uuid4().hex}{suffix}"

        content = await upload_file.read()
        file_path.write_bytes(content)
        await upload_file.close()
        return file_path

    @staticmethod
    def build_output_path(temp_dir: Path, original_name: str) -> Path:
        """构建输出文件路径。"""
        safe_name = Path(original_name).name
        return temp_dir / f"{uuid4().hex}_rendered_{safe_name}"

    @staticmethod
    def remove_file(path: Path) -> None:
        """删除临时文件，不抛出不存在异常。"""
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
