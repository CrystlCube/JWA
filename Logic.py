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
            total_DNA = self.get_total_DNA(dino_name, dino.activation_level(), dino.activation_amount(), True)
            current_DNA = self.get_total_DNA(dino_name, dino.lvl, 0, False)
            for key in total_DNA:
                total_dict[key] += max(total_DNA[key] - current_DNA[key], 0)
        return total_dict

    def get_total_DNA(self, dino_name: str, needed_lvl: int, added_amount: int, aiming_for: bool):
        """
        Given the dinosaur name, this functions returns all dinosaur DNA amounts needed to get the dinosaur to the needed level with that added amount
        The aiming_for bool distinguishes two different types of behavoir:
            When aiming_for == True:
                This function accounts for having to upgrade each dino to the correct level to count towards creating hybrid DNA
            When aiming_for == False:
                This function doesn't account for the above, so it is used more to calculate "This much DNA of X is equivalent to how much DNA of Y"
        Parameters
        ----------
        dino : str
            The name of the dinosaur for which you need the total DNA amount
        needed_lvl : int
            The level at which the dinosaur needs to be
        added_amount : int
            The additional DNA that will be needed for the dinosaur
        aiming_for : bool
            Described in the function documentation
        """
        dino = self.current_dinos[dino_name]
        amount = added_amount + (dino.get_amount() if not aiming_for else 0)
        amount += dino.DNA_to_certain_level(dino.activation_level(), needed_lvl)

        if not dino.is_hybrid():
            return {dino_name: amount} if amount > 0 and dino.get_level() != dino.activation_level() else {}
        else:
            full_dict = defaultdict(lambda: 0)
            p1 = self.current_dinos[dino.first]
            p1_rank_diff = (dino.rarity_rank()-p1.rarity_rank())
            p1_cost_per_fuse = 10*(5 if p1_rank_diff%2 else 2)*10**int(p1_rank_diff/2)
            p1_amount = p1_cost_per_fuse*math.ceil(amount/DNA_PER_FUSE)
            p1_results = self.get_total_DNA(dino.first, (dino.activation_level() if aiming_for else min(p1.lvl, dino.activation_level())), p1_amount, aiming_for)
            for key in p1_results:
                full_dict[key] += p1_results[key]
            
            p2 = self.current_dinos[dino.second]
            p2_rank_diff = (dino.rarity_rank()-p2.rarity_rank())
            p2_cost_per_fuse = 10*(5 if p2_rank_diff%2 else 2)*10**int(p2_rank_diff/2)
            p2_amount = p2_cost_per_fuse*math.ceil(amount/DNA_PER_FUSE)
            p2_results = self.get_total_DNA(dino.second, (dino.activation_level() if aiming_for else min(p2.lvl, dino.activation_level())), p2_amount, aiming_for)
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
                    total_DNA = self.get_total_DNA(dino_name, dino.activation_level(), dino.activation_amount(), True)
                    current_DNA = self.get_total_DNA(dino_name, dino.lvl, 0, False)
                    max = 0
                    max_dino = ""
                    for root in total_DNA:
                        p = total_DNA[root] - current_DNA[root]
                        if p > max:
                            max = p
                            max_dino = root
                    if max != 0:
                        percentages[dino_name] = (max_dino, max)

            for i in sorted(percentages, key = lambda x: percentages[x][1]):
                output_string += i + ": " + percentages[i][0] + ", " + str(percentages[i][1]) + ", " + self.current_dinos[percentages[i][0]].rarity + "\n"
        
        return output_string
    
    def get_percentages(self) -> str:
        """
        TODO
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
                    total_DNA = self.get_total_DNA(dino_name, dino.activation_level(), dino.activation_amount(), True)
                    current_DNA = self.get_total_DNA(dino_name, dino.lvl, 0, False)
                    min = 1
                    min_dino = dino_name
                    for root in total_DNA:
                        p = current_DNA[root]/total_DNA[root]
                        if p < min:
                            min = p
                            min_dino = root
                    percentages[dino_name] = (min_dino, min)

            for i in sorted(percentages, reverse=True, key = lambda x: percentages[x][1]):
                output_string += i + ": " + percentages[i][0] + ", " + str(percentages[i][1]) + ", " + self.current_dinos[percentages[i][0]].rarity + "\n"
        
        return output_string



if __name__=='__main__':
    current_dinos, needed_dinos = FileFunctions.create_dino_info()
    x = Logic(current_dinos, needed_dinos)
    print(x.get_tags())
    print(x.DNA_still_needed())
    print(x.get_percentages())