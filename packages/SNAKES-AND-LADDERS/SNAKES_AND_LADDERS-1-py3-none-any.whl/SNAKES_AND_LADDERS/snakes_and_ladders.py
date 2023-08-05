"""
This file contains code for the game "Snakes and Ladders".
Author: GlobalCreativeCommunityFounder
"""


# Importing necessary libraries


import sys
import os
import random


# Creating necessary functions to be used throughout the code generator.


def value_in_dict(dictionary: dict, value: object) -> bool:
    return value in dictionary.keys() or value in dictionary.values()


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating main function used to run the game.


def main():
    """
    This function is used to run the game.
    :return: None
    """

    print("Welcome to 'Snakes and Ladders' by 'GlobalCreativeCommunityFounder'.")
    print("This game is a command line interface version of 'Snakes and Ladders' with 100 tiles on the board.")
    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    continue_playing: str = input("Do you want to continue playing 'Snakes and Ladders'? ")
    while continue_playing == "Y":
        # Creating the locations of snakes
        snakes: dict = {}  # initial value
        for i in range(5):
            snake_from: int = random.randint(2, 99)
            snake_to: int = random.randint(2, 99)
            while snake_to >= snake_from or value_in_dict(snakes, snake_to) or value_in_dict(snakes, snake_from):
                snake_from = random.randint(2, 99)
                snake_to = random.randint(2, 99)

            snakes[snake_from] = snake_to

        # Creating the locations of ladders
        ladders: dict = {}  # initial value
        for i in range(5):
            ladder_from: int = random.randint(2, 99)
            ladder_to: int = random.randint(2, 99)
            while ladder_to >= ladder_from or value_in_dict(snakes, ladder_from) or value_in_dict(snakes, ladder_to) \
                    or value_in_dict(ladders, ladder_from) or value_in_dict(ladders, ladder_to):
                ladder_from = random.randint(2, 99)
                ladder_to = random.randint(2, 99)

            ladders[ladder_from] = ladder_to

        # Location of both the player and the opponent
        player_location: int = 1
        opponent_location: int = 1

        # Variable determining whether it is player's or opponent's turn
        turn: int = 0

        while player_location < 100 and opponent_location < 100:
            clear()
            print("Your location: " + str(player_location))
            print("Your opponent's location: " + str(opponent_location))

            turn += 1
            if turn % 2 == 1:
                print("It is your turn to roll the dice!")
                print("Enter 'R' to roll the dice.")
                print("Enter anything else to quit.")
                action: str = input("What do you want to do? ")
                if action == "R":
                    dice_roll: int = random.randint(1, 6)
                    print("You are moving " + str(dice_roll) + " step(s) forwards.")
                    player_location += dice_roll
                    if player_location in snakes.keys():
                        print("You fall from tile number " + str(player_location) + " to tile number " +
                              str(snakes[player_location]))
                        player_location = snakes[player_location]

                    if player_location in ladders.keys():
                        print("You go up from tile number " + str(player_location) + " to tile number " +
                              str(ladders[player_location]))
                        player_location = ladders[player_location]

                if player_location >= 100:
                    print("YOU WIN!")
                    break

            else:
                print("It is your opponent's turn to roll the dice.")
                dice_roll: int = random.randint(1, 6)
                print("Your opponent is moving " + str(dice_roll) + " step(s) forwards.")
                opponent_location += dice_roll
                if opponent_location in snakes.keys():
                    print("Your opponent falls from tile number " + str(opponent_location) + " to tile number " +
                          str(snakes[opponent_location]))
                    opponent_location = snakes[opponent_location]

                if opponent_location in ladders.keys():
                    print("Your opponent goes up from from tile number " + str(opponent_location) + " to tile number " +
                          str(ladders[opponent_location]))
                    opponent_location = ladders[opponent_location]

                if opponent_location >= 100:
                    print("YOU LOSE!")
                    break

        clear()
        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_playing = input("Do you want to continue playing 'Snakes and Ladders'? ")
    sys.exit()


if __name__ == '__main__':
    main()
