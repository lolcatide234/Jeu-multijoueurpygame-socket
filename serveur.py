import socket
import threading
import pickle

def handle_client(client_socket, addr, clients):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            clients[addr] = pickle.loads(data)

            for c_addr, c_vars in clients.items():
                if c_addr != addr:
                    client_socket.send(pickle.dumps((c_addr, c_vars)))

        except Exception as e:
            print(f"Erreur: {e}")
            break

    
    del clients[addr]
    client_socket.close()

def main():
    host = '192.168.1.48'
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Serveur en attente sur {host}:{port}")

    clients = {}

    while True:
        client_socket, addr = server.accept()
        print(f"Connexion acceptée de {addr}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, clients))
        client_thread.start()

if __name__ == "__main__":
    main()
