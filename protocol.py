"""Encrypted sockets implementation
   Author: Eden Amiga
   Date: June 30 2024
"""

from socket import socket
import random
import logic
import time
import sys

MAX_BUFFER_LENGTH = 1024
LENGTH_FIELD_SIZE = 2 # means 99 max number -> 7 bits
PORT = 8820
DIFFIE_HELLMAN_P = 151
DIFFIE_HELLMAN_G = 43
MAC_LENGTH = 16
LENGTH_FIELD_SIZE_BIN = 7

def slow_print(string:str, sec=0.05, newline=True):
    for char in string:
        if char != " ":
            time.sleep(sec)

        sys.stdout.write(char)
        sys.stdout.flush()
    if newline: 
        print('\n')

def flash_print(string:str):
    for _ in range(3):
        sys.stdout.write('\r' + string)
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write('\r' + ' ' * len(string))
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write(string)
    sys.stdout.flush()
    time.sleep(0.5)
 

def symmetric_encryption(input_data, key):
    """Return the encrypted / decrypted data
    The key is 16 bits. If the length of the input data is odd, use only the bottom 8 bits of the key.
    Use XOR method"""    
    return logic.xor_coding(logic.str2bytes(input_data), key)


def symmetric_decryption(output_data, key):
    return logic.bin2text(logic.xor_coding(logic.bin2bytes(output_data), key))


def diffie_hellman_choose_private_key():
    """Choose a 16 bit size private key """
    return random.randint(0, 2**16-1)


def diffie_hellman_calc_public_key(private_key):
    """G**private_key mod P"""
    return pow(DIFFIE_HELLMAN_G, private_key, DIFFIE_HELLMAN_P)


def diffie_hellman_calc_shared_secret(other_side_public, my_private):
    """other_side_public**my_private mod P"""
    return pow(other_side_public, my_private, DIFFIE_HELLMAN_P)


def calc_hash(message):
    checksum = 0
    for char in message:
        checksum = (checksum >> 1) + ((checksum & 1) << 15)
        checksum += ord(char)
        checksum &= 0x3fff
    return checksum
    

def calc_signature(hash_num:int, RSA_private_key:int, pq:int):
    """Calculate the signature, using RSA algorithm:
    \nhash ^ RSA_private_key mod (P*Q)"""
    return pow(hash_num, RSA_private_key, pq)


def create_msg(data):
    """Create a valid protocol message, with length field
    * For example, if data = "hello world",
    then "11hello world" should be returned"""
    if isinstance(data, str) and not data.startswith('('):
        msg = data[:len(data) - MAC_LENGTH]
        mac = data[-MAC_LENGTH:]
        text_length = len(msg) >> 3 # divide by BYTE length 2^3
        t_msg = f'{logic.align_len(text_length)}{msg}{mac}'
    else:
        if f'{data}'.startswith('(') and f'{data}'.endswith(')'):
            bin = logic.text2bin(data)
            t_msg = f'{logic.align_len(len(bin))}{data}'
            return t_msg.encode()
        else:
            bin = logic.int2bin(data)
        t_msg = f'{logic.align_len(len(bin))}{bin}'

    if len(t_msg) > MAX_BUFFER_LENGTH:
        return "Error"

    return t_msg.encode()


def get_msg(my_socket:socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    recv_msg = my_socket.recv(MAX_BUFFER_LENGTH).decode()
    r_len = int(recv_msg[:LENGTH_FIELD_SIZE_BIN], 2)
    
    if r_len > 99:
        return False, "Error"
    else:
        return True, recv_msg[LENGTH_FIELD_SIZE_BIN:]


def check_RSA_public_key(key, totient):
    """Check that the selected public key satisfies the conditions
     * key is prime
     * key < totoent
     * totient mod key != 0"""
    return logic.isPrime(key) and key < totient and totient % key != 0
    
    
def get_RSA_private_key(p, q, public_key):
    """Calculate the pair of the RSA public key.
    Use the condition: Private*Public mod Totient == 1
    Totient = (p-1)(q-1)"""
    private = 1
    totient = (p-1)*(q-1)
    while private * public_key % totient != 1:
        private += 1
    return private


def totient(p,q):
    return (p - 1) * (q - 1)


def get_P_and_Q(pq):
    primes = [x for x in range(pq) if logic.isPrime(x)]
    for p in range(len(primes)):
        for q in range(p, len(primes)):
            P = primes[p]
            Q = primes[q]
            if pq == totient(P+1,Q+1):
                return P,Q


def rand_prime():
    primes = [x for x in range(1000) if logic.isPrime(x)]
    return primes[random.randint(0, len(primes)-1)]


def unzip(message:str):
    """First returns the encoded message and then the MAC signature
    """
    return message[:len(message) - MAC_LENGTH],\
           int(message[-MAC_LENGTH:],2)


def rsa_exchange_msg(msg:str, target:socket, rsa_key:int, pq:int, dh_secret:int):
    hash = calc_hash(msg)
    signature = calc_signature(hash, rsa_key, pq)
    b_encrypted = symmetric_encryption(msg, dh_secret)
    send_msg = create_msg(f'{b_encrypted}{logic.align_word(signature)}')
    target.send(send_msg)