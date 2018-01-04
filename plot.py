import numpy as np
import matplotlib.pyplot as plt

# TODO make more accessible for more than just one plot! refactor!!!!


class Plot:

    def __init__(self, class_name):

        self.fig, self.ax = plt.subplots()

        self.class_name = class_name

        self.percents = [x / 4 for x in range(0, 17)]
        self.ax.set_yticks(self.percents)

        self.percentages = []
        for value in class_name.show_sim_live()[1]:
            self.percentages.append(value / sum(class_name.prop_probability) * 100)

        # percentages.sort(reverse=True)

        self.x = np.arange(len(self.percentages))  # the x locations for the groups

        self.bar = self.ax.bar(self.x, self.percentages, 0.6, color='b', edgecolor='#000000')

    def labels(self, x_label, title, rot, size):
        # add some text for labels, title and axes ticks
        self.ax.set_ylabel(x_label)
        self.ax.set_title(title)
        self.ax.set_xticks(self.x)
        self.ax.set_xticklabels(self.class_name.show_sim_live()[0], rotation=rot, ha='right', size=size)

    def custom_colors(self, x, color, hatch=''):
        for column in x:
            self.bar[column].set_color(color)
            self.bar[column].set_edgecolor('black')
            self.bar[column].set_hatch(hatch)

    def autolabel(self, rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            self.ax.text(rect.get_x() + rect.get_width()/2., 1.0*height, round(height, 2),
                         ha='center', va='bottom', size=8)

    def show(self):
        plt.show()
