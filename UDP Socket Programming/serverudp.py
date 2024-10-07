import socket
import os

file1 = "checkin.txt"

def read_file():
    if os.path.exists(file1):
        with open(file1, 'r') as file:
            return [line.strip() for line in file.readlines()]
    return []

def update_attendance(st_list):
    with open(file1, 'w') as file:
        for entry in st_list:
            file.write(f"{entry}\n")

def process_message(message, st_list):

    parts = message.split('-')
    if len(parts) != 3:
        return "Invalid message format.", st_list

    roll_number = f"{parts[0]}-{parts[1]}"
    action = parts[2]
    
    if action == "CI":
        if roll_number in st_list:
            return "You are already here.", st_list
        else:
            st_list.append(roll_number)
            return f"Welcome Student {roll_number}", st_list

    elif action == "CO":
        # Check-out action
        if roll_number not in st_list:
            return "You didn’t check in today. Contact System Administrator.", st_list
        else:
            st_list.remove(roll_number)
            st_list.insert(0, roll_number) 
            return f"Goodbye Student {roll_number}! Have a nice day.", st_list
    else:
        return "Invalid action. Use CI for Check-in or CO for Check-out.", st_list

def main():
    
    # Define server address and port
    server_ip = '127.0.0.1'
    server_port = 2000

    st_list = read_file()

    # Create UDP socket
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((server_ip, server_port))
        print("Socket Created and Bound")
    except socket.error as err:
        print(f"Could not create or bind socket. Error: {err}")
        return

    print("Listening for Messages...\n")

    while True:
        # Receive the message from the client
        try:
            client_message, client_address = udp_socket.recvfrom(2000)
            client_message = client_message.decode().strip()
            print(f"Received Message from IP: {client_address[0]} and Port No: {client_address[1]}")
            print(f"Client Message: {client_message}")
        except socket.error as err:
            print(f"Receive Failed. Error: {err}")
            continue

        response_message, updated_attendance_list = process_message(client_message, st_list)

        update_attendance(updated_attendance_list)

        # Send the response back to the client
        try:
            udp_socket.sendto(response_message.encode(), client_address)
            print(f"Response Sent: {response_message}")
        except socket.error as err:
            print(f"Send Failed. Error: {err}")
            continue

        # Print current attendance
        print("\nCurrent Attendance List:")
        for student in updated_attendance_list:
            print(student)
        print("\n")

if __name__ == "__main__":
    main()

