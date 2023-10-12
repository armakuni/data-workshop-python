from typing import Generator

import pytest
from pykka import ActorRef

from data_workshop.actors.std_dev_actor import StdDevActor, get_std_dev
from tests.data_workshop.actors.actor_test_probe import wait_for_empty_inbox


@pytest.fixture
def actor() -> Generator[ActorRef[StdDevActor], None, None]:
    actor_ref = StdDevActor.start(3)
    yield actor_ref
    actor_ref.stop()


def test_windows_standard_dev(actor: ActorRef[StdDevActor]) -> None:
    actor.tell(99999.0)
    actor.tell(10.0)
    actor.tell(5.0)
    actor.tell(0.0)

    wait_for_empty_inbox(actor)
    assert actor.ask(get_std_dev) == 5
