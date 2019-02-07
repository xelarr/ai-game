"""
Name: CoreGame.py
Version: 0.01
Purpose: Basic Connect 4 game for AI group project
Author: Daniel Allen
Date: 07/02/19
"""
# Todo: Convert to pygame
# Todo: Add logging
# Todo: Unit testing hooks
# Todo: Test different grid sizes (should already work but better to be sure)
import numpy as np
import pprint
import logging
import coloredlogs

ROW_COUNT = 6
COLUMN_COUNT = 7
log = logging.getLogger(__name__)
fieldStyle = dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color='white',),
    programname=dict(color='cyan'),
    name=dict(color='blue'))
levelStyle = dict(
    spam=dict(color='green', faint=True),
    debug=dict(color='cyan'),
    verbose=dict(color='blue'),
    info=dict(),
    notice=dict(color='magenta'),
    warning=dict(color='yellow'),
    success=dict(color='green', bold=True),
    error=dict(color='red'),
    critical=dict(color='red', bold=True))
"""Mapping of log format names to default font styles."""
coloredlogs.install(level='DEBUG',
                    logger=log,
                    datefmt='%H:%M:%S',
                    fmt='[%(levelname)s]%(asctime)s || %(message)s',
                    field_styles=fieldStyle, level_styles=levelStyle)

def _create_playField(x=6, y=7):
    """
    Creates a 2D matrix of zeros. Default size is 6X7

    :param x: int: X axis size
    :param y: int: Y axis Size
    :return: 2D int array
    """
    log.debug("Generating playfield with dimensions [{}][{}]".format(x, y))
    playField = np.zeros((x, y))
    return playField


def _drop_piece(playField, row, col, player):
    """
    Places the piece onto the playField

    :param playField: The play field
    :param row: The target row
    :param col: The target column
    :param player: The player making the move
    :return: None
    """
    log.debug("P{}: Placing piece at [{}][{}]".format(player, row, col))
    playField[row][col] = player


def _validate_move(playField, col):
    """
    Checks to make sure the move in question is possible

    :param playField: The play field
    :param col: The target column
    :return: int representing if move possible
    """
    return playField[ROW_COUNT-1][col] == 0


def _get_next_open_row(playField, col):
    """
    Checks where the piece will land on this row

    :param playField: The play field
    :param col: The target column
    :return: int representing the row number
    """
    for i in range(ROW_COUNT):
        if playField[i][col] == 0:
            log.debug("Selected row {} for {}".format(i, col))
            return i


def _winning_move(playField, player):
    """
    Checks if a player has won

    :param playField:
    :param player:
    :return:
    """
    # Check horizontal locations
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if (playField[row][col] == player and
                    playField[row][col+1] == player and
                    playField[row][col+2] == player and
                    playField[row][col+3] == player):
                return True
    # Check vertical locations
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if (playField[row][col] == player and
                    playField[row+1][col] == player and
                    playField[row+2][col] == player and
                    playField[row+3][col] == player):
                return True
    # check diagonal right slope
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT-3):
            if (playField[row][col] == player and
                    playField[row+1][col+1] == player and
                    playField[row+2][col+2] == player and
                    playField[row+3][col+3] == player):
                return True
    # check diagonal left slope
    for col in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT):
            if (playField[row][col] == player and
                    playField[row-1][col+1] == player and
                    playField[row-2][col+2] == player and
                    playField[row-3][col+3] == player):
                return True


def renderer(playField):
    """
    Inverts and prints out the play field

    :param playField: The play field
    :return: None
    """
    pprint.pprint(np.flip(playField, 0))
    # todo: Implement pygame for true gui, rather than cmdline


def _input(playField, turn):
    """
    Gets the player's move and validate it

    param playField: the play field
    :param turn: the current turn
    :return: the column the player chose
    """
    # P1 input
    while True:
        try:
            if turn % 2 == 0:
                col = int(input("Player 1 Make your move (0-6): ").strip())
            # P2 input
            else:  # todo: AI would go here
                col = int(input("Player 2 Make your move (0-6): ").strip())
            if _validate_move(playField, col):
                return col
            else:
                print("Invalid move!")
        except Exception as e:
            log.error(e)
            print("Invalid move!")


def _game_loop(playField):
    """
    The main game loop
    
    :param playField: the play field
    :return: 
    """
    log.info("Game Loop started")
    turn = 0
    while True:
        col = _input(playField, turn)
        row = _get_next_open_row(playField, col)
        _drop_piece(playField, row, col, turn % 2 + 1)
        if _winning_move(playField, turn % 2 + 1):
            log.info("Win condition met for player {}".format(turn % 2 + 1))
            renderer(playField)
            print("Player {} is the Winner in {} turns!".format(turn % 2 + 1, turn))
            return
        renderer(playField)
        turn += 1


def start_game():
    """
    Initialises the game and begins the main loop

    :return: None
    """
    log.info("Initialising game...")
    playField = _create_playField(ROW_COUNT, COLUMN_COUNT)
    _game_loop(playField)


if __name__ == "__main__":
    start_game()