import random
from game_search_algorithms import alfabeta_search, minimax_search
from game import Game

class TicTacToe(Game):

    def __init__(self, height = 3, width = 3, to_win = 3):
        self.height = height
        self.width = width
        self.to_win = to_win

        steps = [(x,y) for x in range(1, self.height +1) for y in range(1, self.width + 1)]
        #print(steps)
        self.initial = {
            'next': 'X',
            'board': {},
            'steps': steps,
            'result': 0
        }

    def legal_steps(self, state):
        return state['steps']

    def take_step(self, step, state):
        if step not in self.legal_steps(state):
            return state
        board = state['board'].copy()
        board[step] = state['next']

        steps = list(state['steps'])
        steps.remove(step)

        next = state['next']
        if next == 'X':
            next = 'O'
        else:
            next = 'X'

        return{
            'next': next,
            'result': self.result(board, step, next),
            'board': board,
            'steps': steps
        }

    def result(self, board, step, player):
        """If X wins with this step then return 1. If O wins with this then return -1. Else return 0."""
        if (self.check_triples(board, step, player, (0, 1)) or self.check_triples(board, step, player, (1, 0)) or
                self.check_triples(board, step, player, (1, -1)) or self.check_triples(board, step, player, (1, 1))):
            return 1 if player == 'X' else -1
        return 0

    def check_triples(self, board, step, player, direction):
        """Check for triples in a direction."""
        delta_x, delta_y = direction
        x, y = step
        n = 0
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = step
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1
        return n >= self.to_win

    def goodness(self, state, player):
        return state['result'] if player == 'X' else -state['result']

    def print(self, state):
        """Let's see the current state."""
        board = state['board']
        for x in range(1, self.height + 1):
            for y in range(1, self.width + 1):
                print(board.get((x, y), '.'), end=" ")
            print()
        print('Result of the game: ', state['result'])
        print()


# PLAYERS
def random_player(game, state):
    """Randomly choose between options"""
    return random.choice(game.legal_steps(state))


def alfabeta_player(game, state):
    """Search in game tree"""
    return alfabeta_search(state, game)


def minimax_player(game, state):
    """Search in game tree"""
    return minimax_search(state, game)


def play_game(game, *players):
    state = game.initial
    game.print(state)
    while True:
        for player in players:
            step = player(game, state)
            state = game.take_step(step, state)
            game.print(state)
            if game.is_leaf(state):
                end_result = game.goodness(state, 'X')
                return "X wins" if end_result == 1 else "O wins" if end_result == -1 else "Draw"


tto = TicTacToe()

# Test if playing works
play_game(tto, random_player, random_player)

# Demonstrate the power of the search algorithms
# you can comment out the game.print(state) lines in the play_game function for this
#for i in range(20):
#    print(play_game(tto, random_player, random_player))  # outcome will be random (starting player has the edge)
    # print(play_game(tto, alfabeta_player, random_player))  # X will always win
    # print(play_game(tto, random_player, alfabeta_player))  # O will most likely win
    # print(play_game(tto, alfabeta_player, alfabeta_player))  # game will always end in draw