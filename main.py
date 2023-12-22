import asyncio
import time
import MESSAGE
import Trichess
import test
import algorithm
import threading


async def wait_connection(trichess):
    while True:
        try:
            game_start = await trichess.receive_response()
            if game_start['Status'] != "Success":
                return
        except:
            pass

        time.sleep(1)

async def wait_my_turn(trichess):
    while True:
        try:
            await trichess.check_turn()
            turn_response = await trichess.receive_response()

            if turn_response['Status'] == "Success":
                if turn_response['YourTurn']:
                    return turn_response
        except:
            pass

        time.sleep(1)

async def check_promote(trichess):
        while True:
            try:
                promotecheck = await trichess.receive_response()
                if "promotion" in promotecheck["Message"]:
                    return True
                else:
                    return False
            except:
                pass
            
            time.sleep(1)

async def get_my_piece(trichess):
    while True:
        await trichess.myPiece()
        my_piece_response = await trichess.receive_response()

        if my_piece_response['Status'] == 'Success':
            if 'Check board for piece' in my_piece_response['Message']:
                trichess.Piece = my_piece_response['Board']
                break
            
        time.sleep(1)
    return None


async def get_all_possible_move(trichess):
    field = {}
    for current_place in trichess.Piece:
        current_place = current_place['Field']
        
        await trichess.move_able(current_place)
        piece_movable = await trichess.receive_response()

        # handle no movable
        if piece_movable['Status'] == 'Fail' or 'no movable' in piece_movable['Message']:
            continue

        if piece_movable['Status'] == 'Success':
            # print(f'Test on {current_place} success')
            if 'MovableFields' in piece_movable['Message']:
                for val in piece_movable['MovableFields']:
                    if current_place not in field:
                        field[current_place] = []
                    else:
                        field[current_place].append(val['Field'])
                    
    return field

async def get_all_danger(trichess):
    danger = {}
    chesslist = []
    for chess in trichess.Board:
        if chess["Owner"] != trichess.Player:
            chesslist.append(chess)
            
    for chess in chesslist:
        chess = chess['Field']

        await trichess.move_able(chess)
        danger_movable = await trichess.receive_response()

        if danger_movable['Status'] == 'Fail' or 'no movable' in danger_movable['Message']:
            continue
        
        if danger_movable['Status'] == 'Success':
            if 'MovableFields' in danger_movable['Message']:
                for val in danger_movable['MovableFields']:
                    if chess not in danger:
                        danger[chess] = []
                    else:
                        danger[chess].append(val['Field'])

    return danger
    

def check_pass(possible_move):
    return all(len(value) == 0 for value in possible_move.values())


async def main(url, type_algorithm):

    trichess = Trichess.Trichess(url)
    await trichess.connect()

    # loop wait to connect to game
    await wait_connection(trichess)
    
    # loop playgame
    while True:
    # loop wait my turn
        turn_response = await wait_my_turn(trichess)
        if turn_response:
            # if turn_response
            print(MESSAGE.MY_TURN)


            # await check_promote(trichess)
            # if check_promote:
            #     await trichess.promote()


            trichess.Board = turn_response['Board']

            trichess.Danger = await get_all_danger(trichess)

            await get_my_piece(trichess)
            possible_move = await get_all_possible_move(trichess)
                
            # TODO: check if all possible move is None
            if check_pass(possible_move):
                await trichess.pass_turn()
                pass_response = await trichess.receive_response()
                if pass_response['Status'] == 'Success':
                    print(MESSAGE.PASS)
                continue
            
            print("This is possible move: ", possible_move)
            print("This is Danger zone: ", trichess.Danger)
            print("This is a Board: ",trichess.Board)

            '''
            TODO: call algorithm and return piece and move
            '''
            curr_position, move_to = algorithm.algorithm_provider(possible_move, trichess.Board, trichess.Danger, type_algorithm)
                
            await trichess.send_move(curr_position, move_to)
            move_response = await trichess.receive_response()
            
            print(move_response)

            if move_response['Status'] == 'Success':
                print(MESSAGE.MOVE_SUCCESS)
            elif move_response['Status'] == 'Fail':
                await trichess.pass_turn()


            try:
                await check_promote(trichess)
                if check_promote:
                    await trichess.promote()
            except IndexError:
                continue


if __name__ == '__main__':
    URL = 'ws://192.168.1.175:8181/game'
    n_player = int(input("Enter number of player [int]: "))
    # URL = input("Enter URL: ")
    
    for i in range(n_player):
        print(f"Select algorithm for player {i+1}")
        print(MESSAGE.ALGORITHM)
        algo = int(input("Enter algorithm [int]: "))
        
        threading.Thread(target=asyncio.run, args=(main(URL, algo),)).start()
        print("Thread: ", i, " started")

        time.sleep(1)