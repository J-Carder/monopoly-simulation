import random
from plot import Plot as new_plot
from plot import Pie as new_pie

# 1 run is one time around the board
# 1 roll is one roll of the dice
# TODO more data!!! (pie chart, heat map?)


class Game:

    def __init__(self, rolls, rand_start=False):

        self.triple_count = 0

        self.d1 = 0
        self.d2 = 0

        # roll produced by dice
        self.roll = 0

        # Place on the board (Default is 0 (GO) or set to random to get different results)
        if rand_start:
            self.move = random.randint(0, 40)
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
        self.prop_probability = []
        self.prop_set_probability = []
        self.prop_set_probability_avg = []

        # names of places on the board
        self.places = ['GO', 'Mediterranean', 'Community Chest', 'Baltic', 'Income Tax', 'Reading Railroad', 'Oriental', 'Chance', 'Vermont', 'Connecticut','Just Visiting',
                       'St. Charles','Electric Company', 'States', 'Virginia', 'Pennsylvania Railroad', 'St. James', 'Community Chest', 'Tennessee', 'New York', 'Free Parking',
                       'Kentucky','Chance','Indiana', 'Illinois', 'B. & O.', 'Atlantic', 'Ventnor', 'Water Works', 'Marvin Gardens', 'Go to jail',
                       'Pacific', 'North Carolina', 'Community Chest','Pennsylvania','Short Line', 'Chance', 'Park Place', 'Luxury Tax', 'Boardwalk']

        # create dictionary for name, space number and number times landed on
        self.places_dict = {}
        for i in range(0, 40):

            # self.places_dict[self.places[i]] = [i, 0]

            # format: places_dict[space number] = [name, number times landed on]
            self.places_dict[i] = [self.places[i], 0]

        # create places outside for loop, for ex. jail and just visiting are the same tile # but have two different
        # conditions
        self.places_dict['10a'] = ['Jail', 0]

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

        self.places_dict[self.move][1] += 1

        if self.move == 30:
            self.go_to(jail=True)

    def sim_data(self):
        """Show sim while running"""

        self.prop_names = []
        self.prop_probability = []
        self.prop_set_probability = []
        self.prop_set_probability_avg = []

        for key, value in self.places_dict.items():
            self.prop_names.append(value[0])
            self.prop_probability.append(value[1])

        prop_set = [[1, 3], [6, 8, 9], [11, 13, 14], [16, 18, 19], [21, 23, 24], [26, 27, 29], [31, 32, 34],
                    [37, 39], [5, 15, 25, 35], [12, 28], [12, 22, 36], [2, 17, 33]]

        for prop_group in prop_set:
            sum_props = 0
            for prop in prop_group:
                sum_props += self.prop_probability[prop]
            # print(sum_props, self.prop_set_probability)
            self.prop_set_probability.append(sum_props)
            self.prop_set_probability_avg.append(sum_props / len(prop_group))

        return [self.prop_names, self.prop_probability, self.prop_set_probability, self.prop_set_probability_avg]

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

    def community_chest(self):
        """draws a card from community chest and executes action on card"""

        if self.move == 2 or self.move == 17 or self.move == 33:

            self.chest_drawn = self.card_seq_chest.pop(0)

            if self.chest_drawn == 0:
                self.go_to(jail=True)
            elif self.chest_drawn == 1:
                self.go_to()

    def go_to(self, tile_number=0, jail=False):
        """goes to tile number specified"""

        if jail:
            self.move = '10a'
            self.places_dict[self.move][1] += 1
            self.move = 10
        else:
            self.move = tile_number
            self.places_dict[self.move][1] += 1

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
            self.roll_die()
            self.check_reset()
            self.check_triple()
            self.reset_cards()
            self.community_chest()
            self.chance()
            print(monopoly.total_rolls / (self.rolls_for / 100))

        # print(self.sim_data())


monopoly = Game(100000, rand_start=True)

monopoly.run()

colors_list = ['g', '#955436', '#03b1f8', '#955436', 'white', 'black', '#aae0fa', 'grey', '#aae0fa', '#aae0fa',
               '#a95b00', '#d93a96', 'grey', '#d93a96', '#d93a96', 'black', '#f7941d', '#03b1f8', '#f7941d', '#f7941d',
               '#ef1722', '#ed1b24', 'grey', '#ed1b24', '#ed1b24', 'black', '#fef200', '#fef200', 'grey', '#fef200',
               '#a95b00', '#1fb25a', '#1fb25a', '#03b1f8', '#1fb25a', 'black', 'grey', '#0072bb', 'white', '#0072bb',
               '#a95b00']

hatch_data = [2, 17, 33, 7, 22, 36, 4, 38, '//']

prop_prob = new_plot([x / 4 for x in range(0, 17)], [value / sum(monopoly.prop_probability) * 100 for value in
                                                     monopoly.sim_data()[1]], bar_color=colors_list,
                     hatch_data=hatch_data, autolabel=True)

prop_prob.labels("Monopoly Property Probabilities", y_label="Probability (%)", rotation=45, size=9,
                 x_tick_names=monopoly.sim_data()[0], ha='right')

prop_prob.autolabel(8)
prop_prob.show()

hatch_data[8] = '--'

for i in range(0, 4):
    colors_list[i*10 +5] = '#444444'

pie_sim = new_pie([value / sum(monopoly.prop_probability) * 100 for value in monopoly.sim_data()[1]], monopoly.sim_data()[0], colors_list)
pie_sim.show(autopct='%1.1f%%', pd=0.9, ld=1.05, hatch_data=hatch_data)


colors_list = ['#955436', '#aae0fa', '#d93a96', '#f7941d', '#ed1b24', '#fef200', '#1fb25a', '#0072bb', 'black', 'grey',
               'grey', '#03b1f8']

hatch_data = [10, 11, '//']

x_labels = ['Browns', 'Light blues', 'Pinks', 'Oranges', 'Reds', 'Yellows', 'Greens', 'Dark blues', 'Railroads',
            'Utilities', 'Chance', 'Community Chest']

for i in range(0, 2):
    prop_set_prob = new_plot([x / 2 for x in range(0, int(25 / ((2 * i) + 1)))], [value / sum(monopoly.prop_probability)
                    * 100 for value in monopoly.sim_data()[i+2]], autolabel=True, bar_color=colors_list,
                    hatch_data=hatch_data, width=0.6)

    title = 'Monopoly Probability of Landing on sets'
    if i == 1:
        title += " (Average)"
    prop_set_prob.labels(title, y_label='Probability (%)',
                         x_tick_names=x_labels, rotation=45, ha='right', size=10)

    prop_set_prob.autolabel(10, dec_places=4)

    prop_set_prob.show()

    if i == 0:
        colors_list[8] = '#444444'
        pie_sim = new_pie([value / sum(monopoly.prop_probability) * 100 for value in monopoly.sim_data()[2]], x_labels, colors_list)
        pie_sim.show(autopct='%1.1f%%', pd=0.75, ld=1.05, hatch_data=hatch_data)
        
