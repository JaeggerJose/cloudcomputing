
import hashlib
from library import checkBlock
# arg 1: sender, arg 2: receiver, arg 3: amount

# get arg from python3 app_transaction.py sender receiver amount
import sys
try:
    sender = sys.argv[1]
    receiver = sys.argv[2]
    amount = sys.argv[3]
except:
    print("Usage: python3 app_transaction.py sender receiver amount")
    sys.exit()
if len(sys.argv) != 4:
    print("Usage: python3 app_transaction.py sender receiver amount")
    sys.exit()

        
def writeBlock(currentBlock, sender, receiver, amount):
    f = open("{}.txt".format(currentBlock), "a")
    f.write("{}, {}, {}\n".format(sender, receiver, amount))
    f.close()
    print("Transaction written to block {}.txt".format(currentBlock))
        
currentBlock = checkBlock()
print("Current block: {}.txt".format(currentBlock-1))
# check the current block >= 6 items, if so, create a new block
f = open("{}.txt".format(currentBlock-1), "r")
lines = f.readlines()
if len(lines) >= 8:
    # get all text from the current block and hash it
    f = open("{}.txt".format(currentBlock-1), "r")
    lines = f.readlines()
    # print lines
    text = ""
    for line in lines:
        text += line
    # hash the text
    print("Text: ", text)
    hash_object = hashlib.sha256(text.encode())
    print("Hash: ", hash_object.hexdigest())
    # open a new block
    f = open("{}.txt".format(currentBlock), "w+")
    f.write("Sha256 of previous block: {}\n".format(hash_object.hexdigest()))
    f.write("Next block: {}.txt\n".format(currentBlock+1))
    writeBlock(currentBlock, sender, receiver, amount)
else:
    writeBlock(currentBlock-1, sender, receiver, amount)
    
    