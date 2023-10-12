from typing import Generator

import pytest
from pykka import ActorRef

from data_workshop.actors.get_renewables_consumption_actor import (
    GetRenewableConsumptionActor,
)
from data_workshop.repositories.energy_data_repository import EnergyDataRecordFactory
from tests.data_workshop.actors.actor_test_probe import (
    ActorTestProbe,
    wait_for_empty_inbox,
)


@pytest.fixture
def test_probe() -> Generator[ActorRef[ActorTestProbe], None, None]:
    actor_ref = ActorTestProbe.start()
    yield actor_ref
    actor_ref.stop()


@pytest.fixture
def actor(
    test_probe: ActorRef[ActorTestProbe],
) -> Generator[ActorRef[GetRenewableConsumptionActor], None, None]:
    actor_ref = GetRenewableConsumptionActor.start(test_probe)
    yield actor_ref
    actor_ref.stop()


def test_get_renewable_consumption(
    actor: ActorRef[GetRenewableConsumptionActor], test_probe: ActorRef[ActorTestProbe]
) -> None:
    fixture = EnergyDataRecordFactory().build()
    actor.tell(fixture)
    wait_for_empty_inbox(actor)

    assert test_probe.proxy().get_messages().get() == [fixture.renewables_consumption]
