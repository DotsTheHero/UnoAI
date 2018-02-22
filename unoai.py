import random
import subprocess as sp
class Player(object):
	def __init__(self, isai):
		self.score=0
		self.hand=[]
		self.handno=0
		self.isai=isai
	def showhand(self):
		i=0
		for card in self.hand:
			print (str(i)+": "+str(card)+"\n")
			i+=1
	def draw(self, deck):
		self.hand.append(deck.draw())
		self.handno=self.handno+1
	def drawx(self, deck, i):
		for x in range(0,i):
			self.draw(deck)
	def playcard(self, deck, i): #all logic checking to see if card is valid to be played occurs here. It returns a 1 on error and a 0 on success
		i=int(i)
		if i<-1 or i>self.handno-1:
			print("Violation: That card doesn't exist")
			return -1
		elif i==-1:
			self.draw(deck)
			i=self.handno-1
			print ("You have drawn a card. It is a "+str(self.hand[self.handno-1])+" ")
			j=input('Would you like to play it? 0=no 1=yes')
			if j==1 and (deck.curcard.cardid[0]==self.hand[i].cardid[0] or deck.curcard.cardid[1]==self.hand[i].cardid[1] or self.hand[i].cardid[0]==4):
				self.handno=self.handno-1
				effect=self.hand[i].cardid[1]
				deck.play(self.hand.pop(i))
				return effect
			#elif j==1 and (not(deck.curcard.cardid[0]==self.hand[i].cardid[0] or deck.curcard.cardid[1]==self.hand[i].cardid[1] or self.hand[i].cardid[0]==4)):
			input("That card was unplayable, sorry. Hit enter to continue.")
			return 0
		elif(deck.curcard.cardid[0]==self.hand[i].cardid[0] or deck.curcard.cardid[1]==self.hand[i].cardid[1] or self.hand[i].cardid[0]==4):
			self.handno=self.handno-1
			effect = self.hand[i].cardid[1]
			deck.play(self.hand.pop(i))
			return effect
		else:
			print ("Violation: Card is not playable")
			return -1
	def emptyhand(self, deck):#empties the hand of the player into the deck provided
		deck.discardpile=deck.discardpile+self.hand
		handno=0
		self.hand=[]
		
class Card(object):
	def __init__(self, cardid):
		self.cardid=cardid
	def __str__(self):
		ret=""
		if self.cardid[0]==0:
			ret+="Red "
		elif self.cardid[0]==1:
			ret+="Blue "
		elif self.cardid[0]==2:
			ret+="Yellow "
		elif self.cardid[0]==3:
			ret+="Green "
		elif self.cardid[0]==4:
			ret+="Wild "
		else:
			ret+="INVALID "

		if self.cardid[1]>=0 and self.cardid[1]<=9:
			ret+=str(self.cardid[1])
		elif self.cardid[1]==10:
			ret+="Draw 2"
		elif self.cardid[1]==11:
			ret+="Reverse"
		elif self.cardid[1]==12:
			ret+="Skip"
		elif self.cardid[1]==13:
			ret+=""
		elif self.cardid[1]==14:
			ret+="Draw Four"
		elif self.cardid[1]==15:
			ret+="Any"
		elif self.cardid[1]==16:
			ret+="Any4"
		return ret
	def __cmp__(self, other):
		if self.cardid==other.cardid:
			return 0
		else:
			return 1
		

