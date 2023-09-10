import socket
import time
import json
import glob
import sys
from info import *

message_size = 2048
approved_directories = ('cache', 'latin_dictionary', 'noun_adjective_dictionary', 'timed_vocabulary_dictionary', 'timed_morphology_dictionary', 'reading_keys')
approved_directory_path = f'.{subDirectory}data{subDirectory}'
run_server = True
server_running = False


def handle_connection(conn, addr) -> None:
    """
    Handles incoming connections from clients.

    :param conn: The connection socket.
    :param addr: The client's address.
    :return: None
    """

    raw_data = conn.recv(1024)
    data = json.loads(str(raw_data.decode()))

    request = data.get('request')
    command = None
    sub_command = None

    if data.get('user') is None:
        conn.send('{}')
        conn.close()
        return None

    print(f"Connected by {addr} | user: {data.get('user')} | request: {request}")

    if request is not None:
        request = request.split(' ')
        command = request[0]
    
    if len(request) >= 2:
        sub_command = request[1]
    
    response = None

    match command:
        case "list":
            response = {}

            if sub_command in approved_directories:
                files = glob.glob(f'.{subDirectory}data{subDirectory}{sub_command}{subDirectory}*.json')

                for temp_file in files:
                    with open(temp_file, mode='r', encoding='utf-8') as file:
                        file_data = json.load(file)

                        response[temp_file.replace(subDirectory, '(sub)')] = sys.getsizeof(str(file_data).encode())
        
        case "get":
            response = None

            for approved_directory in approved_directories:
                sub_command = sub_command.replace('(sub)', subDirectory)

                if f'{approved_directory_path}{approved_directory}{subDirectory}' in sub_command and response is None and os.path.exists(sub_command) == True:
                    with open(sub_command, mode='r', encoding='utf-8') as file:
                        response = json.load(file)
    
    offset = 0
    response = str(response).encode()

    while offset < len(response):
        chunk = response[offset:offset+message_size]
        sent = conn.send(chunk)
        if sent == 0:
            raise RuntimeError("socket connection broken")
        offset += sent

    conn.close()


def server(host: str, port: int) -> None:
    """
    Starts a server and listens for incoming connections.

    :param host: The host address to bind to.
    :param port: The port to listen on.
    :return: None
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((host, port))
    sock.listen()
    print('starting server!')

    server_running = True

    while run_server == True:
        conn, addr = sock.accept()
        try:
            handle_connection(conn, addr)
        except Exception as error:
            print(error)
        time.sleep(.5)
    server_running = False


def stop_server() -> None:
    """
    Stops the server.

    :return: None
    """

    while (server_running == True):
        run_server = False
        time.sleep(.5)
    run_server = True
    

def connect_to_peer(peer_host, peer_port, message: dict) -> None:
    """
    Connects to a peer and sends a message.

    :param peer_host: The peer's host address.
    :param peer_port: The peer's port.
    :param message: The message to send.
    :return: None
    """

    peer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    peer_sock.connect((peer_host, peer_port))
    peer_sock.sendall(message.encode())

    response = b''

    while True:
        chunk = peer_sock.recv(message_size)
        if not chunk:
            break
        response += chunk

    print(f"Received response: {response.decode()}")
    peer_sock.close()


def get_local_ip() -> str:
    """
    Gets the local IP address of the machine.

    :return: The local IP address as a string.
    """
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        sock.connect(("8.8.8.8", 80))
        ip_address = sock.getsockname()[0]
        
        sock.close()
        
        return ip_address
    except socket.error:
        return None