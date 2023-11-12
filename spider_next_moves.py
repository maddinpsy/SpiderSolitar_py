from SpiderSolitar import SpiderSolitaire
import random


def remove_moves_between_empty_piles(spider_game, moves):
    is_valid_move = lambda move: not (len(spider_game.tableau[move[1]]) == 0 and len(spider_game.tableau[move[0]]) == move[2])
    return list(filter(is_valid_move, moves))

def remove_moves_to_multiple_empty_piles(spider_game, moves):
    empty_piles = [i for i, pile in enumerate(spider_game.tableau) if len(pile)==0]

    if len(empty_piles) <= 1:
        return moves  # No need to filter if there are 1 or 0 empty piles.

    filtered_moves = [move for move in moves if move[1] not in empty_piles[1:]]

    return filtered_moves

def remove_moves_to_same(spider_game, moves):
    def not_reversible(move):
        source_pile, dest_pile, number_of_cards = move
        return not (
            len(spider_game.tableau[source_pile]) > number_of_cards
            and len(spider_game.tableau[dest_pile]) > 0
            and spider_game.tableau[source_pile][-number_of_cards - 1][0] == spider_game.tableau[dest_pile][-1][0]
        )
    filtered_moves = list(filter(not_reversible, moves))
    return filtered_moves
                                                        
def get_valid_moves(spider_game):
    valid_moves = []
    for source_pile in range(spider_game.NUM_PILES):
        for dest_pile in range(spider_game.NUM_PILES):
            if source_pile == dest_pile:
                continue
            for number_of_cards in range(1,len(spider_game.tableau[source_pile])+1):
                cards_to_move = spider_game.tableau[source_pile][-number_of_cards:]
                if spider_game.is_valid_move(cards_to_move, spider_game.tableau[dest_pile]):
                    valid_moves.append((source_pile, dest_pile, number_of_cards))
    valid_moves=remove_moves_between_empty_piles(spider_game, valid_moves)
    valid_moves=remove_moves_to_multiple_empty_piles(spider_game, valid_moves)
    valid_moves=remove_moves_to_same(spider_game, valid_moves)
    # add the deal move
    if len(spider_game.deck) >= spider_game.NUM_PILES and all(len(pile)>0 for pile in spider_game.tableau):
        valid_moves.append("deal")
    return valid_moves

def apply_random_move(spider_game):
    valid_moves = get_valid_moves(spider_game)
    if valid_moves:
        random_move = random.choice(valid_moves)
        if random_move == 'deal':
            spider_game.deal()
        else:
            source_pile, dest_pile, card_count = random_move
            spider_game.move_card(source_pile, dest_pile, card_count)
        return random_move
    return None