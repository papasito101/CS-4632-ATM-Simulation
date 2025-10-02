class ATM(object):
    __slots__ = ("aid", "is_busy", "busy_time")
    
    def __init__(self, aid):
        self.aid = aid
        self.is_busy = False
        self.busy_time = 0.0 
        
    def __repr__(self):
        return "ATM(aid={}, busy={}, busy_time={:.4f}h)".format(self.aid, self.is_busy, self.busy_time)
