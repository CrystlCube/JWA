class Dino:
    """
    A class that keeps track of a dinosaur and all its needed information
    ...

    Attributes
    ----------
    name : str
        The name of the dinosaur
    lvl : int
        The level of the dinosaur
    amount : int
        The amount of DNA the dinosaur currently has
    rarity : str
        The rarity of the dinosaur represented as the first letter of the rarity (e.g. Epic -> E)
    first : str
        The name of the first parent of the dinosaur (can be None)
    second : str
        The name of the second parent of the dinosaur (can be None)

    Methods
    -------
    set_parents()
        Set first and second equal to the specified parent names
    is_hybrid()
        Returns whether or not the dino is a hybrid (i.e. has parents)
    parent_to_string()
        Returns a dino's parental information as a string
    to_string()
        Returns a dino's information as a string

    """
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
                First parent of dinosaur (str) (optional)
                Second parent of dinosaur (str) (optional)
        """
        if len(data_list) == 4:
            self.name, self.lvl, self.amount, self.rarity = data_list
            self.first = None
            self.second = None
        else:
            self.name, self.lvl, self.amount, self.rarity, self.first, self.second = data_list
        self.lvl = int(self.lvl)
        self.amount = int(self.amount)

    # def updateInfo(self, newDNA, newLvl, newRarity):
    #     self.amount = newDNA
    #     self.lvl = newLvl
    #     self.rarity = newRarity

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

    def is_hybrid(self) -> bool:
        """
        Returns whether the current dino is a hybrid or not by checking if it has a parent

        Returns
        -------
        bool
            Whether or not the current dino is a hybrid
        """
        return bool(self.first)

    # def getName(self):
    #     return self.name

    # def getLvl(self):
    #     return self.lvl

    # def getDNA(self):
    #     return self.amount

    # def getRarity(self):
    #     return self.rarity
    
    # def activationLvl(self):
    #     return 5*self.rarityRank()
    
    # def activationDNA(self):
    #     return 50*(self.rarityRank()+1)

    # def rarityRank(self):
    #     if self.rarity == "C":
    #         return 0
    #     if self.rarity == "R":
    #         return 1
    #     if self.rarity == "E":
    #         return 2
    #     if self.rarity == "L":
    #         return 3
    #     if self.rarity == "U":
    #         return 4
    #     if self.rarity == "A":
    #         return 5
    #     return 0

    # def DNAforLvl(self, lvl):
    #     diff = lvl - self.activationLvl()
    #     if diff == 1:
    #         return (self.rarityRank()+1)*50
    #     if diff < 7:
    #         return (50*diff)+50
    #     if diff < 8:
    #         return (100*diff)-300
    #     if diff < 12:
    #         return (250*diff)-1500
    #     if diff < 16:
    #         return (500*diff)-4500
    #     return 10*self.DNAforLvl(lvl-10)
    
    # def toString(self, depth):
    #     indent = ''
    #     for i in range(depth):
    #         indent += '\t'
    #     print(indent + self.name + ':')
    #     print(indent + '\tLevel: ' + self.lvl)
    #     print(indent + '\tAmount of DNA: ' + self.amount)
    #     print(indent + '\tRarity: ' + self.rarity)
    #     print()
    #     if (self.first):
    #         print(indent + 'Parents:')
    #         self.first.toString(depth + 1)
    #         self.second.toString(depth + 1)

    def parent_to_string(self) -> str:
        """
        Returns a string representing the dinosaur's relation to its parents
        Only is supposed to be called for dinosaurs with parents

        Returns
        -------
        str
            A string containing the dinosaur, a colon, and the dinosaur's two parents
        """
        return self.name + ': ' + self.first + ' ' + self.second

    def to_string(self) -> str:
        """
        Returns a string representing the dinosaur's information

        Returns
        -------
        str
            A string containing the dinosaur's name, level, amount of DNA, and its rarity
        """
        return self.name + ' ' + self.lvl + ' ' + self.amount + ' ' + self.rarity