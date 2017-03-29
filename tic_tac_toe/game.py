from tic_tac_toe.exceptions import *

# internal helpers
def _position_is_empty_in_board(position, board):
    """
    Checks if given position is empty ("-") in the board.

    :param position: Two-elements tuple representing a
                     position in the board. Example: (0, 1)
    :param board: Game board.

    Returns True if given position is empty, False otherwise.
    """
    position_row = position[0]
    position_column = position[1]

    return board[position[0]][position[1]] == '-'


def _position_is_valid(position):
    """
    Checks if given position is a valid. To consider a position as valid, it
    must be a two-elements tuple, containing values from 0 to 2.
    Examples of valid positions: (0,0), (1,0)
    Examples of invalid positions: (0,0,1), (9,8), False

    :param position: Two-elements tuple representing a
                     position in the board. Example: (0, 1)

    Returns True if given position is valid, False otherwise.
    """

    valid_positions = (
        # horizontals
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2),

        # verticals
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
        (0, 2), (1, 2), (2, 2),

        # diagonals
        (0, 0), (1, 1), (2, 2),
        (2, 0), (1, 1), (0, 2),

    )
    
    return position in valid_positions


def _board_is_full(board):
    """
    Returns True if all positions in given board are occupied.

    :param board: Game board.
    """
    for i in board:
        for j in i:
            if j == '-':
                return False
    return True


def _is_winning_combination(board, combination, player):
    """
    Checks if all 3 positions in given combination are occupied by given player.

    :param board: Game board.
    :param combination: Tuple containing three position elements.
                        Example: ((0,0), (0,1), (0,2))

    Returns True of all three positions in the combination belongs to given
    player, False otherwise.
    """
    for position in combination:
        # If we find any position that doesn't contain a player
        # we can just return False
        if board[position[0]][position[1]] != player:
            return False
    return True
#


def _check_winning_combinations(board, player):
    """
    There are 8 possible combinations (3 horizontals, 3, verticals and 2 diagonals)
    to win the Tic-tac-toe game.
    This helper loops through all these combinations and checks if any of them
    belongs to the given player.

    :param board: Game board.
    :param player: One of the two playing players.

    Returns the player (winner) of any of the winning combinations is completed
    by given player, or None otherwise.
    """
    combinations = (
        # horizontals
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),

        # verticals
        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),

        # diagonals
        ((0, 0), (1, 1), (2, 2)),
        ((2, 0), (1, 1), (0, 2)),

    )

    for combination in combinations:
        if _is_winning_combination(board, combination, player):
            return player
    return None


# public interface
def start_new_game(player1, player2):
    """
    Creates and returns a new game configuration.
    """
    return {
        'player1': player1,
        'player2': player2,
        'board': [
            ["-", "-", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"]

        ],
        'next_turn': player1,
        'winner': None
    }


def get_winner(game):
    """
    Returns the winner player if any, or None otherwise.
    """
    return game['winner']


def move(game, player, position):
    """
    Performs a player movement in the game. Must ensure all the pre requisites
    checks before the actual movement is done.
    After registering the movement it must check if the game is over.
    """

    # Get the current board
    board = game['board']

    # If the game already has a winner or the board is full
    # there's nothing else to see. We raise an InvalidMovement exception
    # We rely on _board_is_full here
    
    if game['winner'] or _board_is_full(board):
        raise InvalidMovement('Game is over.')

    # If the player attempting to make the move is not
    # the allowed one, we raise another exception
    # We use get_next_turn here
    if player != get_next_turn(game):
        raise InvalidMovement('"{}" moves next.'.format(game['next_turn']))

    # If the position that the user is trying to move is not valid
    # we raise another exception.
    # We rely on the _position_is_valid function
    if not _position_is_valid(position):
        raise InvalidMovement('Position out of range.')

    # If the position is already full (someone performed a previous
    # move on that position) we raise another exception.
    # We use the _position_is_empty_in_board function
    if not _position_is_empty_in_board(position, board):
        raise InvalidMovement('Position already taken.')

    # IMPORTANT POINT
    # Up to this point, we've checked all the ILLEGAL moves.
    # From now on everything else is valid

    # The first thing we do is we make the actual move
    # We mark the position with the player
    board[position[0]][position[1]] = player

    # We then check to see if that last move, made
    # some player to win
    winner = _check_winning_combinations(board, player)

    # If the movement resulted in a winner we do some
    # book-keeping tasks
    # If we didn't produce a winner, but we filled a whole board
    # we raise the GameOver exception with a "tied game".
    # Or in any other case (final _else_), we just
    # swap the next player to keep the game going

    if winner:
        game['winner'] = winner
        game['next_turn'] = None
        raise GameOver('"{}" wins!'.format(winner))
    elif _board_is_full(board):
        game['next_turn'] = None
        raise GameOver('Game is tied!')
    else:
        game['next_turn'] = game['player1'] if game['next_turn'] == game['player2'] else game['player2']


def get_board_as_string(game):
    """
    Returns a string representation of the game board in the current state.
    """
    
    board = game['board']
    board_string= """
{}  |  {}  |  {}
--------------
{}  |  {}  |  {}
--------------
{}  |  {}  |  {}
"""
    
    flattened = sum(board, [])
    
    return board_string.format(*flattened)


def get_next_turn(game):
    """
    Returns the player who plays next, or None if the game is already over.
    """
    return game['next_turn']
