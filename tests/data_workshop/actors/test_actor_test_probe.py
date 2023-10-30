from typing import Generator

import pytest
from pykka import ActorRef

from tests.data_workshop.actors.actor_test_probe import (
    ActorTestProbe,
    wait_for_empty_inbox,
)


@pytest.fixture
def actor() -> Generator[ActorRef[ActorTestProbe], None, None]:
    actor_ref = ActorTestProbe.start()
    yield actor_ref
    actor_ref.stop()


def test_records_any_sent_messages(actor: ActorRef[ActorTestProbe]) -> None:
    actor.tell("a")
    actor.tell(1)
    actor.tell("y")

    wait_for_empty_inbox(actor)

    assert actor.proxy().get_messages().get() == ["a", 1, "y"]
