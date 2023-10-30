from time import sleep
from typing import Any, TypeVar

import pykka
from pykka import Actor, ActorRef


class ActorTestProbe(pykka.ThreadingActor):
    def __init__(self) -> None:
        super().__init__()
        self._messages: list[Any] = []

    def on_receive(self, message: Any) -> None:
        self._messages.append(message)

    def get_messages(self) -> list[Any]:
        return self._messages


T = TypeVar("T", bound=Actor)


def wait_for_empty_inbox(actor: ActorRef[T]) -> None:
    while not actor.actor_inbox.empty():
        sleep(0.1)
