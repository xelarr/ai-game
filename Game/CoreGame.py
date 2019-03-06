"""
Name: CoreGame.py
Version: 0.01
Purpose: Basic Connect 4 game for AI group project
Author: Daniel Allen
Date: 07/02/19
"""
import numpy as np
import pprint
import contextlib
import math
with contextlib.redirect_stdout(None):
    import pygame
from logManager import log
import os


ROW_COUNT = 6
COLUMN_COUNT = 7

AIMode = False
log.debug("AI mode set to {}".format(AIMode))
pygame.init()
width = (COLUMN_COUNT+2) * 100
height = (ROW_COUNT + 1) * 100
size = (width, height)
radius = int(100/2 - 5)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4 AI Game")
logo_image = pygame.image.load("unnamed.png")
pygame.display.set_icon(logo_image)

def flattenAndExport(playfield):
    dataForExport = []
    for row in playfield:
        for item in row:
            dataForExport.append(item)
    fileNum = 0
    if not os.path.isdir("trainingData"):
        log.debug("Training Data folder missing... creating")
        os.mkdir("trainingData")

    while True:
        filename = "trainingData/ExportedState{}.txt".format(fileNum)
        if os.path.isfile(filename):
            fileNum += 1
        else:
            f = open(filename, "w")
            f.write(str(dataForExport))
            f.close()
            log.info("Exported current state to {}".format(filename))
            return


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
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-1):
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
    playField = np.flip(playField, 0)

    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, (0, 89, 179), ((col*100), (row*100)+100, 100, 100))
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if playField[row][col] == 0:
                pygame.draw.circle(screen, (0, 0, 0), ((col*100)+50, (row*100)+150), radius)
            if playField[row][col] == 1:
                pygame.draw.circle(screen, (206, 22, 48), ((col*100)+50, (row*100)+150), radius)
            if playField[row][col] == 2:
                pygame.draw.circle(screen, (255, 201, 23), ((col*100)+50, (row*100)+150), radius)
    playField = np.flip(playField, 0)


def _quit(code=0):
    """Cleanly closes the game"""
    if code == 1:
        log.critical("Game quiting with errors!")
    else:
        log.info("Game quiting...")
    pygame.display.quit()
    pygame.quit()
    exit(code)


def _input(playField, turn, pos):
    """
    Gets the player's move and validate it

    param playField: the play field
    :param turn: the current turn
    :return: the column the player chose
    """
    # If AI is enabled, this if statement will call ai to give a column number
    if turn % 2 == 0 and AIMode:
        log.debug("Polling AI code for its move...")
        # todo: call some function that'll return a column number
        col = 0 # todo: remove this line
        return  # todo: remove this line and uncomment and edit the line below
        col = ["some function to get a value off the AI"]

        ### SANITY CHECKS ###
        if col is None:
            log.critical("AI returned Null value")
            _quit(1)  # exit with an error condition
        try:
            int(col)
        except ValueError:
            log.critical("AI didnt return an int")
            _quit(1)  # exit with an error condition
        if col > COLUMN_COUNT-1:
            log.critical("AI returned an impossible position")
            _quit(1)  # exit with an error condition
        else:
            # value from the AI should be known good now, it can be used safely
            log.debug("AI is putting its piece on column {}".format(col))
            return col

    else:
        # if AIMode is not enabled, or its player 1, take input
        posx = pos[0]
        col = int(math.floor(posx/100))
        if col > COLUMN_COUNT-1:
            return None
        log.debug("Player clicked at {}|{} = column: {}".format(pos[0], pos[1], col))
        return col


def _game_loop(playField):
    """
    The main game loop
    
    :param playField: the play field
    :return: 
    """
    log.info("Game Loop started")
    turn = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Allow game to quit
                _quit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, 100))
                posx = event.pos[0]
                if posx < (COLUMN_COUNT * 100) -25 and posx > 25:
                    if turn % 2 == 0:
                        pygame.draw.circle(screen, (206, 22, 48), (posx, 50), int(radius))
                    else:
                        pygame.draw.circle(screen, (255, 201, 23), (posx, 50), int(radius))
                    pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # click = drop piece
                col = _input(playField, turn, event.pos)
                if col is not None:
                    row = _get_next_open_row(playField, col)
                    _drop_piece(playField, row, col, turn % 2 + 1)
                    if _winning_move(playField, turn % 2 + 1):
                        log.info("Win condition met for player {}".format(turn % 2 + 1))
                        renderer(playField)
                        print("Player {} is the Winner in {} turns!".format(turn % 2 + 1, turn))
                        pygame.display.update()
                        pygame.time.wait(2000)
                        quit()
                        return
                    renderer(playField)
                    pygame.display.update()
                    turn += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F6:
                    log.debug("Exporting current game state...")
                    flattenAndExport(playField)


def start_game():
    """
    Initialises the game and begins the main loop

    :return: None
    """
    log.info("Initialising game...")
    playField = _create_playField(ROW_COUNT, COLUMN_COUNT)
    log.info("Rendering playfield...")
    renderer(playField)
    pygame.display.update()
    log.info("Ready!")
    _game_loop(playField)


if __name__ == "__main__":
    start_game()
