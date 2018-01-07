import numpy as np
import matplotlib.pyplot as plt


class Plot:

    def __init__(self, y_values, x_values, bar_color='b', hatch_data='', width=0.6):

        self.fig, self.ax = plt.subplots()

        if y_values is not 'auto':
            self.y_values = y_values
            self.ax.set_yticks(self.y_values)

        self.x_values = x_values

        plt.ylim(ymax=max(y_values))

        self.x_places = np.arange(len(self.x_values))  # the x locations for the groups
        self.ax.set_xticks(self.x_places)

        self.bar = self.ax.bar(self.x_places, self.x_values, width, color=bar_color, edgecolor='black')

        for bar in hatch_data[:-1]:
            self.bar[bar].set_hatch(hatch_data[-1])

    def labels(self, title, y_label='', x_label='', x_tick_names='', rotation=0, size=10, ha='center'):
        # add some text for labels, title and axes ticks
        self.ax.set_ylabel(y_label)
        self.ax.set_xlabel(x_label)
        self.ax.set_title(title)
        self.ax.set_xticklabels(x_tick_names, rotation=rotation, ha=ha, size=size)

    def autolabel(self, size, dec_places=2):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in self.bar:
            height = rect.get_height()
            self.ax.text(rect.get_x() + rect.get_width()/2., 1.005*height, round(height, dec_places),
                         ha='center', va='bottom', size=size)

    def show(self):
        plt.tight_layout()
        plt.show()


class Pie:

    def __init__(self, sizes, labels, colors):
        # Data to plot
        self.labels = labels
        self.sizes = sizes
        self.colors = colors
        # self.explode = [x/x / 100 for x in range(1, 13)]

    def show(self, autopct='%1.2f%%', pd=0.5, ld=1.1, hatch_data=''):

        # Plot
        piechart = plt.pie(self.sizes, labels=self.labels, colors=self.colors,
                           autopct=autopct, startangle=-90, pctdistance=pd, labeldistance=ld)[0]

        for wedge in hatch_data[:-1]:
            piechart[wedge].set_hatch(hatch_data[-1])

        plt.axis('equal')
        plt.tight_layout()
        plt.show()


class Text:

    def __init__(self):

        self.fig, self.ax = plt.subplots()

    def text(self, x, y, text, color, facecolor='none', edgecolor='black', ha='left'):

        self.ax.text(x, y, text, color=color, ha=ha, bbox=dict(facecolor=facecolor, edgecolor=edgecolor))

    def show(self):

        self.ax.set_axis_off()
        plt.show()

