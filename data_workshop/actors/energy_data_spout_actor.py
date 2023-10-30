from typing import Any

import pykka
from pykka import Actor, ActorRef

from data_workshop.repositories.energy_data_repository import EnergyDataRepository

get_total = "sum"


class EnergyDataSpoutActor(pykka.ThreadingActor):
    def __init__(
        self, destination: ActorRef[Actor], repo: EnergyDataRepository
    ) -> None:
        super().__init__()
        self._destination = destination
        self._repo = repo

    def on_receive(self, message: Any) -> None:
        match message:
            case "start":
                for record in self._repo.list_all():
                    self._destination.tell(record)

    def on_start(self) -> None:
        self.actor_ref.tell("start")
