import requests, json
from pprint import pprint


class RyuApi:
    def __init__(self, _url= 'http://127.0.0.1:8080', _dc=1):
        self.URL = _url
        self.dc = _dc

    def change_meter(self, dpid=1, meter_id=1, rate=300, a_type="DROP", flag="KBPS", bsize=10):
        data = json.dumps(dict(
                dpid=int(dpid),
                meter_id=int(meter_id),
                flags=flag,
                bands=[
                    dict(
                        type=a_type,
                        rate=rate,
                        burst_size=bsize,
                    )
                ]
            ))
        route = f"{self.URL}/stats/meterentry/modify"
        response = requests.post(
            url=route,
            data=data,
        )
        return response.text

    def get_meter(self, dpid=1, meter_id=""):
        route = f"{self.URL}/stats/meterconfig/{dpid}"
        response = requests.get(route)
        for i in response.json()[str(dpid)]:
            if str(i["meter_id"]) == str(meter_id):
                return i['bands'][0]['rate']
        return response.text

    def get_table(self, dpid=1):
        route = f"{self.URL}/stats/flow/{dpid}"
        response = requests.get(route)
        return response.text

    def add_meter(self, dpid, meter_id, rate):
        response = requests.post(
            url=f"{self.URL}/stats/meterentry/add",
            data=json.dumps(dict(
                dpid=dpid,
                meter_id=meter_id,
                flags="KBPS",
                bands=[
                    dict(
                        type="DROP",
                        rate=rate,
                        burst_size=10
                    )
                ]
            ))
        )
        return response.text

    def add_flow(self, dpid, meter_id=1, host = '3'):
        route = '/stats/flowentry/add'
        data = {
            "dpid": dpid,
            "priority": 4,
            "match":{
                #"nw_dst": f"10.0.0.{host}",
                "nw_src": f"10.0.0.{host}",
                "dl_type": 2048,
            },
            "actions":[
                {
                    "type":"METER",
                    "meter_id": meter_id
                },
                {
                    "type": "OUTPUT",
                    "port": str(self.dc)
                },

            ]
         }
        response = requests.post(self.URL + route, json.dumps(data))
        return response.text


class DC:
    def __init__(self, id, load, cap):
        self.id = id
        self.cap = cap
        self.load = load


class Client:
    def __init__(self, id, bw, dc=1):
        self.id = id
        self.bw = bw
        self.nbw = bw
        self.dc = dc
        self.rapi = RyuApi(_dc=self.dc)
        self.dpid = 1
        self.bootstrap()

    def bootstrap(self):
        # install meter
        self.rapi.add_meter(self.dpid, self.id, self.bw)

        # install flow
        self.rapi.add_flow(self.dpid, self.id, self.id)

    def t_rate(self):
        return self.rapi.get_meter(self.dpid, self.id)

    def set_rate(self, rate):
        self.rapi.change_meter(self.dpid, self.id, rate)

    def sum_rate(self, num):
        self.rapi.change_meter(self.dpid, self.id, int(self.t_rate()) + num)

if __name__ == "__main__":
    rapi = RyuApi(_dc=1)
    pprint(rapi.add_meter(1, 2, 600))
    pprint(rapi.add_flow(1,2))
    pprint(rapi.get_meter())
    pprint(rapi.get_table())
