class Metrics(object):
    def __init__(self):
        self.arrivals = 0
        self.balked = 0
        self.completed = 0
        self.started = 0
        self.wait_times = []
    def inc_arrivals(self):
        self.arrivals += 1
    def inc_balked(self): 
        self.balked += 1
    def inc_completed(self): 
        self.completed += 1
    def inc_started(self): 
        self.started += 1
