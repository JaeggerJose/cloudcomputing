# init first block

import hashlib
import os, time

def initBlock():
    f = open("1.txt", "w+")
    # check if the file is empty
    if os.stat("1.txt").st_size != 0:
        # stop the program
        print("The file is not empty")
        exit()
    # write the first block using time to generate the hash
    header = str(time.time())
    firstHash = hashlib.sha256(header.encode('utf-8')).hexdigest()
    f.write("Sha256 of previous block: {}\n".format(firstHash))
    f.write("Nect block: 2.txt\n")
    # write the first transaction
    transaction = "god, angle, 1000000\n"
    f.write(transaction)
    f.close()
    
def checkBlock():
    i = 1
    while True:
        try:
            f = open("{}.txt".format(i), "r")
        except:
            return i            
        i += 1
