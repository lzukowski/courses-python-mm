from abc import abstractmethod
from datetime import datetime
from typing import List
from uuid import UUID, uuid1

from returns.result import Result as Returns

from .unchangable import UnchangeableMixIn

_NOW = object()
_UUID = object()

CommandId = UUID


class Command(UnchangeableMixIn):
    command_id: CommandId
    timestamp: datetime

    def __init__(
            self,
            command_id: CommandId = _UUID,
            timestamp: datetime = _NOW,
            **kwargs,
    ):
        super().__init__(
            command_id=uuid1() if command_id is _UUID else command_id,
            timestamp=datetime.utcnow() if timestamp is _NOW else timestamp,
            **kwargs,
        )


EventId = UUID


class Event(UnchangeableMixIn):
    command_id: CommandId
    event_id: EventId
    timestamp: datetime

    def __init__(
            self,
            command_id: CommandId,
            event_id: EventId = _UUID,
            timestamp: datetime = _NOW,
            **kwargs,
    ):
        super().__init__(
            command_id=command_id,
            event_id=uuid1() if event_id is _UUID else event_id,
            timestamp=datetime.utcnow() if timestamp is _NOW else timestamp,
            **kwargs
        )


Result = Returns[List[Event], Exception]


class CommandHandler:
    @abstractmethod
    def __call__(self, command: Command) -> Result:
        raise NotImplementedError


def successful(result: Returns) -> bool:
    return isinstance(result, Returns.success_type)
