'''Back end Poker functions for deck and hand creation, drawing or shuffling cards from a deck, and hand scoring.'''
import random
import os


def build_deck() -> list[str]:
    '''Create a deck of cards in suit+number format with the number being an integer and the suit is a letter:
    Heart (H)
    Spades (S)
    Club (C)
    Diamond (D)'''
    numbers=list(range(2,15))
    suits = ['H','S','C','D']
    deck = []
    for number in numbers:
        for suit in suits:
            card = suit+str(number)
            deck.append(card)
    return deck


def shuffle_deck(cards_being_shuffled: list) -> list[str]:
    '''Given a list, returns the list in a random order.'''
    random.shuffle(cards_being_shuffled)
    return cards_being_shuffled


def draw_cards(deck: list, draw_number: int) -> tuple[list[str], list[str]]:
    '''Draws cards from the deck provided. Returns hand and remaining deck '''
    cards_drawn = []
    i = 0
    while i < draw_number:
        cards_drawn.append(deck.pop(0))
        i += 1
    return cards_drawn, deck


def create_hand(deck: list) -> tuple[list[str], list[str]]:
    '''
    Provided a deck, shuffles, and creates a hand.
    Returns a tuple, (Hand,Remaining Deck)
    '''
    deck = build_deck()
    deck = shuffle_deck(deck)
    return draw_cards(deck,5)


def score_four_of_a_kind(numbers: list) -> int:
    '''Evaluates a int list to determine the score of quads - does not check the hand'''
    for i in numbers:
        if numbers.count(i) == 4:
            four_of_a_kind = i
        elif numbers.count(i) == 1:
            card = i
    return 105 + four_of_a_kind + card/100


def score_full_house(numbers: list) -> int:
    '''Evaluates a int list to determine the score of a full house - does not check the hand'''
    for i in numbers:
        if numbers.count(i) == 3:
            trips = i
        elif numbers.count(i) == 2:
            pair = i
    return 90 + trips + pair/100


def score_three_of_a_kind(numbers: list) -> int:
    '''Evaluates a int list to determine the score of a three of a kind - does not check the hand'''
    trips = 0
    cards = []
    for i in numbers:
        if numbers.count(i) == 3:
            trips = i
        else:
            cards.append(i)
    return 45 + trips


def score_two_pair(numbers: list) -> int:
    '''Evaluates a int list to determine the score of a two pair hand - does not check the hand'''
    pairs = []
    cards = []
    for i in numbers:
        if numbers.count(i) == 2:
            pairs.append(i)
        elif numbers.count(i) == 1:
            cards.append(i)
            cards = sorted(cards,reverse=True)
    return 30 + max(pairs) + min(pairs)/100 + cards[0]/1000


def score_pair(numbers: list) -> int:
    '''Evaluates a int list to determine the score of a pair - does not check the hand'''
    pair = []
    cards  = []
    for i in numbers:
        if numbers.count(i) == 2:
            pair.append(i)
        elif numbers.count(i) == 1:
            cards.append(i)
            cards = sorted(cards,reverse=True)
    return 15 + pair[0] + cards[0]/100 + cards[1]/1000 + cards[2]/10000


