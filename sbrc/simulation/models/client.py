from .ryuapi import RyuApi
from .agent import Agent
import time


class Client:
    def __init__(self, id, bw, dc):
        self.id = id
        self.bw = bw
        self.nbw = bw
        self.new_nbw = bw
        self.dc = dc
        self.rapi = RyuApi(_dc=self.dc)
        self.dpid = id
        self.bootstrap()
        self.nbw_bw = 1
        self.nbw_rate = 1
        self.agent = Agent(self, dc)
        self.bytes = 0
        self.old_bytes = 0
        self.enabled = True
        self.old_time = time.time()

    def __str__(self):
        return f"CLIENT:{self.id}"

    def bootstrap(self):
        # install meter
        self.rapi.add_meter(self.dpid, self.id, int(self.bw/1000))

        # install flow
        self.rapi.add_flow(self.dpid, self.id, self.id)

        self.set_rate(300)

    def get_rate(self):
        return int(self.rapi.get_meter(self.dpid, self.id))

    def set_rate(self, rate):
        if rate * 1000 >= self.bw:
            self.rapi.change_meter(self.dpid, self.id, rate)

    def port_stats(self):
        return self.rapi.get_port_stats(self.dc.id, port_no=self.id)

    def speed(self):
        new_time = time.time()
        new_value = self.port_stats()
        speed = (new_value - self.old_bytes) / (new_time - self.old_time)
        self.old_time = new_time
        self.old_bytes = new_value
        return speed

    def get_nbw(self):
        if self.enabled:
            return self.nbw
        else:
            return 0

    def get_gain1(self):
        try:
            return abs(self.new_nbw - self.bw) / self.nbw_bw
        except ZeroDivisionError:
            return 1

    def get_gain2(self):
        try:
            return abs(self.new_nbw - self.get_rate()) / self.nbw_rate
        except ZeroDivisionError:
            return 1

    def set_bytes(self, bytes):
        self.bytes = bytes


    def update(self):
        self.nbw = self.new_nbw
        self.nbw_rate = abs(self.nbw - self.get_rate())
        self.nbw_bw = abs(self.nbw - self.bw)

    def sum_rate(self, num):
        new_rate =int(self.get_rate()) + num
        if new_rate * 1000 >= self.bw:
            self.rapi.change_meter(self.dpid, self.id, new_rate)

    def set_nbw(self, nbw):
        self.new_nbw = int(nbw)

    def step(self, rp):
        clients = rp.clients
        self.agent.step(clients)