class Deck(object):
	def __init__(self):#(color,rank)
		self.cards = [Card((0,0)),Card((0,1)),Card((0,1)),Card((0,2)),Card((0,2)),Card((0,3)),Card((0,3)),Card((0,4)),Card((0,4)),Card((0,5)),Card((0,5)),Card((0,6)),Card((0,6)),Card((0,7)),Card((0,7)),Card((0,8)),Card((0,8)),Card((0,9)),Card((0,9)),Card((0,10)),Card((0,10)),Card((0,11)),Card((0,11)),Card((0,12)),Card((0,12)),Card((1,0)),Card((1,1)),Card((1,1)),Card((1,2)),Card((1,2)),Card((1,3)),Card((1,3)),Card((1,4)),Card((1,4)),Card((1,5)),Card((1,5)),Card((1,6)),Card((1,6)),Card((1,7)),Card((1,7)),Card((1,8)),Card((1,8)),Card((1,9)),Card((1,9)),Card((1,10)),Card((1,10)),Card((1,11)),Card((1,11)),Card((1,12)),Card((1,12)),Card((2,0)),Card((2,1)),Card((2,1)),Card((2,2)),Card((2,2)),Card((2,3)),Card((2,3)),Card((2,4)),Card((2,4)),Card((2,5)),Card((2,5)),Card((2,6)),Card((2,6)),Card((2,7)),Card((2,7)),Card((2,8)),Card((2,8)),Card((2,9)),Card((2,9)),Card((2,10)),Card((2,10)),Card((2,11)),Card((2,11)),Card((2,12)),Card((2,12)),Card((3,0)),Card((3,1)),Card((3,1)),Card((3,2)),Card((3,2)),Card((3,3)),Card((3,3)),Card((3,4)),Card((3,4)),Card((3,5)),Card((3,5)),Card((3,6)),Card((3,6)),Card((3,7)),Card((3,7)),Card((3,8)),Card((3,8)),Card((3,9)),Card((3,9)),Card((3,10)),Card((3,10)),Card((3,11)),Card((3,11)),Card((3,12)),Card((3,12)),Card((4,13)),Card((4,13)),Card((4,13)),Card((4,13)),Card((4,14)),Card((4,14)),Card((4,14)),Card((4,14))]
		random.shuffle(self.cards)
		self.discardpile = []
		self.pilesize= 0
		self.cardno=108
		self.curcard=self.draw()
	def showcurcard(self):
		print("Current Card: "+str(self.curcard))
	def draw(self):
		self.cardno=self.cardno-1
		ret = self.cards.pop()
		if self.cardno==0:
			self.shuffle()
		return ret
	def shuffle(self):
		self.cardno+=self.pilesize
		self.cards=self.cards+self.discardpile
		self.pilesize=0
		self.discardpile=[]
		random.shuffle(self.cards)
		print ("The deck was exhausted, and thus, reshuffled the discard pile into itself\n")
	def discardtop(self):
		self.cardno=self.cardno-1
		self.discardpile.append(self.cards.pop())
		self.pilesize+=1
	def play(self, playcard):#This merely recieves a card being played. It puts complete faith in the fact that checking has been done already, and makes no checks of its own
		self.pilesize+=1
		if  self.curcard.cardid[1]==15:
				self.curcard= Card((4,13))
		elif self.curcard.cardid[1]==16:
				self.curcard= Card((4,14))
		self.discardpile.append(self.curcard)
		self.curcard=playcard
	def __str__(self):
		ret=""
		for card in self.cards:
			ret=ret+str(card)+"\n"
		return ret
