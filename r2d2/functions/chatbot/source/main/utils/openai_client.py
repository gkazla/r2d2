from __future__ import annotations

import os

from openai import Client, Timeout

DEFAULT_TIMEOUT = Timeout(20.0)


class OpenAiClient(Client):
    _instance = None

    def __new__(cls, *args, **kwargs) -> OpenAiClient:
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self, api_key: str = None, timeout: float | Timeout = DEFAULT_TIMEOUT) -> None:
        """
        Initialize the OpenAI client.

        :param api_key: The OpenAI API key.
        :param timeout: The timeout for the requests. Default is 20.0 seconds.

        :return: No return.
        """
        super().__init__(api_key=api_key or os.environ['OPENAI_API_KEY'], timeout=timeout)
