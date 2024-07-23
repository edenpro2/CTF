# CTF

*The code snippets for the code behind is at the end of this readme*

* Starting file:
  
![image](https://github.com/user-attachments/assets/ad312e7f-3a11-448a-82a1-832d11063855)

* In the pulsating heartbeat of 1990s New York City, a shadowy figure known as Hans Gruber's prodigious brother, Simon, emerges as a ruthless mastermind. With a blend of suave charisma and chilling efficiency, he orchestrates a diabolical plot to detonate the city's financial hub. Armed with cunning intellect and a team of skilled mercenaries, Simon Gruber's ambition to rewrite the city's skyline in flames threatens to unleash unparalleled chaos and cement his legacy as a malevolent force to be reckoned with.
* He leaves Detective McClaine a file containing a riddle, but that's not all he left
* With enough digging, he'll notice that the photo embedded in the file is too large for its dimensions, hence, intriguing his curiosity
* Inside the image, McClaine uses a hex editor to read the underlying bytes
* Upon first look, it's a normal JFIF (JPG) image, but it still doesn't explain the large file size
* He first tries looking through the file for anything suspicious, like another photo or file...
![image](https://github.com/user-attachments/assets/a7f4cc2c-1e9c-498a-99a5-3128db340ede)

* After searching enough, he finally lands on an EXE appended to the JPG file, starting with the ubiquitous MZ header
![image](https://github.com/user-attachments/assets/9a97cdfe-a420-4b7a-9ba0-89883c5d37b4)

* This is how Simon did it:
```powershell
# Paths to input files
$file1 = "diehard3.jpg"
$file2 = "client.exe"

# Path to output file
$outputFile = "output_image.jpg"

# Read binary content of file1 and file2
$content1 = [System.IO.File]::ReadAllBytes($file1)
$content2 = [System.IO.File]::ReadAllBytes($file2)

# Combine binary content
$combinedContent = $content1 + $content2

# Write combined content to output file
[System.IO.File]::WriteAllBytes($outputFile, $combinedContent)
```

* Deleting the previous bytes up to the MZ header leaves us with an executable file: **diehard3.exe**

* Running the file gives:\
![image](https://github.com/user-attachments/assets/43f079b1-e61e-4008-8441-d2206d430b25)

* The code is the answer to the riddle, which is a trick
* The answer is 555[ANSWER] which is ANSWER = 0001 since only the man was on his way to St. Ives

* After successfully defusing the bomb, another message pops up:\
![image](https://github.com/user-attachments/assets/f7d64071-22d5-49b7-8ac4-452b8e845957)

* To solve for P and Q, write an algorithm to search through pairs of primes
```python
def get_P_and_Q(pq):
    primes = [x for x in range(pq) if logic.isPrime(x)]
    for p in range(len(primes)):
        for q in range(p, len(primes)):
            P = primes[p]
            Q = primes[q]
            if pq == totient(P+1,Q+1):
                return P,Q
```

* After solving for P and Q, the last message pops up:\
![image](https://github.com/user-attachments/assets/f59b219f-7bb6-4fe6-b1e0-a77d55492461)

* It seems that this is the end... but after a few seconds, the number `405` appears multiple times\
![image](https://github.com/user-attachments/assets/548fdda9-1901-43bd-b738-c2e0a2c22775)

* What does 405 mean? Google searching gives us Interstate 405, which isn't in NYC.
* New York State Route 405 - but it's not in NYC
* Restaurant 405 - not a school
* And so on...

* But alas, what does 405 mean on its own?
* Besides an area code.. in terms of HTTP, it means 405 Method Not Allowed
* A clue...
* Opening *Wireshark* to inspect any outgoing packets:\
![image](https://github.com/user-attachments/assets/d037da1b-78ac-4a9b-9e92-66adaea8c775)

* The program is trying to send something to a web server using a POST request...

* We can export any POST objects in HTTP using EXPORT:\
![image](https://github.com/user-attachments/assets/971e3109-1fb3-4423-bba5-0815e92c98e4)
![image](https://github.com/user-attachments/assets/78f1417b-9b6c-4fa6-89e3-0aeea95e9dcd)

* The files are missing an extension.
* Trying out image formats, exe, code files... until txt works
One of the files contains:
```html
<html>
     <head><title>405 Not Allowed</title></head>
     <body>
     <center><h1>405 Not Allowed</h1></center>
     <hr><center>nginx/1.18.0 (Ubuntu)</center>
     </body>
</html>
```
The other one contains:
```txt
[Lat,Long,Acc=111mm] d8fde39f832a41187bf9fd109b0c74c1, 9a745c279c8a2b3e5c1abf0edddb8e80
```
* Another clue to the second location
* It seems that the Lat and Long are hashed...
* Each string is 32 characters long. Looking for a hash with the same output length gives us MD5 (and a few others)

* Since MD5 is a one-way hash, we need to somehow compare the hashes of lat and long... but the problem will take forever since there are 15 digits after the decimal = 10^15 combinations for each whole number
* We can make this faster by only taking coordinates between [40, 41] Latitude and [-74, -73] Longitude since this is in New York
* Another thing is the Acc=111mm in the text file... this means that only 6 digits after the decimal are used -> another reduction from 10^15 to 10^6!

```python
import hashlib

hash_lat = "d8fde39f832a41187bf9fd109b0c74c1"
hash_lon = "9a745c279c8a2b3e5c1abf0edddb8e80"

lat = ""
lon = ""

def HashLatLon(l, r, hash:str, acc:int):    
    for i in range(l, r+1):
        for j in range(10**acc):
            degree = f'{i}.{j}' 
            if hashlib.md5(degree.encode()).hexdigest() == hash:
                return degree

print("Comparing lat")
print(HashLatLon(40, 40, hash_lat, 6))
print("Comparing lon")
print(HashLatLon(-74, -73, hash_lon, 6))
```

* The output:
```python
Comparing lat
40.846360
Comparing lon
-73.935039
```

Plugging the coordinates in:\
![image](https://github.com/user-attachments/assets/3a0bdc59-a2d1-4677-ad1d-1b6c107e8869)

..which is the location of Chester A. Arthur Elementary in DH3:
![image](https://github.com/user-attachments/assets/b0dfcf17-3a3c-458c-9ca9-874826f27524)

#### client.py
```python
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
```

####server.py
```python
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
```
