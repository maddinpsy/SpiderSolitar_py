from astar import AStar   
from spider_next_moves import SpiderSolitaireNextMoves
from spider_reverse import SpiderSolitaireReverse
from SpiderSolitar import SpiderSolitaire

class SpiderStart(AStar):
    def neighbors(self, node:SpiderSolitaire):
        moves = SpiderSolitaireNextMoves.get_valid_moves(node)
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
            
    def heuristic_cost_estimate(self, current, goal):
        return 1
    
    def is_goal_reached(self, current, goal):
        return current == goal


if __name__ == "__main__":
    goal = SpiderSolitaire.goal()
    last = goal.copy()
    for _ in range(5):
        SpiderSolitaireReverse.do_random_reverse_move(last)
    s = SpiderStart()
    path = s.astar(last,goal)
    print(list(map(lambda state: state.last_move, path)))