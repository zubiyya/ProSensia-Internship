import tkinter as tk
from tkinter import messagebox
import random
import json
import os
from arcadehub.core.theme_manager import ThemeManager
from arcadehub.core.stats_manager import StatsManager
from arcadehub.core.player_manager import PlayerManager

#---- Markers ----
PLAYER1 = 'X'
PLAYER2 = 'O'
AI_PLAYER = 'O'
HUMAN_PLAYER = 'X'

#----- TIC TAC TOE -----
class TicTacToe:
    def __init__(self, root, theme_manager, stats_manager, player_manager):
        self.root = tk.Toplevel(root)
        self.root.title("Tic Tac Toe")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.theme_manager = theme_manager
        self.stats_manager = stats_manager
        self.player_manager = player_manager
        
        self.buttons = [[None]*3 for _ in range(3)]
        self.board = [[' ']*3 for _ in range(3)]
        self.current_player = PLAYER1
        self.vs_ai = None
        self.game_over = False
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        
        self.apply_theme()
        self.mode_selection()

    def apply_theme(self):
        theme = self.theme_manager.get_theme()
        self.root.configure(bg=theme['bg'])

    def mode_selection(self):
        theme = self.theme_manager.get_theme()
        
        self.mode_frame = tk.Frame(self.root, bg=theme['bg'])
        self.mode_frame.pack(pady=20)
        
        tk.Label(self.mode_frame, text="Choose Game Mode", 
                font=('Arial', 12, 'bold'), bg=theme['bg'], fg=theme['text']).pack(pady=10)
        
        tk.Button(self.mode_frame, text="Single Player (vs AI)", width=20, 
                 bg=theme['button'], fg=theme['text'], font=('Arial', 10),
                 command=lambda: self.set_mode(True)).pack(pady=5)
        
        tk.Button(self.mode_frame, text="Multiplayer", width=20, 
                 bg=theme['button'], fg=theme['text'], font=('Arial', 10),
                 command=lambda: self.set_mode(False)).pack(pady=5)

    def set_mode(self, vs_ai):
        self.vs_ai = vs_ai
        self.player1_name, self.player2_name = self.player_manager.get_player_names(vs_ai)
        self.mode_frame.destroy()
        self.setup_game()

    def setup_game(self):
        theme = self.theme_manager.get_theme()
        
        #rules 
        rules_text = "Rules:\n1. Players take turns marking a square\n2. First to get 3 in a row wins\n3. X goes first"
        rules_label = tk.Label(self.root, text=rules_text, font=('Arial', 10), 
                              bg=theme['bg'], fg=theme['text'], justify=tk.LEFT)
        rules_label.pack(pady=5)
        
        current_name = self.player1_name if self.current_player == PLAYER1 else self.player2_name
        self.turn_label = tk.Label(self.root, text=f"{current_name}'s Turn ({self.current_player})", 
                                  font=('Arial', 12, 'bold'), bg=theme['bg'], fg=theme['text'])
        self.turn_label.pack(pady=5)
        
        self.frame = tk.Frame(self.root, bg=theme['bg'])
        self.frame.pack()
        
        self.buttons = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.frame, text=' ', width=6, height=3, font=('Arial', 16), 
                              bg=theme['accent'], fg=theme['text'],
                              command=lambda r=i, c=j: self.make_move(r, c))
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[i][j] = btn
                
        tk.Button(self.root, text="Restart Game", bg=theme['button'], fg=theme['text'],
                 command=self.restart_game).pack(pady=10)

    def make_move(self, r, c):
        if self.board[r][c] == ' ' and not self.game_over:
            self.board[r][c] = self.current_player
            self.buttons[r][c].config(text=self.current_player, state='disabled', fg='black', font=('Arial', 16, 'bold'))
        
            if self.check_winner(self.current_player):
                self.game_over = True
                winner_name = self.player1_name if self.current_player == PLAYER1 else self.player2_name
                self.turn_label.config(text=f"{winner_name} wins!")
            
                if self.vs_ai:
                    if self.current_player == HUMAN_PLAYER:
                        self.stats_manager.update_stats('tic_tac_toe', 'wins')
                    else:
                        self.stats_manager.update_stats('tic_tac_toe', 'losses')
            
                self.show_game_over(f"{winner_name} wins!")
                return
            elif self.is_draw():
                self.game_over = True
                self.turn_label.config(text="It's a draw!")
                if self.vs_ai:
                    self.stats_manager.update_stats('tic_tac_toe', 'draws')
                self.show_game_over("It's a draw!")
                return
            
        self.switch_turn()
        if self.vs_ai and self.current_player == AI_PLAYER and not self.game_over:
            self.root.after(500, self.ai_move)

    def ai_move(self):
        best_score = -float('inf')
        move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = AI_PLAYER
                    score = self.minimax(False)
                    self.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        if move:
            self.make_move(*move)

    def minimax(self, is_maximizing):
        if self.check_winner(AI_PLAYER):
            return 1
        elif self.check_winner(HUMAN_PLAYER):
            return -1
        elif self.is_draw():
            return 0

        if is_maximizing:
            best = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = AI_PLAYER
                        score = self.minimax(False)
                        self.board[i][j] = ' '
                        best = max(score, best)
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = HUMAN_PLAYER
                        score = self.minimax(True)
                        self.board[i][j] = ' '
                        best = min(score, best)
            return best

    def switch_turn(self):
        self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1
        current_name = self.player1_name if self.current_player == PLAYER1 else self.player2_name
        self.turn_label.config(text=f"{current_name}'s Turn ({self.current_player})")

    def check_winner(self, symbol):
        b = self.board
        return any(all(cell == symbol for cell in row) for row in b) or \
               any(all(b[r][c] == symbol for r in range(3)) for c in range(3)) or \
               all(b[i][i] == symbol for i in range(3)) or \
               all(b[i][2 - i] == symbol for i in range(3))

    def is_draw(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def show_game_over(self, message):
        response = messagebox.askyesno("Game Over", message + "\nWould you like to play again?")
        if response:
            self.restart_game()
        else:
            self.root.destroy()

    def restart_game(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ' '
                self.buttons[i][j].config(text=' ', state='normal', fg='black', font=('Arial', 16, 'bold'))
        self.current_player = PLAYER1
        self.game_over = False
        current_name = self.player1_name if self.current_player == PLAYER1 else self.player2_name
        self.turn_label.config(text=f"{current_name}'s Turn ({self.current_player})")

    def on_close(self):
        self.root.destroy()