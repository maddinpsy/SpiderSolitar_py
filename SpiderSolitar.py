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

    @staticmethod
    def tableau_from_string(tableau_string):
        tableau_rows = SpiderSolitaire.remove_indent(tableau_string).split('\n')
        max_pile_length = max(len(row) for row in tableau_rows)
        tableau = [[] for _ in range(SpiderSolitaire.NUM_PILES)]
        for row in tableau_rows:
            for i in range(0,max_pile_length,3):
                if i < len(row) and row[i] != ' ':
                    rank_str, suit_str = row[i], row[i+1]
                    rank = "A23456789TJQK".index(rank_str) + 1
                    suit = "cdhs".index(suit_str)
                    card = (rank, suit)
                    tableau[i//3].append(card)
        return tableau
    
    @staticmethod
    def remove_indent(input_str):
        lines = input_str.split('\n')
        indent = -1

        # Find the indentation from the first non-empty line
        for line in lines:
            if len(line.strip()) > 0:
                indent = len(line) - len(line.lstrip())
                break

        if indent == -1:
            return input_str  # No non-empty lines found

        # Remove the found indentation from each line
        result_lines = [line[indent:] if len(line.strip()) > 0 else line for line in lines]
        return '\n'.join(result_lines)            
    
    
    def display_tableau(self):
        for pile in self.tableau:
            print(pile)
    
    def tableau_to_string(self):
        tableau_string = ""
        max_pile_length = max(len(pile) for pile in self.tableau)
        
        for row in range(max_pile_length):
            for pile in self.tableau:
                if row < len(pile):
                    rank, suit = pile[row]
                    rank_symbol = "A23456789TJQK"[rank - 1]
                    suit_symbol = "cdhs"[suit]
                    card_str = f"{rank_symbol}{suit_symbol}"
                else:
                    card_str = "  "
                tableau_string += card_str + " "
            tableau_string += "\n"
        
        return tableau_string
    
    def move_card(self, source_pile, dest_pile, number_of_cards):
        if source_pile < 0 or source_pile >= self.NUM_PILES or dest_pile < 0 or dest_pile >= self.NUM_PILES:
            return "Invalid pile number"
        
        if number_of_cards < 1 or number_of_cards > len(self.tableau[source_pile]):
            return "Invalid number of cards to move"

        cards_to_move = self.tableau[source_pile][-number_of_cards:]
        if not self.is_valid_move(cards_to_move, self.tableau[dest_pile]):
            return "Invalid move"

        self.tableau[dest_pile].extend(cards_to_move)
        self.tableau[source_pile] = self.tableau[source_pile][:-number_of_cards]
        self.remove_full_sequence()

    def is_valid_move(self, cards_to_move, dest_pile):
        for i in range(1, len(cards_to_move)):
            if cards_to_move[i][0] != cards_to_move[i - 1][0] - 1 or cards_to_move[i][1] != cards_to_move[i - 1][1]:
                return False

        return len(dest_pile) == 0 or cards_to_move[0][0] == dest_pile[-1][0] - 1

    def remove_full_sequence(self):
        for pile in self.tableau:
            if (
                len(pile) >= 13 
                and all(card[1] == pile[-1][1] for card in pile[-13:]) 
                and [card[0] for card in pile[-13:]] == list(range(13,0,-1))
            ):
                pile[-13:] = []
                
    def deal(self):
        if len(self.deck) < self.NUM_PILES:
            raise ValueError("Not enough cards in the deck to deal to all the piles.")

        for i in range(self.NUM_PILES):
            self.tableau[i].append(self.deck.pop())
            
    def display_tableau_ascii(self):
        suits_symbols = ["♠", "♥", "♦", "♣"]
        ranks_symbols = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        max_pile_length = max(len(pile) for pile in self.tableau)

        for row in range(max_pile_length):
            for pile in self.tableau:
                if row < len(pile):
                    rank, suit = pile[row]
                    print(f"{ranks_symbols[rank - 1]}{suits_symbols[suit]}\t", end="")
                else:
                    print("   \t", end="")  # Empty space
            print()  # Newline for the next row
            
    def display_tableau_html(self):
        from IPython.display import HTML
        suits_symbols = ["♠", "♥", "♦", "♣"]
        ranks_symbols = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        max_pile_length = max(len(pile) for pile in self.tableau)
        
        html = "<table style='border-collapse: collapse;'>"
        for row in range(max_pile_length):
            html += "<tr>"
            for pile in self.tableau:
                if row < len(pile):
                    rank, suit = pile[row]
                    card_symbol = f"{ranks_symbols[rank - 1]}<span style='color:{'red' if suit in [1, 2] else 'black'};'>{suits_symbols[suit]}</span>"
                    html += f"<td style='border: 1px solid black; padding: 5px; text-align: center;'>{card_symbol}</td>"
                else:
                    html += "<td style='border: 1px solid black;'></td>"  # Empty space
            html += "</tr>"
        html += "</table>"
        return HTML(html)

    def remove_moves_between_empty_piles(self, moves):
        is_valid_move = lambda move: not (len(self.tableau[move[1]]) == 0 and len(self.tableau[move[0]]) == move[2])
        return list(filter(is_valid_move, moves))

    def remove_moves_to_multiple_empty_piles(self, moves):
        empty_piles = [i for i, pile in enumerate(self.tableau) if len(pile)==0]

        if len(empty_piles) <= 1:
            return moves  # No need to filter if there are 1 or 0 empty piles.

        first_empty_pile = empty_piles[0]
        filtered_moves = [move for move in moves if move[1] not in empty_piles[1:]]

        return filtered_moves
    
    def remove_moves_to_same(self, moves):
        def not_reversible(move):
            source_pile, dest_pile, number_of_cards = move
            return not (
                len(self.tableau[source_pile]) > number_of_cards
                and len(self.tableau[dest_pile]) > 0
                and self.tableau[source_pile][-number_of_cards - 1][0] == self.tableau[dest_pile][-1][0]
            )
        filtered_moves = list(filter(not_reversible, moves))
        return filtered_moves
                                                            
    def get_valid_moves(self):
        valid_moves = []
        for source_pile in range(self.NUM_PILES):
            for dest_pile in range(self.NUM_PILES):
                if source_pile == dest_pile:
                    continue
                for number_of_cards in range(1,len(self.tableau[source_pile])+1):
                    cards_to_move = self.tableau[source_pile][-number_of_cards:]
                    if self.is_valid_move(cards_to_move, self.tableau[dest_pile]):
                        valid_moves.append((source_pile, dest_pile, number_of_cards))
        valid_moves=self.remove_moves_between_empty_piles(valid_moves)
        valid_moves=self.remove_moves_to_multiple_empty_piles(valid_moves)
        valid_moves=self.remove_moves_to_same(valid_moves)
        # add the deal move
        if len(self.deck) >= self.NUM_PILES and all(len(pile)>0 for pile in self.tableau):
            valid_moves.append("deal")
        return valid_moves
   
    def apply_random_move(self):
        valid_moves = self.get_valid_moves()
        if valid_moves:
            random_move = random.choice(valid_moves)
            if random_move == 'deal':
                self.deal()
            else:
                source_pile, dest_pile, card_index = random_move
                self.move_card(source_pile, dest_pile, card_index)
