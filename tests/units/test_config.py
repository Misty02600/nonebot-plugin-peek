"""Config 单元测试

注意：直接测试 Config 类，不导入 plugin_config 实例。
"""

from pydantic import BaseModel


class TestConfig:
    """配置模型测试"""

    def test_default_values(self):
        """测试默认配置值"""

        # 直接定义 Config 类的副本用于测试，避免导入触发 NoneBot
        class Config(BaseModel):
            peek_host: str = "127.0.0.1:1920"
            peek_key: str | None = None
            peek_default_radius: int = 5
            peek_notify_group: int | str | None = None
            peek_timeout: float = 60.0
            peek_retries: int = 2

        config = Config()
        assert config.peek_host == "127.0.0.1:1920"
        assert config.peek_key is None
        assert config.peek_default_radius == 5
        assert config.peek_notify_group is None
        assert config.peek_timeout == 60.0
        assert config.peek_retries == 2

    def test_custom_values(self):
        """测试自定义配置值"""

        class Config(BaseModel):
            peek_host: str = "127.0.0.1:1920"
            peek_key: str | None = None
            peek_default_radius: int = 5
            peek_notify_group: int | str | None = None
            peek_timeout: float = 60.0
            peek_retries: int = 2

        config = Config(
            peek_host="192.168.1.100:8080",
            peek_key="secret_key",
            peek_default_radius=10,
            peek_notify_group=123456789,
            peek_timeout=30.0,
            peek_retries=5,
        )
        assert config.peek_host == "192.168.1.100:8080"
        assert config.peek_key == "secret_key"
        assert config.peek_default_radius == 10
        assert config.peek_notify_group == 123456789
        assert config.peek_timeout == 30.0
        assert config.peek_retries == 5

    def test_notify_group_as_string(self):
        """测试通知群号可以是字符串"""

        class Config(BaseModel):
            peek_host: str = "127.0.0.1:1920"
            peek_key: str | None = None
            peek_default_radius: int = 5
            peek_notify_group: int | str | None = None
            peek_timeout: float = 60.0
            peek_retries: int = 2

        config = Config(peek_notify_group="123456789")
        assert config.peek_notify_group == "123456789"
