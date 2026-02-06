from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_configure


nr = InitNornir(config_file='config.yaml')


results = nr.run(task=napalm_configure, configuration='interface loo100')


print_result(results)


