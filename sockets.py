# -*- coding: utf-8 -*-

import socket
import subprocess
import paramiko
from os import sys


def check_ping(host):  # host = ip address
    
    if 'win' in os.sys.platform.lower():
        ping_ = "ping -n 2 {}".format(host)
    else:
        ping_ = "ping -c 2 {}".format(host)
    
    response = subprocess.run(ping_,
                              shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL)
                              
    if response.returncode == 0:
        if b"ttl=" in response.stdout.lower():
            return True
        else:
            return False
    else:
        return False                          


def pars_vendor(string):

    """
    b'SSH-2.0-ZTE_SSH.2.0\n',
    b'SSH-1.99-Cisco-1.25\n',
    b'SSH-2.0-HUAWEI-1.5\n',
    b'SSH-2.0--\r\n',
    b'SSH-2.0-VRP-3.3\n',
    b'SSH-2.0-ROSSSH\r\n',
    b'SSH-1.99-Comware-5.20\r\n',
    b'SSH-1.99-OpenSSH_4.4\n'
    """

    if b'HUAWEI' in string.strip():
        return b'Huawei'

    elif b'VRP' in string.strip():
        return b'H3C'

    elif b'Cisco' in string.strip():
        return b'Cisco'

    elif b'FIPS' in string.strip():
        return b'Nexus'

    elif b'ROSSSH' in string.strip():
        return b'Mikrotic'

    elif b'ZTE' in string.strip():
        return b'Poligon'

    elif b'Comware' in string.strip():
        # H3C MSR 20-21
        return b'HP'

    elif b'SSH-2.0--' in string.strip():
        return b'Huawei'

    elif b'SSH-1.99--' in string.strip():
        return b'Huawei'

    else:
        # print("VENDOR isn't DETECTED")
        return


def ssh_version_checker(host_ip):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname=host_ip,
                       username='test',
                       password='test',
                       look_for_keys=False,
                       allow_agent=False,
                       timeout=5,
                       banner_timeout=2)

    except paramiko.ssh_exception.AuthenticationException:
        return 'SSH'
    except paramiko.ssh_exception.SSHException as e:
        if 'Incompatible version (1.5 instead of 2.0)' in e.__str__():
            return 'SSHv1'
        if 'Error reading SSH protocol banner' in e.__str__():
            return 'SSHv1'
    except Exception:
        return 'SSHv1'

    return 'SSH'


def socket_checker(host_ip):
    
    """
    socket_checker('192.168.88.100')  
    returns dictionary in current format:
        {'ip addr':'{}',
        'SSH':'',
        'Telnet':'', 
        'Vendor':''}
    """
    
    res = {'IP': '{}'.format(host_ip),
           'SSH': None,
           'Telnet': None,
           'Vendor': None
           }

    ports = {'Telnet': 23,
             'SSH': 22
             }

    reach = None

    for protocol, port in ports.items():

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)

        try:
            client_socket.connect((host_ip, port))
            output = client_socket.recv(1024)

        except socket.timeout:
            continue
        except ConnectionRefusedError:
            continue
        except ConnectionResetError:
            continue
        except TimeoutError:
            print('HOST {} is not reachable by PORT {}'.format(host_ip, port))
            continue

        if output:
            if b'connection refused' in output:
                continue
            if b'connection closed by remote host!' in output:
                continue

            res['protocol'] = str(protocol)

            if port == 22:
                if pars_vendor(output):
                    res['Vendor'] = pars_vendor(output).decode('utf-8')

                if b'1.5-' in output:
                    res['SSH'] = 'SSHv1'
                else:
                    res['SSH'] = ssh_version_checker(host_ip)

                reach = 'SSH'

            else:
                res['Telnet'] = 'Telnet'
                reach = 'Telnet'
        client_socket.close()

    if reach:
        return res
    else:
        print("HOST {} is unreachable neither by Telnet nor SSH".format(host_ip))
        return None


if __name__ == '__main__':
    from pprint import pprint
    pprint(socket_checker('100.100.100.100'))
