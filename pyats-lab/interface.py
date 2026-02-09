from genie.testbed import load
from genie.conf.base import Interface



tb = load('devices.yaml')
dev = tb.devices['R1']

dev.connect(mit=True)

interface = Interface(device=dev, name= "g0/1")


interface.ipv4 = "192.168.10.1/24"
interface.shutdown = False

print(interface.build_config(apply=True))

