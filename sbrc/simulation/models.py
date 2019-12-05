from .ryuapi import RyuApi

class Client:
    def __init__(self, id, bw, dc=1):
        self.id = id
        self.bw = bw
        self.nbw = bw
        self.new_nbw = bw
        self.dc = dc
        self.rapi = RyuApi(_dc=self.dc)
        self.dpid = 1
        self.bootstrap()
        self.nbw_bw = 1
        self.nbw_rate = 1

    def __str__(self):
        return f"CLIENT:{self.id}"

    def bootstrap(self):
        # install meter
        self.rapi.add_meter(self.dpid, self.id, self.bw)

        # install flow
        self.rapi.add_flow(self.dpid, self.id, self.id)

    def get_rate(self):
        return int(self.rapi.get_meter(self.dpid, self.id))

    def set_rate(self, rate):
        self.rapi.change_meter(self.dpid, self.id, rate)

    def get_nbw(self):
        return self.nbw

    def get_gain1(self):
        try:
            return abs(self.new_nbw - self.bw)/self.nbw_bw
        except ZeroDivisionError:
            return 1

    def get_gain2(self):
        try:
            return abs(self.new_nbw - self.get_rate()) / self.nbw_rate
        except ZeroDivisionError:
            return 1

    def update(self):
        self.nbw = self.new_nbw
        self.nbw_rate = abs(self.nbw - self.get_rate())
        self.nbw_bw = abs(self.nbw - self.bw)

    def sum_rate(self, num):
        self.rapi.change_meter(self.dpid, self.id, int(self.t_rate()) + num)

    def set_nbw(self, nbw):
        self.new_nbw = int(nbw)
        


class DC:
    def __init__(self, cap, id=1):
        self.id = id
        self.cap = cap
        self.load = 0