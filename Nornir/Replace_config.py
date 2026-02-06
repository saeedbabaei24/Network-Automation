from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result


nr = InitNornir(config_file='config.yaml', dry_run=False)


results = nr.run(task=napalm_configure, filename='running.txt', replace=False)

print_result(results)



