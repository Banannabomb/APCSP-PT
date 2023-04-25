import random
import os
#This input is for how much money the player has: if they run out of money they can no longer player
money = int(
 input("In an integer value, enter how much money you have to play with"))
cardsDefault = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "A",]
bet = 0
action = None
runTimeCards = []
#Iterates over the default deck and adds all the cards to a "runtime" deck
for x in cardsDefault:
	runTimeCards.append(x)
playerHand = []
dealerHand = []
splitHand1 = []
splitHand2 = []

#This function performs a "hit" on a hand given in the parameter field. It uses the randint function to pull a random hand out of the runtime deck, add its to the hand, and then removes it from the deck.
def hit(player):
	x = random.randint(0, len(runTimeCards) - 1)
	if runTimeCards[x] == "A":
		player.insert(0, runTimeCards[x])
	else:
		player.append(int(runTimeCards[x]))
	runTimeCards.pop(x)


def deal():
	for i in range(2):
		hit(dealerHand)
		hit(playerHand)

#This function evaluates a hand given in the parameter: if there are ace's it treats them as 1 or 11. It will return both sums to the player, so they can feel safe hitting if it is really close, but for gameplay it will treat them as 11's. However if counting them as 11 puts the sum over 21 (bust) then it automatically counts them as 1. If the sum is still over 21, with or without an ace, the hand is considered bust. If the hand is exactly 21, the function will advise the player to stop hitting, as technically in blackjack they are allowed to hit on 21. 
#The function has a special condition, where if the parameter simply says "dealer" it will check for different conditions. This is the "computer" player, in blackjack the dealer has to follow rules to keep hitting or not. If they are below seventeen they must hit, and stop after they are above or equal to seventeen. In this variation of blackjack, if the dealer has an Ace in their hand, they must get above seventeen (this is known as soft seventeen)
def evaluate(player):
	if player == "dealer":
		evaluatedHand = []
		for x in dealerHand:
			evaluatedHand.append(x)
		AceCount = 0
		while ("A" in evaluatedHand):
			AceCount += 1
			evaluatedHand.remove("A")
		total = sum(evaluatedHand)
		if AceCount > 0:
			print("Dealer has an ace. If there sum is 17, they must hit")
			if total + AceCount * 11 < 18:
				hit(dealerHand)
				print("Dealer hand is now")
				print(dealerHand)
				return "Under"
			elif total + AceCount < 18 and total + AceCount * 11 > 21:
				hit(dealerHand)
				print("Dealer hand is now")
				print(dealerHand)
				return "Under"
			else:
				print(dealerHand)
				return "Over"
		elif total < 17:
			hit(dealerHand)
			print("Dealer hand is now")
			print(dealerHand)
			return "Under"
		else:
			return "Over"
	else:
		evaluatedHand = []
		for x in player:
			evaluatedHand.append(x)
		AceCount = 0
		while ("A" in evaluatedHand):
			AceCount += 1
			evaluatedHand.remove("A")
		total = sum(evaluatedHand)
		if AceCount > 0:
			if total + AceCount * 11 > 21:
				if total + AceCount > 21:
					return [("Sum is " + str(total + AceCount) + ", meaning you bust"), "Bust"]
				elif total + AceCount == 21:
	
					return [("Sum is 21. You could hit again but you really shouldn't, because youll lose"), total + AceCount]
				else:
	
					return [("Sum is " + str(total + AceCount)), (total + AceCount)]
			elif total + AceCount * 11 == 21:
	
				return [("Sum is " + str(total + AceCount) + " or " + str(total + 11 * AceCount) + "You have a 21, you could hit again but you really shouldn't, because youll lose"), total + 11 * AceCount]
			else:
	
				return [ ("Sum is " + str(total + AceCount) + " or " + str(total + 11 * AceCount)),	 total + 11 * AceCount]
		else:
			if total > 21:
	
				return [("Sum is " + str(total) + ", meaning you bust"), "Bust"]
			elif total == 21:
	
				return [("Sum is 21. You could hit again but you really shouldn't, because youll lose"), total]
			else:
				return [("Sum is " + str(total)), total]

#This scores the game by comparing two hands: if both dealer and the hand in the parameter bust, it is a draw, if they have the same sum it is a draw. But if one player has a greater score, they win. If the other player busted but one did not, they win
def score(hand):
	player = evaluate(hand)
	dealer = evaluate(dealerHand)
	if player[1] == dealer[1]:
		print("Draw")
		return "Draw"
	elif player[1] == "Bust":
		print("Player busted")
		return "Player Lost"
	elif dealer[1] == "Bust":
		print("Dealer busted")
		return "Player Won"
	elif player[1] > dealer[1]:
		print("Player wins")
		return "Player Won"
	elif player[1] < dealer[1]:
		print("Dealer wins")
		return "Player Lost"

#This function takes the users input, if they hit the function calls the hit function on the hand listed in the parameter. If the hand is the first split hand, it has a unique output
def hitOrStand(action, firstSplitHand, hand):
	if firstSplitHand:
		if action == "hit":
			hit(hand)
			print("This is your hand")
			print(hand)
			print("This is the dealer's showing card")
			print(dealerHand[0])
			print(evaluate(hand)[0])
		if action == "stand":
			print("OK, your first hand is done. We will now play your second hand")
	else:
		if action == "hit":
			hit(hand)
			print("This is your hand")
			print(hand)
			print("This is the dealer's showing card")
			print(dealerHand[0])
			print(evaluate(hand)[0])
		if action == "stand":
			print("The dealer will now play")
			print("This is the dealer's full hand. They must hit if they are below 17, and on soft 17")
			print(dealerHand)
			print(evaluate(dealerHand)[0])
			while (evaluate("dealer") != "Over" and evaluate(dealerHand) != "Bust"):
				evaluate("dealer")
				print(evaluate(dealerHand)[0])

