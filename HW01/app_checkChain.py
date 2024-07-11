from library import checkBlock
import hashlib
import sys, subprocess

if len(sys.argv) != 2 and len(sys.argv) != 1:
    print("Usage: python3 app_checkChain.py [username] or python3 app_checkChain.py")
    sys.exit()

currentBlock = checkBlock()
lineAll = ""
hash_object = ""
failed_block = []
for i in range(1, currentBlock-1):
    lineAll = ""
    print("Block: {}.txt".format(i))
    f = open("{}.txt".format(i), "r")
    lines = f.readlines()
    for line in lines:
        lineAll += line
    hash_object = hashlib.sha256(lineAll.encode())
    f.close()
    # oepn the next block
    f = open("{}.txt".format(i+1), "r")
    # get the first line and compare the hash
    lines = f.readlines()
    firstLine = lines[0]
    firstLine = firstLine.split(" ")[4]
    firstLine = firstLine[:-1]
    # compare the hash
    print(hash_object.hexdigest())
    print(firstLine)
    if hash_object.hexdigest() != firstLine:
        print("The blockchain has been tampered with {}".format(i))
        failed_block.append(i)
if len(failed_block) == 0:
    print("The blockchain is safe")
    if len(sys.argv) == 2:
        user = sys.argv[1]
        # execute python3 app_checktransaction.py angel username 5
        subprocess.call(["python3", "app_transaction.py", "angel", user, "5"])
        
else:
    print("The following blocks have been tampered with: {}".format(failed_block))