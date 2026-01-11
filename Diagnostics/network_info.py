import socket
import subprocess

def get_ip_address():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def ping_test(host):
    try:
        subprocess.check_output(["ping", "-n", "1", host])
        return "Reachable"
    except subprocess.CalledProcessError:
        return "Unreachable"