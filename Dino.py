class Dino:
    def __init__(self, name, lvl=0, amount=0, rarity=''):
        self.name = name
        self.lvl = lvl
        self.amount = amount
        self.rarity = rarity
        self.first = None
        self.second = None

    def updateInfo(self, newDNA, newLvl, newRarity):
        self.currentDNA = newDNA
        self.currentLvl = newLvl
        self.rarity = newRarity

    def setFirst(self, first):
        self.first = first

    def setSecond(self, second):
        self.second = second

    def getName(self):
        return self.name

    def getLvl(self):
        return self.lvl
    
    def activationLVL(self):
        if self.rarity == "C":
            return 0
        if self.rarity == "R":
            return 5
        if self.rarity == "E":
            return 10
        if self.rarity == "L":
            return 15
        if self.rarity == "U":
            return 20
        if self.rarity == "A":
            return 25
        return 0

    def DNAforLVL(self, lvl):
        diff = lvl - self.activationLVL()
        if diff < 7:
            return (50*diff)+50
        if diff < 8:
            return (100*diff)-300
        if diff < 12:
            return (250*diff)-1500
        if diff < 15:
            return (500*diff)-4500

    def enoughForNextLVL(self):
        return self.DNAforLVL(self.currentLvl+1) >= self.currentDNA

    def getHighestPossibleLVL(self):
        tempDNA = self.currentDNA
        lvl = self.lvl
        while tempDNA >= 0:
            tempDNA -= self.DNAforLVL(lvl)
            lvl += 1

        return lvl-1
    
    def toString(self, depth):
        indent = ''
        for i in range(depth):
            indent += '\t'
        print(indent + self.name + ':')
        print(indent + '\tLevel: ' + self.lvl)
        print(indent + '\tAmount of DNA: ' + self.amount)
        print(indent + '\tRarity: ' + self.rarity)
        print()
        if (self.first):
            print(indent + 'Parents:')
            self.first.toString(depth + 1)
            self.second.toString(depth + 1)

    def toFile(self):
        dinoInfo = self.name + ' ' + self.lvl + ' ' + self.amount + ' ' + self.rarity
        return dinoInfo