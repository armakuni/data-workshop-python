from typing import Generator

import pytest
from pykka import ActorRef

from data_workshop.actors.adding_actor import AddingActor, get_total
from tests.data_workshop.actors.actor_test_probe import wait_for_empty_inbox


@pytest.fixture
def actor() -> Generator[ActorRef[AddingActor], None, None]:
    actor_ref = AddingActor.start()
    yield actor_ref
    actor_ref.stop()


def test_adding(actor: ActorRef[AddingActor]) -> None:
    actor.tell(1.0)
    actor.tell(3.0)

    wait_for_empty_inbox(actor)

    assert actor.ask(get_total) == 4
