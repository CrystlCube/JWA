from Dino import Dino
import FileFunctions
import math
from collections import defaultdict

DNA_PER_FUSE = 20

class Logic:
    """
    A class for getting dinosaur information

    Attributes
    ----------
    current_dinos : dict[str : Dino]
        A mapping of dinosaur names to the corresponding Dino objects
    needed_dinos : set[str]
        A set of names of dinosaurs that need to be unlocked
    
    Methods
    -------
    get_total_DNA()
        Returns the total DNA needed (including via fusing) to get a certain dino to a certain level

    """
    def __init__(self, c_dinos: dict[str: Dino], n_dinos: set[str]) -> None:
        """
        Initializes the Logic class with the given current and needed dinos
        
        Parameters
        ----------
        c_dinos: dict[str: Dino]
            A dictionary that stores keys as names of current dinosaurs, and the values as the corresponding Dino objects
        n_dinos: set[str]
            A set of needed dinosaur names
        """
        self.current_dinos = c_dinos
        self.needed_dinos = n_dinos

        self.total_needed_DNA = self.determine_all_needed_DNA()

        # for dino in self.current_dinos:
        #     if dino in self.total_needed_DNA and self.total_needed_DNA[dino] > 0:
        #         print(dino + ": blue " + str(self.total_needed_DNA[dino]))
        #     elif self.current_dinos[dino].get_level() != self.current_dinos[dino].activation_level():
        #         print(dino + ": orange")
        for key in sorted(self.total_needed_DNA, key = lambda x: self.current_dinos[x].rarity_rank()*1000000+self.total_needed_DNA[x]):
            print(key, self.total_needed_DNA[key])

    def determine_all_needed_DNA(self):
        total_dict = defaultdict(lambda: 0)
        for dino_name in self.needed_dinos:
            dino = self.current_dinos[dino_name]
            results = self.get_total_DNA(dino_name, dino.activation_level(), dino.activation_amount())
            for key in results:
                total_dict[key] += results[key]
        return total_dict

    def get_total_DNA(self, dino_name: str, needed_lvl: int, added_amount):
        """
        Parameters
        ----------
        dino : str
            The name of the dinosaur for which you need the total DNA amount
        needed_lvl : int
            The level at which the dinosaur needs to be
        added_amount : int
            The additional DNA that will be needed for the dinosaur
        """
        dino = self.current_dinos[dino_name]
        amount = added_amount - dino.get_amount()
        if dino.get_level() < needed_lvl:
            amount += dino.DNA_to_certain_level(needed_lvl)
        if not dino.is_hybrid():
            return {dino_name: amount} if amount > 0 and dino.get_level() != dino.activation_level() else {}
        else:
            full_dict = defaultdict(lambda: 0)
            if amount > 0:
                # if dino.get_level() != dino.activation_level():
                #     full_dict[dino_name] = 0
                p1 = self.current_dinos[dino.first]
                p1_rank_diff = (dino.rarity_rank()-p1.rarity_rank())
                p1_cost_per_fuse = 10*(5 if p1_rank_diff%2 else 2)*10**int(p1_rank_diff/2)
                p1_amount = p1_cost_per_fuse*math.ceil(amount/DNA_PER_FUSE)
                p1_results = self.get_total_DNA(dino.first, dino.activation_level(), p1_amount)
                for key in p1_results:
                    full_dict[key] += p1_results[key]
                
                p2 = self.current_dinos[dino.second]
                p2_rank_diff = (dino.rarity_rank()-p2.rarity_rank())
                p2_cost_per_fuse = 10*(5 if p2_rank_diff%2 else 2)*10**int(p2_rank_diff/2)
                p2_amount = p2_cost_per_fuse*math.ceil(amount/DNA_PER_FUSE)
                p2_results = self.get_total_DNA(dino.second, dino.activation_level(), p2_amount)
                for key in p2_results:
                    full_dict[key] += p2_results[key]
            return full_dict
            


# def getDNAandCost(dino):
#     if dino in recipes:
#         p1, p2 = recipes[dino]
#         p1DNA, p1Cost = getDNAandCost(p1)
#         p1Fuses = math.floor(p1DNA/DNAforEachFuse(dinos[p1], dinos[dino]))
#         p2DNA, p2Cost = getDNAandCost(p2)
#         p2Fuses = math.floor(p2DNA/DNAforEachFuse(dinos[p2], dinos[dino]))
#         rR = dinos[dino].rarityRank()
#         costPerFuse = 10*(2 if rR%2 else 1)*10**int(rR/2)
#         minFuses = min(p1Fuses, p2Fuses)
#         totalFuseCost = minFuses*costPerFuse
#         return DNA_PER_FUSE*minFuses+dinos[dino].getDNA(), p1Cost+p2Cost+totalFuseCost
#     return dinos[dino].getDNA(), 0

if __name__=='__main__':
    """
    Executes the following steps
        1. Grabs dinosaur information from the database
        2. 
    """
    current_dinos, needed_dinos = FileFunctions.create_dino_info()
    x = Logic(current_dinos, needed_dinos)
   