from SpiderSolitar import SpiderSolitaire


def display_tableau(s):
    for pile in s.tableau:
        print(pile)


def card_to_string(card):
    rank, suit = card
    rank_symbol = "A23456789TJQK"[rank - 1]
    suit_symbol = "cdhs"[suit]
    return f"{rank_symbol}{suit_symbol}"


def tableau_to_string(s):
    tableau_string = ""
    max_pile_length = max(len(pile) for pile in s.tableau)
    
    for row in range(max_pile_length):
        for pile in s.tableau:
            if row < len(pile):
                card_str = card_to_string(pile[row])
            else:
                card_str = "  "
            tableau_string += card_str + " "
        tableau_string += "\n"
    
    return tableau_string


def deck_to_string(s):
    deck_string = ""
    for card_idx, card in enumerate(reversed(s.deck)):
        deck_string += card_to_string(card)
        if((card_idx + 1)% SpiderSolitaire.NUM_PILES == 0):
            deck_string += "\n"
        else:
            deck_string += " "
    return deck_string


def display_tableau_ascii(s):
    suits_symbols = ["♠", "♥", "♦", "♣"]
    ranks_symbols = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    max_pile_length = max(len(pile) for pile in s.tableau)

    for row in range(max_pile_length):
        for pile in s.tableau:
            if row < len(pile):
                rank, suit = pile[row]
                print(f"{ranks_symbols[rank - 1]}{suits_symbols[suit]}\t", end="")
            else:
                print("   \t", end="")  # Empty space
        print()  # Newline for the next row
        

def display_tableau_html(s):
    from IPython.display import HTML
    suits_symbols = ["♠", "♥", "♦", "♣"]
    ranks_symbols = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    max_pile_length = max(len(pile) for pile in s.tableau)
    
    html = "<table style='border-collapse: collapse;'>"
    for row in range(max_pile_length):
        html += "<tr>"
        for pile in s.tableau:
            if row < len(pile):
                rank, suit = pile[row]
                card_symbol = f"{ranks_symbols[rank - 1]}<span style='color:{'red' if suit in [1, 2] else 'black'};'>{suits_symbols[suit]}</span>"
                html += f"<td style='border: 1px solid black; padding: 5px; text-align: center;'>{card_symbol}</td>"
            else:
                html += "<td style='border: 1px solid black;'></td>"  # Empty space
        html += "</tr>"
    html += "</table>"
    return HTML(html)