from spider_next_moves import SpiderSolitaireNextMoves
from spider_reverse import SpiderSolitaireReverse
from SpiderSolitar import SpiderSolitaire
from spider_display import SpiderSolitaireDisplay


if __name__ == "__main__":
    s = SpiderSolitaire()

    while True:
        # Print the current state of the tableau
        print("Deck: " + " ".join([SpiderSolitaireDisplay.card_to_string(card) for card in s.deck]))
        tableau_string = SpiderSolitaireDisplay.tableau_to_string(s)
        print(tableau_string)

        # Take user input
        user_input = input("Enter 'm' for random move, 'd' for deal, 'r' for random reverse, 'c' to clear, 'n' to start new or 'q' to quit: ")

        if user_input == 'q':
            break  # Exit the loop if the user inputs 'q'

        if user_input == 'c':
            s.tableau = [[] for _ in range(s.NUM_PILES)]
            s.deck = []
            s.finished_stacks = [[(rank,suite) for rank in range(13,0,-1)] for suite in range(4) for _ in range(s.num_decks)]
            print("clearing")

        if user_input == 'n':
            s = SpiderSolitaire()
            print("new game")
            
        if user_input == 'm':
            move = SpiderSolitaireNextMoves.apply_random_move(s)
            print(f"moving {move}")
            
        if user_input == 'd':
            s.deal()
            print("dealing")

        if user_input == 'r':
            move = SpiderSolitaireReverse.do_random_reverse_move(s)
            print(f"random reverse move: {move}")
            