import random
from plot import Plot as new_plot
from plot import Pie as new_pie
from plot import Text as new_text
import csv
import time

start_time = time.time()

# TODO more data!!! (heat map?), add rents (single prop, 0-4 houses, hotels?),
# TODO MAJOR CLEAN UP!!, use nested lists instead of dictionaries!!


class Game:

    def __init__(self, rolls, rand_start=False):

        self.triple_count = 0

        self.one_tile_per_turn = False

        self.d1 = 0
        self.d2 = 0

        # roll produced by dice
        self.roll = 0

        # Place on the board (Default is 0 (GO) or set to random to get different results)
        if rand_start:
            self.move = random.randint(0, 39)
        else:
            self.move = 0

        # times to run/roll for
        self.rolls_for = rolls

        self.places_landed = 0

        # running total of rolls/runs
        self.total_rolls = 0

        self.card_seq_chest = random.sample(range(0, 16), 16)
        self.card_seq_chance = random.sample(range(0, 16), 16)

        self.chest_drawn = 0
        self.chance_drawn = 0

        self.total_dub_jails = 0

        self.key_list = []
        self.value_list = []

        self.prop_names = []
        self.prop_landed_on = []
        self.prop_landed_on_combined = []
        self.prop_landed_on_combined_avg = []

        # names of places on the board
        self.places = ['GO', 'Mediterranean', 'Community Chest (1)', 'Baltic', 'Income Tax', 'Reading Railroad',
                       'Oriental', 'Chance (1)', 'Vermont', 'Connecticut', 'Just Visiting',
                       'St. Charles', 'Electric Company', 'States', 'Virginia', 'Pennsylvania Railroad', 'St. James',
                       'Community Chest (2)', 'Tennessee', 'New York', 'Free Parking',
                       'Kentucky', 'Chance (2)', 'Indiana', 'Illinois', 'B. & O.', 'Atlantic', 'Ventnor', 'Water Works',
                       'Marvin Gardens', 'Go to jail',
                       'Pacific', 'North Carolina', 'Community Chest (3)', 'Pennsylvania', 'Short Line', 'Chance (3)',
                       'Park Place', 'Luxury Tax', 'Boardwalk']

        # create dictionary for name, space number and number times landed on
        self.property_data = {}
        for i in range(0, 40):

            # self.places_dict[self.places[i]] = [i, 0]

            # format: places_dict[space number] = [name, number times landed on]
            self.property_data[i] = [self.places[i], 0]

        # create places outside for loop, for ex. jail and just visiting are the same tile # but have two different
        # conditions
        self.property_data['10a'] = ['Jail', 0]

    def roll_die(self):
        """Roll two pseudo-random 'dice' and move that number of spaces"""

        self.d1 = random.randint(1, 6)
        self.d2 = random.randint(1, 6)

        self.roll = self.d1 + self.d2
        self.move += self.roll

        # add to vars
        self.total_rolls += 1
        self.places_landed += 1

    def check_reset(self):
        """make sure players position doesn't exceed tiles on board, add to places, and check if player lands on Go
        to jail"""

        if self.move >= 40:
            self.move -= 40

        if self.one_tile_per_turn:
            if self.move not in [2, 7, 17, 22, 30, 33, 36]:
                self.property_data[self.move][1] += 1
        else:
            self.property_data[self.move][1] += 1

        if self.move == 30:
            self.go_to(jail=True)

    def sim_data(self):
        """Generate data from simulation"""

        self.prop_names = []
        self.prop_landed_on = []
        self.prop_landed_on_combined = []
        self.prop_landed_on_combined_avg = []

        for key, value in self.property_data.items():
            self.prop_names.append(value[0])
            self.prop_landed_on.append(value[1])

        prop_set = [[1, 3], [6, 8, 9], [11, 13, 14], [16, 18, 19], [21, 23, 24], [26, 27, 29], [31, 32, 34],
                    [37, 39], [5, 15, 25, 35], [12, 28], [12, 22, 36], [2, 17, 33]]

        for prop_group in prop_set:
            sum_props = 0
            for prop in prop_group:
                sum_props += self.prop_landed_on[prop]
            # print(sum_props, self.prop_set_probability)
            self.prop_landed_on_combined.append(sum_props)
            self.prop_landed_on_combined_avg.append(sum_props / len(prop_group))

        return [self.prop_names, self.prop_landed_on, self.prop_landed_on_combined, self.prop_landed_on_combined_avg]

    def check_triple(self):
        """Check if player gets three doubles in a row (going to jail)"""

        if self.d1 == self.d2:
            self.triple_count += 1
        else:
            self.triple_count = 0

        if self.triple_count == 3:
            self.go_to(jail=True)
            self.triple_count = 0
            self.total_dub_jails += 1

    def chance(self):
        """draws a card from chance and executes action on card"""

        if self.move == 7 or self.move == 22 or self.move == 36:

            self.chance_drawn = self.card_seq_chance.pop(0)

            if self.chance_drawn == 0:
                self.go_to(jail=True)
            elif self.chance_drawn == 1:
                self.go_to(tile_number=self.move-3)
            elif self.chance_drawn == 2:
                self.go_to(tile_number=5)
            elif self.chance_drawn == 3:
                self.go_to(tile_number=24)
            elif self.chance_drawn == 4:
                self.go_to(tile_number=11)
            elif self.chance_drawn == 5:
                self.go_to(tile_number=0)
            elif self.chance_drawn == 6:
                self.go_to(tile_number=39)
            elif self.chance_drawn == 7:
                if self.move == 22:
                    self.go_to(tile_number=28)
                else:
                    self.go_to(tile_number=12)
            elif self.chance_drawn == 8 or self.chance_drawn == 9:
                if self.move == 7:
                    self.go_to(tile_number=15)
                elif self.move == 22:
                    self.go_to(tile_number=25)
                else:
                    self.go_to(tile_number=5)
            elif self.one_tile_per_turn:
                self.go_to(tile_number=self.move)

    def community_chest(self):
        """draws a card from community chest and executes action on card"""

        if self.move == 2 or self.move == 17 or self.move == 33:

            self.chest_drawn = self.card_seq_chest.pop(0)

            if self.chest_drawn == 0:
                self.go_to(jail=True)
            elif self.chest_drawn == 1:
                self.go_to()
            elif self.one_tile_per_turn:
                self.go_to(tile_number=self.move)

    def go_to(self, tile_number=0, jail=False):
        """goes to tile number specified"""

        if jail:
            self.move = '10a'
            self.property_data[self.move][1] += 1
            self.move = 10
        else:
            self.move = tile_number
            self.property_data[self.move][1] += 1

        self.places_landed += 1

    def reset_cards(self):
        """checks if there are less than 1 cards in chance/community chest pile and 'reshuffles' if true"""

        if len(self.card_seq_chest) <= 0:
            self.card_seq_chest = random.sample(range(0, 16), 16)

        if len(self.card_seq_chance) <= 0:
            self.card_seq_chance = random.sample(range(0, 16), 16)

    def run(self):
        """run simulation"""

        while self.total_rolls < self.rolls_for:
            self.check_reset()
            self.roll_die()
            self.check_triple()
            self.reset_cards()
            self.community_chest()
            self.chance()

            # if self.total_rolls / (self.rolls_for / 100) in [25, 50, 75, 100]:  # (the cost of spitting out updated percentages is a 10% increase in run time)
            #     print(int(self.total_rolls / (self.rolls_for / 100)), '%')


        # print(self.sim_data())


