from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command

def push_rendered_config(nr, device_name: str, rendered_cfg: str):
    nr2 = nr.filter(name=device_name)

    cfg_lines = []
    for line in rendered_cfg.splitlines():
        line = line.strip()
        if not line or line == "!":
            continue
        if line.lower() == "end":
            continue
        cfg_lines.append(line)

    def _task(task):
        # verify where we are
        task.run(task=netmiko_send_command, command_string="show run | i ^hostname")

        # push
        task.run(task=netmiko_send_config, config_commands=cfg_lines)

        # verify BGP + a couple easy lines
        task.run(task=netmiko_send_command, command_string="show run | section router bgp")
        task.run(task=netmiko_send_command, command_string="show run | i ^ip domain name|^ip name-server|^ntp server|^logging host|^snmp-server")

    return nr2.run(task=_task)
