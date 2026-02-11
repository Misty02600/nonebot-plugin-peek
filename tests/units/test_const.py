"""常量定义测试

使用 fixture 加载 const 模块。
"""


class TestConstants:
    """常量测试"""

    def test_message_constants(self, const_module):
        """测试消息常量存在"""
        assert const_module.MSG_401 is not None
        assert const_module.MSG_403 is not None
        assert const_module.MSG_ERROR is not None

    def test_message_content(self, const_module):
        """测试消息内容"""
        assert "ダメ" in const_module.MSG_401
        assert "正在" in const_module.MSG_403

    def test_fallback_stems(self, const_module):
        """测试备用资源前缀常量"""
        assert const_module.FALLBACK_401 == "401"
        assert const_module.FALLBACK_403 == "403"
        assert const_module.FALLBACK_ERROR == "error"

    def test_supported_extensions(self, const_module):
        """测试支持的文件扩展名"""
        assert ".jpg" in const_module.IMAGE_EXTENSIONS
        assert ".png" in const_module.IMAGE_EXTENSIONS
        assert ".wav" in const_module.AUDIO_EXTENSIONS
        assert ".mp3" in const_module.AUDIO_EXTENSIONS
