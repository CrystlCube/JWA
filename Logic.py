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
        Returns the total DNA needed to get the specified dino to the indicated level
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
            
    # RESULTS FUNCTIONS -------------------------------------------------------------------------

    def determine_tag(self, dino_name: str) -> None:
        """
        Determines and assigns the tag for the dinosaur specified based on the previous criteria, along with the following:
            A hybrid will have an orange tag if both of its parents also have an orange tag

        Parameters
        ----------
        dino_name : str
            The name of the dinosaur you want the tag for
        """
        
        if dino_name in self.tags:
            return
        dino = self.current_dinos[dino_name]
        if dino.is_hybrid():
            p1, p2 = dino.get_parents()
            self.determine_tag(p1)
            self.determine_tag(p2)
            if self.tags[p1] == "orange" and self.tags[p2] == "orange":
                self.tags[dino_name] = "orange"
            else:
                self.tags[dino_name] = "blue"
        
        else:
            self.tags[dino_name] = "blue" if self.total_needed_DNA[dino_name] > 0 else "orange"


    def get_tags(self) -> str:
        """
        Prints out each unlocked dinosaur and its tag according to the following conditions:
            Blue: Does not currently have enough DNA to create all its hybrids
            Orange: Has enough DNA to create all its hybrids

        Results
        ----------
        str
            An output of all dinosaurs and their tags in the following format:
                dino_name1: tag_color
                dino_name2: tag_color
                ...
        """

        self.tags = {}
        for dino in self.current_dinos:
            if dino not in self.needed_dinos:
                self.determine_tag(dino)

        output_string = ""
        for dino_name in sorted(self.tags):
            if self.tags[dino_name] == "orange":
                output_string += dino_name + ": " + self.tags[dino_name] + "\n"

        return output_string

    def DNA_still_needed(self) -> str:
        """
        Prints out each blue root dinosaur (see tags) and how much DNA is still required to get it

        Results
        ----------
        str
            An output of all dinosaurs and the amount of DNA still required to get in the following format:
                dino_name1: amount
                dino_name2: amount
                ...
        """

        output_string = ""
        rarities = ["Common", "Rare", "Epic", "Legendary", "Unique"]
        for rarity_id in range(5):
            output_string += "\n" + rarities[rarity_id] + "\n"
            dinos = sorted([dino_name for dino_name in self.current_dinos 
                            if self.current_dinos[dino_name].rarity_rank() == rarity_id and self.total_needed_DNA[dino_name] > 0],
                            key = lambda x: self.total_needed_DNA[x])
            for dino_name in dinos:
                output_string += dino_name + ": " + str(self.total_needed_DNA[dino_name]) + "\n"

        return output_string
    
    def get_completion_percentage(self) -> str:
        """
        Prints out each needed dinosaur and its completion percentage
        Completion percentage is calculated via the following method:


        Results
        ----------
        str
            An output of all needed dinosaurs and their completion percentage in the following format:
                dino_name1: percentage
                dino_name2: percentage
                ...
        """
            

    def helper(self, dino_name, amount):
        dino = self.current_dinos[dino_name]
        if dino.is_hybrid():
            full_dict = defaultdict(lambda: 0)
            p1 = self.current_dinos[dino.first]
            p1_rank_diff = (dino.rarity_rank()-p1.rarity_rank())
            p1_cost_per_fuse = 10*(5 if p1_rank_diff%2 else 2)*10**int(p1_rank_diff/2)
            p1_amount = p1_cost_per_fuse*math.ceil(amount/DNA_PER_FUSE)
            p1_results = self.helper(p1.name, p1_amount)
            for key in p1_results:
                full_dict[key] += p1_results[key]

            p2 = self.current_dinos[dino.second]
            p2_rank_diff = (dino.rarity_rank()-p2.rarity_rank())
            p2_cost_per_fuse = 10*(5 if p2_rank_diff%2 else 2)*10**int(p2_rank_diff/2)
            p2_amount = p2_cost_per_fuse*math.ceil(amount/DNA_PER_FUSE)
            p2_results = self.helper(p2.name, p2_amount)
            for key in p2_results:
                full_dict[key] += p2_results[key]


        else:
            return {dino_name: amount}
        
# 100 -> 100/20 * diff

if __name__=='__main__':
    current_dinos, needed_dinos = FileFunctions.create_dino_info()
    x = Logic(current_dinos, needed_dinos)
    print(x.get_tags())
    #print(x.DNA_still_needed())
   