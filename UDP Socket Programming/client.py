import socket
import re

def check_message(string):

    
    if len(string) != 10:
        print("1")
        return False
    
    if not string[:2].isdigit():
        print("2")
        return False
    
    if string[2] != '-':
        print("3")
        return False
    
    if not string[3:7].isdigit():
        print("4")
        return False
    
    if string[7] != '-':
        print("5")
        return False
    
    if string[8:11] not in ["CI", "CO"]:
        print("6")
        return False
    
    return True

def main():
    # Define server address and port
    server_ip = '127.0.0.1'
    server_port = 2000
    
    # Create UDP socket
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket Created")
    except socket.error as err:
        print(f"Could not create socket. Error: {err}")
        return

    # Get input from user
    client_message = input("Enter Message (Format: YY-AAAA-CI or YY-AAAA-CO): ")
    
    # Validate the message format
    if not check_message(client_message):
        print("Invalid message format. Please follow the format YY-AAAA-CI or YY-AAAA-CO.")
        return
    
    # Send the message to the server
    try:
        udp_socket.sendto(client_message.encode(), (server_ip, server_port))
    except socket.error as err:
        print(f"Send Failed. Error: {err}")
        return

    # Receive the message back from the server
    try:
        server_message, _ = udp_socket.recvfrom(2000)
        print(f"Server Message: {server_message.decode()}")
    except socket.error as err:
        print(f"Receive Failed. Error: {err}")
        return

    # Close the socket
    udp_socket.close()

if __name__ == "__main__":
    main()



