from genie.testbed import load


routers = ('R1','R2','R3')


try:
    for r in routers:
        tb = load('devices.yaml')
        dev = tb.devices[r]
        dev.connect()
        p1 = dev.parse("show ip route")

except Exception as e:
    print(str(e))
