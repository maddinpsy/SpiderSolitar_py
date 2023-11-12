from SpiderSolitar import SpiderSolitaire
import random

def max_cards_placed(pile):
    con_cards = SpiderSolitaire.num_connected_cards(pile)
    if len(pile) == con_cards:
        return con_cards
    elif pile[-con_cards][0] == pile[-con_cards-1][0] - 1:
        return con_cards
    else:
        return con_cards-1
    
        
def do_reverse_basic_move(spider_game, source_idx = None):
    # Randomly select a source pile
    if source_idx is None:
        src_piles_idx = list(range(spider_game.NUM_PILES))
        # Only take source piles, where at least one card might have been placed
        src_piles_idx = [idx for idx in src_piles_idx if max_cards_placed(spider_game.tableau[idx])>0]
        if not src_piles_idx:
            raise ValueError("No move is possible")
        weights = [len(spider_game.tableau[pile_idx]) for pile_idx in src_piles_idx]
        source_idx = random.choices(src_piles_idx,weights)[0]
    pile = spider_game.tableau[source_idx]

    # Count the number of connected cards at the end of the pile
    # Randomly select a number of connected cards to move
    number_of_cards = random.randint(1, max_cards_placed(pile))

    # destination pile must be different from the source pile
    dst_piles_idx = list(range(spider_game.NUM_PILES))
    dst_piles_idx.remove(source_idx)

    # If all cards are moved, the destination pile may not be empty
    if number_of_cards == len(pile):
        dst_piles_idx = [pile for pile in dst_piles_idx if len(spider_game.tableau[pile]) > 0]

    # pick a random destination pile
    # use length of piles as wights. Preferring short piles.
    weights = [1/(len(spider_game.tableau[pile_idx])+0.01) for pile_idx in dst_piles_idx]
    dest_idx = random.choices(dst_piles_idx,weights)[0]

    # Move the selected cards and update the tableau
    cards_to_move = spider_game.tableau[source_idx][-number_of_cards:]
    spider_game.tableau[dest_idx].extend(cards_to_move)
    spider_game.tableau[source_idx] = spider_game.tableau[source_idx][:-number_of_cards]

    # return the move switching src and dst to make it a legal move
    return dest_idx, source_idx, number_of_cards

def do_reverse_deal(spider_game):
    # Define probabilities based on the number of connected piles
    PROBABILITIES = [1, 0.5, 0.1, 0, 0, 0, 0, 0, 0, 0]

    # Count the number of connected piles
    num_piles_with_moves = 0
    for pile in spider_game.tableau:
        if len(pile) < 2:
            return None  # To reverse a deal, all piles must have at least two cards
        if max_cards_placed(pile) > 0:
            num_piles_with_moves += 1

    # Check if the un-deal action should run based on probabilities
    if random.random() <= PROBABILITIES[num_piles_with_moves]:
        # Reverse the order of piles during the un-deal
        for i in reversed(range(len(spider_game.tableau))):
            pile = spider_game.tableau[i]
            spider_game.deck.append(pile.pop())
        return 'deal'
    else:
        return None
    
def undo_remove_full_sequence(spider_game):
    # Define probabilities based on the number of empty piles
    PROBABILITIES = [0, 0, 0, 0, 0.1, 0.1, 0.1, 0.5, 0.7, 1]

    # get number of empty stacks
    empty_stacks = sum([1 for pile in spider_game.tableau if len(pile) == 0])

    pile_index = None  # Initialize to an invalid index
    if random.random() <= PROBABILITIES[empty_stacks - 1] and len(spider_game.finished_stacks) > 0:
        # Randomly select a pile index to add the full sequence
        pile_index = random.randint(0, len(spider_game.tableau) - 1)
        pile = spider_game.tableau[pile_index]
        stack_idx = random.randint(0,len(spider_game.finished_stacks)-1)
        pile.extend(spider_game.finished_stacks[stack_idx])
        del spider_game.finished_stacks[stack_idx]

    return pile_index

def do_random_reverse_move(spider_game):
    
    move = do_reverse_deal(spider_game)
    if move is not None:
        return move
    
    unstack_idx = undo_remove_full_sequence(spider_game)

    move = do_reverse_basic_move(spider_game, unstack_idx)

    return move
