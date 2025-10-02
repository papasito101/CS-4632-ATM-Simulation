class Customer(object):
    __slots__ = ("cid", "arrival_time")
    def __init__(self, cid, arrival_time):
        self.cid = cid
        self.arrival_time = float(arrival_time)
    def __repr__(self):
        return "Customer(cid={}, t={:.4f})".format(self.cid, self.arrival_time)
