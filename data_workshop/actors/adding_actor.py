from typing import Any

import pykka

get_total = "sum"


class AddingActor(pykka.ThreadingActor):
    def __init__(self) -> None:
        super().__init__()
        self._running_total: float = 0.0

    def on_receive(self, message: Any) -> None | float:
        match message:
            case float(new_value):
                self._running_total += new_value
                return None
            case "sum":
                return self._running_total

        return None
