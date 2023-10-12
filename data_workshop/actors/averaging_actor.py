from typing import Any

import pykka

get_average = "average"


class AveragingActor(pykka.ThreadingActor):
    def __init__(self) -> None:
        super().__init__()
        self._average: float = float("nan")
        self._count = 0
        self._running_total: float = 0.0

    def on_receive(self, message: Any) -> None | float:
        match message:
            case float(new_value):
                self._running_total += new_value
                self._count += 1
                self._average = self._running_total / self._count
                return None
            case "average":
                return self._average if self._average is not None else float("nan")
        return None
