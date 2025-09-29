from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Any, List, Tuple
import heapq

@dataclass(order=True)
class Event:
    time: float
    seq: int
    action: Callable = field(compare=False)
    args: Tuple[Any, ...] = field(default=(), compare=False)

class SimulationEngine:
    """Minimal discrete-event simulation engine with a priority-queue scheduler."""
    def __init__(self):
        self.time: float = 0.0
        self._queue: List[Event] = []
        self._seq: int = 0
        self.running: bool = False

    def schedule(self, delay: float, action: Callable, *args: Any) -> None:
        """Schedule an event 'delay' minutes from now."""
        if delay < 0:
            raise ValueError("delay must be non-negative")
        evt = Event(self.time + delay, self._seq, action, args)
        self._seq += 1
        heapq.heappush(self._queue, evt)

    def run(self, until: float) -> None:
        """Run the simulation until 'until' minutes of simulated time."""
        self.running = True
        while self.running and self._queue and self.time <= until:
            evt = heapq.heappop(self._queue)
            if evt.time > until:
                # push back and stop at horizon
                heapq.heappush(self._queue, evt)
                break
            self.time = evt.time
            evt.action(*evt.args)
        # advance clock to horizon end consistently
        self.time = until
        self.running = False

    def stop(self) -> None:
        self.running = False
