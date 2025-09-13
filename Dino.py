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
    TODO

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

    def get_name(self) -> str:
        """
        Returns the name of the dino

        Returns
        -------
        str
            The name of the dino
        """
        return self.name

    def get_level(self) -> int:
        """
        Returns the current level of the dino

        Returns
        -------
        int
            The current level of the dino
        """
        return self.lvl

    def get_amount(self) -> int:
        """
        Returns the amount of DNA the dino currently has

        Returns
        -------
        int
            The DNA amount of the dino
        """
        return self.amount
    
    def set_level(self, lvl):
        """
        Sets the current level of the dino given the input

        Parameters
        ----------
        lvl: int
            The new level of the dino
        """
        self.lvl = lvl
    
    def set_amount(self, amount):
        """
        Sets the current level of the dino given the input

        Parameters
        ----------
        lvl: int
            The new level of the dino
        """
        self.amount = amount

    def get_rarity(self):
        return self.rarity
    
    def activation_level(self):
        """
        Returns the level the dinosaur is at before it is unlocked (one below the first level)
        For instance, for a Unique dinosaur, the activation level is 20

        Returns
        -------
        int
            The prequisite level
        """
        return 5*self.rarity_rank()
    
    def activation_amount(self) -> int:
        """
        Returns the amount of DNA required to unlock the dino
        This amount follows a linear scale dependent on the rarity of the dino

        Returns
        -------
        int
            The amount of DNA needed
        """
        return 50*(self.rarity_rank()+1)

    def rarity_rank(self) -> int:
        """
        Returns a integer value of the rarity, with Apex being highest at 5, and Common being lowest at 0

        Returns
        -------
        int
            The integer value of the rarity
        """
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

    def DNA_for_one_lvl(self, lvl):
        """
        Returns the amount of DNA required at a given level to level up

        Parameters
        ----------
        lvl : int
            The hypothetical level the dinosaur is at 
    
        Returns
        -------
        int
            The amount of DNA required to level up
        """
        
        diff = lvl - self.activation_level()
        if diff == 0:
            return self.activation_amount()
        if diff < 8:
            return (50*diff)+50
        if diff < 9:
            return (100*diff)-300
        if diff < 13:
            return (250*diff)-1500
        if diff < 17:
            return (500*diff)-4500
        return 10*self.DNA_for_one_lvl(lvl-10)
    
    def DNA_to_certain_level(self, start_level, final_level):
        """
        Returns the amount of DNA needed to get the dino to a certain level from a specified level

        Parameters
        ----------
        lvl : int
            The level the dinosaur needs to get to
    
        Returns
        -------
        int
            The amount of DNA required to reach the given level
        """
        total_amount = 0
        level = start_level
        while level < final_level:
            total_amount += self.DNA_for_one_lvl(level)
            level += 1
        return total_amount
    
    def get_parents(self) -> list[str]:
        return [self.first, self.second]
    
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
        return self.name + ' ' + str(self.lvl) + ' ' + str(self.amount) + ' ' + self.rarity
    
# Leveling Up Costs (for DNA)
# Taken in difference from activation level
# 1: 100
# 2: 150
# 3: 200
# 4: 250
# 5: 300
# 6: 350
# 7: 400
# 8: 500
# 9: 750
# 10: 1000
# 11: 1250
# 12: 1500
# 13: 2000
# 14: 2500
# 15: 3000
# 16: 3500
# 17: 4000
# 18: 5000?
# 19: 7500?
# 20: 10000
