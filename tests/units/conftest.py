"""单元测试配置

为单元测试提供 pytest 配置。

重要：单元测试直接测试独立模块，不触发 __init__.py 的导入链。
使用 importlib 直接加载模块文件。
"""

import importlib.util
import sys
from pathlib import Path

import pytest

# 项目 src 目录
SRC_DIR = Path(__file__).parent.parent.parent / "src" / "nonebot_plugin_peek"


def load_module_directly(module_name: str, file_name: str):
    """直接加载模块，绕过 __init__.py"""
    file_path = SRC_DIR / file_name
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def service_module():
    """加载 service 模块"""
    return load_module_directly("_test_service", "service.py")


@pytest.fixture(scope="session")
def const_module():
    """加载 const 模块"""
    return load_module_directly("_test_const", "const.py")
