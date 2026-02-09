from genie.testbed import load


tb = load('devices.yaml')
dev = tb.devices['R1']

dev.connect(mit=True)

route_table = dev.api.get_routes()

print(route_table)

