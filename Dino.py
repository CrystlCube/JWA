class Dino:
    def __init__(self, name, lvl=0, amount=0, rarity='', first=None, second=None):
        self.name = name
        self.lvl = lvl
        self.amount = amount
        self.rarity = rarity
        self.first = first
        self.second = second

    def __init__(self, data_list: list) -> None:
        """
        Initializes a dino with the given data

        Parameters
        ----------
        data_list : list
            A list of data for the dino, formatted as:
                Dinosaur name (str)
                Level of dinosaur (int)
                Amount of DNA (int)
                Rarity of dinosaur (str)
        """
        self.name, self.lvl, self.amount, self.rarity = data_list
        self.lvl = int(self.lvl)
        self.amount = int(self.amount)
        self.first = None
        self.second = None

    def updateInfo(self, newDNA, newLvl, newRarity):
        self.amount = newDNA
        self.lvl = newLvl
        self.rarity = newRarity

    def set_parents(self, parents: tuple[str, str]) -> None:
        """
        Sets the parents of the current dino
        
        Parameters
        ----------
        parents : tuple[str, str]
            The names of the two parents, stored as strings in a tuple
        """
        
        self.first = parents[0]
        self.second = parents[1]

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