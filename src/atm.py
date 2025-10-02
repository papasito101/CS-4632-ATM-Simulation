class ATM(object):
    __slots__ = ("aid", "is_busy", "busy_time")
    def __init__(self, aid):
        self.aid = aid
        self.is_busy = False
        self.busy_time = 0.0 
