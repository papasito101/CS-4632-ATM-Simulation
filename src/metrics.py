class Metrics(object):
    def __init__(self):
        self.arrivals = 0

    def inc_arrivals(self):
        self.arrivals += 1
