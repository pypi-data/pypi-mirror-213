from shekan_cli.linux_dns import *

platform = os.name

def change_dns(dns:list):
    if platform == 'posix':
        return change_dns_linux(dns)
 

def read_dns():
    if platform == 'posix':
        return read_dns_linux()
    


def query_dns():
    if platform == 'posix':
        return query_dns_linux()