# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
msg=""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    def drawback(self, canvas, pos):
        card_loc = (CARD_BACK_CENTER[0] , 
                    CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand=[]	# create Hand object
        
    def __str__(self):
        sHand=""
        for card in self.hand:	# return a string representation of a hand
          sHand = sHand + str(card) + " " 
        return "Hand contains "+sHand
        
    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value=0
        hasAce=False
        for card in self.hand:
            value = value + VALUES[card.get_rank()]
            if card.get_rank()=='A':
                hasAce=True
        if hasAce and value+10 <= 21 :
                value=value+10
        return value
                          
    def draw(self, canvas, pos):
        i=0
        for card in self.hand:
            card.draw(canvas,(pos[0]+i, pos[1]))
            i=i+100
        
        # draw a hand on the canvas, use the draw method for cards
 
     
# define deck class 
class Deck:
    def __init__(self):
        self.deck_of_cards=[]	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                self.deck_of_cards.append(Card(suit,rank))
              

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_of_cards)    # use random.shuffle()

    def deal_card(self):
        return self.deck_of_cards.pop()	# deal a card object from the deck
    
    def __str__(self):
        sDeck="" 	# return a string representing the deck
        for card in self.deck_of_cards:	
          sDeck = sDeck + str(card) + " " 
        return "Deck contains "+sDeck



#define event handlers for buttons
def deal():
    global outcome, in_play,msg,score
    global DeckOfCards, DealerHand, PlayerHand
    if in_play:
        msg="You loose!"
        score+=-1
        in_play=False
    outcome="Hit or Stand?"
    in_play = True
    msg=""
    DeckOfCards = Deck()
    PlayerHand=Hand()
    DealerHand=Hand()
    #print str(DeckOfCards)
    DeckOfCards.shuffle()
    #print str(DeckOfCards)
    PlayerHand.add_card(DeckOfCards.deal_card())
    PlayerHand.add_card(DeckOfCards.deal_card())
    DealerHand.add_card(DeckOfCards.deal_card())
    DealerHand.add_card(DeckOfCards.deal_card())
    #  print "Player Hand " + str(PlayerHand)
    # print "Dealer Hand " + str(DealerHand)
    

def hit():
    global in_play,score,PlayerHand,DeckOfCards,outcome,msg
    if in_play:
       PlayerHand.add_card(DeckOfCards.deal_card())
       if PlayerHand.get_value()>21:
            in_play=False
            outcome="New Deal?"
            score+=-1
            #print str(PlayerHand)
            msg="You have Busted! Dealer wins!"
            #print score
            #print "dealer"+str(DealerHand)
            #print "player"+str(PlayerHand)
        # else:
        # print "Player"+str(PlayerHand)
            
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global score,DealerHand,PlayerHand,DeckOfCards,in_play,outcome,msg
    if in_play:
       while DealerHand.get_value()<17:
        DealerHand.add_card(DeckOfCards.deal_card()) 
       in_play=False
       outcome="New Deal?"
       if DealerHand.get_value()>21:
            msg ="Dealer busts. You win!"
            score+=1
       elif DealerHand.get_value()>=PlayerHand.get_value() :
            score+=-1
            msg = "Dealer won"
       else:
            score+=1
            msg= "You won!"
         
              
       
            
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global PlayerHand,DealerHand,score,in_play,msg
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])
    PlayerHand.draw(canvas,(100,100))
    DealerHand.draw(canvas,(100,300))
    if in_play:
        DealerHand.hand[0].drawback(canvas,(100,300))      
    canvas.draw_text('Blackjack', (30, 30), 30, 'Red')
    canvas.draw_text(outcome, (30, 70), 30, 'Red')
    canvas.draw_text('Score: '+str(score), (300, 70), 30, 'Red')
    canvas.draw_text(msg, (100, 500), 30, 'Red')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric