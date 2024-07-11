import socket, os, time
import threading
import hashlib


class P2PNode:
    def __init__(self, port, peers):
        self.port = port
        self.peers = peers
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('172.17.0.19', self.port)) #這是本節點的 IP
        self.node = '172.17.0.19'
        self.shaList = []
        self.blockList = []
        self.changeBlockFlag = False
    
    def getLastBlock(self):
        currentBlock = 1
        while True:
            # open the current existing block, if not exist, break
            try:
                f = open("{}.txt".format(currentBlock), "r")
            except:
                break
            currentBlock += 1
        
        return currentBlock-1

    def cmdParser(self, argv, addr):
        if len(argv) == 0:
            print("Please enter a command")
            return
        
        if argv[0] == "exit":
            print("Exit")
            os._exit(0)
        
        # defined cmd "checkMoney, checkLog, transaction, checkChain, checkAllChains"
        if argv[0] == "checkMoney":
            # checkMoney <account>
            if len(argv) != 2:
                print("Usage: checkMoney <account>")
                return
            account = argv[1]
            os.system(f"/tmp/db/app_checkMoney {account}")
            
        elif argv[0] == "checkLog":
            
            # checkLog <account>
            if len(argv) != 2:
                print("Usage: checkLog <account>")
                return
            account = argv[1]
            os.system(f"/tmp/db/app_checkLog {account}")
            
        elif argv[0] == "transaction":
            print("transaction")
            
            # transaction <from> <to> <amount>
            if len(argv) != 4:
                print("Usage: transaction <from> <to> <amount>")
                return
            from_account = argv[1]
            to_account = argv[2]
            amount = argv[3]
            # check amount is number
            if not amount.isdigit():
                print("Amount must be a number")
                return
            # broadcast transaction
            for peer in self.peers:
                self.sock.sendto(f"app_transaction {from_account} {to_account} {amount}".encode('utf-8'), peer)
            os.system(f"/tmp/db/app_transaction {from_account} {to_account} {amount}")
        elif argv[0] == "app_transaction":
            if len(argv) != 4:
                print("Usage: transaction <from> <to> <amount>")
                return
            from_account = argv[1]
            to_account = argv[2]
            amount = argv[3]
            # check amount is number
            if not amount.isdigit():
                print("Amount must be a number")
                return
            os.system(f"/tmp/db/app_transaction {from_account} {to_account} {amount}")
        elif argv[0] == "checkChain":
            print("checkChain")
            
            # checkChain <account>
            if len(argv) != 2:
                print("Usage: checkChain <account>")
                return
            account = argv[1]
            print(f"checkChain {account}")
            os.system(f"/tmp/db/app_checkChain {account}")
            for peer in self.peers:
                self.sock.sendto(f"award {account} 5".encode('utf-8'), peer)
        elif argv[0] == "award":
            print("award")
            
            # award <account> <amount>
            if len(argv) != 3:
                print("Usage: award <account> <amount>")
                return
            account = argv[1]
            amount = argv[2]
            # check amount is number
            if not amount.isdigit():
                print("Amount must be a number")
                return
            os.system(f"/tmp/db/app_transaction angel {account} {amount}")
        elif argv[0] == "checkAllChains":
            print("checkAllChains")
            
            # checkAllChains <account>
            if len(argv) != 2:
                print("Usage: checkAllChains <account>")
                return
            account = argv[1]

            for peer in self.peers:
                self.sock.sendto(f"checkAllChainsSHA".encode('utf-8'), peer)
            # find the last block
            
            currentBlock = self.getLastBlock()
            
            f = open("{}.txt".format(currentBlock), "r")
            lines = f.readlines()
            # Sha256 of previous block: 41c56f28f5889a9734576090d1a2f3e527931fecc5d5db729aa2e3037c6c49da
            self.shaList.append(lines[0].split(": ")[1].strip())
            # receive other nodes' sha256
            print("waiting for sha256 from other nodes")
            while len(self.shaList) != len(self.peers)+1:
                time.sleep(1)
                print(f"wainting for sha256, current sha256: {self.shaList}")
                if len(self.shaList) == len(self.peers)+1:
                    break
            print("All sha256 received")
            # compare all sha256
            for sha in self.shaList:
                if sha != self.shaList[0]:
                    print("Blockchain is not consistent")
                    # clear shaList
                    self.shaList.clear()
                    return
            self.shaList.clear()
            print("Blockchain is consistent")
            os.system(f"/tmp/db/app_checkChain {account}")
            # send to other nodes to check local chain
            for peer in self.peers:
                self.sock.sendto(f"award {account} 5".encode('utf-8'), peer)
            print(f"check local chain {account}")
        elif argv[0] == "changeBlockSend":
            # get current block
            currentBlock = self.getLastBlock()
            print(f"currentBlock: {currentBlock}")
            blockData = []
            for i in range(1, currentBlock+1):
                f = open("{}.txt".format(i), "r")
                lines = f.readlines()
                blockData.append(lines)
            # encrypt the blockData
            hash_object = hashlib.sha256()
            hash_object.update(str(blockData).encode('utf-8'))
            # return the hash value to requester
            self.sock.sendto(f"changeBlockSHA {hash_object.hexdigest()}".encode('utf-8'), addr)
        elif argv[0] == "changeBlock":
            self.blockList.clear()
            for peer in self.peers:
                self.sock.sendto(f"changeBlockSend".encode('utf-8'), peer)
            
            # find the last block
            currentBlock = self.getLastBlock()
            print(f"currentBlock: {currentBlock}")
            blockData = []
            for i in range(1, currentBlock+1):
                f = open("{}.txt".format(i), "r")
                lines = f.readlines()
                blockData.append(lines)
            # encrypt the blockData
            hash_object = hashlib.sha256()
            hash_object.update(str(blockData).encode('utf-8'))
            # append nodeIP:hash to blockList
            self.blockList.append(f"{self.node}:{hash_object.hexdigest()}")
            
            while len(self.blockList) != len(self.peers)+1:
                time.sleep(1)
                print(f"waiting for block, current block: {self.blockList}")
                if len(self.blockList) == len(self.peers)+1:
                    break
            # sort the blockList according to split(":")[0]
            self.blockList.sort()
            # compare which is different from other nodes
            block1SHA = self.blockList[0].split(":")[1]
            block2SHA = self.blockList[1].split(":")[1]
            block3SHA = self.blockList[2].split(":")[1]
            block1Node = self.blockList[0].split(":")[0]
            block2Node = self.blockList[1].split(":")[0]
            block3Node = self.blockList[2].split(":")[0]
            if block1SHA == block2SHA and block1SHA != block3SHA:
                print("State1")
                print(f"{block3Node} is different from {block1Node} and {block2Node}, block3: {block3Node}")
                # send Data to block2Node to change block
                self.sock.sendto(f"removeData".encode('utf-8'), (block3Node, 8001))
                time.sleep(1)
                try:
                    os.system("rm -f /home/share/*.txt")
                except:
                    pass
                # copy all blockData to block2Node
                for i in range(1, currentBlock+1):
                    os.system(f"cp {i}.txt /home/share/")
                    print(f"cp {i}.txt /home/share/")
                self.sock.sendto(f"changeBlockData  {currentBlock}".encode('utf-8'), (block3Node, 8001))
                print("All blockData sent")
            
            elif block1SHA == block3SHA and block1SHA != block2SHA:
                print("State2")
                print(f"{block2Node} is different from {block1Node} and {block3Node}, block2: {block2Node}")
                # send Data to block2Node to change block
                self.sock.sendto(f"removeData".encode('utf-8'), (block2Node, 8001))
                time.sleep(1)
                try:
                    os.system("rm -f /home/share/*.txt")
                except:
                    pass
                # copy all blockData to block2Node
                for i in range(1, currentBlock+1):
                    os.system(f"cp {i}.txt /home/share/")
                    print(f"cp {i}.txt /home/share/")
                self.sock.sendto(f"changeBlockData  {currentBlock}".encode('utf-8'), (block2Node, 8001))
                print("All blockData sent")
                
            elif block2SHA == block3SHA and block1SHA != block3SHA:
                print("State3")
                print(f"{block1Node} is different from {block2Node} and {block3Node}, block1: {block1Node}")
                # send Data to block3Node to change block
                try:
                    os.system("rm -f /home/share/*.txt")
                    os.system("rm -f /tmp/db/*.txt")
                except:
                    pass
                # request blockData from other nodes
                self.sock.sendto(f"syncData".encode('utf-8'), (block2Node, 8001))
                    
                
            elif block1SHA == block2SHA == block3SHA:
                print("Blockchain is consistent")
            else:
                print("Blockchain is not consistent")
            self.blockList.clear()
        
        elif argv[0] == "removeData":
            try:
                os.system("rm -f *.txt")
            except:
                pass
        elif argv[0] == "checkAllChainsSHA":
            print("checkAllChainsSHA")
            currentBlock = self.getLastBlock()
            print(f"currentBlock: {currentBlock}")
            
            f = open("{}.txt".format(currentBlock), "r")
            lines = f.readlines()
            # Sha256 of previous block: 41c56f28f5889a9734576090d1a2f3e527931fecc5d5db729aa2e3037c6c49da
            sha = lines[0].split(": ")[1].strip()
            self.sock.sendto("checkAllChainsSHARecive {}".format(sha).encode('utf-8'), addr)
        elif argv[0] == "syncData":
            currentBlock = self.getLastBlock()
            # mv all block data to /home/share
            try:
                os.system("cp /tmp/db/*.txt /home/share/")
            except:
                pass
            self.sock.sendto("mvData".encode('utf-8'), addr)
        
        else:
            print("Invalid command")
            return
    
    def start(self):
        threading.Thread(target=self._listen).start()
        threading.Thread(target=self._send_messages).start()

    def _listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print(f"Received {data.decode('utf-8')} from {addr}")
            # if data contain checkAllChainsSHA, append sha256 to self.shaList
            if "checkAllChainsSHARecive" in data.decode('utf-8'):
                sha = data.decode('utf-8').split()[1]
                self.shaList.append(sha)
                continue
            if "changeBlockSHA" in data.decode('utf-8'):
                block = data.decode('utf-8').split()[1]
                # append nodeIP:hash to blockList
                self.blockList.append(f"{addr[0]}:{block}")
                continue
            if "mvData" in data.decode('utf-8'):
                print("Sync data successfully")
                try:
                    os.system("mv /home/share/*.txt /tmp/db/")
                except:
                    pass
                continue
            if data.decode('utf-8').split()[0] == "changeBlockData":
                # mv all block data to /tmp/db
                try:
                    os.system("mv /home/share/*.txt /tmp/db/")
                except:
                    pass
                continue
            self.cmdParser(data.decode('utf-8').split(), addr)
            print("cmd: 'checkMoney, checkLog, transaction, checkChain, checkAllChains changeBlock'")

    def _send_messages(self):
        while True:
            # print defined cmd
            print("cmd: 'checkMoney, checkLog, transaction, checkChain, checkAllChains changeBlock'")
            message = input("Enter a command: ")

            argv = message.split()
            self.cmdParser(argv, None)
        

if __name__ == '__main__':
    port = 8001 #本節點的port 
    peers = [('172.17.0.20', 8001), ('172.17.0.21', 8001)]  #跟另外二個IP:8001 節點通信
    node = P2PNode(port, peers)
    node.start()

