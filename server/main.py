import uuid
from fastapi import FastAPI, Request

app = FastAPI(debug=True)

games = {}


class Map:
    def __init__(self):
        self.map = [[1, 0, 2, 3],
                    [2, 3, 1, 0]]

    def serialize(self):
        return self.map

class Player:
    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {'name': self.name}


class Game:
    def __init__(self, player: Player):
        self.map = Map()
        self.player = player

    def info(self):
        return {'map': self.map.serialize(),
                'players': [self.player.serialize()]
                }

    def check(self):
        return {'status': 'ok'}


@app.post("/")
async def create_game(request: Request):
    rq = await request.json()

    player_1 = rq['player_1']
    p1_name = player_1['name']
    p1 = Player(p1_name)

    uid = str(uuid.uuid4())
    games[uid] = Game(p1)

    return {'id': uid}


@app.get('/{id}')
def info(id):
    game = games[id]
    return game.info()

@app.get('/{id}/check')
def check(id):
    game = games[id]
    return game.check()
