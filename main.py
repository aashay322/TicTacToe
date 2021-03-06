#Credits to aqeelanwar
#www.aqeel-anwar.com
#Referenced from Git repository: https://github.com/aqeelanwar/Tic-Tac-Toe

from tkinter import *
import numpy as np

size = 600
symbol_size = (size / 3 - size / 8) / 2
symbol_thickness = 50
symbolX_color = '#EE4035'
symbolO_color = '#0492CF'
green_color = '#7BC043'


class tic_tac_toe():
    def __init__(self):
        self.window = Tk()
        self.window.title("Tic-Tac-Toe")
        self.canvas = Canvas(self.window, width=size, height=size)

        #Input from user in the form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.playerX_turns = True
        self.board_status = np.zeros(shape=(3,3))
        self.playerX_starts = True
        
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.XWins = False
        self.OWins = False

        self.X_Score = 0
        self.O_Score = 0
        self.Tie_Score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size / 3, 0, (i + 1) * size / 3,
                                    size)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size / 3, size,
                                    (i + 1) * size / 3)

    def play_again(self):
        self.initialize_board()
        self.playerX_starts = not self.playerX_starts
        self.playerX_turns = self.playerX_starts
        self.board_status = np.zeroes(shape=(3, 3))

    #Drawing functions: Modules required to draw reuqired game based object on canvas

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        #logical_position - grid value on the board
        #grid_position - actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size,
                                grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size,
                                grid_position[1] + symbol_size,
                                width=symbol_thickness,
                                outline=symbolO_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size,
                                grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size,
                                grid_position[1] + symbol_size,
                                width=symbol_thickness,
                                fill=symbolX_color)
        self.canvas.create_line(grid_position[0] - symbol_size,
                                grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size,
                                grid_position[1] - symbol_size,
                                width=symbol_thickness,
                                fill=symbolX_color)
    
    def display_gameover(self):

      if self.X_wins:
        self.X_score += 1 
        text = 'Winner: Player 1 (X)'
        color = symbolX_color
      elif self.O_wins:
        self.O_score += 1
        text = 'Winner: Player 2 (O)'
        color = symbolO_color
      else:
        self.tie_score += 1
        text = 'It is a tie'
        color = 'gray'

      self.canvas.delete("all")
      self.canvas.create_text(size/2, size/3, font = "cmr 60 bold", fill=color, text=text)

      score_text = 'Scores \n'

      self.canvas.create_text(size/2, 5 * size/8, font = "cmr 40 bold", fill = green_color, text = score_text)

      score_text = 'Player 1 (X): ' + str(self.X_Score) +'\n'
      score_text += 'Player 2 (O): ' + str(self.O_Score) + '\n'
      score_text += 'Tie             : ' + str(self.tie_score)

      self.canvas.create_text(size/2, 4 * size/4, font = "cmr 30 bold", fill = green_color, text = score_text)

      self.reset_board = True

      score_text = "Click to play again \n"

      self.canvas.create_text(size/2, 15 * size/16, font = "cmr 20 bold", fill = "gray", text = score_text)

    #Logical Functions: Decide who wins the game and how the game runs 

    def convert_logical_to_grid_position(self, logical_position):
      logical_position = np.array(logical_position, dtype = int)
      return (size/3) * logical_position + size/6
    
    def convert_grid_to_logical_position(self, grid_position):
      grid_position = np.array(grid_position)
      return np.array(grid_position // (size/3), dtype = int)

    def is_grid_occupied (self, logical_position):
      if self.board_status[logical_position[0]][logical_position[1]] == 0: 
        return False
      else: 
        return True

    #Important function to check status of the winner of the game
    def is_winner(self, player): 

      player = -1 if player == 'X' else 1

      #Three in a row 
      for i in range(3):
        #To check if 3 in a row
        if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player: 
          return True 
        #To check if 3 in a column
        if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player: 
          return True 

      #Diagonals 
      if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player: 
        return True 

      if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player: 
        return True 
      
      return False 

    #Check if the game is a tie 
    def is_tie(self): 
      r, c = np.where(self.board_status == 0)
      tie = False 
      if len(r) == 0: 
        tie = True 

      return tie 

    def is_gameover(self): 
      #Either someone wins the game or the entire grid is occupied 
      self.X_wins = self.is_winner('X')

      if not self.X_wins: 
        self.O_wins = self.is_winner('O')

      if not self.O_wins: 
        self.tie = self.is_tie()

      gameover = self.X_wins or self.O_wins or self.tie

      if self.X_wins: 
        print('X Wins')
      if self.O_wins: 
        print("O wins")
      if self.tie: 
        print("It's a tie")

      return gameover
    
    def click(self, event):
      grid_position = [event.x, event.y]
      
      logical_position = self.convert_grid_to_logical_position(grid_position)

      if not self.reset_board: 
        if self.playerX_turns: 
          if not self.is_grid_occupied(logical_position):
            self.draw_X(logical_position)
            self.board_status[logical_position[0]][logical_position[1]] = -1
            self.playerX_turns = not self.playerX_turns
        else: 
          if not self.is_grid_occupied(logical_position):
            self.draw_O(logical_position)
            self.board_status[logical_position[0]][logical_position[1]] = 1
            self.playerX_turns = not self.playerX_turns
        
        #Check if the game has concluded 
        if self.is_gameover():
          self.display_gameover()
        
      else: 
        self.canvas.delete("all")
        self.play_again()
        self.reset_board = False 


game_instance = tic_tac_toe()
game_instance.mainloop()