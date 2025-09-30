class QueueSystem(object):
    """Simple FIFO queue with sampling helpers (Python 3.6 compatible)."""
    def __init__(self):
        self._q = []
        self.samples = []  # (time, length)

    def enqueue(self, item):
        self._q.append(item)

    def dequeue(self):
        if self._q:
            return self._q.pop(0)
        return None

    def __len__(self):
        return len(self._q)

    def sample_len(self, now):
        # Record (time, length) for average queue length estimate
        self.samples.append((float(now), len(self)))

    def average_len(self, until_time):
        """Piecewise-constant average queue length over [0, until_time].
        Assumes sample_len is called at each event time and at t=0.
        """
        if not self.samples:
            return 0.0
        # Ensure last time is until_time
        if self.samples[-1][0] < until_time:
            self.samples.append((until_time, len(self)))
        total_area = 0.0
        for i in range(1, len(self.samples)):
            t0, l0 = self.samples[i-1]
            t1, l1 = self.samples[i]
            # length is constant between samples: use l0
            total_area += (t1 - t0) * l0
        return total_area / max(until_time, 1e-12)
