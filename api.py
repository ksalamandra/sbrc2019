import requests, json
from pprint import pprint
rate = 500

class RYU:
    def __init__(self, _url= 'http://127.0.0.1:8080'):
        self.URL = _url

    def change_meter(self, dpid=1, meter_id=1, a_type="DROP", rate=300):
        response = requests.post(
            url=f"{self.URL}/stats/meterentry/modify",
            data=json.dumps(dict(
                dpid=1,
                meter_id=1,
                flags="KBPS",
                bands=[
                    dict(
                        type="DROP",
                        rate=rate,

                    )
                ]
            ))
        )
        return response.text

    def get_meter(self, dpid=1, meter_id=""):
        if meter_id: meter_id = f"/{meter_id}"
        route = f"{self.URL}/stats/meterconfig/{dpid}{meter_id}"
        print(route)
        response = requests.get(route)
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
                    "port": "2"
                },

            ]
         }
        response = requests.post(self.URL + route, json.dumps(data))
        return response.text

if __name__ == "__main__":
    rapi = RYU()
    pprint(rapi.add_meter(1, 2, 600))
    pprint(rapi.add_flow(1,2))
    pprint(rapi.get_meter())
    pprint(rapi.get_table())
