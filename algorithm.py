import random
import time

def algorithm_provider(possible_move, current_board, current_danger, type_algorithm):
    if type_algorithm == 1:
        return play_random(possible_move)
    elif type_algorithm == 2:
        return play_main(possible_move, current_board, current_danger)
    else:
        return play_random(possible_move)

def play_random(possible_move):
    while True:
        try:
            random_piece = random.choice(list(possible_move.keys()))
            random_move = random.choice(possible_move[random_piece])
            return random_piece, random_move
        except IndexError:
            continue 

        time.sleep(1)
    

def play_main(possible_move, current_board, current_danger):
    Chesstarget_value = {'Pawn': 2, 'Knight': 4, 'Bishop': 4, 'Rook': 6, 'Queen': 9, 'King': 99}
    Chessvalue = {'Pawn': 4, 'Knight': 2, 'Bishop': 2, 'Rook': 2, 'Queen': 1, 'King': 0}
    best_score = -1
    best_move = {}
    dangerzone = []

    def get_piecetarget_value(field, board):
        for piece_info in board:
            if piece_info['Field'] == field:
                return Chesstarget_value.get(piece_info['Piece'], 0)
        return 0
    
    def get_piece_value(field, board):
        for piece_info in board:
            if piece_info['Field'] == field:
                return Chessvalue.get(piece_info['Piece'], 0)
        return 0
        
    for items in current_danger.values():
            for i in items:
                if i not in dangerzone:
                    dangerzone.append(i)

    for piece, moves in possible_move.items():
        for move in moves:

            if move in dangerzone:
                continue

            move_score = 0
        
            if move in [info['Field'] for info in current_board]:
                move_score = get_piecetarget_value(move, current_board)

            if piece in [info['Field']  for info in current_board]:
                move_score += get_piece_value(piece, current_board)

            if move_score > best_score:
                best_score = move_score
                best_move = (piece, move)

    print(f"Best move selected: {best_move}")
    return best_move if best_move else play_random(possible_move)


