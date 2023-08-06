from shekan_cli.dns import *
from shekan_cli.functions import *
from shekan_cli.config import config

shekan_dns, default_dns = config['shekan_dns'], config['default_dns']

def enable_shekan():
    _ = change_dns(shekan_dns)
    ip = query_dns()
    _ = f"Shekan Enabled {colorify('✓', TextStyle.GREEN)}\nDNS: {ip}" if _ == 0 else colorify("An Error Occured !", TextStyle.RED)
    print(_)

def disable_shekan():
    _ = change_dns(default_dns)
    ip = query_dns()
    _ = f"Shekan Disabled {colorify('X', TextStyle.RED)}\nDNS: {ip}" if _ == 0 else colorify("An Error Occured !", TextStyle.RED)
    print(_)

def status_shekan():
    ip = query_dns()
    for i in shekan_dns:
        if ip == i:
            print(f"Shekan is Enable {colorify('✓', TextStyle.GREEN)}\nDNS: {ip}")
            return
    print(f"Shekan is Disable {colorify('X', TextStyle.RED)}\nDNS: {ip}")

