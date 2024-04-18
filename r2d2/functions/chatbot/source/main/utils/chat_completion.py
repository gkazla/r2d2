from __future__ import annotations

from enum import Enum

from openai import AuthenticationError, APITimeoutError
from pydantic import BaseModel, StrictStr

from .openai_client import OpenAiClient
from .retry_decorator import retry


class MessageRole(Enum):
    SYSTEM = 'system'
    USER = 'user'


class Message(BaseModel):
    role: MessageRole
    content: StrictStr

    class Config:
        use_enum_values = True
        frozen = True

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Message:
        return cls.parse_obj(data)


class ChatCompletion:
    def __init__(self, client: OpenAiClient = None, gpt_model: str | None = None) -> None:
        self._client = client or OpenAiClient()
        self._gpt_model = gpt_model or "gpt-3.5-turbo"
        self._messages: list[Message] = []

    @property
    def gpt_model(self) -> str:
        return self._gpt_model

    @property
    def messages(self) -> list[dict[str, str]]:
        return [message.dict() for message in self._messages]

    @messages.setter
    def messages(self, messages: list[Message]) -> None:
        self._messages.extend(messages)

    @retry(times=3, delay=1, exceptions=(AuthenticationError, APITimeoutError,), raise_after=False)
    def chat(self) -> str | None:
        """
        Forwards the messages to the OpenAI chat completion API and returns the response.
        Adds the response to the messages list.

        :return: The response from the OpenAI chat completion API.
        """
        if not self._messages:
            return

        response = self._client.chat.completions.create(
            model=self._gpt_model,
            messages=self.messages,
            temperature=1.0,
            max_tokens=256
        )

        message = response.choices[0].message.content

        self.messages = [Message(role=MessageRole.SYSTEM, content=message)]

        return message
