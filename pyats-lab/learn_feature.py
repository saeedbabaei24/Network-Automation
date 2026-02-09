from genie.testbed import load



tb = load('devices.yaml')
dev = tb.devices['R1']
dev.connect(mit=True)
p1 = dev.learn('ospf')
p1 = dev.learn('bgp')

