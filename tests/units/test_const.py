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
        assert const_module.MSG_CHECK_OK is not None
        assert const_module.MSG_CHECK_FAIL is not None

    def test_message_content(self, const_module):
        """测试消息内容"""
        assert "ダメ" in const_module.MSG_401
        assert "正在" in const_module.MSG_403

    def test_fallback_filenames(self, const_module):
        """测试备用文件名常量"""
        assert const_module.FALLBACK_401 == "401.jpg"
        assert const_module.FALLBACK_403 == "403.jpg"
        assert const_module.FALLBACK_ERROR == "error.jpg"
        assert const_module.FALLBACK_403_AUDIO == "403.wav"
        assert const_module.FALLBACK_ERROR_AUDIO == "error.wav"

    def test_fallback_extensions(self, const_module):
        """测试备用文件扩展名正确"""
        # 图片文件应该是 .jpg
        assert const_module.FALLBACK_401.endswith(".jpg")
        assert const_module.FALLBACK_403.endswith(".jpg")
        assert const_module.FALLBACK_ERROR.endswith(".jpg")

        # 音频文件应该是 .wav
        assert const_module.FALLBACK_403_AUDIO.endswith(".wav")
        assert const_module.FALLBACK_ERROR_AUDIO.endswith(".wav")
