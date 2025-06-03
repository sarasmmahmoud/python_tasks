import random

words = ["python", "programming", "computer", "algorithm", "database"]
word = random.choice(words)


print("***********************Hangman Game *****************************************!")

print("Guess the word!")

guessed = ""
turns = 6

while turns > 0:
    failed = 0  
    for char in word:
        if char in guessed:
            print(char, end=" ")
        else:
            print("_", end=" ")
            failed += 1
    if failed == 0:
        print("You Win!")
        print("The word is:", word)
        break

    guess = input("Guess a letter: ").lower()

    if guess in guessed:
        print("You already guessed this letter.")
    else:
        guessed += guess

    if guess not in word:
        turns -= 1
        print("Wrong guess.")
        print("You have", turns, "more guesses")

        if turns == 0:
            print("You Lose. The word was:", word)