from SpiderSolitar import SpiderSolitaire


class SpiderSolitaireParser:
    
    @staticmethod
    def card_from_string(card_string):
        rank_str, suit_str = card_string[0], card_string[1]
        rank = "A23456789TJQK".index(rank_str) + 1
        suit = "cdhs".index(suit_str)
        return (rank, suit)

    
    @staticmethod
    def tableau_from_string(tableau_string):
        tableau_rows = SpiderSolitaireParser.remove_indent(tableau_string).split('\n')
        max_pile_length = max(len(row) for row in tableau_rows)
        tableau = [[] for _ in range(SpiderSolitaire.NUM_PILES)]
        for row in tableau_rows:
            for i in range(0,max_pile_length,3):
                if i < len(row) and row[i] != ' ':
                    card = SpiderSolitaireParser.card_from_string(row[i:i+2])
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
    