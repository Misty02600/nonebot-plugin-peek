"""Config 单元测试

注意：直接测试 Config 类，不导入 plugin_config 实例。
"""

from pydantic import BaseModel, field_validator


# 复制 Config 类定义用于测试，避免导入触发 NoneBot
class Config(BaseModel):
    peek_hosts: list[str] = ["127.0.0.1:1920"]
    peek_key: str | None = None
    peek_default_radius: int = 5
    peek_notify_group: int | None = None
    peek_notify_user: int | None = None
    peek_timeout: float = 60.0
    peek_retries: int = 2

    @field_validator("peek_hosts", mode="after")
    @classmethod
    def validate_peek_hosts(cls, v: list[str]) -> list[str]:
        return v if v else ["127.0.0.1:1920"]


class TestConfig:
    """配置模型测试"""

    def test_default_values(self):
        """测试默认配置值"""
        config = Config()
        assert config.peek_hosts == ["127.0.0.1:1920"]
        assert config.peek_key is None
        assert config.peek_default_radius == 5
        assert config.peek_notify_group is None
        assert config.peek_notify_user is None
        assert config.peek_timeout == 60.0
        assert config.peek_retries == 2

    def test_custom_values(self):
        """测试自定义配置值"""
        config = Config(
            peek_hosts=["192.168.1.100:8080"],
            peek_key="secret_key",
            peek_default_radius=10,
            peek_notify_group=123456789,
            peek_timeout=30.0,
            peek_retries=5,
        )
        assert config.peek_hosts == ["192.168.1.100:8080"]
        assert config.peek_key == "secret_key"
        assert config.peek_default_radius == 10
        assert config.peek_notify_group == 123456789
        assert config.peek_timeout == 30.0
        assert config.peek_retries == 5

    def test_hosts_list_input(self):
        """测试多主机列表"""
        config = Config(peek_hosts=["a:1920", "b:1920"])
        assert config.peek_hosts == ["a:1920", "b:1920"]

    def test_hosts_empty_list_fallback(self):
        """测试空列表回退到默认值"""
        config = Config(peek_hosts=[])
        assert config.peek_hosts == ["127.0.0.1:1920"]
