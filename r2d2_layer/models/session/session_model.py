from __future__ import annotations

import logging
from enum import Enum
from uuid import uuid4

from b_lambda_layer_common.exceptions.container.bad_request_error import BadRequestError
from b_lambda_layer_common.exceptions.container.not_found_error import NotFoundError
from b_lambda_layer_common.util.os_parameter import OSParameter
from pynamodb.attributes import UnicodeAttribute, ListAttribute, MapAttribute
from pynamodb.exceptions import DoesNotExist
from pynamodb.models import Model
from pynamodb.pagination import ResultIterator

logger = logging.getLogger(__name__)

__all__ = ['Session', 'SessionStatus']


class SessionStatus(Enum):
    OPEN = 'open'
    CLOSED = 'closed'

    @classmethod
    def available_values(cls) -> list[str]:
        """
        All available enum values.

        :return: A list of available values.
        """

        return [item.value for item in cls]


class SessionStatusAttribute(UnicodeAttribute):
    def serialize(self, value: str) -> str:
        available_values = SessionStatus.available_values()
        if value not in available_values:
            raise BadRequestError(f'Unsupported session status: {value}. Available values: {available_values}')

        return super().serialize(value)


class Session(Model):
    """
    Model for the R2D2 Chatbot Session.
    """

    class Meta:
        table_name = OSParameter('R2D2_SESSION_TABLE_NAME').value
        region = OSParameter('R2D2_SESSION_TABLE_REGION').value

    # Partition key is used for storing WebSocket connection ID.
    connection_id = UnicodeAttribute(attr_name='pk', hash_key=True)
    # Range key is used for storing R2D2 Chatbot session ID.
    session_id = UnicodeAttribute(attr_name='sk', range_key=True)
    status = SessionStatusAttribute()
    gpt_model = UnicodeAttribute(null=True)
    messages = ListAttribute(of=MapAttribute, null=True)

    @classmethod
    def get_session(
            cls,
            session_id: str,
            connection_id: str,
            consistent_read: bool = False
    ) -> Session:
        """
        Get R2D2 Chatbot session item.

        :param session_id: R2D2 Chatbot session ID.
        :param connection_id: WebSocket Connection ID.
        :param consistent_read: Whether to perform a consistent read.

        :return: R2D2 session model instance.

        :raises NotFoundError: If the session for the given session ID does not exist.
        """
        try:
            session = cls.get(hash_key=connection_id, range_key=session_id, consistent_read=consistent_read)
        except DoesNotExist:
            raise NotFoundError(f'Session with ID {session_id} not found.')

        return session

    @classmethod
    def create_session(
            cls,
            connection_id: str,
            gpt_model: str | None = None
    ) -> Session:
        """
        Creates a new session.

        :param connection_id: WebSocket Connection ID to create the session for.
        :param gpt_model: GPT model for the R2D2 Chatbot session to use. Defaults to 'gpt-3.5-turbo'.

        :return: Session model instance.
        """
        session = cls(
            connection_id=connection_id,
            session_id=str(uuid4()),
            status=SessionStatus.OPEN.value,
            gpt_model=gpt_model or 'gpt-3.5-turbo'
        )
        session.save(condition=(Session.connection_id.does_not_exist() & Session.session_id.does_not_exist()))

        return session

    @classmethod
    def query_connection_active_sessions(
            cls,
            connection_id: str,
    ) -> ResultIterator[Session]:
        """
        Queries the active sessions for the given connection ID.

        :param connection_id: WebSocket Connection ID to query the sessions for.

        :return: Result iterator of active sessions.
        """
        return cls.query(hash_key=connection_id, filter_condition=Session.status != SessionStatus.CLOSED.value)

    def update_session(
            self,
            session_status: SessionStatus | None = None,
            gpt_model: str | None = None,
            messages: list[dict[str, str]] | None = None
    ) -> None:
        """
        Updates the session.

        :param session_status: Session Status to update the session with.
        :param gpt_model: GPT model to update the session with.
        :param messages: Messages to update the session with.

        :return: No return.
        """
        actions = []

        if session_status is not None:
            actions.append(Session.status.set(session_status.value))

        if gpt_model is not None:
            actions.append(Session.gpt_model.set(gpt_model))

        if messages is not None:
            actions.append(Session.messages.set(messages))

        self.update(actions=actions)
