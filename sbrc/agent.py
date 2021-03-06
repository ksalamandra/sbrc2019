"""Training the agent"""

import numpy as np
import requests
import json
import random


class Agent(object):
    def __init__(self, _get_url = "http://127.0.0.1:8080/stats/meterconfig/1", _set_url="http://127.0.0.1:8080/stats/meterentry/modify", _range=2):
        """ Agente """

        "Ambiente"
        self.ACTION_SPACE = 1000  # 0 to 1000 Kbps
        self.OSERVATION_SPACE = len(self.action_map(_range=_range))  # Increase or decrease

        "Rest API info"
        self.GET_URL = _get_url
        self.SET_URL = _set_url

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

    def action_map(self, _range=1):
        self.actions = set()
        for i in range(_range):
            self.actions.add(i)
            self.actions.add(-i)
        self.actions = tuple(self.actions)
        return self.actions

    def get_reward(self, server_load, legit_traffic_percentage_increase):
        """ recuperar a recompensa para uma mudança de estado """
        if server_load > self.MAX_SERVER_LOAD:
            return -10
        else:
            return legit_traffic_percentage_increase*1

    def get_current_state(self):
        response = requests.get(url=self.GET_URL).json()
        drop_rate = response['1'][0]['bands'][0]["rate"]
        return drop_rate

    def set_new_drop_rate(self, action):
        increase_by = self.actions[action]
        self.state = self.get_current_state()
        new_rate = self.state + increase_by
        response = requests.post(
            url=self.SET_URL,
            data=json.dumps(dict(
                dpid=1,
                meter_id=1,
                flags="KBPS",
                bands=[
                    dict(
                        type="DROP",
                        rate=new_rate,
                    )
                ]
            ))
        )
        if response.status_code == 200:
            self.old_state = self.state
            self.old_action = action
            self.state = self.get_current_state()
        else:
            raise Exception(f"Unreachable URL: {self.SET_URL}")

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
        self.dump_data(server_load, total_legit_percent)
        if random.uniform(0, 1) < self.EPSILON:
            action = self.sample_action()  # Explore action space
        else:
            action = self.choose_action()  # Exploit learned values

        if self.old_state > 0:
            # Atualiza a Q-Table -> Aprendizado
            reward = self.get_reward(server_load, legit_traffic_percentage_increase)
            next_state = self.state + self.actions[action]
            next_max = np.argmax(self.q_table[next_state-1])
            old_value = self.q_table[self.old_state-1][self.old_action]
            new_value = (1 - self.ALPHA) * old_value + self.ALPHA * (reward + self.GAMMA * next_max)
            self.q_table[self.old_state - 1][self.old_action] = new_value
        self.set_new_drop_rate(action)
        print(self.state)

agent = Agent()
old_legit_percent = 10
for i in range(1000):
    print("EPOCH:" + str(i))
    server_load = random.randrange(20000, 50000)
    legit_traffic_percentage_increase = random.randrange(-20, 20)
    total_legit_percent = old_legit_percent + legit_traffic_percentage_increase
    agent.step(server_load, legit_traffic_percentage_increase, total_legit_percent)
    old_legit_percent = total_legit_percent

my_str = "<table><tbody>"
for i in agent.q_table:
    my_str += "<tr>"
    for j in i:
        my_str += "<td>"
        my_str += str(j)
        my_str += "</td>"
    my_str += "</tr>"
my_str += '</tbody></table>'
file = open("output.html", "w+")
file.write(my_str)
file.close()




