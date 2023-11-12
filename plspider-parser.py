import pandas as pd
import logging
import re

def load(filename='plspider.txt'):
    df_new = load_v30_v41(filename)
    logging.debug(f"{len(df_new)} read into df_new")
    df_old = load_v13_v29(filename)
    logging.debug(f"{len(df_old)} read into df_old")

    df_new = filter_moves_valid(df_new)
    logging.debug(f"filter_moves_valid df_new: {len(df_new)} remain")
    df_new = filter_empties_valid(df_new)
    logging.debug(f"filter_empties_valid df_new: {len(df_new)} remain")
    df_new = filter_version_valid(df_new)
    logging.debug(f"filter_version_valid df_new: {len(df_new)} remain")

    df_old = filter_moves_valid(df_old)
    logging.debug(f"filter_moves_valid df_old: {len(df_old)} remain")
    df_old = filter_version_valid(df_old)
    logging.debug(f"filter_version_valid df_old: {len(df_old)} remain")

    all = pd.concat([df_old,df_new])
    logging.debug(f"concatenating to total: {len(all)}")
    all = filter_result_valid(all)
    logging.debug(f"filter_result_valid: {len(all)} remain")


    parse_moves(all)
    parse_result(all)
    parse_move_count(all)
    all = validate_move_count(all)
    logging.debug(f"validate_move_count: {len(all)} remain")

    return all


def load_v30_v41(file_path):
    columns_info = [
        ("Result", 5),
        ("Seed", 6),
        ("Time", 7),
        ("Seconds", 14),
        ("Keys", 10),
        ("MoveCount", 11),
        ("Empties", 11),
        ("Version", 6),
        ("Date", 30),
        ("MovesStr", 999999),
    ]
    column_names, column_widths = zip(*columns_info)
    df = pd.read_fwf(file_path, widths=column_widths, header=None)
    df.columns = column_names

    return df

def load_v13_v29(file_path):
    columns_info = [
        ("Result", 5),
        ("Seed", 6),
        ("Time", 7),
        ("Seconds", 14),
        ("Keys", 10),
        ("MoveCount", 11),
        ("Version", 6),
        ("Date", 30),
        ("MovesStr", 999999),
    ]
    column_names, column_widths = zip(*columns_info)
    df = pd.read_fwf(file_path, widths=column_widths, header=None)
    df.columns = column_names

    return df

def filter_result_valid(df):
    return df[df['Result'].isin(["Won", "Lost"])]

def filter_moves_valid(df):
    return df[df['MoveCount'].str.endswith("moves")]

def filter_empties_valid(df):
    return df[df['Empties'].str.endswith("empties")]

def filter_version_valid(df):
    return df[df['Version'].str.match(r"V\d\.\d{2}")]

def parse_move_count(df):
    df['MoveCount'] = df['MoveCount'].str.extract(r'(\d+)').astype(int)

def parse_single_move(str):
    # 5:5>10
    pattern = re.compile(r"(\d+):(\d+)>(\d+)")
    match = pattern.match(str)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    elif str == "D":
        return 'deal'
    elif str.endswith("C"):
        return ('clear', int(str[:-1]))
    else:
        raise ValueError("Invalid move string: " + str)

def parse_move_line(line):
    if(isinstance(line, str)):
        try:
            return list(map(parse_single_move,line.split(' ')))
        except ValueError as err:
            logging.warning(err)
            return None

def parse_moves(df):
    df['Moves'] = df['MovesStr'].apply(parse_move_line).apply(convert_moves_to_num_cards_and_zero_idx)

def parse_result(df):
    df['Won'] = df['Result'] == "Won"

def validate_move_count(df):
    return df[df['MoveCount'] == df['Moves'].apply(lambda x: len(x) if x is not None else 0)]

def convert_moves_to_num_cards_and_zero_idx(moves):
    if moves is None:
        return
    num_cards = [6,5,5,6,5,5,6,5,5,6]
    new_moves = []
    for move in moves:
        if move == 'deal':
            num_cards = [x+1 for x in num_cards]   
            new_moves.append('deal')
        elif move[0] == 'clear':
            col = move[1]
            num_cards[col-1] -= 13
            new_moves.append(move)
        else:
            src, idx, dst = move
            num = num_cards[src-1]-idx + 1
            num_cards[src-1] -= num
            num_cards[dst-1] += num
            new_moves.append((src-1, dst-1, num))
    return new_moves

if __name__=='__main__':
    data = load('plsmall.txt')
    print(data.head())
