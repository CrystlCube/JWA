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
        self.new_dino_levels = {}

        self.total_needed_DNA = self.determine_all_needed_DNA()

    def determine_all_needed_DNA(self):
        total_dict = defaultdict(lambda: 0)
        for dino_name in self.needed_dinos:
            dino = self.current_dinos[dino_name]
            needed_DNA = self.get_total_DNA(dino_name, dino.activation_level(), 0)
            for key in needed_DNA:
                total_dict[key] += needed_DNA[key]
        return total_dict
    
    def get_parent_amount(self, parent_name: str, child_name: str, child_amount: int):
        child = self.current_dinos[child_name]
        parent = self.current_dinos[parent_name]
        p1_rank_diff = (child.rarity_rank()-parent.rarity_rank())
        p1_cost_per_fuse = 10*(5 if p1_rank_diff%2 else 2)*10**int(p1_rank_diff/2)
        return p1_cost_per_fuse*math.ceil(child_amount/DNA_PER_FUSE)
           
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
                p1_amount = self.get_parent_amount(dino.first, dino, amount)
                p1_results = self.get_total_DNA(dino.first, dino.activation_level(), p1_amount)
                for key in p1_results:
                    full_dict[key] += p1_results[key]

                p2_amount = self.get_parent_amount(dino.second, dino, amount)
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
        for rarity_id in range(len(rarities)):
            output_string += "\n" + rarities[rarity_id] + "\n"
            dinos = sorted([dino_name for dino_name in self.current_dinos 
                            if self.current_dinos[dino_name].rarity_rank() == rarity_id and self.total_needed_DNA[dino_name] > 0],
                            key = lambda x: self.total_needed_DNA[x])
            for dino_name in dinos:
                output_string += dino_name + ": " + str(self.total_needed_DNA[dino_name]) + "\n"

        return output_string
    
    def get_limiting_factors(self) -> str:
        """
        Prints out each needed dinosaur and its limiting factor, i.e. the dinosaur that needs the most DNA to reach activation

        Results
        ----------
        str
            An output of all needed dinosaurs and their limitingfactor in the following format:
                dino_name1: limiting_factor (amount, name)
                dino_name2: limiting_factor (amount, name)
                ...
        """
        output_string = ""
        rarities = ["Common", "Rare", "Epic", "Legendary", "Unique", "Apex"]
        for rarity_id in range(len(rarities)):
            output_string += "\n" + rarities[rarity_id] + "\n"
            percentages = {}
            for dino_name in self.needed_dinos:
                dino = self.current_dinos[dino_name]
                if dino.rarity_rank() == rarity_id:
                    max = 0
                    max_dino = ""
                    for root in self.total_needed_DNA:
                        p = self.total_needed_DNA[root]
                        if p > max:
                            max = p
                            max_dino = root
                    if max != 0:
                        percentages[dino_name] = (max_dino, max)

            for i in sorted(percentages, key = lambda x: percentages[x][1]):
                output_string += i + ": " + percentages[i][0] + ", " + str(percentages[i][1]) + ", " + self.current_dinos[percentages[i][0]].rarity + "\n"
        
        return output_string
    
    # def get_percentages(self) -> str:
    #     """
    #     TODO
    #     Prints out each needed dinosaur and its limiting factor, i.e. the dinosaur that needs the most DNA to reach activation

    #     Results
    #     ----------
    #     str
    #         An output of all needed dinosaurs and their limitingfactor in the following format:
    #             dino_name1: limiting_factor (amount, name)
    #             dino_name2: limiting_factor (amount, name)
    #             ...
    #     """
    #     output_string = ""
    #     rarities = ["Common", "Rare", "Epic", "Legendary", "Unique", "Apex"]
    #     for rarity_id in range(len(rarities)):
    #         output_string += "\n" + rarities[rarity_id] + "\n"
    #         percentages = {}
    #         for dino_name in self.needed_dinos:
    #             dino = self.current_dinos[dino_name]
    #             if dino.rarity_rank() == rarity_id:
    #                 total_DNA = self.get_total_DNA(dino_name, dino.activation_level(), dino.activation_amount(), True)
    #                 current_DNA = self.get_total_DNA(dino_name, dino.lvl, 0, False)
    #                 min = 1
    #                 min_dino = dino_name
    #                 for root in total_DNA:
    #                     p = current_DNA[root]/total_DNA[root]
    #                     if p < min:
    #                         min = p
    #                         min_dino = root
    #                 percentages[dino_name] = (min_dino, min)

    #         for i in sorted(percentages, reverse=True, key = lambda x: percentages[x][1]):
    #             output_string += i + ": " + percentages[i][0] + ", " + str(percentages[i][1]) + ", " + self.current_dinos[percentages[i][0]].rarity + "\n"
        
    #     return output_string



if __name__=='__main__':
    current_dinos, needed_dinos = FileFunctions.create_dino_info()
    x = Logic(current_dinos, needed_dinos)
    print(x.get_tags())
    print(x.DNA_still_needed())
    #print(x.get_percentages())