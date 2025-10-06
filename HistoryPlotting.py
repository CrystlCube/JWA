import datetime
from matplotlib import pyplot as plt

class HistoryPlotting:
    """
    A class for storing and plotting historical data

    Attributes
    ----------
    amount_history : dict[str : list[int]]
        A collection of dinosaur names mapped to their DNA amounts on certain days
    dates : list[str]
        A list of dates that correspond to the DNA amounts in amount_history
    """

    def __init__(self) -> None:
        self.amount_history = {}
        self.dates = []

        self.parse_amount_input()

    def parse_amount_input(self) -> None:
        """
        Sets amount_history and dates to the values specified in AmountHistory.txt
        """
        amount_reader = open("AmountHistory.txt", "r")
        day_amounts = amount_reader.read().split('\n\n')
        all_dino_names = set()
        for day in day_amounts:
            amounts = day.split('\n')
            self.dates.append(amounts[0])
            amount_changed = {name: False for name in all_dino_names}
            for i in range(1,len(amounts)):
                dino_name, amount = amounts[i].split(': ')
                amount = int(amount)
                if dino_name[0] == '#': continue
                if dino_name not in all_dino_names:
                    all_dino_names.add(dino_name)
                    self.amount_history[dino_name] = [amount]
                else:
                    self.amount_history[dino_name].append(amount)
                    amount_changed[dino_name] = True
            for dino_name in amount_changed:
                if not amount_changed[dino_name]:
                    self.amount_history[dino_name].append(self.amount_history[dino_name][-1])
                    amount_changed[dino_name] = True

    def archive_dino(self, dino_name: str) -> None:
        """
        Takes in a dinosaur name and comments out all of its amount history

        Parameters
        ----------
        dino_name: str
            Name of the dinosaur to archive
        """
        f = open("AmountHistory.txt", "r")
        original = f.read()
        changed = original.replace(dino_name + ":", "# " + dino_name + ":")
        f = open("AmountHistory.txt", "w")
        f.write(changed)
   
    def send_amount_update(self, needed_amounts: dict[str : int]) -> None:
        """
        Takes new dinosaur amounts and adds them to amount_history and AmountHistory.txt

        Parameters
        ----------
        needed_amounts: dict[str : int]
            A mapping of dinosaur names to their new needed amounts
        """
        formatted_date = datetime.datetime.now().strftime("%m/%d/%Y")
        self.dates.append(formatted_date)

        amount_writer = open("AmountHistory.txt", "a")
        amount_writer.write('\n')
        amount_writer.write('\n' + formatted_date)
        for dino_name in sorted(needed_amounts):
            if dino_name not in self.amount_history or needed_amounts[dino_name] != self.amount_history[dino_name][-1]:
                amount_writer.write('\n' + dino_name + ": " + str(needed_amounts[dino_name]))

        for dino_name in needed_amounts:
            if dino_name not in self.amount_history:
                self.amount_history[dino_name] = []
            self.amount_history[dino_name].append(needed_amounts[dino_name])

    def display_amount_history(self, dinos_to_display: set[str]) -> None:
        """
        Displays a line graph of the amount history for the given dinos

        Parameters
        ----------
        dinos_to_display: set[str]
            A set of dinosaur names that we should display that data for
        """
        for dino_name in dinos_to_display:
            if dino_name not in self.amount_history: continue
            x_axis = self.dates
            y_axis = [int(i) for i in self.amount_history[dino_name]]
            len_of_history = len(self.amount_history[dino_name])
            if len(self.amount_history[dino_name]) != len(self.dates):
                x_axis = self.dates[-len_of_history:]
            plt.plot(x_axis,y_axis,label=dino_name)
        plt.legend()
        plt.show()