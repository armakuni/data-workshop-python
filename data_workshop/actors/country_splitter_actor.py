from typing import Any

import pykka
from pykka import Actor, ActorRef

from data_workshop.repositories.energy_data_record import EnergyDataRecord

get_average = "average"


class CountrySplitterActor(pykka.ThreadingActor):
    def __init__(
        self, united_kingdom: ActorRef[Actor], united_states: ActorRef[Actor]
    ) -> None:
        super().__init__()
        self._united_states = united_states
        self._united_kingdom = united_kingdom

    def on_receive(self, message: Any) -> None:
        if not isinstance(message, EnergyDataRecord):
            return

        match message.model_dump():
            case {"iso_code": "GBR"}:
                self._united_kingdom.tell(message)
            case {"iso_code": "USA"}:
                self._united_states.tell(message)
