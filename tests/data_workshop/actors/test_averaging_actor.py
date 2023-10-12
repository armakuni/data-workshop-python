from typing import Generator

import pytest
from pykka import ActorRef

from data_workshop.actors.averaging_actor import AveragingActor, get_average
from tests.data_workshop.actors.actor_test_probe import wait_for_empty_inbox


@pytest.fixture
def actor() -> Generator[ActorRef[AveragingActor], None, None]:
    actor_ref = AveragingActor.start()
    yield actor_ref
    actor_ref.stop()


def test_averaging(actor: ActorRef[AveragingActor]) -> None:
    actor.tell(1.0)
    actor.tell(3.0)

    wait_for_empty_inbox(actor)

    assert actor.ask(get_average) == 2.0
