import requests, json
from pprint import pprint


class RyuApi:
    def __init__(self, _url= 'http://127.0.0.1:8080', _dc=1):
        self.URL = _url
        self.dc = _dc

    def change_meter(self, dpid=1, meter_id=1, rate=300, a_type="DROP", flag="KBPS", bsize=10):
        if int(rate) > 0:
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
        try:
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
            print(response.text)
            return response.text
        except Exception as e:
            print(e)


    def add_flow(self, dpid, meter_id=1, host = '3'):
        route = '/stats/flowentry/add'
        data = {
            "dpid": dpid,
            "priority": 4,
            "match":{
                #"nw_dst": f"10.0.0.{self.dc}",
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
        print(f"SOURCE: 10.0.0.{host}, PORT: {str(self.dc)}")
        try:
            response = requests.post(self.URL + route, json.dumps(data))
            return response.text
        except Exception as e:
            print(e)

    def get_port_stats(self, dpid=1, port_no=1):
        route = f"/stats/port/{dpid}"
        response = requests.get(self.URL + route)
        sw = response.json()[str(dpid)]
        for i in sw:
            if i.get('port_no') == int(port_no) and port_no == 1:
                return i.get('tx_bytes')
            elif i.get('port_no') == int(port_no):
                return i.get('rx_bytes')
        return 0



