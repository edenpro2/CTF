from protocol import slow_print, flash_print
import socket
import protocol


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    client_socket, _ = server_socket.accept()
    slow_print(". . . .", 1)
    flash_print("\rClient connected")

    # Diffie Hellman
    private_key = protocol.diffie_hellman_choose_private_key()
    public_key = protocol.diffie_hellman_calc_public_key(private_key)
    
    # 3 - interact with client and calc shared secret
    _, rcv = protocol.get_msg(client_socket)
    client_public_key = int(rcv, 2)

    client_socket.send(protocol.create_msg(public_key))
    DH_secret = protocol.diffie_hellman_calc_shared_secret(client_public_key, private_key)

    # RETRY
    _, rcv = protocol.get_msg(client_socket)

    if not rcv.isnumeric() and rcv == "EXIT":
        client_socket.close()
        server_socket.close()
        exit()

    client_public_key = int(rcv, 2)
    DH_secret = protocol.diffie_hellman_calc_shared_secret(client_public_key, private_key)

    # RSA
    # Exchange RSA public keys with client
    _, client_rsa_msg = protocol.get_msg(client_socket)
    client_rsa_msg = client_rsa_msg[1:len(client_rsa_msg)-1].split(',')
    client_rsa_public_key = int(client_rsa_msg[0])
    PQ = int(client_rsa_msg[1])
    RSA_P, RSA_Q = protocol.get_P_and_Q(PQ)

    rsa_public_key = protocol.rand_prime()
    while not protocol.check_RSA_public_key(rsa_public_key, (RSA_P-1)*(RSA_Q-1)):
        rsa_public_key = protocol.rand_prime()

    # Calculate matching private key
    rsa_private_key = protocol.get_RSA_private_key(RSA_P, RSA_Q, rsa_public_key)
    
    client_socket.send(protocol.create_msg(rsa_public_key))

    protocol.rsa_exchange_msg("The other bomb location is in a New York school", client_socket, rsa_public_key, PQ, DH_secret)
    
    client_socket.close()
    server_socket.close()
    
