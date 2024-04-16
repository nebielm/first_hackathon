import wikipedia
import random
from thefuzz import process

GREEN = '\033[92m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
RED = '\033[31m'
RESET = '\033[0m'

# get number and name of the players


def game_setup():
    print(GREEN + BOLD + "Welcome to the Wi-keep-Guessia Game!\n" + RESET)
    print("Get ready to embark on an epic journey through the vast realm of Wikipedia.")
    print("Set up the game, dive into a random Article, and guess what could be a Wiki-Article linked to it, with three chances per turn.")
    print("Who among you will emerge as the ultimate Wikipedia Champion?")
    print("Let the guessing adventure begin!\n")
    number_of_players = int(input("Players number: "))
    names_of_players = []
    for player in range(1, number_of_players + 1):
        name = input(f"Name of player {player}: \n")
        names_of_players.append(name)
    return number_of_players, names_of_players

# get a title from a random wikipedia article


def get_random_title():
    topics = [
        'history',
        'mathematics',
        'economics',
        'engineering',
        'programming',
        'movies',
        'sport',
        'health',
        'politics',
        'music'
    ]
    # use randint to get a random index of the topics list
    topic = topics[random.randint(0, len(topics) - 1)]
    # return a list of tiles similar to the topic
    title = wikipedia.search(topic)
    return title[0]

# get all link-titles from the specific wikipedia article


def get_article_links(title):
    return wikipedia.page(title, auto_suggest=False).links

# ask the player to replay or  end the game


def end_game():
    print(GREEN + BOLD + "Thank you for playing Wi-keep-Guessia!" + RESET)
    while True:
        choice = input("Do you want to play again? (yes/no): ").lower()
        if choice == "yes":
            print("\nLet's start a new game!\n")
            main()
        elif choice == "no":
            print("Goodbye! See you next time.")
            break
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")


def main():

    number_of_players, names_of_players = game_setup()
    ranking_dict = {}

    for player in range(number_of_players):
        name = names_of_players[player]
        print(f"Attention {name}, it's time to prove your mastery!")
        print("Prepare yourself for the challenge ahead!")
        print("Your journey begins with a title from a randomly selected Wikipedia article.\n")

        right_guesses = 0
        wrong_guesses = 0
        right_guesses_list = []

        first_title = get_random_title()
        print("The first article to explore is: ", first_title)
        right_guesses_list.append(first_title)
        # actualizes itself through while loop
        last_article_links = get_article_links(right_guesses_list[-1])

        while wrong_guesses < 3:
            guessed_title = input(
                f"Guess a title of an article linked to {right_guesses_list[-1]} (min. 5 letters long): \n")
            print()
            if len(guessed_title) < 5:
                print(
                    YELLOW + "You've entered a title under 5 letters. Try again" + RESET)
                continue

            # gets the best match link to the user input and shows the similarity score
            # example syntax of match: ('Python (programming language)', 95)
            match = process.extractOne(guessed_title, last_article_links)

            # checks if the similarity score is above 85% and if guessed_title was guessed before
            if match[1] > 85 and match[0] not in right_guesses_list:
                print(GREEN + "Bravo! You've made a correct guess!" + RESET)
                print(
                    f"The best match found to your guess was: {match[0]}.\n")
                right_guesses += 1
                right_guesses_list.append(match[0])
                last_article_links = get_article_links(match[0])

            elif match[1] > 85 and match[0] in right_guesses_list:
                print(
                    YELLOW + "Oops! You've already explored this Title. Try another one!\n" + RESET)

            else:
                wrong_guesses += 1
                if wrong_guesses < 3:
                    print(
                        RED + f"Sorry, that's not the right path. Keep trying! You have {3 - wrong_guesses} guesses left.\n" + RESET)

        print(f"You've used up all wrong guesses  " + RED +
              "Game over" + RESET + f" Right guesses: {right_guesses}\n")
        ranking_dict[name] = right_guesses

    ordered_ranking_list = sorted(ranking_dict.items(), key=lambda item: int(item[1]), reverse=True)

    print("..................And the winner is ...................")
    print("*******************************************************")
    print("*                                                     *")
    print("*                 🎉🎉 Winner! 🎉🎉                  *")
    print(
        f"*                      {ordered_ranking_list[0][0]}                         *")
    print("*                                                     *")
    print(
        f"*    Congratulations {ordered_ranking_list[0][0]} wins with {ordered_ranking_list[0][1]} right guesses!    *")
    print("*                                                     *")
    print("*******************************************************")

    end_game()  # Call the end_game function after the game finishes


if __name__ == '__main__':
    main()
