import statistics
from collections import deque
from typing import Any

import pykka

get_std_dev = "std_deviation"


class StdDevActor(pykka.ThreadingActor):
    def __init__(self, window_size: int) -> None:
        super().__init__()
        self._stddev: float | None = None
        self._messages: deque[float] = deque(maxlen=window_size)

    def on_receive(self, message: Any) -> float | None:
        match message:
            case float(new_value):
                self._messages.append(new_value)

                if len(self._messages) >= 2:
                    self._stddev = statistics.stdev(self._messages)
                return None
            case "std_deviation":
                return self._stddev
        return None
