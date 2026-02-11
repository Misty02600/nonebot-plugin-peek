"""PeekAPI 客户端服务"""

from dataclasses import dataclass
from enum import IntEnum

import httpx
from nonebot.log import logger


class StatusCode(IntEnum):
    """API 响应状态码"""

    OK = 200
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    ERROR = 500


@dataclass
class APIResponse:
    """API 响应结果"""

    status: StatusCode
    content: bytes | None = None


@dataclass
class IdleInfo:
    """空闲时间信息"""

    idle_seconds: float
    """用户空闲秒数"""

    last_input_time: str
    """最后操作时间 (ISO 格式)"""


class PeekAPIClient:
    """PeekAPI 客户端"""

    def __init__(
        self,
        host: str,
        key: str | None = None,
        timeout: float = 60.0,
        retries: int = 2,
    ):
        self.base_url = self._normalize_url(host)
        self.key = key
        self.timeout = timeout
        self.retries = retries

    @staticmethod
    def _normalize_url(host: str) -> str:
        """规范化 URL，确保有协议前缀"""
        if not host.startswith(("http://", "https://")):
            return f"http://{host}"
        return host

    async def _request(self, endpoint: str, **params) -> APIResponse:
        """发送请求，支持重试"""
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            for attempt in range(1, self.retries + 1):
                try:
                    response = await client.get(
                        url,
                        params=params,
                        timeout=self.timeout,
                    )
                    if response.status_code in (200, 401, 403):
                        return APIResponse(
                            status=StatusCode(response.status_code),
                            content=response.content,
                        )
                    # 500 等错误，继续重试
                    logger.warning(f"请求 {endpoint} 返回状态码 {response.status_code}")
                except Exception as e:
                    logger.warning(f"请求 {endpoint} 第 {attempt} 次失败: {e}")

        return APIResponse(status=StatusCode.ERROR)

    async def get_screenshot(
        self, radius: int = 0, use_key: bool = False
    ) -> APIResponse:
        """
        获取屏幕截图

        Args:
            radius: 高斯模糊半径，0 表示原图
            use_key: 是否使用 API 密钥

        Returns:
            APIResponse: 包含状态码和图片数据
        """
        params: dict[str, str | int] = {"r": radius}
        if use_key and self.key:
            params["k"] = self.key
        return await self._request("/screen", **params)

    async def get_recording(self) -> APIResponse:
        """
        获取音频录制

        Returns:
            APIResponse: 包含状态码和音频数据
        """
        return await self._request("/record")

    async def check_health(self) -> bool:
        """
        检查服务健康状态

        Returns:
            bool: 服务是否可用
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/check",
                    timeout=5.0,
                )
                return response.status_code == 200
        except Exception:
            return False

    async def get_idle_info(self) -> IdleInfo | None:
        """
        获取用户空闲时间信息

        Returns:
            IdleInfo | None: 空闲时间信息，失败时返回 None
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/idle",
                    timeout=5.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    return IdleInfo(
                        idle_seconds=data["idle_seconds"],
                        last_input_time=data["last_input_time"],
                    )
                return None
        except Exception as e:
            logger.debug(f"获取空闲时间失败 ({self.base_url}): {e}")
            return None

    @property
    def host(self) -> str:
        """返回主机地址（用于日志和显示）"""
        return self.base_url.replace("http://", "").replace("https://", "")


async def select_active_client(clients: list[PeekAPIClient]) -> PeekAPIClient:
    """
    从多个客户端中选择最活跃的（空闲时间最短）。

    - 单客户端时直接返回
    - 多客户端时并发查询 /idle，选空闲最短的
    - 全部不可达时返回第一个
    """
    if len(clients) == 1:
        return clients[0]

    import asyncio

    tasks = [client.get_idle_info() for client in clients]
    results = await asyncio.gather(*tasks)

    best: PeekAPIClient | None = None
    best_idle = float("inf")

    for client, idle_info in zip(clients, results, strict=True):
        if idle_info is not None:
            logger.debug(f"主机 {client.host} 空闲 {idle_info.idle_seconds:.1f}s")
            if idle_info.idle_seconds < best_idle:
                best = client
                best_idle = idle_info.idle_seconds

    if best is None:
        logger.warning("所有主机均无法获取空闲时间，使用第一个主机")
        return clients[0]

    logger.info(f"选择最活跃主机: {best.host}")
    return best
