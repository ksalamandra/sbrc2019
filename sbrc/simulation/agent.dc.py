"""Training the agent"""

import numpy as np
import requests
import json
import random
import models
import paramiko
import time


class Agent(object):
    def __init__(self, _get_url = "http://127.0.0.1:8080/stats/meterconfig/1", _set_url="http://127.0.0.1:8080/stats/meterentry/modify", _range=2, clients=tuple(), dc=models.DC(cap=2000)):
        """ Agente """

        "Nodes"
        self.clients = clients
        self.dc = dc

        "Ambiente"
        self.ACTION_SPACE = len(self.action_map(_range=_range))  # 0 to 1000 Kbps
        self.OSERVATION_SPACE = 10 # Increase or decrease

        "Rest API info"
        self.GET_URL = _get_url
        self.SET_URL = _set_url

        "Server ip"
        self.SERVER_IP = '192.168.0.22'

        "Modelagem das recompensas"
        self.MAX_SERVER_LOAD = 30000  # Max msg/seg

        "Q-table"
        self.q_table = np.zeros([self.ACTION_SPACE, self.OSERVATION_SPACE])  # Creating the Q-table
        self.old_state = -1

        "Parâmetros"
        self.ALPHA = 0.1  # A importancia da nova experiencia adquirida
        self.GAMMA = 0.6  # O peso das acoes futuras
        self.EPSILON = 0.1  # A Ganancia do agente

        "Graficos"
        self.epochs = []
        self.server_loads = []
        self.legit_traffics = []

    def get_conn(self):
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(hostname=self.SERVER_IP, username="root", password="ubuntu")
        self.conn = conn

    def check_conn(self):
        if not getattr(self, "conn", False):
            return self.get_conn()
        if self.conn.get_transport() is not None:
            if self.conn.get_transport().is_active():
                return True
        return self.get_conn()

    def check_nbw(self):
        self.check_conn()
        stdin, stdout, stderr = self.conn.exec_command('cat /tmp/test.txt')
        report = stdout.read().decode('utf-8')
        for i in report.splitlines():
            if i:
                src = i.split(',')[3]
                bw = i.split(',')[8]
                client = self.get_client(src.split('.')[-1])
                if client is not None:
                    client.set_nbw(bw)
        self.conn.exec_command('echo "" > /tmp/test.txt')

    def get_client(self, id):
        for c in self.clients:
            if str(c.id) == str(id):
                return c


    def action_map(self, _range=1):
        self.actions = set()
        for i in range(_range):
            self.actions.add(i)
            self.actions.add(-i)
        self.actions = tuple(self.actions)
        return self.actions

    def get_reward(self):
        """ recuperar a recompensa para uma mudança de estado """

        self.check_nbw()
        current_server_load = 0
        server_overload = 0
        reward = 0

        # Server Overload [DC]
        for client in self.clients:
            current_server_load += client.new_nbw
        self.dc.load = current_server_load
        if current_server_load >= self.dc.cap:
            reward = len(self.clients)*-10

        # Clients band [HClients]
        for client in self.clients:
            gain1 = 1 + client.get_gain1()
            gain2 = 1 + client.get_gain2()
            reward += gain1 + gain2
            client.update()

        return reward

    def get_current_state(self):
        return int(self.dc.load/(self.dc.cap/self.ACTION_SPACE))

    def do_action(self, action):
        increase_by = self.actions[action]
        self.state = self.get_current_state()
        for client in clients:
            client.sum_rate(increase_by)
        self.state = self.get_current_state()


    def sample_action(self):
        """Toma uma decisão aleatoriamente (descobre)"""
        self.state = self.get_current_state()
        if self.state >= len(self.q_table):
            actions = [i for i in self.actions if i <= 0]
        elif self.state <= 1:
            actions = [i for i in self.actions if i >= 0]
        else:
            actions = self.actions
        chosen = random.randint(min(actions), max(actions))
        return self.actions.index(chosen)

    def choose_action(self):
        """Toma decisão embasada no que foi aprendido (Escolhe da Q-table)"""
        self.state = self.get_current_state()
        action = np.argmax(self.q_table[self.state - 1])
        if self.q_table[self.state - 1][action]:
            return action
        else:
            return self.sample_action()

    def dump_data(self, server_load, total_legit_percent):
        """Guarda os dados"""
        if not self.epochs:
            self.epochs = [0]
        else:
            self.epochs.append(self.epochs[-1] + 1)
        self.server_loads.append(server_load)
        self.legit_traffics.append(total_legit_percent)

    def step(self, server_load, legit_traffic_percentage_increase, total_legit_percent):
        """O agente toma uma ação baseado no que aprendeu, com certa ganancia de apredizado, e verifica a efetividade de sua ultima decisão"""
        #self.dump_data(server_load, total_legit_percent)

        # a ação precisa ser escolhida várias vezes em um único episódio
        if random.uniform(0, 1) < self.EPSILON:
            action = self.sample_action()  # Explore action space
        else:
            action = self.choose_action()  # Exploit learned values

        if self.old_state > 0:
            # Atualiza a Q-Table -> Aprendizado
            reward = self.get_reward()
            next_state = self.state + self.actions[action]
            next_max = np.argmax(self.q_table[next_state-1])
            old_value = self.q_table[self.old_state-1][self.old_action]
            new_value = (1 - self.ALPHA) * old_value + self.ALPHA * (reward + self.GAMMA * next_max)
            self.q_table[self.old_state - 1][self.old_action] = new_value

        # tomar a ação vetorial
        self.do_action(action)

        print(self.state)

clients = []
clients.append(models.Client(id=16, bw=500))
dc = models.DC(cap=2000)

agent = Agent(clients=clients, dc=dc)
while 1:
    agent.check_nbw()
    time.sleep(1)



#old_legit_percent = 10
#for i in range(1000):
#    print("EPOCH:" + str(i))
#    server_load = random.randrange(20000, 50000)
#    legit_traffic_percentage_increase = random.randrange(-20, 20)
#    total_legit_percent = old_legit_percent + legit_traffic_percentage_increase
#    agent.step(server_load, legit_traffic_percentage_increase, total_legit_percent)
#    old_legit_percent = total_legit_percent

#my_str = "<table><tbody>"
#for i in agent.q_table:
#    my_str += "<tr>"
#    for j in i:
#        my_str += "<td>"
#        my_str += str(j)
#        my_str += "</td>"
#    my_str += "</tr>"
#my_str += '</tbody></table>'
#file = open("output.html", "w+")
#ile.write(my_str)
#file.close()




