import random
from IPython.display import clear_output
all_players_data={}
ranks=['Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
suits=['Hearts','Diamonds','Spades','Clubs']
values={'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}
class card:
    def __init__(self,rank,suit):
        self.rank=rank
        self.suit=suit
        self.value=values[rank]
    def __str__(self):
        return f'{self.rank} of {self.suit}'

class deck:
    def __init__(self):
        self.all_cards=[]
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(card(rank,suit))
    def __len__(self):
        return len(self.all_cards)
    def __str__(self):
        for c in self.all_cards:
            print(c)
    def shuffle(self):
        random.shuffle(self.all_cards)
    def get_one(self):
        return self.all_cards.pop(0)
    
class player:
    def __init__(self,name,balance):
        self.name=name
        self.balance=balance
        all_players_data[name]=self
    def __str__(self):
        return f'Name: {self.name}\nCurrent Balance: {self.balance}'
    def take_bet_amount(self):
        while True:
            try:
                value=int(input('Please place your bet - >'))
            except:
                continue
            else:
                if value>self.balance:
                    print('Not enough funds !')
                    continue
                else:
                    return value
    def playerwon(self,bet):
        print('Congratulations you have won the game')
        self.balance+=bet
        print(f'New Balance : {self.balance}')
    def playerlost(self,bet):
        print('Sorry you have lost the game')
        self.balance-=bet
        print(f'New Balance : {self.balance}')

def get_value(crd):
    if crd.rank=='Ace':
        val=0
        while val not in [1,11]:
            val=int(input('You have got an ace....choose a value (1 or 11)'))
        return val
    else:
        return values[crd.rank]

class player_hand:
    def __init__(self,card1,card2):
        self.all_cards=[card1,card2]
        self.all_values=[get_value(card1),get_value(card2)]
        self.sum=sum(self.all_values)
    def add_to_hand(self,CARD):
        self.all_cards.append(CARD)
        self.all_values.append(get_value(CARD))
        self.sum+=self.all_values[-1]
    def prnt(self):
        print('PLAYER\'S HAND')
        for i in range(len(self.all_cards)):
            print(f'{str(self.all_cards[i])}  :  {self.all_values[i]}')
        print('--------------------------------')
        print(f'Current sum of player\'s hand : {self.sum}')
        
class dealer_hand:
    def __init__(self,crd1,crd2):
        self.all_cards=[crd1,crd2]
        self.all_values=[values[crd1.rank]]
        self.sum=values[crd1.rank]
    def reveal_facedown(self):
        facedowncard=self.all_cards[1]
        valueoffdc=values[facedowncard.rank]
        if valueoffdc+self.sum>21:
            valueoffdc=1
            self.all_values.append(1)
        else:
            self.all_values.append(valueoffdc)
        self.sum+=valueoffdc
    def add_to_hand(self,CARD):
        self.all_cards.append(CARD)
        if CARD.rank=='Ace' and 11+self.sum>21:
            self.all_values.append(1)
        else:
            self.all_values.append(values[CARD.rank])
        self.sum+=self.all_values[-1]
    def prnt(self):
        print('DEALER\'S HAND')
        for i in range(len(self.all_values)):
            print(f'{str(self.all_cards[i])}  :  {self.all_values[i]}')
        print('--------------------------------')
        print(f'Current sum of dealer\'s hand : {self.sum}')
def play_game(user):
    print('! WELCOME TO BLACKJACK GAME !')
    gamedeck=deck()
    gamedeck.shuffle()
    print('LETS START THE GAME')
    bet=user.take_bet_amount()
    c1=gamedeck.get_one()
    c2=gamedeck.get_one()
    print(f'Players cards => {str(c1)} , {str(c2)}')
    playerhand=player_hand(c1,c2)
    dealerhand=dealer_hand(gamedeck.get_one(),gamedeck.get_one())
    dealerhand.prnt()
    print('\n\n\n\n\n')
    playerhand.prnt()
    action=''
    gameended=0
    while action not in ['hit','stay']:
        action=input('Choose an action (hit or stay)')
    while action=='hit':
        playerhand.add_to_hand(gamedeck.get_one())
        clear_output()
        dealerhand.prnt()
        print('\n\n\n\n\n')
        playerhand.prnt()
        if playerhand.sum>21:
            print('Player bust')
            user.playerlost(bet)
            gameended=1
            break
        else:
            action=''
            while action not in ['hit','stay']:
                action=input('Choose an action (hit or stay)')
            if action=='hit':
                continue
            else:
                dealerhand.reveal_facedown()
                while dealerhand.sum<=playerhand.sum:
                    dealerhand.add_to_hand(gamedeck.get_one())
                clear_output()
                dealerhand.prnt()
                print('\n\n\n\n\n')
                playerhand.prnt()
                if dealerhand.sum>21:
                    print('Dealer bust')
                    user.playerwon(bet)
                else:
                    print('Dealer has a closer value to 21 than the player')
                    user.playerlost(bet)
                gameended=1
                break
    if gameended==0:
        dealerhand.reveal_facedown()
        while dealerhand.sum<=playerhand.sum:
            dealerhand.add_to_hand(gamedeck.get_one())
        clear_output()
        dealerhand.prnt()
        print('\n\n\n\n\n')
        playerhand.prnt()
        if dealerhand.sum>21:
            print('Dealer bust')
            user.playerwon(bet)
        else:
            print('Dealer has a closer value to 21 than the player')
            user.playerlost(bet)
    ans=''
    while ans not in ['Yes','No']:
        ans=input('Do you wish to play again (Yes or No)')
    if ans=='Yes':
        play_game(user)
def mainmenu():
    while True:
        
        Ans=''
        while Ans not in ['play','quit']:
            clear_output()
            print('MAIN MENU')
            Ans=input('Choose an option (play or quit) - >')
        if Ans=='play':
            innermenu()
            continue
        else:
            break
def innermenu():
    username=input('Enter username - >')
    if username not in all_players_data.keys():
        initialbalance=int(input('Enter opening balance of your account - >'))
        user=player(username,initialbalance)
    else:
        user=all_players_data[username]
    print('Logged In !')
    while True:
        
        response=''
        while response not in ['playgame','logout']:
            response=input('Choose an option (playgame or logout)')
        if response=='playgame':
            play_game(user)
            continue
        else:
            break
if __name__=='__main__':
    mainmenu()




