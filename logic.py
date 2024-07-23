BYTE = 8

def int2byte(num:int):
    return "{0:b}".format(num).zfill(8)

def int2word(num:int):
    return "{0:b}".format(num).zfill(16)

def int2bin(num:int):
    return "{0:b}".format(num)
 
def text2bin(text:str):
    return ''.join([int2bin(ord(c)) for c in text])

def bin2text(str): 
    return ''.join([chr(int(x, 2)) for x in bin2bytes(str)])

def align_len(num):
    """ Returns the length of a sequence in 7-bit binary string
    """
    return bin(num)[2:].zfill(7)

def str2bytes(str:str):
    return [int2byte(ord(c)) for c in str]

def xor(x, y):
    return "{0:b}".format((int(x, 2) ^ int(y, 2))).zfill(max(len(x),len(y)))

def bin2bytes(bin):
    total = len(bin)
    blocks = []
    for i in range(0,total,BYTE):
        blocks.append(bin[i:i+BYTE])
    return blocks

def xor_coding(bytes:str, key:int):
    key_b = align_word(key)
    xored = ""
    i = 0

    while i < len(bytes):
        if i + 1 >= len(bytes):
            xored += xor(bytes[i], key_b[-BYTE:])
            break
        else:
            xored += xor(bytes[i] + bytes[i+1], key_b)
            i += 2

    return xored

def isPrime(n):
    if n==2 or n==3: return True
    if n%2==0 or n<2: return False
    for i in range(3, int(n**0.5)+1, 2):   # only odd numbers
        if n%i==0:
            return False    

    return True


def align_word(int:int):
    """ Returns a 16-bit aligned binary string of an input number
    """
    return int2byte(int).zfill(16)
