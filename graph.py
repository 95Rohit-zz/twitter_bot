from matplotlib import pyplot as plt
import numpy as np

class graphData():

    def RankGraph(self,dataValues,filename):
        y_axis= []
        x_axis = []
        for individual_data in dataValues:
            y_axis.append(individual_data[0])           # companies name
            x_axis.append(individual_data[1])           # Number of tweets
        plt.barh(x_axis,y_axis, align='center', alpha=0.5)  #bar plot of the data
        plt.xlabel('Number of tweets')
        plt.ylabel('Companies')
        plt.title('Rank Graph')
        plt.savefig(filename)
        plt.clf()

    def KeyWordsGraph(self,dataValues,filename):
        listAll = []
        # data to plot in listAll
        for first in dataValues:
            listIndividual = []
            varName = []
            for second in first:
                listIndividual.append(second[2])
                varName.append(second[1])           #to get a list of all keywords
            listAll.append(listIndividual)

        #create a plot
        n_groups = len(varName)
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.15
        opacity = 0.8

        rects1 = plt.bar(index, listAll[0], bar_width,
                 alpha=opacity,
                 color='b',
                 label='JCPenney')

        rects2 = plt.bar(index + bar_width, listAll[1], bar_width,
                 alpha=opacity,
                 color='g',
                 label='Macys')

        rects3 = plt.bar(index + 2*bar_width, listAll[2], bar_width,
                 alpha=opacity,
                 color='r',
                 label='Nordstrom')

        rects4 = plt.bar(index + 3*bar_width, listAll[3], bar_width,
                 alpha=opacity,
                 color='y',
                 label='Kohls')

        plt.xlabel('Keywords')
        plt.ylabel('Companies')
        plt.title('Keywords Graph')
        plt.xticks(index + bar_width, (varName))
        plt.legend()

        plt.tight_layout()
        plt.savefig(filename)