def score_hand(hand: list) -> int:
    ''' Given a hand in ['5H','3H','5C','5D','C14'] format return the poker score.

    Scoring Table:
    	                MIN	MAX
        Royal Flush	    135	135
        Straight Flush	120	134
        Four of a Kind	105	119
        Full House	    90	104
        Flush	        75	89
        Straight	    60	74
        Three of a Kind	45	59
        Two Pair        30	44
        Pair	        15	29
        High Card	     0	14
    
    Scoring for each hand has ranges to allow for payouts of different types four of a kinds.
    '''
    letters = [hand[i][:1] for i in range(5)] # We get the suit for each card in the hand
    repeat_suit = [letters.count(i) for i in letters]  # We count repetitions for each suit ex [5,5,5,5,5] for flush

    numbers = [int(hand[i][1:]) for i in range(5)]  # We get the number for each card in the hand
    repeat_number = [numbers.count(i) for i in numbers] # We create a list with the repetitions of each number ex) [2,2,3,3,3] for fullhouse

    dif = max(numbers) - min(numbers) # The difference between the greater and smallest number
    handtype = 'Hand Ranking'
    score = 0

    #If all cards in hand share a suit, evaluate the type of flush.
    if 5 in repeat_suit:
        if numbers ==[14,13,12,11,10]:
            handtype = 'ROYAL FLUSH'
            score = 135
            print(f'this hand is a {handtype}: with score: {score}')
        elif dif == 4 and max(repeat_number) == 1:
            handtype = 'STRAIGHT FLUSH'
            score = 120 + max(numbers)
            print(f'this hand is a {handtype}: with score: {score}')
        else:
            handtype = 'FLUSH'
            score = 75 + max(numbers)
            print(f'this hand is a {handtype}: with score: {score}')

    #Evaluate other hands in decending ranking
    elif 4 in repeat_number:
        handtype = 'FOUR OF A KIND'
        score = score_four_of_a_kind(numbers)
        print(f'this hand is a {handtype}: with score: {score}')
    elif sorted(repeat_number) == [2,2,3,3,3]:
        handtype = 'FULL HOUSE'
        score = score_full_house(numbers)
        print(f'this hand is a {handtype}: with score: {score}')
    elif dif == 4 and max(repeat_number) == 1:
        handtype = 'STRAIGHT'
        score = 60 + max(numbers)
        print(f'this hand is a {handtype}: with score: {score}')
    elif 3 in repeat_number:
        handtype = 'TRIPS'
        score = score_three_of_a_kind(numbers)
        print(f'this hand is a {handtype}: with score: {score}')
    elif repeat_number.count(2) == 4:
        handtype = 'TWO PAIR'
        score = score_two_pair(numbers)
        print(f'this hand is a {handtype}: with score: {score}')
    elif repeat_number.count(2) == 2:
        handtype = 'PAIR'
        score = score_pair(numbers)
        print(f'this hand is a {handtype}: with score: {score}')
    else:
        handtype= 'HIGH CARD'
        num = sorted(numbers,reverse=True)
        score = num[0] + num[1]/100 + num[2]/1000 + num[3]/10000 + num[4]/100000
        print(f'this hand is a {handtype}: with score: {score}')
    return score, handtype


def calculate_payout(input_score: int, input_credits: int) -> int:
    '''Takes a score and number of paid credits, returns payout
    
    input_score = Accepts a number between 5 and 135.
    input_credits = Accepts a number between 0 and 4.
    '''
    score_dict = {
        'royal_flush': {'payout': [250,500,750,1000,4000]},
        'straight_flush': {'payout': [50,100,150,200,250]},
        'quad_aces_234_kicker': {'payout': [400,800,1200,1600,2000]},
        'quad_aces_jackqueenking_kicker': {'payout': [320,640,960,1280,1600]},
        'quad_234_ace_kicker': {'payout': [160,320,480,640,800]},
        'quad_jackqueenking_face_kicker': {'payout': [160,320,480,640,800]},
        'quad_aces': {'payout': [160,320,480,640,800]},
        'quad_234': {'payout': [80,160,240,320,400]},
        'quad_5toking': {'payout': [50,100,150,200,250]},
        'full_house': {'payout': [7,14,21,28,35]},
        'flush': {'payout': [5,10,15,25,25]},
        'straight': {'payout': [4,8,12,16,20]},
        'trips': {'payout': [3,6,9,12,15]},
        'two_pair': {'payout': [1,2,3,4,5]},
        'pair_jacks_better': {'payout': [1,2,3,4,5]}
    }

    if input_score == 135:
        return score_dict['royal_flush']['payout'][input_credits]

    elif input_score > 120:
        return score_dict['straight_flush']['payout'][input_credits]

    elif input_score > 119.10:
        return score_dict['quad_aces_jackqueenking_kicker']['payout'][input_credits]

    elif input_score > 119.4:
        return score_dict['quad_aces']['payout'][input_credits]

    elif input_score > 119.0:
        return score_dict['quad_jackqueenking_face_kicker']['payout'][input_credits]

    elif input_score > 110.0:
        return score_dict['quad_5toking']['payout'][input_credits]
    
    elif input_score == 106.14 or input_score == 107.14 or input_score == 108.14:
        return score_dict['quad_234_ace_kicker']['payout'][input_credits]

    elif input_score > 107.0:
        return score_dict['quad_234']['payout'][input_credits]

    elif input_score > 90:
        return score_dict['full_house']['payout'][input_credits]

    elif input_score > 89.00:
        return score_dict['flush']['payout'][input_credits]

    elif input_score > 70.00:
        return score_dict['straight']['payout'][input_credits]

    elif input_score > 51:
        return score_dict['trips']['payout'][input_credits]

    elif input_score > 30:
        return score_dict['two_pair']['payout'][input_credits]

    elif input_score > 26:
        return score_dict['pair_jacks_better']['payout'][input_credits]

    else:
        #Hand does not meet minimum payout
        return 0


def load_player_balance(bank_file_location = os.path.dirname(os.path.realpath(__file__))) -> int:
    '''Load the player balance from bank.txt'''
    bank_store_path = os.path.join(bank_file_location, 'fcd_bank.txt' )
    bank_store = open(bank_store_path, 'r', encoding = 'utf-8')
    return int(bank_store.read())