class Game(object):
	def __init__(self, deck, players):
		self.deck=deck
		self.players=players
		self.curturn=0
		self.cureffect=0 #The current unresolved effect from a card play. This could be a skip, a draw, a reverse, or a wild
		self.skipflag=0 #The flag that represents whether a skip is in effect
		self.roundendflag=0 #This is how a round knows how to end. When it's 1, it will end, this is mainly to check to see if the game is over.
		self.gameendflag=0 #This is how the game knows when to end. When it's 1, it will end
	def rungame(self):
		while self.gameendflag==0:
			self.gameendflag=self.runround()
			print ("Round over!")
		print ("The game is over! Player "+str(self.curturn+1)+" won!\n")
		input("Hit enter to continue.")
	def runround(self):
		self.deal()
		while self.roundendflag==0:
			self.roundendflag=self.runturn()
		#Must now award points, curturn should be currently pointing at the player who won, and therefore must get points.
		self.players[self.curturn].score+=1
		if self.players[self.curturn].score==1:
			return 1
	def runturn(self):#This will differentiate between player and AI and run the turn properly.
		if self.players[self.curturn].isai==0: #the player isn't an AI, run turn as normal
			
			print ("Your turn! You have "+str(self.players[self.curturn].handno)+" cards in your hand")
			print ("Your opponent has "+str(self.players[(self.curturn+1)%2].handno))
			print ("The deck has "+str(self.deck.cardno)+" cards remaining")
			#First, show the player their hand
			players[self.curturn].showhand() #THIS CAN AND SHOULD BE REPLACED BY SOME PYGAME STUFF TO MAKE IT PRETTY LATER
			#Show them the current card next to the deck face up
			self.deck.showcurcard()
			#Then, accept the card that they wish to play and try to play it
			self.cureffect=-1
			while self.cureffect==-1: #will keep going until proper input is entered
				i = input('Select a card to try to play, or -1 to draw a card\n')
				self.cureffect = players[self.curturn].playcard(self.deck, i) #Tries to play the card told to it, and saves the effect, or uses the effect in to handle erroneous input
			tmp=sp.call('cls',shell=True)
		else: #Then the player is an AI. This will be far more complicated but ultimately get the same things done
			self.cureffect= self.aiturn()
		
		#Here, you must deal with any outstanding, unhandled card effects as a result of the card played this turn
		if self.cureffect==10:
			#DEAL WITH A DRAW 2 HERE
			self.skipflag=1
			self.players[(self.curturn+1)%2].drawx(self.deck, 2)
			print("Draw 2 played")
		elif self.cureffect==12:
			#DEAL WITH A SKIP HERE
			self.skipflag=1
			print("Skip played")
		elif self.cureffect==13:
			#DEAL WITH A WILD CARD HERE
			i=-1
			while i==-1:
				if self.players[self.curturn].isai==0:
					i=input('Select a color for your Wild card: 0=red, 1=blue, 2=yellow, 3=green\n')
				else:
					i=self.getbestcolor()
				if i>=0 and i<=3:
					self.deck.curcard= Card((i,15))
				else:
					i=-1
			print("Wild played")
		elif self.cureffect==14:
			#DEAL WITH A DRAW 4 HERE
			i=-1
			while i==-1:
				if self.players[self.curturn].isai==0:
					i=input('Select a color for your Wild card: 0=red, 1=blue, 2=yellow, 3=green\n')
					i=int(i)
				else:
					i=self.getbestcolor()
				if i>=0 and i<=3:
					self.deck.curcard= Card((i,15))
				else:
					i=-1
			self.skipflag=1
			players[(self.curturn+1)%2].drawx(self.deck, 4)
			print("Wild Draw 4 played")
		
		if (players[self.curturn].handno==0):#if a player's hand is empty...
			self.roundendflag=1
			return 1
		
		
		if self.skipflag==1:
			self.skipflag=0
		else:	
			self.curturn=(self.curturn+1)%2 #Sets the turn to be the other player's turn
		return 0
	def deal(self): #Deals out the cards at the beginning of a round
		for player in players:
			for i in range(0,7):
				player.draw(self.deck)
	def aiturn(self):
		#Checks to make sure that it can play, and doesn't have to draw. It does this by creating a list of which of its cards are playable. Does not get wilds, those are saved for emergencies
		x=0
		playables=[]#stores all playable cards, except for wilds
		wilds=[]#stores wilds for emergency use
		for card in self.players[self.curturn].hand:
			if card.cardid[0]==self.deck.curcard.cardid[0] or card.cardid[1]==self.deck.curcard.cardid[1]:
				playables.append(x)
			elif card.cardid[0]==4:
				wilds.append(x)
			x+=1
		#It should now have a list, playables, of the index numbers of all playable cards in its hand. Each will be analyzed and the most optimal will be chosen.
		if not playables: #If probs is empty, it has to draw.
			#but first it will try to play any wilds or wild draw 4s it has to save itself the indignity
			if not wilds:
				self.players[self.curturn].draw(self.deck)#draws new card
				temp = self.players[self.curturn].hand[-1]#saves reference to card
				if temp.cardid[0]==self.deck.curcard.cardid[0] or temp.cardid[1]==self.deck.curcard.cardid[1] or temp.cardid[0]==4:#if it works, play it
					return players[self.curturn].playcard(self.deck, self.players[self.curturn].handno-1)#Last card, which will always be the one just draw, is played
				else:
					return 0
			else:
				cardtoplay = wilds[0]
				effect = self.players[self.curturn].playcard(self.deck, cardtoplay)
				return effect
		
		#It will never play skips or draw cards unless it has no other options. Ideally, it wishes to save these kinds of cards up for an unstoppable combo-victory with them and skips.
		
		#Failing that, it will, using probability math, find the card in its hand that its opponent is the least likely to have a response to
		#This variable simulates the deck, so that we can estimate what cards we know are still 'out there' so to speak
		simuldeck = [Card((0,0)),Card((0,1)),Card((0,1)),Card((0,2)),Card((0,2)),Card((0,3)),Card((0,3)),Card((0,4)),Card((0,4)),Card((0,5)),Card((0,5)),Card((0,6)),Card((0,6)),Card((0,7)),Card((0,7)),Card((0,8)),Card((0,8)),Card((0,9)),Card((0,9)),Card((0,10)),Card((0,10)),Card((0,11)),Card((0,11)),Card((0,12)),Card((0,12)),Card((1,0)),Card((1,1)),Card((1,1)),Card((1,2)),Card((1,2)),Card((1,3)),Card((1,3)),Card((1,4)),Card((1,4)),Card((1,5)),Card((1,5)),Card((1,6)),Card((1,6)),Card((1,7)),Card((1,7)),Card((1,8)),Card((1,8)),Card((1,9)),Card((1,9)),Card((1,10)),Card((1,10)),Card((1,11)),Card((1,11)),Card((1,12)),Card((1,12)),Card((2,0)),Card((2,1)),Card((2,1)),Card((2,2)),Card((2,2)),Card((2,3)),Card((2,3)),Card((2,4)),Card((2,4)),Card((2,5)),Card((2,5)),Card((2,6)),Card((2,6)),Card((2,7)),Card((2,7)),Card((2,8)),Card((2,8)),Card((2,9)),Card((2,9)),Card((2,10)),Card((2,10)),Card((2,11)),Card((2,11)),Card((2,12)),Card((2,12)),Card((3,0)),Card((3,1)),Card((3,1)),Card((3,2)),Card((3,2)),Card((3,3)),Card((3,3)),Card((3,4)),Card((3,4)),Card((3,5)),Card((3,5)),Card((3,6)),Card((3,6)),Card((3,7)),Card((3,7)),Card((3,8)),Card((3,8)),Card((3,9)),Card((3,9)),Card((3,10)),Card((3,10)),Card((3,11)),Card((3,11)),Card((3,12)),Card((3,12)),Card((4,13)),Card((4,13)),Card((4,13)),Card((4,13)),Card((4,14)),Card((4,14)),Card((4,14)),Card((4,14))]
		data=self.players[self.curturn].hand+self.deck.discardpile #This has important data for its calculations coming now
		datatotal=self.deck.cardno
		for x in data:#for each card we have in data
			if x in simuldeck:
				simuldeck.remove(x)
		#Simuldeck now has every card we have reason to believe exists in the unknown area. Now find the playable with the lowest value.
		bestplayable=0#index number of best playable
		leastresp=108#amount of responses of best playable. This will always be overwritten
		index=0#iteration index
		for x in playables:
			count=0
			for y in simuldeck:
				if self.players[self.curturn].hand[x].cardid[0]==y.cardid[0] or self.players[self.curturn].hand[x].cardid[1]==y.cardid[1] or y.cardid[0]==4:
					count+=1
			if count<=leastresp:
				leastresp=count
				bestplayable=index
			index+=1
		cardtoplay= playables[bestplayable]#index of the best card, which will now be played
		effect= self.players[self.curturn].playcard(self.deck, cardtoplay)
		return effect
	def getbestcolor(self):#finds the color for which a player has the most of. Used by the AI to decide what to do with its WILDs
		reds=0
		blues=0
		yellows=0
		greens=0
		for card in self.players[self.curturn].hand:
			if card.cardid[0]==0:
				reds+=1
			elif card.cardid[0]==1:
				blues+=1
			elif card.cardid[0]==2:
				yellows+=1
			elif card.cardid[0]==3:
				greens+=1
		bestcol=max([reds,blues,yellows,greens])
		if reds==bestcol:
			return 0
		elif blues==bestcol:
			return 1
		elif yellows==bestcol:
			return 2
		elif greens==bestcol:
			return 3
