from Dino import Dino
from HistoryPlotting import HistoryPlotting
import FileFunctions
import math
from collections import Counter, defaultdict
from collections import Counter, defaultdict

DNA_PER_FUSE = 20

class DNAAnalytics:
    """
    A class for manipulating and analyzing dinosaur DNA

    Attributes
    ----------
    current_dinos : dict[str : Dino]
        A current collection of dinosaur names mapped to their corresponding Dino objects
    needed_dinos : set[str]
        A set of names of dinosaurs that need to be unlocked
    updated_levels : dict[str : int]
        A mapping of dinosaur names to a level; used for one dinosaur being used for multiple descendants
    updated_amounts : dict[str : int]
        A mapping of dinosaur names to an amount; used for one dinosaur being used for multiple descendants
    ancestors : dict[str : set[str]]
        A mapping of each needed dinosaur to a set of its ancestors
    history : HistoryPlotting
        A class instantiation to keep track of amount history
    tags : dict[str : str]
        A mapping of dinosaur names to their tag color
    total_needed_DNA : dict[str : int]
        A mapping of dinosaur names to amounts of DNA needed to unlock all needed dinosaurs
    """

    def __init__(self, c_dinos: dict[str: Dino], n_dinos: set[str]) -> None:
        """
        Initializes class variables and calculates all needed DNA
        
        Parameters
        ----------
        c_dinos : dict[str : Dino]
            A current collection of dinosaur names mapped to their corresponding Dino objects
        n_dinos : set[str]
            A set of names of dinosaurs that need to be unlocked
        """
        self.current_dinos = c_dinos
        self.needed_dinos = n_dinos
        self.updated_levels = self.get_default_levels()
        self.updated_amounts = self.get_default_amounts()
        self.ancestors = self.get_all_ancestors()
        self.history = HistoryPlotting()

        self.total_needed_DNA = self.determine_all_needed_DNA()

    # NEEDED DNA FUNCTIONS -------------------------------------------------------------------------

    def get_default_levels(self) -> dict[str : int]:
        """
        Returns a mapping of dinosaur names to their current level

        Returns
        -------
        dict[str : int]
            A mapping of dinosaur names to their current level
        """
        default_levels = {}
        for dino_name in self.current_dinos:
            dino = self.current_dinos[dino_name]
            default_levels[dino_name] = dino.get_level()
        return default_levels
    
    def get_default_amounts(self) -> dict[str : int]:
        """
        Returns a mapping of dinosaur names to their current amount

        Returns
        -------
        dict[str : int]
            A mapping of dinosaur names to their current amount
        """
        default_amounts = {}
        for dino_name in self.current_dinos:
            dino = self.current_dinos[dino_name]
            default_amounts[dino_name] = dino.get_amount()
        return default_amounts
    
    def calculate_parent_amount(self, parent_name: str, child_name: str, child_amount: int) -> int:
        """
        Given the amount of DNA for the child provided, this function calculates the amount of parent DNA needed

        Parameters
        ----------
        parent_name : str
            The name of the parent dinosaur
        child_name : str
            The name of the child dinosaur
        child_amount : int
            The amount of child DNA required

        Returns
        -------
        int
            The amount of parent DNA needed to get the required child DNA
        """
        child = self.current_dinos[child_name]
        parent = self.current_dinos[parent_name]
        parent_rank_diff = (child.rarity_rank()-parent.rarity_rank())
        parent_cost_per_fuse = 10*(5 if parent_rank_diff%2 else 2)*10**int(parent_rank_diff/2)
        return parent_cost_per_fuse*math.ceil(child_amount/DNA_PER_FUSE)
           
    def get_needed_DNA(self, dino_name: str, needed_level: int, needed_amount: int) -> dict[str : int]:
        """
        Returns the total DNA needed to get the specified dinosaur to the indicated level

        Parameters
        ----------
        dino_name : str
            The name of the dinosaur for which you need the total DNA amount
        needed_level : int
            The level at which the dinosaur needs to be
        needed_amount : int
            Any additional DNA that will be needed for the dinosaur

        Returns
        -------
        dict[str : int]
            A mapping of dinosaur names to the total DNA needed to get the specified dinosaur to the indicated level
        """
        dino = self.current_dinos[dino_name]
        # if dino_name == 'Velociraptor':
        #     pass

        # Account for the DNA required to get the specified level
        updated_level = self.updated_levels[dino_name]
        if updated_level < needed_level:
            needed_amount += dino.DNA_to_certain_level(updated_level, needed_level)
            self.updated_levels[dino_name] = needed_level
        
        # Account for the DNA that the dinosaur already has
        updated_amount = self.updated_amounts[dino_name]
        if updated_amount < needed_amount:
            needed_amount -= updated_amount
            self.updated_amounts[dino_name] = 0
        else:
            self.updated_amounts[dino_name] -= needed_amount
            needed_amount = 0
            return {dino_name: 0}

        # Translate the DNA amounts to parent amounts if applicable
        if dino.is_hybrid():
            p1_amount = self.calculate_parent_amount(dino.first, dino_name, needed_amount)
            p1_results = self.get_needed_DNA(dino.first, dino.activation_level(), p1_amount)

            p2_amount = self.calculate_parent_amount(dino.second, dino_name, needed_amount)
            p2_results = self.get_needed_DNA(dino.second, dino.activation_level(), p2_amount)

            return Counter(p1_results) + Counter(p2_results)
        else:
            return {dino_name: needed_amount}
        
    def determine_all_needed_DNA(self) -> dict[str : int]:
        """
        Return all the amounts of DNA needed to unlock all needed dinosaurs

        Returns
        -------
        dict[str : int]
            A mapping of dinosaur names to amounts of DNA needed to unlock all needed dinosaurs
        """
        total_DNA_count = Counter()
        for dino_name in self.needed_dinos:
            dino = self.current_dinos[dino_name]
            needed_DNA = self.get_needed_DNA(dino_name, dino.activation_level()+1, 0)
            total_DNA_count += Counter(needed_DNA)
        return total_DNA_count
            
    # ANCESTOR FUNCTIONS ------------------------------------------------------------------------

    def get_all_ancestors(self) -> dict[str : set[str]]:
        """
        Return a mapping of each needed dinosaur to a set of its ancestors

        Returns
        -------
        dict[str : set[str]]
            A mapping of each needed dinosaur to a set of its ancestors
        """
        ancestors = {}
        for dino_name in self.needed_dinos:
            ancestors[dino_name] = self.get_ancestors(dino_name)
        return ancestors

    def get_ancestors(self, dino_name) -> set[str]:
        """
        Return a set of all of the ancestors of the provided dinosaur

        Parameters
        ----------
        dino_name : str
            The name of the dinosaur for which you want the ancestors

        Returns
        -------
        set[str]
            The ancestors of the provided dinosaur
        """
        dino = self.current_dinos[dino_name]
        if dino.is_hybrid():
            return self.get_ancestors(dino.first).union(self.get_ancestors(dino.second))
        else:
            return set([dino_name])
            
    # RESULTS FUNCTIONS -------------------------------------------------------------------------

    def determine_tag(self, dino_name: str) -> None:
        """
        Determines and assigns the tag for the dinosaur specified based on the rules mentioned in print_tags(), along with the following:
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

    def print_tags(self) -> str:
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

    def print_DNA_still_needed(self) -> str:
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
    
    def print_limiting_factors(self) -> str:
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
                    for root in self.ancestors[dino_name]:
                        p = self.total_needed_DNA[root]
                        if p > max:
                            max = p
                            max_dino = root
                    if max != 0:
                        percentages[dino_name] = (max_dino, max)

            for i in sorted(percentages, key = lambda x: percentages[x][1]):
                output_string += i + ": " + percentages[i][0] + ", " + str(percentages[i][1]) + ", " + self.current_dinos[percentages[i][0]].rarity + "\n"

        b = {}
        c = defaultdict(lambda: [])
        for needed_dino in percentages:
            for anc in self.ancestors[needed_dino]:
                if anc in b:
                    c[needed_dino].append(b[anc][-1])
                else:
                    b[anc] = []
                b[anc].append(needed_dino)
        
        for i in sorted(b):
            print(i, b[i])
        print()
        for i in sorted(c):
            print(i, c[i])
        
        #return output_string
    def update_amount_history(self) -> None:
        """
        Send an update of needed amounts to the HistoryPlotting class instance
        """
        self.history.send_amount_update(self.total_needed_DNA)

    def select_dinos_for_display(self):
        """
        Determine which dinosaurs to display the account history for and display it via the HistoryPlotting instance
        """
        print("Here are the options for which dinosaurs you can display amount history for:")
        print("1: A single dinosaur")
        print("2: The ancestors of a single dinosaur")
        print("3. All dinosaurs of a certain rarity")
        user_input = int(input("Select the option you'd like by typing the number (i.e. 2): "))
        if user_input == 1:
            dino_name = input("Enter the dinosaur name you'd like the history for: ")
            self.history.display_amount_history(set([dino_name]))
        elif user_input == 2:
            dino_name = input("Enter the descendant dinosaur name you'd like the ancestors' history for: ")
            self.history.display_amount_history(self.ancestors[dino_name])
        elif user_input == 3:
            rarity = input("Enter the rarity that you'd like to see all the dinosaur amount history for: ")
            dinos_with_rarity = set()
            for dino_name in self.total_needed_DNA:
                if self.current_dinos[dino_name].get_rarity() == rarity:
                    dinos_with_rarity.add(dino_name)
            self.history.display_amount_history(dinos_with_rarity)

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
    #                 current_DNA = self.get_total_DNA(dino_name, dino.level, 0, False)
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
    x = DNAAnalytics(current_dinos, needed_dinos)
    print("Welcome to Data Analytics section of this project!")
    print("Here are some options of what you can get:")
    while True:
        print("1: Get all the dinosaurs that should have orange tags")
        print("2: Get all the DNA still needed to get every needed dinosaur, sorted by rarity")
        print("3. Get the most needed dinosaur for each needed dinosaur")
        print("4. Save your current dino amounts to the historical database")
        print("5. Display a history of DNA amounts")
        user_input = int(input("Select the option you'd like by typing the number (i.e. 2): "))
        if user_input == 0:
            break
        if user_input == 1:
            print(x.print_tags())
        elif user_input == 2:
            print(x.print_DNA_still_needed())
        elif user_input == 3:
            print(x.print_limiting_factors())
        elif user_input == 4:
            x.update_amount_history()
        elif user_input == 5:
            x.select_dinos_for_display()
        print()
        print("If you're interested in running something else, simply type it again. Otherwise, type 0 to quit the program.")
 