import random  # imported to create a randomizer function for both computer card selection and deck shuffling
import sys  # imported to use sys.exit() at game completion


index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,  # index numbers for all 52 cards in the deck,
         # corresponding to the index==>English translation key dictionaries below
         14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
         27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
         40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]

decksuits = {1: "clubs", 2: "diamonds", 3: "hearts", 4: "spades",  # index==>suit translator
             5: "clubs", 6: "diamonds", 7: "hearts", 8: "spades",
             9: "clubs", 10: "diamonds", 11: "hearts", 12: "spades",
             13: "clubs", 14: "diamonds", 15: "hearts", 16: "spades",
             17: "clubs", 18: "diamonds", 19: "hearts", 20: "spades",
             21: "clubs", 22: "diamonds", 23: "hearts", 24: "spades",
             25: "clubs", 26: "diamonds", 27: "hearts", 28: "spades",
             29: "clubs", 30: "diamonds", 31: "hearts", 32: "spades",
             33: "clubs", 34: "diamonds", 35: "hearts", 36: "spades",
             37: "clubs", 38: "diamonds", 39: "hearts", 40: "spades",
             41: "clubs", 42: "diamonds", 43: "hearts", 44: "spades",
             45: "clubs", 46: "diamonds", 47: "hearts", 48: "spades",
             49: "clubs", 50: "diamonds", 51: "hearts", 52: "spades"}

decklist = {1: "ace", 2: "ace", 3: "ace", 4: "ace",  # index==>face value translator
            5: "two", 6: "two", 7: "two", 8: "two",
            9: "three", 10: "three", 11: "three", 12: "three",
            13: "four", 14: "four", 15: "four", 16: "four",
            17: "five", 18: "five", 19: "five", 20: "five",
            21: "six", 22: "six", 23: "six", 24: "six",
            25: "seven", 26: "seven", 27: "seven", 28: "seven",
            29: "eight", 30: "eight", 31: "eight", 32: "eight",
            33: "nine", 34: "nine", 35: "nine", 36: "nine",
            37: "ten", 38: "ten", 39: "ten", 40: "ten",
            41: "jack", 42: "jack", 43: "jack", 44: "jack",
            45: "queen", 46: "queen", 47: "queen", 48: "queen",
            49: "king", 50: "king", 51: "king", 52: "king"}

pural = ["aces", "twos", "threes", "fours", "fives", "sevens",  # trying to recapture pluralized forms of card values
         "eights", "nines", "tens", "jacks", "queens", "kings"]
sixes = ["sixes"]  # special case for six as it has unique pluralization
#   in the future I want to include cases where the player inputs the numerical value for the card they're trying to ask for