tmp=sp.call('cls',shell=True)
unodeck = Deck()
meplayer = Player(0)
themplayer = Player(1)
players = [meplayer,themplayer]
thisgame = Game(unodeck,players)
thisgame.rungame()
#simuldeck = [Card((0,0)),Card((0,1)),Card((0,1)),Card((0,2)),Card((0,2)),Card((0,3)),Card((0,3)),Card((0,4)),Card((0,4)),Card((0,5)),Card((0,5)),Card((0,6)),Card((0,6)),Card((0,7)),Card((0,7)),Card((0,8)),Card((0,8)),Card((0,9)),Card((0,9)),Card((0,10)),Card((0,10)),Card((0,11)),Card((0,11)),Card((0,12)),Card((0,12)),Card((1,0)),Card((1,1)),Card((1,1)),Card((1,2)),Card((1,2)),Card((1,3)),Card((1,3)),Card((1,4)),Card((1,4)),Card((1,5)),Card((1,5)),Card((1,6)),Card((1,6)),Card((1,7)),Card((1,7)),Card((1,8)),Card((1,8)),Card((1,9)),Card((1,9)),Card((1,10)),Card((1,10)),Card((1,11)),Card((1,11)),Card((1,12)),Card((1,12)),Card((2,0)),Card((2,1)),Card((2,1)),Card((2,2)),Card((2,2)),Card((2,3)),Card((2,3)),Card((2,4)),Card((2,4)),Card((2,5)),Card((2,5)),Card((2,6)),Card((2,6)),Card((2,7)),Card((2,7)),Card((2,8)),Card((2,8)),Card((2,9)),Card((2,9)),Card((2,10)),Card((2,10)),Card((2,11)),Card((2,11)),Card((2,12)),Card((2,12)),Card((3,0)),Card((3,1)),Card((3,1)),Card((3,2)),Card((3,2)),Card((3,3)),Card((3,3)),Card((3,4)),Card((3,4)),Card((3,5)),Card((3,5)),Card((3,6)),Card((3,6)),Card((3,7)),Card((3,7)),Card((3,8)),Card((3,8)),Card((3,9)),Card((3,9)),Card((3,10)),Card((3,10)),Card((3,11)),Card((3,11)),Card((3,12)),Card((3,12)),Card((4,13)),Card((4,13)),Card((4,13)),Card((4,13)),Card((4,14)),Card((4,14)),Card((4,14)),Card((4,14))]
#data= [Card((0,0)),Card((0,1)),Card((0,1)),Card((0,2))]
#for x in data:
#	if x in simuldeck:
#		simuldeck.remove(x)
#for card in simuldeck:
#	print card




