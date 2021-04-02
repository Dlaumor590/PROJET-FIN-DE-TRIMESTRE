from queue import Queue
import socket
import threading
import datetime

target = input("Entrer l'adresse à scanner au format x.x.x.x : ")
queue = Queue()
open_ports = []


def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False


def get_ports(mode):
    if mode == 1:
        for port in range(0, 1025):
            queue.put(port)
    elif mode == 2:
        for port in range(1025, 65535):
            queue.put(port)
    elif mode == 3:
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            queue.put(port)
    elif mode == 4:
        for port in range(0, 65535):
            queue.put(port)
    elif mode == 5:
        ports = input("Enter les numéros de ports séparés par un espace: ")
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)


def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print("Le port {} est ouvert!".format(port))
            open_ports.append(port)


def run_scanner(threads, mode):

    get_ports(mode)

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("Les ports ouverts sont :", open_ports)


mode = int(input("\n**************Choisissez le mode d'exécution du scan :**************\n1-Scan des ports 0 à 1024\n2-Scan des ports 1025 à 65535\n3-Scan des ports suivants:\n*20 ftp data\n*21 ftp control\n*22 ssh\n*23 telnet\n*25 smtp \n*53 dns \n*80 http \n*110 POP3 \n*443 https\n\n4-Scan de tous les ports de 0 à 65535\n5-Scan manuel des ports (Vous devrez spécifier les ports à scanner)\n:"))
run_scanner(500, mode)


report = open("Résultat_scan.txt", "w")
date_du_scan = str(datetime.datetime.now())
report.writelines(date_du_scan + '\n')
report.writelines(
    '**********Les ports ouverts trouvés par le scan**********\n')
report.writelines(str(open_ports))
report.close()