class Player:  # initializing a player class to handle some specific functions/track unique counters
    def __init__(self, name, hand, books, index, decksuits, decklist):
        self.name = name
        self.hand = hand
        self.book = books

    def checkhand(player, card):  # function that identifies if a card is in a player's hand
        n = 0  # one call form of this function is to check the validity of asking for a card
        if isinstance(card, int) == True:  # the other answers whether or not the asked player has the card requested
            card = decklist[card]
        togive = []
        for cards in player.hand:
            if card != decklist[cards]:
                decklist[cards]
                n += 1
                if n == len(player.hand):
                    return False
            else:
                togive.append(player.hand[n])
        return togive  # returns a list of valid cards in the case of players having more than one "two" for example
        #   the returned values are in index form

    def ask(human, comp, turn):  # handles player v computer making requests of each other
        if turn == 1:  # I ended up hardcoding in turn structure, I wasn't quite good enough to get
            print("You have:", end="\n")  # this done with a requester-agnostic structure yet,
            for cards in human.hand:  # my next pass will be trying to streamline the code via better class method structuring and calls
                print(decklist[cards], "of", decksuits[cards], end="\n")
            # player input selector from available cards in hand
            print("\nWhat card do you want to ask for?:\n")
            card = input("Card:").lower()
            if card in pural:
                card = card[0: -1]
                # this block is the translator from plural inputs to the singular versions accepted
                card = ''.join(card)
            elif card in sixes:  # by the asker function
                card = "six"
            if human.checkhand(card) == False:  # case for checkhand identifying the card choice as invalid
                print(f"{"\nYou don't have any"} {card}{"s. Please select a valid card.\n"}")
                # re-runs the ask function on human turn if invalid input supplied
                human.ask(comp, turn)
            else:
                if card == "six":
                    print(f"{"\nYou ask: Do you have any"} {card}{"es?\n"}")
                    card = human.checkhand(card)[0]
                else:
                    print(f"{"\nYou ask: Do you have any"} {card}{"s?\n"}")
                    card = human.checkhand(card)[0]
            return card, turn  # if a valid card is selected, the indecised version is pulled and returned for the give() function
        else:
            # computer logic allows guaranteed selection of valid card in range(handsize)
            card = comp.hand[random.randint(0, len(comp.hand)-1)]
            if decklist[card] == "six":  # allowed me to skip running it through the checker on one step
                print(f"{"Computer says: Do you have any sixes?"}")
            else:
                print(f"{"Computer says: Do you have any"} {decklist[card]}{"s?"}")
            return card, turn  # returns the indecised card as in the human version


def give(human, comp, card, turn):  # handles requests from the other player for a valid card
    match = 0  # safeguard to reset the match condition for future use
    if turn == 1:  # again, yucky hard-coding; to be fixed in a future version :)
        if comp.checkhand(card) == False:  # instance of the second case call for checkhand
            # returns a response if card not found by asked player
            print("Computer says: No I don't have that kind of card\n")
        else:
            cards = comp.checkhand(card)  # if card found
            print("Computer says: Yes I do, here they are!\n")  # indicates to user
            transfer(comp, human, cards)  # runs the transfer function to fulfill request
            match = 1  # updates the match condition to allow repeating turns
    else:
        if human.checkhand(card) == False:  # as above
            print("You say: No I don't have that kind of card\n")
        else:
            cards = human.checkhand(card)  # as above
            print("You say: Yes I do, here they are!\n")
            transfer(human, comp, cards)
            print("You have:", end="\n")
            for cards in human.hand:
                print(decklist[cards], "of", decksuits[cards], end="\n")
            match = 1
    return match  # only returned portion is the match condition, as Player.hand handles the card transfers, no other return values needed


def transfer(giver, recipient, cards):  # handles transfer requests for valid cards found in giver's hand
    receipt = set()  # utilizing set to ensure no duplication happens--I found this to be a specific bug in earlier versions
    for card in cards:
        for item in giver.hand:  # iterating over the giver's hand to find all valid matches
            # checking an equality between the translated versions of cards in hand v card requested
            if decklist[card] == decklist[item]:
                card = item  # setting the card to the card found in the giver's hand
                # in previous versions not having this check prevented me from tranferrint all matches
                receipt.add(card)
    for card in receipt:  # after I'm just adding it to the set and then iterating through the set
        recipient.hand.append(card)  # to update the recipient's (asker's) hand
        # indicating to the user which cards were moved
        print(decklist[card], "of", decksuits[card], "transferred")
    receipt.clear()  # hard clearing the set in case of errant storage--there was a bug in previous versions where I didn't do
    # this where the card would be added multiple times or create dupes across the hands
    giver.hand = [card for card in giver.hand if card not in recipient.hand]
    #   after we just update the giver hand by removing any cards that are now in the asker's


def shuffle(index):  # shuffle function, its really straightforwards but it took foreeeeeeeeever to make and I'm quite proud of it
    deckindex = list(index)  # creates a dupe index to avoid accidentally updating the global copy and invalidating other functions
    holder = []  # creates a deck that will return for the deal function and the rest of the game to utilize
    n = 0
    while n < 52:  # failsave condition, makes sure the function only runs while there are still un-indexed cards in the deck
        n += 1
        number = random.choice(deckindex)  # randomizer, chooses from the dupe index
        holder.append(number)  # and adds to the new deck
        deckindex.remove(number)  # and removes them from the dupe index to avoid duplicates
    print("Deck is shuffled!")  # maybe I can do this with some set method in the next version
    return holder  # returns the deck


def draw(deck, human, comp, turn):  # this is probably THE most bloated function in the game
    match = 0  # hard coding match again     #   I definitely want to pare this down later on
    if len(deck) == 0:
        out = 1  # out condition used in the winning function to determine WHY the game is ending for printout
        winning(human, comp, out, deck, turn)  # which we call here
    if turn == 2:  # special turn counter, only utilized by the deal function to ensure no accidental
        n = 14  # 7 card draws outside of deal
        while n > 0:
            if n % 2 == 0:  # I actually really like this alternator logic I wrote in, dunno if there's a cleaner way or not
                human.hand.append(deck[0])  # just adding the drawn card to the appropriate hand
                # and indicating for the player
                print("You drew:", decklist[deck[0]], "of", decksuits[deck[0]])
                deck.pop(0)  # removes the top card of the deck so the deck actually cycles
                n -= 1  # decrements the n function as a countdown
            else:
                comp.hand.append(deck[0])
                deck.pop(0)
                n -= 1
    elif turn == 1:  # turn == 1 is the player condition as before
        # I still want to avoid this hard-coding in future versions
        print("You drew:", decklist[deck[0]], "of", decksuits[deck[0]])
        print()
        card = deck[0]  # assigning the drawn card to a variable for access in other funcitions
        for cards in human.hand:
            if decklist[cards] == decklist[deck[0]]:  # looking to see if the drawn card is a match
                match = 1
                # I only append AFTER checking for a match to make sure the game doesn't
                human.hand.append(deck[0])
                # add the card to the hand and then find that the card it just added matches the card it drew
                deck.pop(0)
                # which is obviously the same card--this was a funny bug to find when I had the timing wrong
                print("You drew a match!")
                return deck, turn, match, card  # returns these values for the gofish() funciion to handle match/turn logic
        human.hand.append(deck[0])
        deck.pop(0)
        return deck, turn, match, card  # same
    elif turn == 0:
        print()
        card = deck[0]
        for cards in comp.hand:
            if decklist[cards] == decklist[deck[0]]:
                match = 1
                comp.hand.append(deck[0])
                deck.pop(0)
                # as above this is just a game stage indicator for clarity
                print("Computer drew a match!")
                return deck, turn, match, card
        comp.hand.append(deck[0])
        deck.pop(0)
        return deck, turn, match, card
    human.hand.sort()  # I sorted the hands after every drawing iteration
    comp.hand.sort()  # I also do this in the turns() function as a readability concession
    return deck, turn


def deal(deck, human, comp):  # very short deal function
    # basically just calls the draw function with the special turn condition
    deck, turn = draw(deck, human, comp, 2)
    print()
    turn = random.randint(0, 1)  # I also used this to code in the "who goes first" coinflip
    return deck, turn  # in future versions I plan to let the player select heads or tails and have a printout of this


# this function is called in turns() whenever a player fails to find a match from their opponent
def gofish(deck, human, comp, turn):
    # calls the draw function passing in the turns counter to ID the player
    deck, turn, match, card = draw(deck, human, comp, turn)
    if match == 1:  # handles the return value to ID if a player found a match on the topdeck
        if turn == 1:  # ID's the player who drew the match
            player = human
        else:
            player = comp
        # runs the books() function which checks to see if a player hit four of a kind
        count, turn = books(human, comp, turn, card)
        player.book += count  # increments the Player.book count to keep track of score
        out = 0  # the second case for the out condition, IDs for the winning() function that if the game ends
        # here that it wasn't because the deck ran out (this is for the function's print out)
        winning(human, comp, out, deck, turn)
    else:
        # calls the turn swapping logic to make sure if no match is found that players take turns
        turner(deck, human, comp, turn)


def end(human, comp):  # this is the "determine the winner" logic block
    if human.book > comp.book:  # directly compares the number of books each player completed
        win = 1
    elif human.book < comp.book:
        win = 2
    else:
        win = 0
    if win == 1:
        winner = str(human.name) + " has collected more books, " + \
            str(human.name) + " is the winner!"
    elif win == 2:
        winner = str(comp.name) + " has collected more books, " + str(comp.name) + " is the winner!"
    else:
        # in the ultra rare case, the deck runs out while neither player passed the other in books
        winner = "Neither player collected more books, game ends in a draw."
    print(winner)
    # I tried to get as many forms of yes in as possible for repeating the game
    if input("Would you like to play again?:") in {"y", "ya", "yes", "yea", "yep", "yeah", "sure"}:
        main()
    else:
        sys.exit()  # just allowing you to close the program if you're done after a round


def turner(deck, human, comp, turn):  # turn swapping logic block
    if turn == 1:
        turn = 0
    else:
        turn = 1
    # re-calls the turns function to restart the gameplay loop with the updated turns
    turns(deck, human, comp, turn)


def books(human, comp, turn, card):  # four of a kind checker function
    key = decklist[card]  # reads the  drawn/recieved card into a variable
    booklist = [key]  # adds the variable to a list
    for cards in decklist:  # iterates through the english library of card values
        if decklist[cards] == decklist[card]:
            booklist.append(cards)  # appends the remaining three index numbers to the list
    if turn == 1:
        player = human
    else:
        player = comp
    count = 0  # establishes a 0 case for how many cards/4 in a book are found in hand
    for cards in player.hand:  # iterates through the checked player hand
        # if any matches are found between their hand and the card value of the added card
        if decklist[cards] == decklist[card]:
            count += 1  # count increments
            if count == 4:  # if the player has 4 copies of a specific card, say, "kings"
                # it rewrites the hand as cards - cards in the booklist
                player.hand = [card for card in player.hand if card not in booklist]
                # indicates which cards are removed from the hand and game
                print(f"{"\nBook complete,"} {decklist[cards]}{"'s removed\n"}")
                return count, turn  # returns needed values to the turns() function for player ID and scoring
    count = 0  # safety condition to prevent the game erroneously indicating a player completed books on the backend when they did not
    return count, turn


def winning(human, comp, out, deck, turn):  # determines if the game ends based on
    if len(human.hand) == 0:  # someone going out
        print(f"{human.name} {"has gone out, game will now end!"}")
        end(human, comp)
    elif len(comp.hand) == 0:
        print(f"{comp.name} {"has gone out, game will now end!"}")
        end(human, comp)
    elif out == 1:  # or the deck running out of cards
        print("Deck has run out of cards, game will now end!")
        end(human, comp)
    else:
        turns(deck, human, comp, turn)  # in the null case, the game just continues
        #   I structured it this way so every turn and every draw
        #   the game would check to see if it should still keep going


def turns(deck, human, comp, turn):  # gameplay loop function
    human.hand.sort()  # as mentioned before, SORTING
    comp.hand.sort()
    if turn == 1:
        card, turn = human.ask(comp, turn)  # runs the asker function
        match = give(human, comp, card, turn)  # runs the give and transfer functions as appropriate
    else:
        card, turn = comp.ask(comp, turn)
        match = give(human, comp, card, turn)
    if match == 1:  # handles players finding a match
        if turn == 1:
            player = human
        else:
            player = comp
        count, turn = books(human, comp, turn, card)
        player.book += count
        out = 0
        winning(human, comp, out, deck, turn)
    else:
        print("Go fish!")  # or not!
        gofish(deck, human, comp, turn)


def main():  # main block, I tried to keep this as minimal as possible1
    name = input("Welcome to GoFish, what is your name?:")  # for display on game end
    deck = shuffle(index)  # calls the shuffle function utilizing the card index
    playerhand = []  # initializes both human and comp hands for use
    comphand = []
    playerbooks = 0  # as well as their # of books completed
    compbooks = 0
    # initializing the Player instances once the needed
    human = Player(name, playerhand, playerbooks, index, decksuits, decklist)
    comp = Player("Computer", comphand, compbooks, index,
                  decksuits, decklist)  # variables are there
    # finishes the game setup by dealing cards and deciding who goes first
    deck, turn = deal(deck, human, comp)
    turns(deck, human, comp, turn)  # RUNS THE GAME!


if __name__ == '__main__':
    main()
