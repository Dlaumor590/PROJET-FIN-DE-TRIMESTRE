# Le module queue implémente des files multi-productrices et multi-consommatrices
# C'est particulièrement utile en programmation multi-thread,
# lorsque les informations doivent être échangées sans risques entre plusieurs threads
# Dans notre cas il nous sert à exécuter plusieurs threads sur nos ports pour accélérer le scan
# Sans ce module le scan serait très lent sur une grande plage de ports
from queue import Queue

# En réseau un socket est l'association unique d'une adresse ip et d'un numéro de port
# Le module socket nous permet de nous connecter à un hôte sur le réseau
import socket

# Le module threading servira à lancer plusieurs threads dans notre cas 500
# pour effectuer le scan des ports dans le but de rendre le scan beaucoup plus rapide
import threading

# Le module datetime nous sera utile lors de la sauvergarde du scan dans un fichier
# il permettra de spécifier la date et l'heure du scan
import datetime


target = input("Entrer l'adresse à scanner au format x.x.x.x : ")


# on créé une queue vide dans laquelle on attachera les numéros de ports a scanner
queue = Queue()

open_ports = []

# la fonction portscan effectue une connexion basique à un hôte avec son adresse ip
# et le numéro de port en utilisant les fonctions du module socket


def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        sock.settimeout(1)
        return True
    except:
        return False

# la fonction get_ports nous permet de récupérer les numéros de port
# et les insérer dans la queue en fonction de l'option qu'aura choisi l'utilisateur


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


# la fontion worker récupère les numéros de port dans la queue.
# Lorsque la fonction portscan retourne un True ce qui veut dire que la connexion à l'hôte
# sur le port spécifié à réussie, on affiche un message pour signaler que le port est ouvert.
# De plus à la fin on récupère les numéros de ports ouverts qu'on ajoute à la liste open_ports
def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print("Le port {} est ouvert!".format(port))
            open_ports.append(port)

# la fonction run_scanner crée et exécute les threads sur le scan et fait en sorte de
# terminer l'exécution de tous les threads et du scan avant d'afficher le message


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

# on lance la fonction en indiquant qu'on veut utiliser 500 threads
run_scanner(500, mode)


# on créé un fichier qui contiendra la date du scan, le résultat du scan c'est à dire
# les ports ouverts et d'autres résultats de plusieurs scans peuvent également être ajoutées.
# Le texte est formaté de telle sorte que chaque résultat est lisible
# et différencié des autres
report = open("Résultat_scan.txt", "a")
date_du_scan = str(datetime.datetime.now())
report.writelines('\n' + date_du_scan + '\n')
report.writelines(
    '**********Les ports ouverts trouvés par le scan**********\n')
report.writelines('Hôte : ' + target + '\n')
report.writelines('Liste des ports ouverts: ' + str(open_ports) + '\n')
report.close()
