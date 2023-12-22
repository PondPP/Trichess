import json
import websockets

class Trichess:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.Password = None
        self.Player = None
        self.Board = None
        self.Piece = None
        self.Danger = None

    async def receive_response(self):
        response = await self.websocket.recv()
        response = response.replace("True", 'true')
        response = response.replace("False", 'false')

        try:
            json_response = json.loads(response)
        except json.JSONDecodeError:
            print(f'Received non-JSON response: {response} unable to extract json.')

        return json_response

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        player_data = await self.receive_response()
        self.Password = player_data['Password']
        self.Player = player_data['Player']
        print(f'Password: {self.Password}, Player: {self.Player}')
    
    async def move_able(self, piece_field):
        data = {
            "Command": "Movable",
            "Password": self.Password,
            "Field": piece_field
        }
        await self.websocket.send(json.dumps(data))

    async def send_move(self, piece_field_from, piece_field_to):
        data = {
            "Command": "Move",
            "Password": self.Password,
            "Move": {
                "From": piece_field_from,
                "To": piece_field_to,
            }
        }
        await self.websocket.send(json.dumps(data))

    async def pass_turn(self):
        data = {
            "Command": "PassTurn",
            "Password": self.Password,
        }
        await self.websocket.send(json.dumps(data))

    async def myPiece(self):
        data = {
            "Command": "MyPiece",
            "Password": self.Password
        }
        await self.websocket.send(json.dumps(data))

    async def check_turn(self):
        data = {
            "Command": "CheckTurn",
            "Password": self.Password,
        }
        await self.websocket.send(json.dumps(data))

    async def promote(self):
        data = {"Command": "Promote",
                "Password": self.Password,
                "Promotion": "Queen"
            }
        await self.websocket.send(json.dumps(data))

    def reconnecting_game(self):
        pass
    def check_king(self):
        pass



            