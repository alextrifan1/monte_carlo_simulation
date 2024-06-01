# Monte Carlo Simulation - following a youtube tutorial
# https://www.youtube.com/playlist?list=PLQVvvaa0QuDdhOnp-FnVStDsALpYk2hk0
# we are using the Monte Carlo simulator to account for randomness and the degree of risk associated with a betting strategy

import random
import time
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg') #for a pop-up window

#valorile pe care vrem sa le atingem
lower_bust = 29.222
higher_profit = 64.723


sample_size = 1000
starting_funds = 10000
wager_size = 100
wager_count = 10000


def roll_dice():
    roll = random.randint(1,100)
    if roll <= 50 or roll == 100:
        #print("Ai pierdut")
        return False
    else:
        #print("Ai castigat")
        return True

def doubler_bettor(funds, initial_wager, wager_count, color):
    """

    :param funds: the initial funds of the bettor
    :param initial_wager: how much we bett in the begining
    :param wager_count: how many wagers we want to do
    :return:
    """
    value = funds  # value mai change latter
    wager = initial_wager
    current_wagers = 1
    previous_wager = 'win'
    previous_wager_amount = initial_wager

    global doubler_busts
    global doubler_profits

    wager_x = []
    value_y = []

    while current_wagers <= wager_count:
        if previous_wager == 'win':
            if roll_dice():
                value = value + wager
                wager_x.append(current_wagers)
                value_y.append(value)
            else:
                value = value - wager
                previous_wager = 'loss'
                previous_wager_amount = wager
                wager_x.append(current_wagers)
                value_y.append(value)
                if value <= 0:
                    doubler_busts = doubler_busts + 1
                    value = 0
                    break
        elif previous_wager == 'loss':
            #we double the wager
            if roll_dice():
                wager = previous_wager_amount * 2
                if (value-wager) < 0:
                    wager = value
                value = value + wager
                wager = initial_wager #we won so we revert back to ta initial wager in order to lower the risk of lossing money
                previous_wager = 'win'
                wager_x.append(current_wagers)
                value_y.append(value)
            else:
                wager = previous_wager_amount * 2
                if (value-wager) < 0:
                    wager = value
                value = value - wager
                previous_wager_amount = wager
                wager_x.append(current_wagers)
                value_y.append(value)
                if value <= 0:
                    doubler_busts = doubler_busts + 1
                    value = 0
                    break
                previous_wager = 'loss'

        current_wagers = current_wagers+1

    plt.plot(wager_x, value_y, color)
    if value > funds:
        value = 0
        doubler_profits = doubler_profits + 1


def simple_bettor(funds, initial_wager, wager_count, color):
    """
    this bettor only wagers the initial wager over and over
    :param funds: the initial funds of the bettor
    :param initial_wager: how much we bett in the begining
    :param wager_count: how many wagers we want to do
    :return:
    """

    value = funds #value mai change latter
    wager = initial_wager
    current_wagers = 1

    global simple_busts
    global simple_profits

    wager_x = []
    value_y = []

    while current_wagers <= wager_count:
        if roll_dice(): #we won
            value = value + wager
            wager_x.append(current_wagers)
            value_y.append(value)
        else:
            value = value - wager
            if value <= 0:
                simple_busts = simple_busts + 1
                value = 0
                break
            wager_x.append(current_wagers)
            value_y.append(value)
        current_wagers  = current_wagers + 1

    #print("Funds: ", value)
    plt.plot(wager_x, value_y, color)
    if value > funds:
        value = 0
        simple_profits = simple_profits + 1


simple_busts = 0.0
simple_profits = 0.0
doubler_busts = 0.0
doubler_profits = 0.0

for i in range(sample_size):
    simple_bettor(starting_funds, wager_size, wager_count, 'k')
    doubler_bettor(starting_funds, wager_size, wager_count, 'c')

print("Simple Bettor bust chane: ", (simple_busts/sample_size)*100.00)
print("Doubler Bettor bust chance: ", (doubler_busts/sample_size)*100.00)

print("Simple Bettor profit chane: ", (simple_profits/sample_size)*100.00)
print("Doubler Bettor profit chance: ", (doubler_profits/sample_size)*100.00)

plt.axhline(0, color = 'r')
plt.ylabel('Account Value')
plt.xlabel('Wager Count')
plt.show()