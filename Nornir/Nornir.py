from nornir import InitNornir

from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_cli, napalm_configure, napalm_get
from nornir.core.task import Task


nr = InitNornir(
    config_file="config.yaml", dry_run=True
)

def multiple_task(task: Task):

    task.run(
        task=napalm_cli, commands=["show ip int brief"]
    )

results = nr.run(
    task=multiple_task
)

print_result(results)