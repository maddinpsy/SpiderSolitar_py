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
    
    @staticmethod
    def card_to_string(card):
        rank, suit = card
        rank_symbol = "A23456789TJQK"[rank - 1]
        suit_symbol = "cdhs"[suit]
        return f"{rank_symbol}{suit_symbol}"

    def tableau_to_string(self):
        tableau_string = ""
        max_pile_length = max(len(pile) for pile in self.tableau)
        
        for row in range(max_pile_length):
            for pile in self.tableau:
                if row < len(pile):
                    card_str = SpiderSolitaire.card_to_string(pile[row])
                else:
                    card_str = "  "
                tableau_string += card_str + " "
            tableau_string += "\n"
        
        return tableau_string
    
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

    def remove_full_sequence(self):
        for pile in self.tableau:
            if len(pile) >= 13 and SpiderSolitaire.allowed_cards_to_move(pile) >= 12:
                self.finished_stacks.append(pile[-13:])
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
                source_pile, dest_pile, card_count = random_move
                self.move_card(source_pile, dest_pile, card_count)
            return random_move
        return None

    @staticmethod
    def allowed_cards_to_move(pile):
        if len(pile) == 0:
            return 0
        elif len(pile) == 1:
            return 1
        else:
            connected_count = 0
            for i in range(len(pile) - 2, -1, -1):
                if pile[i][0] == pile[i + 1][0] + 1 and pile[i][1] == pile[i + 1][1]:
                    connected_count += 1
                else:
                    break
            return connected_count

    def do_reverse_basic_move(self, source_idx = None):
        # Randomly select a source pile
        if source_idx is None:
            src_piles_idx = list(range(self.NUM_PILES))
            # Only take source piles, that have at leas one connection
            src_piles_idx = [idx for idx in src_piles_idx if SpiderSolitaire.allowed_cards_to_move(self.tableau[idx])>0]
            if not src_piles_idx:
                raise ValueError("No move is possible")
            source_idx = random.choice(src_piles_idx)
        pile = self.tableau[source_idx]

        # Count the number of connected cards at the end of the pile
        # Randomly select a number of connected cards to move
        number_of_cards = random.randint(1, SpiderSolitaire.allowed_cards_to_move(pile))

        # destination pile must be different from the source pile
        dst_piles = list(range(self.NUM_PILES))
        dst_piles.remove(source_idx)

        # If all cards are moved, the destination pile may not be empty
        if number_of_cards == len(pile):
            dst_piles = [pile for pile in dst_piles if len(self.tableau[pile]) > 0]

        # pick a random destination pile
        dest_pile = random.choice(dst_piles)

        # Move the selected cards and update the tableau
        cards_to_move = self.tableau[source_idx][-number_of_cards:]
        self.tableau[dest_pile].extend(cards_to_move)
        self.tableau[source_idx] = self.tableau[source_idx][:-number_of_cards]

        # return the move switching src and dst to make it a legal move
        return dest_pile, source_idx, number_of_cards
   
    def do_reverse_deal(self):
        # Define probabilities based on the number of connected piles
        PROBABILITIES = [1, 0.5, 0.1, 0, 0, 0, 0, 0, 0, 0]

        # Count the number of connected piles
        number_of_connected_piles = 0
        for pile in self.tableau:
            if len(pile) < 2:
                return None  # To reverse a deal, all piles must have at least two cards
            if SpiderSolitaire.allowed_cards_to_move(pile)>0:
                number_of_connected_piles += 1
        
        # Check if the un-deal action should run based on probabilities
        if random.random() <= PROBABILITIES[number_of_connected_piles]:
            # Reverse the order of piles during the un-deal
            for i in reversed(range(len(self.tableau))):
                pile = self.tableau[i]
                self.deck.append(pile.pop())
            return 'deal'
        else:
            return None
        
    def undo_remove_full_sequence(self):
        pile_index = None  # Initialize to an invalid index
        if len(self.finished_stacks) > 0:
            # Randomly select a pile index to add the full sequence
            pile_index = random.randint(0, len(self.tableau) - 1)
            pile = self.tableau[pile_index]
            pile.extend(self.finished_stacks[-1])
            del self.finished_stacks[-1]

        return pile_index

    def do_random_reverse_move(self):
        PROBABILITY_TO_UNSTACK = 0.3
        
        move = self.do_reverse_deal()
        if move is not None:
            return move
        
        unstack_idx = None
        if random.random() > PROBABILITY_TO_UNSTACK:
            unstack_idx = self.undo_remove_full_sequence()

        move = self.do_reverse_basic_move(unstack_idx)

        return move
    
if __name__ == "__main__":
    s = SpiderSolitaire()

    while True:
        # Print the current state of the tableau
        print("Deck: " + " ".join([SpiderSolitaire.card_to_string(card) for card in s.deck]))
        tableau_string = s.tableau_to_string()
        print(tableau_string)

        # Take user input
        user_input = input("Enter 'm' for random move, 'd' for deal, 'r' for random reverse, or 'q' to quit: ")

        if user_input == 'q':
            break  # Exit the loop if the user inputs 'q'

        if user_input == 'm':
            move = s.apply_random_move()
            print(f"moving {move}")
            
        if user_input == 'd':
            s.deal()
            print("dealing")

        if user_input == 'r':
            move = s.do_random_reverse_move()
            print(f"random reverse move: {move}")
            