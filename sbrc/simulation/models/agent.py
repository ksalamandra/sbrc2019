from .datacenter import DC
import random
import numpy as np
from . import settings

class Agent(object):
    def __init__(self, client, dc, _range=settings.ACTIONS, max_percent=8):
        """ Agente """

        "Nodes"
        self.client = client
        self.dc = dc

        "Max percent of max server load"
        self.max_percent = max_percent

        "File for dump data"
        self.file = f"client_{str(self.client.id)}.txt"
        f = open(self.file, "w+")
        f.write("")
        f.close()

        "Ambiente"
        self.ACTION_SPACE = len(self.action_map(_range=_range))  # 0 to 1000 Kbps
        self.OSERVATION_SPACE = settings.STATES  # Increase or decrease

        "Modelagem das recompensas"
        self.MAX_SERVER_LOAD = self.dc.cap  # Max msg/seg

        "Q-table"
        self.q_table = np.zeros([self.OSERVATION_SPACE, self.ACTION_SPACE])  # Creating the Q-table
        self.old_state = -1

        "Parâmetros"
        self.ALPHA = settings.ALPHA  # A importancia da nova experiencia adquirida
        self.GAMMA = settings.GAMMA  # O peso das acoes futuras
        self.EPSILON = settings.EPSILON  # A Ganancia do agente

        "Graficos"
        self.epochs = []
        self.server_loads = []
        self.legit_traffics = []

        "LOCK MODE"
        self.LOCK_MODE = False

    def action_map(self, _range=1):
        self.actions = set()
        for i in range(_range):
            self.actions.add(i)
            self.actions.add(-i)
        self.actions = tuple(self.actions)
        return self.actions

    def get_reward(self, clients):
        """ recuperar a recompensa para uma mudança de estado """
        reward = 0
        gain1 = self.client.get_gain1()
        #gain2 = self.client.get_gain2()
        self.client.update()
        if self.dc.load >= self.dc.cap:
            reward = -(self.dc.load/self.dc.cap)
            return reward
        reward += gain1
        if gain1 < 1:
            return -reward
        return reward

    def get_current_state(self):
        state = int(self.dc.load/(self.dc.cap/self.OSERVATION_SPACE))

        if state > self.OSERVATION_SPACE:
            return self.OSERVATION_SPACE
        return state

    def do_action(self, action):
        increase_by = 0
        if self.actions[action] != 0:
            percent = ((self.max_percent/100)*(self.dc.cap/1000))
            increase_by = percent*(self.actions[action])
            print("increase_by =",increase_by)
        self.state = self.get_current_state()
        self.client.sum_rate(increase_by)
        self.state = self.get_current_state()
        self.old_state = self.get_current_state()

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

    def dump_data(self, *args):
        f = open(self.file, "a+")
        ex = ",".join([str(i) for i in args])
        data = f"{self.client.id},{self.dc.load},{self.client.get_rate()*1000},{ex}"
        #print(data)
        f.write(data + "\n")
        f.close()

    def choose_action(self):
        """Toma decisão embasada no que foi aprendido (Escolhe da Q-table)"""
        self.state = self.get_current_state()
        action = np.argmax(self.q_table[self.state - 1])
        if self.q_table[self.state - 1][action]:
            return action
        else:
            return self.sample_action()

    def force_down_action(self):
        #print(min(self.actions))
        return self.actions.index(min(self.actions))



    def step(self, clients):
        """O agente toma uma ação baseado no que aprendeu, com certa ganancia de apredizado, e verifica a efetividade de sua ultima decisão"""
        self.LOCK_MODE = False
        for client in clients:
            # self.client.nbw >= client.nbw and \
            if (client.nbw < client.bw and \
                    client.id != self.client.id and \
                    client.bw > self.client.bw and \
                    client.nbw < client.bw and
                    client.enabled) or self.dc.load > self.dc.cap:
                self.LOCK_MODE = True

        if self.LOCK_MODE:
            print(self.client.id, "LOCK MODE")

        # Escolha da ação baseada na taxa
        if not self.LOCK_MODE:
            self.ALPHA = 0.1
            if random.uniform(0, 1) < self.EPSILON:
                action = self.sample_action()  # Explore action space
            else:
                action = self.choose_action()  # Exploit learned values
        else:
            self.ALPHA = settings.LOCK_ALPHA
            action = self.force_down_action()

        #print(self.actions[action])

        if self.old_state > 0:
            # Atualiza a Q-Table -> Aprendizado
            reward = self.get_reward(clients)
            print(self.client.id, "reward =", reward, self.old_state)
            next_state = self.get_current_state()
            next_max = np.argmax(self.q_table[next_state-1])
            old_value = self.q_table[self.old_state-1][self.old_action]
            new_value = (1 - self.ALPHA) * old_value + self.ALPHA * (reward + self.GAMMA * next_max)
            self.q_table[self.old_state - 1][self.old_action] = new_value
        else:
            reward = self.get_reward(clients)
            print(self.client.id, "reward =", reward, self.old_state)

        self.old_action = action
        self.dump_data(reward)

        # tomar a ação vetorial
        self.do_action(action)