monopoly = Game(100000, rand_start=True)
monopoly.run()
print("--- %s seconds ---" % (time.time() - start_time))


plots = False
if plots:
    # ### PLOTS ###

    # text 1
    colors_list = ['g', '#955436', '#03b1f8', '#955436', 'white', 'black', '#aae0fa', 'grey', '#aae0fa', '#aae0fa',
                   '#a95b00', '#d93a96', 'grey', '#d93a96', '#d93a96', 'black', '#f7941d', '#03b1f8', '#f7941d',
                   '#f7941d',
                   '#ef1722', '#ed1b24', 'grey', '#ed1b24', '#ed1b24', 'black', '#fef200', '#fef200', 'grey', '#fef200',
                   '#a95b00', '#1fb25a', '#1fb25a', '#03b1f8', '#1fb25a', 'black', 'grey', '#0072bb', 'white',
                   '#0072bb',
                   '#a95b00']

    for i in range(0, len(colors_list)):
        if i < 4:
            colors_list[i * 10 + 5] = '#555555'

    rank_list = []  # new dict containing only property names and times landed on

    for i, [key, value] in enumerate(monopoly.property_data.items()):
        rank_list.append([value[1], value[0], colors_list[i]])

    rank_list.sort(reverse=True)

    text_box = new_text()

    x_align = 0.5

    x_align_num = 0.02

    x_space = -0.2

    for i, color in enumerate(colors_list):  # first time using enumerate!!
        if i < 21:

            text_box.text(x_align - 0.5 - x_align_num, (i - 18) / 17 * -1, str(i + 1) + '.', 'black', ha='right')
            text_box.text(x_align - 0.5, (i - 18) / 17 * -1, rank_list[i][1], 'black', facecolor=rank_list[i][2])
        else:
            text_box.text(x_align - x_align_num + x_space, (i - 39) / 17 * -1, str(i + 1) + '.', 'black', ha='right')
            text_box.text(x_align + x_space, (i - 39) / 17 * -1, rank_list[i][1], 'black', facecolor=rank_list[i][2])

    text_box.show()

    # plot 1 (probability of landing on each property) ##
    colors_list = ['g', '#955436', '#03b1f8', '#955436', 'white', 'black', '#aae0fa', 'grey', '#aae0fa', '#aae0fa',
                   '#a95b00', '#d93a96', 'grey', '#d93a96', '#d93a96', 'black', '#f7941d', '#03b1f8', '#f7941d',
                   '#f7941d', '#ef1722', '#ed1b24', 'grey', '#ed1b24', '#ed1b24', 'black', '#fef200', '#fef200', 'grey',
                   '#fef200', '#a95b00', '#1fb25a', '#1fb25a', '#03b1f8', '#1fb25a', 'black', 'grey', '#0072bb',
                   'white', '#0072bb', '#a95b00']

    hatch_data = [2, 17, 33, 7, 22, 36, 4, 38, '//']

    prop_prob = new_plot([x / 4 for x in range(0, 17)], [value / sum(monopoly.prop_landed_on) * 100 for value in
                                                         monopoly.sim_data()[1]], bar_color=colors_list,
                         hatch_data=hatch_data)

    prop_prob.labels("Monopoly Property Probabilities", y_label="Probability (%)", rotation=45, size=9,
                     x_tick_names=monopoly.sim_data()[0], ha='right')

    prop_prob.autolabel(8)
    prop_prob.show()

    # pie 1 (probability of landing on each property) ##
    hatch_data[8] = '--'

    for i in range(0, 4):
        colors_list[i*10 + 5] = '#444444'

    pie_sim = new_pie([value / sum(monopoly.prop_landed_on) * 100 for value in monopoly.sim_data()[1]],
                      monopoly.sim_data()[0], colors_list)
    pie_sim.show(autopct='%1.1f%%', pd=0.9, ld=1.05, hatch_data=hatch_data)

    # plots 2, pie 2 and plot 3 ##

    colors_list = ['#955436', '#aae0fa', '#d93a96', '#f7941d', '#ed1b24', '#fef200', '#1fb25a', '#0072bb', 'black',
                   'grey', 'grey', '#03b1f8']

    hatch_data = [10, 11, '//']

    x_labels = ['Browns', 'Light blues', 'Pinks', 'Oranges', 'Reds', 'Yellows', 'Greens', 'Dark blues', 'Railroads',
                'Utilities', 'Chance', 'Community Chest']

    for i in range(0, 2):
        prop_set_prob = new_plot([x / 2 for x in range(0, int(25 / ((2 * i) + 1)))],
                                 [value / sum(monopoly.prop_landed_on) * 100 for value in monopoly.sim_data()[i+2]],
                                 bar_color=colors_list, hatch_data=hatch_data, width=0.6)

        title = 'Monopoly Probability of Landing on sets'
        if i == 1:
            title += " (Average)"
        prop_set_prob.labels(title, y_label='Probability (%)',
                             x_tick_names=x_labels, rotation=45, ha='right', size=10)

        prop_set_prob.autolabel(10, dec_places=4)

        prop_set_prob.show()

        if i == 0:
            colors_list[8] = '#444444'
            pie_sim = new_pie([value / sum(monopoly.prop_landed_on) * 100 for value in monopoly.sim_data()[2]],
                              x_labels, colors_list)
            pie_sim.show(autopct='%1.1f%%', pd=0.75, ld=1.05, hatch_data=hatch_data)

    export = False
    if monopoly.rolls_for > 10000000:
        export = True

    if export:

        #  export data to *.csv files ##
        def write_to_csv(csv_file, data):
            with open(csv_file, "w") as output:
                writer = csv.writer(output, lineterminator='\n')
                for val in data:
                    writer.writerow([val])

        write_to_csv("csv/property_probabilities.csv", [value / sum(monopoly.prop_landed_on) * 100 for value in
                                                        monopoly.sim_data()[1]])
        write_to_csv("csv/property_set_probabilities.csv", [value / sum(monopoly.prop_landed_on) * 100 for value in
                                                            monopoly.sim_data()[2]])
        write_to_csv("csv/property_set_probabilities_avg.csv", [value / sum(monopoly.prop_landed_on) * 100 for value in
                                                                monopoly.sim_data()[3]])
