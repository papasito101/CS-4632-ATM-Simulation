class QueueSystem(object):
    def __init__(self):
        self._q = []
        self.samples = []

    def enqueue(self, item):
        self._q.append(item)

    def dequeue(self):
        if self._q:
            return self._q.pop(0)
        return None

    def __len__(self):
        return len(self._q)

    def sample_len(self, now):
        self.samples.append((float(now), len(self)))

    def average_len(self, until_time):
        if not self.samples:
            return 0.0
        if self.samples[-1][0] < until_time:
            self.samples.append((until_time, len(self)))
        total_area = 0.0
        for i in range(1, len(self.samples)):
            t0, l0 = self.samples[i-1]
            t1, l1 = self.samples[i]
            total_area += (t1 - t0) * l0
        return total_area / max(until_time, 1e-12)
