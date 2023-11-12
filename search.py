from astar import AStar
from spider_display import tableau_to_string   
from spider_next_moves import SpiderSolitaireNextMoves
from spider_reverse import do_random_reverse_move, undo_remove_full_sequence
from SpiderSolitar import SpiderSolitaire
from spider_parser import tableau_from_string


class SpiderStart(AStar):
    def neighbors(self, node:SpiderSolitaire):
        moves = get_valid_moves(node)
        neighbors = []
        for move in moves:
            neighbor = node.copy()
            if move == 'deal':
                neighbor.deal()
            else:
                source_pile, dest_pile, card_count = move
                neighbor.move_card(source_pile, dest_pile, card_count)
            neighbor.last_move = move
            neighbors.append(neighbor)
        return neighbors
    
    def distance_between(self, n1, n2):
        return 1
            
    def heuristic_cost_estimate(self, current:SpiderSolitaire, goal:SpiderSolitaire):
        rem_stacks = abs(len(current.finished_stacks) - len(goal.finished_stacks))
        #sum_connected = sum([SpiderSolitaire.num_connected_cards(pile) for pile in current.tableau])
        # free_piles = sum([1 for pile in current.tableau if len(pile) == 0])
        return rem_stacks #+ 1/(free_piles+1)
    
    def is_goal_reached(self, current, goal):
        return current == goal

def generate_test_data():
    from load_store import store
    import time
    goal = SpiderSolitaire.goal()
    run = 0
    while True:
        print(f"Run {run}")
        try:
            run+=1
            last = goal.copy()
            for _ in range(5):
                do_random_reverse_move(last)
            s = SpiderStart()
            path = s.astar(last,goal)
            time_string = time.strftime("%Y%m%d-%H%M%S")
            store(last,list(map(lambda state: state.last_move, path)),f"data/3_{time_string}.json")
        except Exception as err:
            print(err)

def load_and_replay(filename="data/2_20231104-162938.json"):
    from load_store import load
    goal = SpiderSolitaire.goal()
    game, sol = load(filename)
    print(tableau_to_string(game))
    s = SpiderStart()
    path = s.astar(game,goal)
    print(list(map(lambda state: state.last_move, path)))
    print(sol)



def random_play():
    goal = SpiderSolitaire.goal()
    last = goal.copy()
    undo_remove_full_sequence(last)
    undo_remove_full_sequence(last)
    undo_remove_full_sequence(last)
    undo_remove_full_sequence(last)
    for _ in range(5):
        do_random_reverse_move(last)
    print(tableau_to_string(last))

    s = SpiderStart()
    path = s.astar(last,goal)
    print(list(map(lambda state: state.last_move, path)))

def one_play():
    goal = SpiderSolitaire.goal()
    last = goal.copy()
    #     last.tableau = tableau_from_string(
    #     """
    # Ts    6s    5s Ks 6s 9s Ks 4s 
    # 9s    5s       Qs    8s Qs 3s
    # 8s    4s       Js    7s Js 2s
    # 7s    3s                As
    #       2s                Ts
    #       As
    #     """)
    # last.finished_stacks.pop()
    # last.finished_stacks.pop()
    s = SpiderStart()
    path = s.astar(last,goal)
    print(list(map(lambda state: state.last_move, path)))


if __name__ == "__main__":
    generate_test_data()
