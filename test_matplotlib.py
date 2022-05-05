import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def demo():
    # basic graph
    x = [1, 2, 3, 4]
    y = [2, 4, 6, 8]

    # resize graph
    fig = plt.figure(figsize=(5, 5), dpi=100)
    plt.plot(x, y, label='2x', color='green', linewidth=3, marker='.', markersize=12, markeredgecolor='red',
             linestyle='--')
    # Line number 2
    x2 = np.arange(0, 4.5, 0.5)  # select interval we want to plot points at

    plt.plot(x2[:5], x2[:5]**2, label='x^2')  # plot part of graph
    plt.plot(x2[4:], x2[4:]**2, linestyle=':')  # plot remainder of graph

    fontdict = {'fontsize': 40, 'fontname': 'Comic Sans MS'}
    plt.title('First plot', fontdict=fontdict)  # add a title
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.xticks(x)  # adjust unit of x axis
    plt.yticks(y)
    plt.legend()
    plt.savefig('first_fig.png', dpi=200)  # save image
    plt.show()


def demo2():
    # bar chart
    labels = ['fancy', 'sof', 'jenny']
    values = [40, 33, 12]
    fig = plt.figure()
    # plot 2 tables into one frame with position 1 and 2 todo: try position 223 and 224
    ax1 = fig.add_subplot(111)
    ax1.bar(labels, values)
    ax2 = fig.add_subplot(112)
    ax2.bar(labels, values)
    # bars = plt.bar(labels, values)
    # bars[0].set_hatch('/')
    # bars[1].set_hatch('o')
    plt.show()


# deal data gas_prices with pandas
def demo3():
    gas = pd.read_csv(r'data/gas_prices.csv')
    pd_year = gas.Year
    plt.title(r'Gas Prices')
    countries_to_look_at = ['Australia', 'France', 'UK']
    # plt.plot(pd_year, gas.USA, 'b.-')
    # plt.plot(pd_year, gas.USA, label='United Stats', marker='b.-')
    # plt.plot(pd_year, gas['South Korea'])
    for country in gas:
        # if country != 'Year':
        if country in countries_to_look_at:
            plt.plot(pd_year, gas[country], marker='.')
    plt.xticks(gas.Year[::2])
    # add more years in x axis by plt.xticks(gas.Year[::2].tolist()+[2012])
    plt.xlabel('Year')
    plt.legend()
    plt.show()
    print(gas)


# fifa data
def demo_hist():
    bins = [20, 40, 60, 80, 100]
    fifa = pd.read_csv('data/fifa_data.csv')
    overall = fifa.Overall
    plt.hist(overall, color='g')
    # plt.hist(overall, bins=bins)
    # plt.xticks(bins)
    plt.ylabel('number of players')
    plt.xlabel('skills')
    plt.show()


def demo_pie():
    fifa = pd.read_csv('data/fifa_data.csv')
    left = fifa.loc[fifa['Preferred Foot'] == 'Left'].count()[0]
    right = fifa.loc[fifa['Preferred Foot'] == 'Right'].count()[0]
    labels = ['left', 'right']
    colors = ['g', 'b']
    plt.pie([left, right], labels=labels, colors=colors, autopct='%.2f')
    plt.show()


def demo_boxplot():
    fifa = pd.read_csv('data/fifa_data.csv')
    print(fifa)
    barcelona = fifa.loc[fifa.Club == 'FC Barcelona']['Overall']
    chelsea = fifa.loc[fifa.Club == 'Chelsea']['Overall']
    labels = ['FC Barcelona', 'chelsea']
    plt.boxplot([barcelona, chelsea], labels=labels)
    plt.show()


if __name__ == '__main__':
    # todo: try plt.style.use, plt.style.available
    # demo()
    demo2()
    # demo3()
    # demo_hist()
    # demo_pie()
    # demo_boxplot()
