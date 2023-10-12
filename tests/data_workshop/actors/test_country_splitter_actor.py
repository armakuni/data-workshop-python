from typing import Generator

import pytest
from pykka import ActorRef

from data_workshop.actors.country_splitter_actor import CountrySplitterActor
from data_workshop.repositories.energy_data_record import (
    EnergyDataRecord,
    ThreeLetterIsoCode,
)
from tests.data_workshop.actors.actor_test_probe import (
    ActorTestProbe,
    wait_for_empty_inbox,
)


@pytest.fixture
def gbr_probe() -> Generator[ActorRef[ActorTestProbe], None, None]:
    actor_ref = ActorTestProbe.start()
    yield actor_ref
    actor_ref.stop()


@pytest.fixture
def usa_probe() -> Generator[ActorRef[ActorTestProbe], None, None]:
    actor_ref = ActorTestProbe.start()
    yield actor_ref
    actor_ref.stop()


@pytest.fixture
def actor(
    gbr_probe: ActorRef[ActorTestProbe], usa_probe: ActorRef[ActorTestProbe]
) -> Generator[ActorRef[CountrySplitterActor], None, None]:
    actor_ref = CountrySplitterActor.start(gbr_probe, usa_probe)
    yield actor_ref
    actor_ref.stop()


def test_gbr_records_go_to_the_gbr_actor(
    actor: ActorRef[CountrySplitterActor],
    gbr_probe: ActorRef[ActorTestProbe],
    usa_probe: ActorRef[ActorTestProbe],
) -> None:
    record = EnergyDataRecord(
        iso_code=ThreeLetterIsoCode.GBR, renewables_consumption=3.0
    )
    actor.tell(record)
    wait_for_empty_inbox(actor)

    assert usa_probe.proxy().get_messages().get() == []
    assert gbr_probe.proxy().get_messages().get() == [record]


def test_usa_records_go_to_the_usa_actor(
    actor: ActorRef[CountrySplitterActor],
    gbr_probe: ActorRef[ActorTestProbe],
    usa_probe: ActorRef[ActorTestProbe],
) -> None:
    record = EnergyDataRecord(
        iso_code=ThreeLetterIsoCode.USA, renewables_consumption=3.0
    )
    actor.tell(record)

    wait_for_empty_inbox(actor)

    assert usa_probe.proxy().get_messages().get() == [record]
    assert gbr_probe.proxy().get_messages().get() == []
