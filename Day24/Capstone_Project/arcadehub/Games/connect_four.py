import tkinter as tk
from tkinter import messagebox, simpledialog
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

#----- CONNECT FOUR -----
class ConnectFour:
    ROWS = 6
    COLS = 7

    def __init__(self, root, theme_manager, stats_manager, player_manager):
        self.root = tk.Toplevel(root)
        self.root.title("Connect Four")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.theme_manager = theme_manager
        self.stats_manager = stats_manager
        self.player_manager = player_manager
        
        self.board = [[' ' for _ in range(self.COLS)] for _ in range(self.ROWS)]
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
        
        #RULES 
        rules_text = "Rules:\n1. Players take turns dropping pieces\n2. First to connect 4 wins\n3. Pieces fall to bottom"
        rules_label = tk.Label(self.root, text=rules_text, font=('Arial', 10), 
                              bg=theme['bg'], fg=theme['text'], justify=tk.LEFT)
        rules_label.pack(pady=5)
        
        current_name = self.player1_name if self.current_player == PLAYER1 else self.player2_name
        self.turn_label = tk.Label(self.root, text=f"{current_name}'s Turn ({self.current_player})", 
                                  font=('Arial', 12, 'bold'), bg=theme['bg'], fg=theme['text'])
        self.turn_label.pack(pady=5)
        
        self.frame = tk.Frame(self.root, bg=theme['bg'])
        self.frame.pack()
        
        #create column buttons
        self.col_buttons = []
        for c in range(self.COLS):
            btn = tk.Button(self.frame, text=f"↓", width=4, height=1, 
                           bg=theme['button'], fg=theme['text'],
                           command=lambda col=c: self.make_move(col))
            btn.grid(row=0, column=c, padx=1, pady=1)
            self.col_buttons.append(btn)
        
        #create grid
        self.buttons = [[None]*self.COLS for _ in range(self.ROWS)]
        for r in range(self.ROWS):
            for c in range(self.COLS):
                btn = tk.Button(self.frame, text=' ', width=4, height=2, 
                              bg=theme['accent'], fg=theme['text'], font=('Arial', 12), state='disabled')
                btn.grid(row=r+1, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn
                
        tk.Button(self.root, text="Restart Game", bg=theme['button'], fg=theme['text'],
                 command=self.restart_game).pack(pady=10)

    def make_move(self, col):
        if self.game_over:
            return
        
        row = self.get_available_row(col)
        if row is not None:
            self.board[row][col] = self.current_player
            theme = self.theme_manager.get_theme()
            color = theme['secondary'] if self.current_player == PLAYER1 else theme['button']
            self.buttons[row][col].config(text=self.current_player, bg=color, fg='black', font=('Arial', 12, 'bold'))
        
            if self.check_winner(self.current_player):
                self.game_over = True
                winner_name = self.player1_name if self.current_player == PLAYER1 else self.player2_name
                self.turn_label.config(text=f"{winner_name} wins!")
            
                if self.vs_ai:
                    if self.current_player == HUMAN_PLAYER:
                        self.stats_manager.update_stats('connect_four', 'wins')
                    else:
                        self.stats_manager.update_stats('connect_four', 'losses')
            
                self.show_game_over(f"{winner_name} wins!")
                return
            elif self.is_draw():
                self.game_over = True
                self.turn_label.config(text="It's a draw!")
                if self.vs_ai:
                    self.stats_manager.update_stats('connect_four', 'draws')
                self.show_game_over("It's a draw!")
                return
            
            self.switch_turn()
            if self.vs_ai and self.current_player == AI_PLAYER and not self.game_over:
                self.root.after(500, self.ai_move)

    def ai_move(self):
        #checks for winning move
        for c in range(self.COLS):
            row = self.get_available_row(c)
            if row is not None:
                self.board[row][c] = AI_PLAYER
                if self.check_winner(AI_PLAYER):
                    self.board[row][c] = ' '
                    self.make_move(c)
                    return
                self.board[row][c] = ' '
        
        #checks for blocking move
        for c in range(self.COLS):
            row = self.get_available_row(c)
            if row is not None:
                self.board[row][c] = HUMAN_PLAYER
                if self.check_winner(HUMAN_PLAYER):
                    self.board[row][c] = ' '
                    self.make_move(c)
                    return
                self.board[row][c] = ' '
        
        #otherwise random move
        available_cols = [c for c in range(self.COLS) if self.get_available_row(c) is not None]
        if available_cols:
            self.make_move(random.choice(available_cols))

    def get_available_row(self, col):
        for r in reversed(range(self.ROWS)):
            if self.board[r][col] == ' ':
                return r
        return None

    def switch_turn(self):
        self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1
        current_name = self.player1_name if self.current_player == PLAYER1 else self.player2_name
        self.turn_label.config(text=f"{current_name}'s Turn ({self.current_player})")

    def check_winner(self, symbol):
        b = self.board
        #horizontal win check
        for r in range(self.ROWS):
            for c in range(self.COLS - 3):
                if all(b[r][c+i] == symbol for i in range(4)):
                    return True
        #vertical win check
        for r in range(self.ROWS - 3):
            for c in range(self.COLS):
                if all(b[r+i][c] == symbol for i in range(4)):
                    return True
        #diagonal win check
        for r in range(self.ROWS - 3):
            for c in range(self.COLS - 3):
                if all(b[r+i][c+i] == symbol for i in range(4)):
                    return True
                if all(b[r+3-i][c+i] == symbol for i in range(4)):
                    return True
        return False

    def is_draw(self):
        return all(self.board[0][c] != ' ' for c in range(self.COLS))

    def show_game_over(self, message):
        response = messagebox.askyesno("Game Over", message + "\nWould you like to play again?")
        if response:
            self.restart_game()
        else:
            self.root.destroy()

    def restart_game(self):
        theme = self.theme_manager.get_theme()
        for r in range(self.ROWS):
            for c in range(self.COLS):
                self.board[r][c] = ' '
                self.buttons[r][c].config(text=' ', bg=theme['accent'], fg='black', font=('Arial', 12, 'bold'))
        self.current_player = PLAYER1
        self.game_over = False
        current_name = self.player1_name if self.current_player == PLAYER1 else self.player2_name
        self.turn_label.config(text=f"{current_name}'s Turn ({self.current_player})")

    def on_close(self):
        self.root.destroy()