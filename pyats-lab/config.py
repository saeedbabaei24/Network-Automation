from genie.testbed import load

config_commands = '''
        interface lo0
        ip add 11.11.11.11 255.255.255.255
        '''

tb = load('devices.yaml')
dev = tb.devices['R1']

dev.connect(mit=True)

dev.configure(config_commands)

print('done!')

