import random
import plot

# 1 run is one time around the board
# 1 roll is one roll of the dice
# TODO more data!!! (pie chart, heat map?) also create graph for all of a set, clean up!!, clean up plot too!!


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

        # interactive
        # self.run_for = int(input("How many tests would you like to run? "))

        # running total of rolls/runs
        self.total_rolls = 0

        self.card_seq_chest = random.sample(range(0, 16), 16)
        self.card_seq_chance = random.sample(range(0, 16), 16)

        self.chest_drawn = 0
        self.chance_drawn = 0

        self.total_dub_jails = 0

        self.key_list = []

        self.prop_names = []
        self.prop_probability = []

        self.value_list = []

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
        """Make sure move number doesn't exceed amount of tiles on board (38), add to runs and check if on action
        space (jail, chance, community chest) then move accordingly"""

        if self.move >= 40:
            self.move -= 40

        self.places_dict[self.move][1] += 1

        if self.move == 29:
            self.go_to(jail=True)

    def show_sim(self):
        """Show data from simulation"""

        for key, value in self.places_dict.items():

            # print(key, value[0])

            self.value_list.append([(value[1]/self.total_rolls) * 100, value[0]])

        self.value_list.sort(reverse=True)
        print(self.value_list, len(self.value_list))

    def show_sim_live(self):
        """Show sim while running"""

        # for key, value in self.places_dict.items():
        #     if key == 10 or key == 29 or key == '10a' or key == 0:
        #         print(value[0], value[1])
        #         return value[0], value[1]
        self.prop_probability = []
        for key, value in self.places_dict.items():
            self.prop_names.append(value[0])
            self.prop_probability.append(value[1])

        return [self.prop_names, self.prop_probability]

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

        if self.move == 2 or self.move == 17 or self.move == 33:

            self.chest_drawn = self.card_seq_chest.pop(0)

            if self.chest_drawn == 0:
                self.go_to(jail=True)
            elif self.chest_drawn == 1:
                self.go_to()

    def go_to(self, tile_number=0, jail=False):

        if jail:
            self.move = '10a'
            self.places_dict[self.move][1] += 1
            self.move = 10
        else:
            self.move = tile_number
            self.places_dict[self.move][1] += 1

        self.places_landed += 1

    def reset_cards(self):

        if len(self.card_seq_chest) <= 0:
            self.card_seq_chest = random.sample(range(0, 16), 16)

        if len(self.card_seq_chance) <= 0:
            self.card_seq_chance = random.sample(range(0, 16), 16)

    def run(self):
        while self.total_rolls < self.rolls_for:
            self.roll_die()
            self.check_reset()
            print(monopoly.total_rolls / (self.rolls_for / 100))
            self.check_triple()
            self.reset_cards()
            self.community_chest()
            self.chance()

        self.show_sim()


monopoly = Game(100000, rand_start=True)

monopoly.run()

print((monopoly.total_dub_jails / monopoly.total_rolls) * 100)

big_data = plot.Plot(monopoly)


big_data.autolabel(big_data.bar)

big_data.custom_colors([0], 'g')

big_data.custom_colors([5, 15, 25, 35], 'black')
big_data.custom_colors([12, 28], 'grey')
big_data.custom_colors([2, 17, 33], '#03b1f8', hatch='/')
big_data.custom_colors([7, 22, 36], 'grey', hatch='/')
big_data.custom_colors([4, 38], '#ffffff', hatch='/')
big_data.custom_colors([20], '#ef1722')
big_data.custom_colors([30], '#a95b00')
big_data.custom_colors([40], '#a95b00')
big_data.custom_colors([10], '#a95b00')

big_data.custom_colors([1, 3], '#955436')
big_data.custom_colors([6, 8, 9], '#aae0fa')
big_data.custom_colors([11, 13, 14], '#d93a96')
big_data.custom_colors([16, 18, 19], '#f7941d')
big_data.custom_colors([21, 23, 24], '#ed1b24')
big_data.custom_colors([26, 27, 29], '#fef200')
big_data.custom_colors([31, 32, 34], '#1fb25a')
big_data.custom_colors([37, 39], '#0072bb')

big_data.labels("Probability (percentage)", "Monopoly Property Probabilities", 45, 7)

big_data.show()
