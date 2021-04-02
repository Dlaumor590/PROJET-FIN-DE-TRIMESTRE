import socket
import ipaddress
import re
from queue import Queue
import threading

queue = Queue()
open_ports = []
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")

while True:
    ip_add_entered = input(
        "\nPlease enter the ip address that you want to scan: ")
    try:
        ip_address_obj = ipaddress.ip_address(ip_add_entered)
        print("You entered a valid ip address.")
        break
    except:
        print("You entered an invalid ip address")

while True:
    print("Please enter the range of ports you want to scan in format: <int>-<int> (ex would be 60-120)")
    port_range = input("Enter port range: ")
    port_range_valid = port_range_pattern.search(port_range.replace(" ", ""))
    if port_range_valid:
        port_min = int(port_range_valid.group(1))
        port_max = int(port_range_valid.group(2))
        break

for port in range(port_min, port_max + 1):
    queue.put(port)


def portscan():
    for port in range(port_min, port_max + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip_add_entered, port))
            return True
        except:
            return False


def worker():
    while not queue.empty():
        port = queue.get()
        if portscan():
            print("Port {} is open!".format(port))
            open_ports.append(port)


def scan():
    worker()
    thread_list = []

    for thread in range(500):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


scan()

print("Open ports are: {} on host {}".format(open_ports, ip_add_entered))
