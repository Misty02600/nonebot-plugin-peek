"""核心工具函数"""

from pathlib import Path


def find_fallback(
    directory: Path, stem: str, extensions: tuple[str, ...]
) -> Path | None:
    """按文件名前缀查找备用资源，返回第一个存在的文件"""
    for ext in extensions:
        path = directory / f"{stem}{ext}"
        if path.exists():
            return path
    return None
