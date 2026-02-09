from genie.testbed import load


tb = load('devices.yaml')

dev = tb.devices['R1']

dev.connect()

