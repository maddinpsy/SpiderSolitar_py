import random


class SpiderSolitaire:
    NUM_PILES = 10
    CARDS_PER_PILE = 6
    
    def __init__(self, num_suits=4, num_ranks=13, num_decks=2):
        self.num_suits = num_suits
        self.num_ranks = num_ranks
        self.num_decks = num_decks
        self.deck = self.initialize_deck()
        self.tableau = self.initialize_tableau()
        self.finished_stacks = []

    def initialize_deck(self):
        deck = []
        for _ in range(self.num_decks):
            for suit in range(self.num_suits):
                for rank in range(1, self.num_ranks + 1):
                    card = (rank, suit)
                    deck.append(card)
        random.shuffle(deck)
        return deck
    
    def initialize_tableau(self):
        tableau = [[] for _ in range(self.NUM_PILES)]
        for i in range(self.NUM_PILES):
            tableau[i] = self.deck[i * self.CARDS_PER_PILE: (i + 1) * self.CARDS_PER_PILE]
        self.deck = self.deck[self.NUM_PILES * self.CARDS_PER_PILE:]
        return tableau

    def initialize_tableau_from_string(self, tableau_string):
        self.tableau = SpiderSolitaire.tableau_from_string(tableau_string)
    
    def move_card(self, source_pile, dest_pile, number_of_cards):
        if source_pile < 0 or source_pile >= self.NUM_PILES or dest_pile < 0 or dest_pile >= self.NUM_PILES:
            raise ValueError("Invalid pile number")
        
        if number_of_cards < 1 or number_of_cards > len(self.tableau[source_pile]):
            raise ValueError("Invalid number of cards to move")

        cards_to_move = self.tableau[source_pile][-number_of_cards:]
        if not self.is_valid_move(cards_to_move, self.tableau[dest_pile]):
            raise ValueError("Invalid move")

        self.tableau[dest_pile].extend(cards_to_move)
        self.tableau[source_pile] = self.tableau[source_pile][:-number_of_cards]
        self.remove_full_sequence()

    def is_valid_move(self, cards_to_move, dest_pile):
        for i in range(1, len(cards_to_move)):
            if cards_to_move[i][0] != cards_to_move[i - 1][0] - 1 or cards_to_move[i][1] != cards_to_move[i - 1][1]:
                return False

        return len(dest_pile) == 0 or cards_to_move[0][0] == dest_pile[-1][0] - 1

    @staticmethod
    def num_connected_cards(pile):
        if len(pile) == 0:
            return 0
        elif len(pile) == 1:
            return 1
        else:
            # rank is okay
            rank_fits = pile[-1][0] == pile[-2][0] - 1
            suite_fits = pile[-1][1] == pile[-2][1]
            if rank_fits and suite_fits:
                return 1 + SpiderSolitaire.num_connected_cards(pile[:-1])
            else:
                return 1
            
    def remove_full_sequence(self):
        for pile in self.tableau:
            if SpiderSolitaire.num_connected_cards(pile) == 13:
                self.finished_stacks.append(pile[-13:])
                pile[-13:] = []
                
    def deal(self):
        if len(self.deck) < self.NUM_PILES:
            raise ValueError("Not enough cards in the deck to deal to all the piles.")

        for i in range(self.NUM_PILES):
            self.tableau[i].append(self.deck.pop())
         
