from abc import ABC
from typing import Any

from r2d2 import GlobApi
from r2d2.api.websocket.base_r2d2_ws_backend import BaseR2D2WsBackend


class BaseChatbotBackend(BaseR2D2WsBackend, ABC):
    def environment(self) -> dict[str, Any]:
        return {
            **super().environment(),
            'CONNECTIONS_URL': GlobApi.websocket_connection_url
        }
