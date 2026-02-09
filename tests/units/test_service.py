"""PeekAPIClient 单元测试

测试 service 模块中的纯 Python 逻辑，不依赖网络请求。
"""


class TestStatusCode:
    """StatusCode 枚举测试"""

    def test_status_codes(self, service_module):
        """测试状态码值"""
        StatusCode = service_module.StatusCode
        assert StatusCode.OK == 200
        assert StatusCode.UNAUTHORIZED == 401
        assert StatusCode.FORBIDDEN == 403
        assert StatusCode.ERROR == 500

    def test_status_code_names(self, service_module):
        """测试状态码名称"""
        StatusCode = service_module.StatusCode
        assert StatusCode.OK.name == "OK"
        assert StatusCode.UNAUTHORIZED.name == "UNAUTHORIZED"
        assert StatusCode.FORBIDDEN.name == "FORBIDDEN"
        assert StatusCode.ERROR.name == "ERROR"


class TestAPIResponse:
    """APIResponse 数据类测试"""

    def test_default_content(self, service_module):
        """测试默认 content 为 None"""
        APIResponse = service_module.APIResponse
        StatusCode = service_module.StatusCode

        response = APIResponse(status=StatusCode.OK)
        assert response.status == StatusCode.OK
        assert response.content is None

    def test_with_content(self, service_module):
        """测试带 content 的响应"""
        APIResponse = service_module.APIResponse
        StatusCode = service_module.StatusCode

        content = b"image data"
        response = APIResponse(status=StatusCode.OK, content=content)
        assert response.status == StatusCode.OK
        assert response.content == content

    def test_error_response(self, service_module):
        """测试错误响应"""
        APIResponse = service_module.APIResponse
        StatusCode = service_module.StatusCode

        response = APIResponse(status=StatusCode.ERROR)
        assert response.status == StatusCode.ERROR
        assert response.content is None


class TestPeekAPIClient:
    """PeekAPIClient 同步逻辑测试"""

    def test_normalize_url_without_protocol(self, service_module):
        """测试 URL 规范化：无协议"""
        PeekAPIClient = service_module.PeekAPIClient
        assert PeekAPIClient._normalize_url("127.0.0.1:1920") == "http://127.0.0.1:1920"

    def test_normalize_url_with_http(self, service_module):
        """测试 URL 规范化：有 http"""
        PeekAPIClient = service_module.PeekAPIClient
        assert (
            PeekAPIClient._normalize_url("http://127.0.0.1:1920")
            == "http://127.0.0.1:1920"
        )

    def test_normalize_url_with_https(self, service_module):
        """测试 URL 规范化：有 https"""
        PeekAPIClient = service_module.PeekAPIClient
        assert (
            PeekAPIClient._normalize_url("https://example.com") == "https://example.com"
        )

    def test_normalize_url_with_port(self, service_module):
        """测试 URL 规范化：带端口"""
        PeekAPIClient = service_module.PeekAPIClient
        assert (
            PeekAPIClient._normalize_url("192.168.1.100:8080")
            == "http://192.168.1.100:8080"
        )

    def test_normalize_url_hostname_only(self, service_module):
        """测试 URL 规范化：仅主机名"""
        PeekAPIClient = service_module.PeekAPIClient
        assert PeekAPIClient._normalize_url("localhost") == "http://localhost"

    def test_client_initialization(self, service_module):
        """测试客户端初始化"""
        PeekAPIClient = service_module.PeekAPIClient
        client = PeekAPIClient(
            host="192.168.1.100:1920",
            key="test_key",
            timeout=30.0,
            retries=3,
        )
        assert client.base_url == "http://192.168.1.100:1920"
        assert client.key == "test_key"
        assert client.timeout == 30.0
        assert client.retries == 3

    def test_client_initialization_defaults(self, service_module):
        """测试客户端默认值"""
        PeekAPIClient = service_module.PeekAPIClient
        client = PeekAPIClient(host="localhost:1920")
        assert client.key is None
        assert client.timeout == 60.0
        assert client.retries == 2

    def test_client_initialization_with_https(self, service_module):
        """测试 HTTPS 客户端初始化"""
        PeekAPIClient = service_module.PeekAPIClient
        client = PeekAPIClient(host="https://secure.example.com:443")
        assert client.base_url == "https://secure.example.com:443"

    def test_client_base_url_construction(self, service_module):
        """测试 base_url 构造"""
        PeekAPIClient = service_module.PeekAPIClient

        # 各种输入格式
        test_cases = [
            ("127.0.0.1:1920", "http://127.0.0.1:1920"),
            ("http://localhost:8080", "http://localhost:8080"),
            ("https://api.example.com", "https://api.example.com"),
            ("192.168.0.1", "http://192.168.0.1"),
        ]

        for host, expected_url in test_cases:
            client = PeekAPIClient(host=host)
            assert client.base_url == expected_url, f"Failed for host: {host}"
