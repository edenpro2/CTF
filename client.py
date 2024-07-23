import socket
import time
import protocol
import threading
import server
from protocol import slow_print, flash_print
import os 

def main():
    t1 = threading.Thread(target=server.start_server)
    t1.start()
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    # Diffie Hellman
    # 1 - choose private keya
    correct_key = 5550001
    
    # 2 - calc public key
    injected_key = 222
    public_key = protocol.diffie_hellman_calc_public_key(injected_key)
    
    # 3 - interact with server and calc shared secret
    my_socket.send(protocol.create_msg(public_key))
    _, server_public_key = protocol.get_msg(my_socket)  
    server_public_key = int(server_public_key, 2)
     
    DH_secret = protocol.diffie_hellman_calc_shared_secret(server_public_key, injected_key)

    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n\n\n')

    slow_print("            Gruber Weapons Exporters GmbH 1995")
    slow_print("               Es lebe die ostdeutschland!")
    print()
    slow_print("                   BOMB HAS BEEN ARMED")
    print()
    slow_print("         PLEASE ENTER THE CORRECT CODE TO DEFUSE IT")
    print()
    slow_print("                     _ _ _ _ _ _ _ _", 0.45)
    print()
    slow_print("                    You have 3 tries\n")
   
    tries = 3
 
    while tries > 0:
        slow_print("Enter: ", newline=False)
        user_input = input()
        if user_input.isnumeric() and int(user_input) == correct_key:
            break
        tries-=1
        slow_print(f"{tries} tries left")
    
    if tries == 0:
        slow_print("You let the people of New York City down") 
        time.sleep(3)
        slow_print("\r[Connection Lost]")
        my_socket.send(protocol.create_msg("EXIT"))
        while True:
            ()

    os.system('cls' if os.name == 'nt' else 'clear')
    flash_print("BOMB DEFUSED")
    os.system('cls' if os.name == 'nt' else 'clear')

 
    # RETRY
    public_key = protocol.diffie_hellman_calc_public_key(correct_key)
    my_socket.send(protocol.create_msg(public_key))
    DH_secret = protocol.diffie_hellman_calc_shared_secret(server_public_key, correct_key)

    # RSA
    RSA_P = 137
    RSA_Q = 151
    PQ = RSA_P * RSA_Q
    T = (RSA_P-1)*(RSA_Q-1)

    # Figure out RSA P and Q
    slow_print("The location of the second bomb...")
    slow_print(f"You must figure out the RSA P and Q given this number: {PQ}")

    entered_P = 0
    entered_Q = 0
    while entered_P != RSA_P and entered_Q != RSA_Q:
        entered_P = int(input("P: "))
        entered_Q = int(input("Q: "))
        if entered_P != RSA_P or entered_Q != RSA_Q:
            print("Server rejected connection. Try again") 
    
    os.system('cls' if os.name == 'nt' else 'clear')
    flash_print("Server authorized connection")
    os.system('cls' if os.name == 'nt' else 'clear')


    rsa_public_key = protocol.rand_prime()
    while not protocol.check_RSA_public_key(rsa_public_key, T):
        rsa_public_key = protocol.rand_prime()

    # Calculate matching private key
    rsa_private_key = protocol.get_RSA_private_key(RSA_P, RSA_Q, rsa_public_key)
    # Exchange RSA public keys with server
    my_socket.send(protocol.create_msg(f'({rsa_public_key}, {PQ})'))
    _, server_rsa_public_key = protocol.get_msg(my_socket)
    server_rsa_public_key = int(server_rsa_public_key, 2)
    
    # Receive server's message
    valid_msg, b_message = protocol.get_msg(my_socket)
    if not valid_msg:
        slow_print("Something went wrong with the length field")

    # Check if server's message is authentic
    # 1 - separate the message and the MAC
    b_recv_msg, recv_sig = protocol.unzip(b_message)
    # 2 - decrypt the message
    decrypted = protocol.symmetric_decryption(b_recv_msg, DH_secret)
    # 3 - calc hash of message
    slow_print(f'Server returned: {decrypted}')
    import requests
    try:
        while True:
            slow_print("405\n", newline=False)
            requests.post('http://httpforever.com/', "[Lat,Long,Acc=111mm] d8fde39f832a41187bf9fd109b0c74c1,9a745c279c8a2b3e5c1abf0edddb8e80") # post text
            time.sleep(4)
    except:
        my_socket.close()

    


if __name__ == "__main__":
    main()
