import os

def change_dns_linux(dns:list):
    # read resolv.conf
    with open('/etc/resolv.conf', 'r') as f:
        resolv_conf = f.read().split('\n')

    # remove previous nameservers
    index = None
    i = 0
    while i < len(resolv_conf):
        line = resolv_conf[i]
        if 'nameserver' in line:
            index = i if index == None else index # get the first index of nameserver
            resolv_conf.pop(i)
        else:
            i += 1

    # add new nameservers
    for i in range(len(dns)):
        resolv_conf.insert(index+i, f'nameserver {dns[i]}')

    # convert list to string
    resolv_conf_str = "\n".join(resolv_conf)

    # write to rseolv.conf
    with open('/etc/resolv.conf', 'w') as f:
        f.write(resolv_conf_str)
    
    return 0


def read_dns_linux():
    nameservers = []
    # read resolv.conf
    with open('/etc/resolv.conf', 'r') as f:
        for line in f:
            if 'nameserver' in line:
                n = line.strip().split(" ")[1]
                nameservers.append(n)
    
    return nameservers


def query_dns_linux():
    output = os.popen("dig google.com").read().split("\n")
    for line in output:
        if 'SERVER' in line:
            nameserver = line.split("SERVER: ")[1].split("#")[0].strip()

            return nameserver