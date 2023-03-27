class Dino:
    def __init__(self, name, lvl=0, amount=0, rarity=''):
        self.name = name
        self.lvl = lvl
        self.amount = amount
        self.rarity = rarity
        self.first = None
        self.second = None

    def updateInfo(self, newDNA, newLvl, newRarity):
        self.amount = newDNA
        self.lvl = newLvl
        self.rarity = newRarity

    def setFirst(self, first):
        self.first = first

    def setSecond(self, second):
        self.second = second

    def getName(self):
        return self.name

    def getLvl(self):
        return self.lvl

    def getDNA(self):
        return self.amount

    def getRarity(self):
        return self.rarity
    
    def activationLvl(self):
        return 5*self.rarityRank()
    
    def activationDNA(self):
        return 50*(self.rarityRank()+1)

    def rarityRank(self):
        if self.rarity == "C":
            return 0
        if self.rarity == "R":
            return 1
        if self.rarity == "E":
            return 2
        if self.rarity == "L":
            return 3
        if self.rarity == "U":
            return 4
        if self.rarity == "A":
            return 5
        return 0

    def DNAforLvl(self, lvl):
        diff = lvl - self.activationLvl()
        if diff == 1:
            return (self.rarityRank()+1)*50
        if diff < 7:
            return (50*diff)+50
        if diff < 8:
            return (100*diff)-300
        if diff < 12:
            return (250*diff)-1500
        if diff < 16:
            return (500*diff)-4500
        return 10*self.DNAforLvl(lvl-10)
    
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