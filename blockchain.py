import hashlib
import json


class Block:
    def __init__(self, timestamp, data, previousHash=""):
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.hash = self.calculateHash()

    def calculateHash(self):
        if isinstance(self.previousHash, str):
            self.previousHash = self.previousHash.encode()
        data = (
            self.previousHash + self.timestamp.encode() + json.dumps(self.data).encode()
        )
        return hashlib.sha256(data).digest()



class Blockchain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()]

    def createGenesisBlock(self):
        print("Creating genesis block")
        return Block("2017-01-01", [], "0")

    def getLatestBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        block.previousHash = self.getLatestBlock().hash
        block.hash = block.calculateHash()
        self.chain += [block]
        print("Added new block:", block.hash)

    def isChainValid(self):
        print("Checking chain validity..")
        realGenesis = self.createGenesisBlock()

        if realGenesis.hash != self.chain[0].hash:
            print("Hash of genesis is not reproducible:", self.chain[0].hash)
            return False

        print("Chain has", len(self.chain), "blocks")
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]

            if previousBlock.hash != currentBlock.previousHash:
                print(
                    "Hash of prev block not the same as previousHash of current block at block number",
                    i,
                )
                return False

            if currentBlock.hash != currentBlock.calculateHash():
                print("Current block hash is not reproducible at block number", i)
                return False

        print("** Chain is valid **")
        return True


supercoin = Blockchain()
print("Ledger length:",len(supercoin.chain))
print("First block:",supercoin.chain[0].data, supercoin.chain[0].timestamp)

b = Block("2023-01-01", "A send B20 to D")
supercoin.addBlock(b)

print('prevHash of second block',supercoin.chain[1].previousHash)
print('Hash of first block',supercoin.chain[0].hash)
# supercoin.addBlock(Block("2023-01-02", "F sends B40 to G"))

# print(supercoin.isChainValid())



b = Block("2024-01-01", "D send B30 to E")
supercoin.addBlock(b)


print('prevHash of third block',supercoin.chain[2].previousHash)
print('Hash of second block',supercoin.chain[1].hash)

supercoin.chain[1].data += "."
supercoin.chain[1].hash = supercoin.chain[1].calculateHash()
print('Hash of second block after tamperting',supercoin.chain[1].hash)