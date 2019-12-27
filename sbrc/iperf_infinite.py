import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bandwidth", help="set bandwidth", type=str, default='200k')
parser.add_argument("-d", "--destination", help="set bandwidth", type=str, default='10.0.0.1')
parser.add_argument("-u", "--udp", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

u = ""
if args.udp:
    u = "-u"

command = f"iperf -c {args.destination} -b {args.bandwidth} {u} --reportstyle C"
print(command)
while 1:
    b = os.popen(command)
    print(b.read())