from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file

from nornir import InitNornir

nr = InitNornir(config_file='config.yaml')



def backup(task):
    get_config = task.run(task=napalm_get, getters=['config'])
    get_running = get_config.result['config']['running']
    task.run(task=write_file, content=get_running, filename='running.txt')

result = nr.run(task=backup)



