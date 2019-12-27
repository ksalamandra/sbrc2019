import paramiko
from .ryuapi import RyuApi
import time
from . import settings

class RewardProvider:
    def __init__(self, ip, clients, dc, filename=settings.MAIN_FILE):
        self.SERVER_IP = ip
        self.clients = clients
        self.dc = dc
        self.current_bytes=0
        self.current_time=time.time()
        self.api = RyuApi()
        self.filename = filename
        self.flush_data()

    def flush_data(self):
        f = open(self.filename, "w")
        f.close()

    def dump_data(self):
        f = open(self.filename, "a")
        server_load = self.dc.load
        mean_rate = 0
        for client in self.clients:
            mean_rate += client.get_rate()
        mean_rate = mean_rate/len(self.clients)
        #dump_string = f"{server_load},{mean_rate*1000}"
        dump_string = f"{self.get_client(2).get_nbw()},{self.get_client(3).get_nbw()},{self.get_client(4).get_nbw()},{self.dc.load}"
        print(dump_string + f"|| {self.get_client(2).get_rate()},{self.get_client(3).get_rate()},{self.get_client(4).get_rate()}")
        f.write(dump_string + "\n")
        f.close()

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
        """
        self.check_conn()
        stdin, stdout, stderr = self.conn.exec_command('cat /tmp/test.txt')
        try:
            report = stdout.read().decode('utf-8')
            for client in self.clients:
                client.set_nbw(0)
                #self.update_client_load(client)

            for i in report.splitlines():
                print(i)
                if i:
                    src = i.split(',')[3]
                    bw = i.split(',')[8]
                    client = self.get_client(src.split('.')[-1])
                    #print(bw, client)
                    if client is not None:
                        client.set_nbw(bw)
        except Exception as e:
            print("Parse error:", e)
        """
        speeds = 0
        for client in self.clients:
            speed = client.speed()
            client.set_nbw(speed)
            speeds += speed
            # self.update_client_load(client)
        self.dc.load = speeds
        #self.conn.exec_command('echo "" > /tmp/test.txt')

    def get_client(self, id):
        for c in self.clients:
            if str(c.id) == str(id):
                return c

    def update_server_load(self):
        try:
            old_time = self.current_time
            old_bytes = self.current_bytes
            self.current_bytes = self.api.get_port_stats()
            if old_bytes != 0:
                self.dc.load = int(((self.current_bytes - old_bytes)*8)/(time.time() - old_time))
        except:
            print("HTTP ERROR")

    def update_client_load(self, client):
        try:
            old_time = self.current_time
            old_bytes = client.bytes
            current_bytes = self.api.get_port_stats(port_no=client.id)
            nbw = int(((current_bytes - old_bytes) * 8) / (time.time() - old_time))
            if old_bytes != 0:
                client.set_nbw(nbw)
            client.set_bytes(current_bytes)
            print(f"{client.id}-{nbw/1000} kbps")

        except Exception as e:
            print("HTTP ERROR", e)

    def check_client(self):
        self.check_conn()
        stdin, stdout, stderr = self.conn.exec_command('cat /tmp/test.txt')
        try:
            report = stdout.read().decode('utf-8')
            for line in report.splitlines():
                if line:
                    client_id, enabled = line.split("=")[0].replace("CLIENT", ""), line.split("=")[1]
                    client = self.get_client(int(client_id))
                    if int(enabled):
                        if not client.enabled:
                            self.get_client(int(client_id)).enabled = True
                            print("CLIENT", client_id, "enabled")
                    else:
                        if client.enabled:
                            self.get_client(int(client_id)).enabled = False
                            client.set_nbw(0)
                            print("CLIENT", client_id, "disabled")
        except Exception as e:
            print("EXCEPTION> ", e)
            pass

    def step(self):
        self.check_nbw()
        self.check_client()
        for client in self.clients:
            if client.enabled:
                client.step(self)
        self.current_time = time.time()
        self.dump_data()
