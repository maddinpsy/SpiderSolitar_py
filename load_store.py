import json
from SpiderSolitar import SpiderSolitaire
from spider_display import SpiderSolitaireDisplay
from spider_parser import SpiderSolitaireParser

def store(spider_game, solution, filename):
    tableau_str = SpiderSolitaireDisplay.tableau_to_string(spider_game)
    deck_str = " ".join([SpiderSolitaireDisplay.card_to_string(card) for card in spider_game.deck])
    # take the suite of the first card of each stack
    finished_stacks_str = "".join(SpiderSolitaireDisplay.card_to_string(stack[0])[1] for stack in spider_game.finished_stacks)
    with open(filename, 'w') as file:
        file.write(f"num_suits: {spider_game.num_suits}\n")
        file.write(f"num_ranks: {spider_game.num_ranks}\n")
        file.write(f"num_decks: {spider_game.num_decks}\n")
        file.write(f"deck: {deck_str}\n")
        file.write(f"tableau: \n{tableau_str}\n")
        file.write(f"finished_stacks: {finished_stacks_str}\n")
        file.write(f"solution: {solution[1:]}\n")

def load(filename):
    num_suits=4
    num_ranks=13
    num_decks=2
    deck=None
    tableau=None
    finished_stacks=None
    solution = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("num_suits"):
                num_suits = int(line.split(": ")[1])
            if line.startswith("num_ranks"):
                num_ranks = int(line.split(": ")[1])
            if line.startswith("num_decks"):
                num_decks = int(line.split(": ")[1])
            if line.startswith("deck"):
                deck_str = line.split(": ")[1].strip()
                deck = [SpiderSolitaireParser.card_from_string(str) for str in deck_str.split()]
            if line.startswith("tableau"):
                tableau_str = ""
                tableau_line = file.readline()
                while tableau_line.strip() != "":
                    tableau_str += tableau_line
                    tableau_line = file.readline()
                tableau = SpiderSolitaireParser.tableau_from_string(tableau_str)
            if line.startswith("finished_stacks"):
                fin_stacks_str = line.split(": ")[1].strip()
                finished_stacks = []
                for suit_str in fin_stacks_str:
                    suite = "cdhs".index(suit_str)
                    finished_stacks.append([(rank,suite) for rank in range(num_ranks,0,-1)])
            if line.startswith("solution"):
                solution_str = line.split(": ")[1].strip()
                raw_numbers = solution_str.replace("(","").replace(")","").replace("[","").replace("]","").split(", ")
                solution = [tuple(map(int, raw_numbers[i:i+3])) for i in range(0, len(raw_numbers), 3)]

    spider_game=SpiderSolitaire(num_suits,num_ranks,num_decks,deck,tableau,finished_stacks)
    return spider_game, solution
