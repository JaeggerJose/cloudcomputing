from library import checkBlock
import sys

if len(sys.argv) != 2:
    print("Usage: python3 app_checkMoney.py username")
    sys.exit()
user = sys.argv[1]
currentBlock = checkBlock()
userBalance = 0
print("Current block: {}.txt".format(currentBlock-1))
for i in range(1, currentBlock):
    # open the current block
    f = open("{}.txt".format(i), "r")
    # check each line for the user
    print("Block: {}.txt".format(i))
    lines = f.readlines()
    for i in range(2, len(lines)):
        line = lines[i]
        line = line.split(", ")
        print(line)
        if line[0] == user:
            userBalance -= int(line[2])
        if line[1] == user:
            userBalance += int(line[2])
    
print("User balance: ", userBalance)
    