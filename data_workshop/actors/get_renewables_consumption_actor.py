from typing import Any

import pykka
from pykka import Actor, ActorRef

from data_workshop.repositories.energy_data_record import EnergyDataRecord


class GetRenewableConsumptionActor(pykka.ThreadingActor):
    def __init__(self, destination: ActorRef[Actor]) -> None:
        super().__init__()
        self._destination = destination

    def on_receive(self, message: Any) -> None:
        if not isinstance(message, EnergyDataRecord):
            return
        self._destination.tell(message.renewables_consumption)