#This function is called in game in the special case where the player has identical cards: it works the same as game, but it plays two hands for the player and evaluates if they won after both hands are played
def splitScenario():
	global action
	global bet
	global money
	splitHand1.append(playerHand[0])
	splitHand2.append(playerHand[1])
	hit(splitHand1)
	hit(splitHand2)
	while (evaluate(splitHand1)[1] != "Bust" and action != "stand"):
		print("Your cards for your first hand are ", end="")
		print(splitHand1)
		print("The dealer is showing " + str(dealerHand[0]))
		print(evaluate(splitHand1)[0])
		action = str(
		 input("Do you want to 'hit' or 'stand' on your first hand").lower())
		hitOrStand(action, True, splitHand1)
	action = None
	while (evaluate(splitHand2)[1] != "Bust" and action != "stand"):
		print("Your cards for your second hand are ", end="")
		print(splitHand2)
		print("The dealer is showing " + str(dealerHand[0]))
		print(evaluate(splitHand2)[0])
		action = str(
		 input("Do you want to 'hit' or 'stand' on your second hand").lower())
		hitOrStand(action, False, splitHand2)
	outcomeHandOne = score(splitHand1)
	outcomeHandTwo = score(splitHand2)
	if outcomeHandOne == "Player Won" and outcomeHandTwo == "Player Won":
		print("Both hands won! You get " + str(2*bet))
		money += 2 * bet
		bet = 0
	elif outcomeHandOne == "Player Lost" and outcomeHandTwo == "Player Lost":
		print("You lost completely. You Lose " + str(bet))
		bet = 0
	elif outcomeHandOne == "Player Lost" and outcomeHandTwo == "Player Won" or outcomeHandOne == "Player Won" and outcomeHandTwo == "Player Lost":
		print("You lost one hand but won the other. You don't lose or gain anything, the bet of " + str(bet) + " is returned.")
		money += bet
		bet = 0
	else:
		print("You and the dealer had the same score, on both hands. Wow! The bet will push")
		

#This is where the main "gameplay" happens: the computer asks for a bet, checks for blackjack or split, and then asks the player how they would like to play. Afterwards, it evaluates and decides if the player won or not
def game():
	global bet
	global money
	global action
	bet += int(input("You have " + str(money) + " dollars. In an integer value, how much money do you want to bet?"))
	if bet > money or not(isinstance(bet, int)) or bet == 0:
		while bet > money or not(isinstance(bet, int)) or bet == 0:
			bet += int(
			 input("That bet is not valid, you have " + str(money) + " dollars. In an integer value, how much money do you want to bet? You must bet at least 1 dollar"))
	deal()
	money -= bet
	if playerHand[0] == playerHand[1]:
		print("Your cards are ", end="")
		print(playerHand)
		print("The dealer is showing " + str(dealerHand[0]))
		print(evaluate(playerHand)[0])
		action = str(input("You have a matching pair, meaning you can 'split.' Do you want to 'split' or 'not'").lower())
		if action == "split":
			splitScenario()
			return
		else:
			print("OK, you will play with your one hand")
	if evaluate(playerHand)[1] == 21 and evaluate(dealerHand)[1] == 21:
		print("Double Black Jack! The bet will push")
		return
	elif evaluate(playerHand)[1] == 21:
		print("Black Jack! You get " + str(2*bet))
		money += 2*bet
		bet = 0
		return
	elif evaluate(dealerHand)[1] == 21:
		print("The dealer hit Black Jack! You lost")
		bet = 0
		return
	else:
		while (evaluate(playerHand)[1] != "Bust" and action != "stand"):
			print("Your cards are ", end="")
			print(playerHand)
			print("The dealer is showing " + str(dealerHand[0]))
			print(evaluate(playerHand)[0])
			action = str(input("Do you want to 'hit' or 'stand'").lower())
			hitOrStand(action, False, playerHand)
		outcome = score(playerHand)
		if outcome == "Player Won":
			print("You won! You get " + str(2*bet))
			money += 2 * bet
			bet = 0
		elif outcome == "Player Lost":
			print("You lost. You Lose " + str(bet))
			bet = 0
		else:
			print("You and the dealer had the same score. The bet will push")

#This loop controls whether or not the next hand gets played: if the player says quit, the program ends. Additionally, if they run out of money, and the last hand was not a push, the game ends
quitOrPlay = "play"
while (quitOrPlay == "play"):
	if (money == 0 and bet == 0):
		print("You are out of money and the last bet did not push. Game over!")
		quitOrPlay == "quit"
		continue
	runTimeCards.clear()
	for x in cardsDefault:
		runTimeCards.append(x)
	playerHand.clear()
	dealerHand.clear()
	splitHand1.clear()
	splitHand2.clear()
	action = None
	if quitOrPlay == "play":
		game()
	elif quitOrPlay == "quit":
		continue
	quitOrPlay = input("Enter 'play' to keep playing or 'quit' to quit").lower()
	while quitOrPlay != "quit" and quitOrPlay != "play":
		quitOrPlay = input("Invalid entry. Enter 'play' to keep playing or 'quit' to quit").lower()
	os.system('cls||clear')
