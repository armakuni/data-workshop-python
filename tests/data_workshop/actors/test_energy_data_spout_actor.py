from typing import Generator
from unittest.mock import MagicMock

import pytest
from pykka import ActorRef

from data_workshop.actors.energy_data_spout_actor import EnergyDataSpoutActor
from data_workshop.repositories.energy_data_record import EnergyDataRecord
from data_workshop.repositories.energy_data_repository import (
    EnergyDataRecordFactory,
    EnergyDataRepository,
)
from tests.data_workshop.actors.actor_test_probe import ActorTestProbe


@pytest.fixture
def test_probe() -> Generator[ActorRef[ActorTestProbe], None, None]:
    actor_ref = ActorTestProbe.start()
    yield actor_ref
    actor_ref.stop()


@pytest.fixture
def repo_list_all_result() -> list[EnergyDataRecord]:
    return [
        EnergyDataRecordFactory().build(),
        EnergyDataRecordFactory().build(),
        EnergyDataRecordFactory().build(),
        EnergyDataRecordFactory().build(),
    ]


@pytest.fixture
def actor(
    test_probe: ActorRef[ActorTestProbe], repo_list_all_result: list[EnergyDataRecord]
) -> Generator[ActorRef[EnergyDataSpoutActor], None, None]:
    repo = MagicMock(spec=EnergyDataRepository)
    repo.list_all.return_value = repo_list_all_result

    actor_ref = EnergyDataSpoutActor.start(test_probe, repo)
    yield actor_ref
    actor_ref.stop()


def test_outputs_from_repository(
    test_probe: ActorRef[ActorTestProbe],
    actor: ActorRef[EnergyDataSpoutActor],
    repo_list_all_result: list[EnergyDataRecord],
) -> None:
    assert test_probe.proxy().get_messages().get() == repo_list_all_result
