from library import checkBlock
import sys

if len(sys.argv) != 2:
    print("Usage: python3 app_checkLog.py username")
    sys.exit()
user = sys.argv[1]

currentBlock = checkBlock()
print("Current block: {}.txt".format(currentBlock-1))
for i in range(1, currentBlock-1):
    
    f = open("{}.txt".format(i), "r")
    lines = f.readlines()
    for line in lines:
        if user in line:
            print(line[:-1])
    f.close()
    