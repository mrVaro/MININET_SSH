import paramiko
import threading

# Fonction pour exécuter la commande en SSH sur l'hôte spécifié avec authentification par mot de passe
def run_command(host, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connexion SSH avec mot de passe
        client.connect(host, username=username, password=password)

        # Exécution de la commande en arrière-plan
        stdin, stdout, stderr = client.exec_command(command)
        
        # Lecture de la sortie
        stdout.channel.recv_exit_status()  # Bloque jusqu'à ce que la commande soit terminée

        # Lecture des erreurs
        stderr_output = stderr.read().decode()
        if stderr_output:
            print(f'Erreur sur {host}: {stderr_output}')

    except Exception as e:
        print(f'Erreur lors de la connexion à {host}: {str(e)}')
    finally:
        client.close()

# Liste des hôtes Mininet à traiter avec leurs interfaces respectives et commandes
host_commands = {
    '10.0.0.2': f'sudo tcpreplay --intf1=h2-eth0 --loop=1 /media/sf_MININET_TEST/DATA/priority6.pcap',
    '10.0.0.3': f'sudo tcpreplay --intf1=h3-eth0 --loop=1 /media/sf_MININET_TEST/DATA/priority5.pcap > /dev/null 2>&1 &',
    '10.0.0.4': f'sudo tcpreplay --intf1=h4-eth0 --loop=1 /media/sf_MININET_TEST/DATA/priority4.pcap > /dev/null 2>&1 &',
    '10.0.0.5': f'sudo iperf3 -c 10.0.0.1 -u -b 100M -t 50 > /dev/null 2>&1 &'
}

# Mot de passe commun pour tous les hôtes
password = 'ubuntu'

# Liste pour stocker les threads
threads = []

# Lancer un thread pour chaque hôte
for host, command in host_commands.items():
    t = threading.Thread(target=run_command, args=(host, 'ubuntu', password, command))
    threads.append(t)
    t.start()

# Attendre que tous les threads se terminent
for t in threads:
    t.join()

print("Tous les processus ont été lancés.")
