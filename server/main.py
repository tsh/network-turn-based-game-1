import uuid
from fastapi import FastAPI

app = FastAPI(debug=True)

games = {}


class Game:
    def info(self):
        return {'map': [[1, 0, 2, 3],
                        [2, 3, 1, 0]],
                'players': [{'name': 'User1', 'is_active': True},
                            {'name': 'User2'}]}

    def check(self):
        return {'status': 'ok'}


@app.post("/")
def create_game():
    uid = str(uuid.uuid4())
    games[uid] = Game()
    return {'id': uid}


@app.get('/{id}')
def info(id):
    game = games[id]
    return game.info()

@app.get('/{id}/check')
def check(id):
    game = games[id]
    return game.check()
