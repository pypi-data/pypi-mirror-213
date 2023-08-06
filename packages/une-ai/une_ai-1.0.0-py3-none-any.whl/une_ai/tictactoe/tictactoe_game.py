from une_ai.tictactoe import TicTacToeGameEnvironment
from une_ai.tictactoe import TicTacToePlayer

import pygame
import math
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
SCORE_BAR_HEIGHT = 40
BOX_SIZE = 50

window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT+SCORE_BAR_HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
window_clock = pygame.time.Clock()

class TicTacToeGame:

    def __init__(self, agent_program_MAX, agent_program_MIN, display_w=DISPLAY_WIDTH, display_h=DISPLAY_HEIGHT, box_size=BOX_SIZE):
        self._box_size = box_size
        self._display = window
        self._display_size = (display_w, display_h)
        self._agents = {}
        self._agents['MAX'] = TicTacToePlayer('MAX', agent_program_MAX)
        self._agents['MIN'] = TicTacToePlayer('MIN', agent_program_MIN)
        self._environment = TicTacToeGameEnvironment(
            self._agents['MAX'],
            self._agents['MIN'],
        )
        
        fonts = pygame.font.get_fonts()
        self._font = fonts[0] # default to a random font
        # try to look among the most common fonts
        test_fonts = ['arial', 'couriernew', 'verdana', 'helvetica']
        for font in test_fonts:
            if font in fonts:
                self._font = font
                break

        self.main()
        
    def _play_step(self):
        game_state = self._environment.get_game_state()
        if TicTacToeGameEnvironment.is_terminal(game_state):
            return
        
        cur_marker = TicTacToeGameEnvironment.turn(game_state)
        cur_player = self._environment.get_player_name(cur_marker)
        
        # SENSE
        self._agents[cur_player].sense(self._environment)
        # THINK
        actions = self._agents[cur_player].think()
        # ACT
        self._agents[cur_player].act(actions, self._environment)
    
    def _reset_bg(self):
        self._display.fill(BLACK)
    
    def _draw_box(self, x, y, color, alpha = 255):
        font = pygame.font.SysFont(self._font, 30)
        game_state = self._environment.get_game_state()
        padding_left = int((self._display_size[0] - 3*self._box_size)/2)
        padding_top = int((self._display_size[1] - 3*self._box_size)/2)
        x_coord = padding_left + x*self._box_size
        y_coord = padding_top + y*self._box_size

        surface = pygame.Surface((self._box_size-2,self._box_size-2))
        surface.set_alpha(alpha) # alpha level
        pygame.draw.rect(surface, color, surface.get_rect())
        self._display.blit(surface, (x_coord, y_coord,self._box_size,self._box_size) )

        cur_mark = game_state.get_item_value(x, y)
        if cur_mark != None:
            color = RED if cur_mark == 'X' else BLUE
            text_size = font.size(cur_mark)
            mark_text = font.render(cur_mark, True, color)
            top = y_coord + int((BOX_SIZE - text_size[1])/2)
            left = x_coord + int((BOX_SIZE - text_size[0])/2)
            self._display.blit(mark_text, (left, top, text_size[0], text_size[1]))
    
    def _draw_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
                self._draw_box(j, i, WHITE)
    
    def _draw_game_over(self):
        mark = TicTacToeGameEnvironment.get_winner(self._environment.get_game_state())
        if mark == 'X':
            winner = 'MAX'
        elif mark == 'O':
            winner = 'MIN'
        else:
            winner = None
        
        if winner is not None:
            text = "Player {1} ({0}) won!".format(mark, winner)
        else:
            text = "Tie!"
        
        font = pygame.font.SysFont(self._font, 20)
        text_size = font.size(text)
        game_over_text = font.render(text, True, WHITE)
        padding_top = int((self._display_size[1] - 3*self._box_size)/2)
        x_coord = int((self._display_size[0] - text_size[0])/2)
        y_coord = padding_top + 3*self._box_size + 30
        self._display.blit(game_over_text, (x_coord, y_coord, text_size[0], text_size[1]))
                
    def _draw_frame(self):
        self._reset_bg()
        self._draw_board()
        if TicTacToeGameEnvironment.is_terminal(self._environment.get_game_state()):
            self._draw_game_over()

    def main(self):
        running = True

        while running:
            # update frame
            self._draw_frame()

            #Event Tasking
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    quit()
            
            # updating game with one step
            # sense - think - act
            self._play_step()

            # Update the clock and display
            pygame.display.update()
            window_clock.tick(1)
