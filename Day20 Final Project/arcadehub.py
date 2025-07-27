import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os

#---- Markers ----
PLAYER1 = 'X'
PLAYER2 = 'O'
AI_PLAYER = 'O'
HUMAN_PLAYER = 'X'

#----- Theme Manager -----
class ThemeManager:
    def __init__(self):
        self.current_theme = 'default'
        self.themes = {
            'default': {
                'bg': '#ccf2ff',
                'button': '#b3e6b3',
                'button_hover': '#99d699',
                'text': '#000000',
                'accent': '#ffcccc',
                'secondary': '#d9b3ff'
            },
            'dark': {
                'bg': '#2c2c2c',
                'button': '#404040',
                'button_hover': '#555555',
                'text': '#ffffff',
                'accent': '#666666',
                'secondary': '#4a4a4a'
            },
            'ocean': {
                'bg': '#001f3f',
                'button': '#0074D9',
                'button_hover': '#0056b3',
                'text': '#ffffff',
                'accent': '#39CCCC',
                'secondary': '#7FDBFF'
            },
            'sunset': {
                'bg': '#ff6b35',
                'button': '#f7931e',
                'button_hover': '#e6820d',
                'text': '#ffffff',
                'accent': '#ffcc02',
                'secondary': '#c5d86d'
            }
        }
    
    def get_theme(self):
        return self.themes[self.current_theme]
    
    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name

#----- STATISTICS MANAGER -----
class StatsManager:
    def __init__(self):
        self.stats_file = 'game_stats.json'
        self.stats = self.load_stats()
    
    def load_stats(self):
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'tic_tac_toe': {'wins': 0, 'losses': 0, 'draws': 0},
            'connect_four': {'wins': 0, 'losses': 0, 'draws': 0},
            'hangman': {'wins': 0, 'losses': 0},
            'rock_paper_scissors': {'wins': 0, 'losses': 0, 'draws': 0}
        }
    
    def save_stats(self):
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f)
        except:
            pass
    
    def update_stats(self, game, result):
        if game in self.stats and result in self.stats[game]:
            self.stats[game][result] += 1
            self.save_stats()
    
    def get_stats(self):
        return self.stats
    
    def reset_stats(self):
        for game in self.stats:
            for key in self.stats[game]:
                self.stats[game][key] = 0
        self.save_stats()

#----- PLAYER MANAGER -----
class PlayerManager:
    def __init__(self):
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
    
    def get_player_names(self, vs_ai=False):
        self.player1_name = simpledialog.askstring("Player Names", "Enter Player 1 name:") or "Player 1"
        if not vs_ai:
            self.player2_name = simpledialog.askstring("Player Names", "Enter Player 2 name:") or "Player 2"
        else:
            self.player2_name = "AI"
        return self.player1_name, self.player2_name

#----- ROCK PAPER SCISSORS -----
class RockPaperScissors:
    def __init__(self, root, theme_manager, stats_manager, player_manager):
        self.root = tk.Toplevel(root)
        self.root.title("Rock Paper Scissors")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.theme_manager = theme_manager
        self.stats_manager = stats_manager
        self.player_manager = player_manager
        
        self.choices = ['Rock', 'Paper', 'Scissors']
        self.player_score = 0
        self.ai_score = 0
        self.rounds_played = 0
        self.max_rounds = 5
        self.vs_ai = None
        
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
        rules_text = f"Rules: Best of {self.max_rounds} rounds\nRock beats Scissors, Scissors beats Paper, Paper beats Rock"
        tk.Label(self.root, text=rules_text, font=('Arial', 10), 
                bg=theme['bg'], fg=theme['text'], justify=tk.LEFT).pack(pady=5)
        
        #score display
        self.score_label = tk.Label(self.root, text=f"{self.player1_name}: {self.player_score} | {self.player2_name}: {self.ai_score}", 
                                   font=('Arial', 12, 'bold'), bg=theme['bg'], fg=theme['text'])
        self.score_label.pack(pady=10)
        
        #round display
        self.round_label = tk.Label(self.root, text=f"Round {self.rounds_played + 1} of {self.max_rounds}", 
                                   font=('Arial', 11), bg=theme['bg'], fg=theme['text'])
        self.round_label.pack(pady=5)
        
        #choice buttons
        self.button_frame = tk.Frame(self.root, bg=theme['bg'])
        self.button_frame.pack(pady=20)
        
        for choice in self.choices:
            btn = tk.Button(self.button_frame, text=choice, width=10, height=2,
                           bg=theme['button'], fg=theme['text'], font=('Arial', 12),
                           command=lambda c=choice: self.make_choice(c))
            btn.pack(side=tk.LEFT, padx=10)
        
        #result display
        self.result_label = tk.Label(self.root, text="Make your choice!", 
                                    font=('Arial', 12), bg=theme['bg'], fg=theme['text'])
        self.result_label.pack(pady=20)
        
        #restart button
        tk.Button(self.root, text="Restart Game", bg=theme['accent'], fg=theme['text'],
                 command=self.restart_game).pack(pady=10)
    
    def make_choice(self, player_choice):
        if self.rounds_played >= self.max_rounds:
            return
        
        if self.vs_ai:
            opponent_choice = random.choice(self.choices)
        else:
            opponent_choice = simpledialog.askstring("Player 2", f"{self.player2_name}, enter your choice (Rock/Paper/Scissors):") or "Rock"
            opponent_choice = opponent_choice.capitalize()
            if opponent_choice not in self.choices:
                opponent_choice = "Rock"
        
        result = self.determine_winner(player_choice, opponent_choice)
        self.rounds_played += 1
        
        #update display
        result_text = f"{self.player1_name}: {player_choice} | {self.player2_name}: {opponent_choice}\n{result}"
        self.result_label.config(text=result_text)
        
        if "wins" in result and self.player1_name in result:
            self.player_score += 1
        elif "wins" in result and self.player2_name in result:
            self.ai_score += 1
        
        self.score_label.config(text=f"{self.player1_name}: {self.player_score} | {self.player2_name}: {self.ai_score}")
        self.round_label.config(text=f"Round {self.rounds_played + 1} of {self.max_rounds}")
        
        #check is game over
        if self.rounds_played >= self.max_rounds:
            self.end_game()
    
    def determine_winner(self, choice1, choice2):
        if choice1 == choice2:
            return "It's a tie!"
        elif (choice1 == "Rock" and choice2 == "Scissors") or \
             (choice1 == "Paper" and choice2 == "Rock") or \
             (choice1 == "Scissors" and choice2 == "Paper"):
            return f"{self.player1_name} wins this round!"
        else:
            return f"{self.player2_name} wins this round!"
    
    def end_game(self):
        if self.player_score > self.ai_score:
            winner_msg = f"{self.player1_name} wins the game!"
            if self.vs_ai:
                self.stats_manager.update_stats('rock_paper_scissors', 'wins')
        elif self.ai_score > self.player_score:
            winner_msg = f"{self.player2_name} wins the game!"
            if self.vs_ai:
                self.stats_manager.update_stats('rock_paper_scissors', 'losses')
        else:
            winner_msg = "It's a tie game!"
            if self.vs_ai:
                self.stats_manager.update_stats('rock_paper_scissors', 'draws')
        
        response = messagebox.askyesno("Game Over", winner_msg + "\nWould you like to play again?")
        if response:
            self.restart_game()
        else:
            self.root.destroy()
    
    def restart_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.rounds_played = 0
        for widget in self.root.winfo_children():
            widget.destroy()
        self.apply_theme()
        self.mode_selection()
    
    def on_close(self):
        self.root.destroy()

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

#----- HANGMAN -----
class Hangman:
    def __init__(self, root, theme_manager, stats_manager, player_manager):
        self.root = tk.Toplevel(root)
        self.root.title("Hangman")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.theme_manager = theme_manager
        self.stats_manager = stats_manager
        self.player_manager = player_manager
        
        self.word_categories = {
            "Programming": ["PYTHON", "JAVASCRIPT", "FUNCTION", "VARIABLE", "ALGORITHM"],
            "Animals": ["ELEPHANT", "GIRAFFE", "KANGAROO", "DOLPHIN", "BUTTERFLY"],
            "Countries": ["CANADA", "BRAZIL", "JAPAN", "GERMANY", "AUSTRALIA"]
        }
        self.current_category = None
        self.secret_word = ""
        self.guesses = []
        self.tries_left = 6
        self.game_over = False
        self.hints_used = 0
        self.max_hints = 2
        self.player_name = "Player"
        
        self.apply_theme()
        self.get_player_name()
        self.setup_ui()
        
    def apply_theme(self):
        theme = self.theme_manager.get_theme()
        self.root.configure(bg=theme['bg'])
    
    def get_player_name(self):
        self.player_name = simpledialog.askstring("Player Name", "Enter your name:") or "Player"
        
    def setup_ui(self):
        theme = self.theme_manager.get_theme()
        
        #select category
        self.category_frame = tk.Frame(self.root, bg=theme['bg'])
        self.category_frame.pack(pady=10)
        
        tk.Label(self.category_frame, text="Select Word Category:", 
                font=('Arial', 12), bg=theme['bg'], fg=theme['text']).pack()
        
        for category in self.word_categories.keys():
            tk.Button(self.category_frame, text=category, width=15,
                     bg=theme['button'], fg=theme['text'], font=('Arial', 10),
                     command=lambda c=category: self.set_category(c)).pack(pady=5)
    
    def set_category(self, category):
        self.current_category = category
        self.secret_word = random.choice(self.word_categories[category])
        self.category_frame.destroy()
        self.start_game()
    
    def start_game(self):
        theme = self.theme_manager.get_theme()
        
        #rules
        rules_frame = tk.Frame(self.root, bg=theme['bg'])
        rules_frame.pack(pady=5)
        
        rules_text = f"""Welcome {self.player_name}!
Rules:
1. Guess letters to reveal the hidden word
2. You have 6 incorrect guesses allowed
3. Use hints carefully (max 2 per game)"""
        tk.Label(rules_frame, text=rules_text, font=('Arial', 10), 
                bg=theme['bg'], fg=theme['text'], justify=tk.LEFT).pack()
        
        #hangman drawing
        self.canvas = tk.Canvas(self.root, width=300, height=200, bg=theme['accent'])
        self.canvas.pack(pady=10)
        
        self.canvas.create_line(50, 180, 150, 180, width=3)  # Base
        self.canvas.create_line(100, 180, 100, 50, width=3)  # Pole
        self.canvas.create_line(100, 50, 160, 50, width=3)   # Top
        self.canvas.create_line(160, 50, 160, 70, width=3)   # Rope
        
        #category label
        self.category_label = tk.Label(self.root, text=f"Category: {self.current_category}", 
                                     font=('Arial', 12, 'bold'), bg=theme['bg'], fg=theme['text'])
        self.category_label.pack()
        
        #word display
        self.word_display = tk.StringVar()
        self.update_word_display()
        tk.Label(self.root, textvariable=self.word_display, font=('Arial', 24), 
                bg=theme['bg'], fg=theme['text']).pack(pady=10)
        
        #wrong guesses
        self.wrong_guesses_label = tk.Label(self.root, text="Wrong guesses: ", 
                                          font=('Arial', 12), bg=theme['bg'], fg=theme['text'])
        self.wrong_guesses_label.pack()
        
        #no of tries left
        self.tries_label = tk.Label(self.root, text=f"Tries left: {self.tries_left}", 
                                   font=('Arial', 12), bg=theme['bg'], fg=theme['text'])
        self.tries_label.pack()
        
        #input frame
        input_frame = tk.Frame(self.root, bg=theme['bg'])
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Guess a letter:", font=('Arial', 12), 
                bg=theme['bg'], fg=theme['text']).pack(side=tk.LEFT)
        self.entry = tk.Entry(input_frame, width=3, font=('Arial', 14))
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind('<Return>', lambda e: self.check_guess())
        
        tk.Button(input_frame, text="Guess", bg=theme['button'], fg=theme['text'],
                 command=self.check_guess).pack(side=tk.LEFT, padx=5)
        
        #hint button
        self.hint_button = tk.Button(input_frame, text="Hint", bg=theme['secondary'], fg=theme['text'],
                                   command=self.give_hint, 
                                   state=tk.NORMAL if self.hints_used < self.max_hints else tk.DISABLED)
        self.hint_button.pack(side=tk.LEFT, padx=5)
        
        #restart button
        tk.Button(self.root, text="Restart Game", bg=theme['accent'], fg=theme['text'],
                 command=self.restart_game).pack(pady=10)
    
    def update_word_display(self):
        display = ' '.join([c if c in self.guesses else '_' for c in self.secret_word])
        self.word_display.set(display)
    
    def update_wrong_guesses(self):
        wrong = [g for g in self.guesses if g not in self.secret_word]
        self.wrong_guesses_label.config(text=f"Wrong guesses: {' '.join(wrong)}")
    
    def draw_hangman(self):
        #draw hangman parts based on tries left
        if self.tries_left == 5:  #head
            self.canvas.create_oval(150, 70, 170, 90, width=3)
        elif self.tries_left == 4:  #body line
            self.canvas.create_line(160, 90, 160, 130, width=3)
        elif self.tries_left == 3:  #left arm
            self.canvas.create_line(160, 100, 140, 110, width=3)
        elif self.tries_left == 2:  #right arm
            self.canvas.create_line(160, 100, 180, 110, width=3)
        elif self.tries_left == 1:  #left leg
            self.canvas.create_line(160, 130, 140, 150, width=3)
        elif self.tries_left == 0:  #right leg
            self.canvas.create_line(160, 130, 180, 150, width=3)
    
    def give_hint(self):
        if self.hints_used >= self.max_hints:
            messagebox.showinfo("No Hints Left", "You've used all your hints!")
            return
            
        #letters not yet guessed
        available_letters = [c for c in self.secret_word if c not in self.guesses]
        if not available_letters:
            return
            
        hint_letter = random.choice(available_letters)
        self.guesses.append(hint_letter)
        self.hints_used += 1
        self.hint_button.config(state=tk.DISABLED if self.hints_used >= self.max_hints else tk.NORMAL)
        
        messagebox.showinfo("Hint", f"The word contains the letter: {hint_letter}")
        
        #check if hint completed the word
        if all(c in self.guesses for c in self.secret_word):
            self.game_over = True
            self.stats_manager.update_stats('hangman', 'wins')
            self.show_game_over(f"Congratulations {self.player_name}! You guessed it right!")
            return
            
        self.update_word_display()
    
    def check_guess(self):
        if self.game_over:
            return
            
        guess = self.entry.get().upper()
        self.entry.delete(0, tk.END)
        
        if not guess or len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Invalid Input", "Please enter a single letter")
            return
            
        if guess in self.guesses:
            messagebox.showinfo("Already Guessed", f"You've already guessed '{guess}'")
            return
            
        self.guesses.append(guess)
        
        if guess not in self.secret_word:
            self.tries_left -= 1
            self.tries_label.config(text=f"Tries left: {self.tries_left}")
            self.draw_hangman()
            
            if self.tries_left == 0:
                self.game_over = True
                self.stats_manager.update_stats('hangman', 'losses')
                self.show_game_over(f"Game Over {self.player_name}! The word was: {self.secret_word}")
                return
        else:
            if all(c in self.guesses for c in self.secret_word):
                self.game_over = True
                self.stats_manager.update_stats('hangman', 'wins')
                self.show_game_over(f"Congratulations {self.player_name}! You guessed it right!")
                return
                
        self.update_word_display()
        self.update_wrong_guesses()
    
    def show_game_over(self, message):
        response = messagebox.askyesno("Game Over", message + "\nWould you like to play again?")
        if response:
            self.restart_game()
        else:
            self.root.destroy()
    
    def restart_game(self):
        #clear the game
        for widget in self.root.winfo_children():
            widget.destroy()
        
        #reset game state
        self.guesses = []
        self.tries_left = 6
        self.game_over = False
        self.hints_used = 0
        
        #category selection again
        self.apply_theme()
        self.setup_ui()
    
    def on_close(self):
        self.root.destroy()

#----- STATISTICS ----
class StatsWindow:
    def __init__(self, root, stats_manager, theme_manager):
        self.root = tk.Toplevel(root)
        self.root.title("Game Statistics")
        self.root.geometry("500x400")
        self.stats_manager = stats_manager
        self.theme_manager = theme_manager
        
        self.apply_theme()
        self.display_stats()
    
    def apply_theme(self):
        theme = self.theme_manager.get_theme()
        self.root.configure(bg=theme['bg'])
    
    def display_stats(self):
        theme = self.theme_manager.get_theme()
        stats = self.stats_manager.get_stats()
        
        tk.Label(self.root, text=" Game Statistics ", 
                font=('Arial', 16, 'bold'), bg=theme['bg'], fg=theme['text']).pack(pady=10)
        
        #frame for stats
        stats_frame = tk.Frame(self.root, bg=theme['bg'])
        stats_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        games = [
            ("Tic Tac Toe", "tic_tac_toe"),
            ("Connect Four", "connect_four"),
            ("Hangman", "hangman"),
            ("Rock Paper Scissors", "rock_paper_scissors")
        ]
        
        for i, (game_name, game_key) in enumerate(games):
            game_frame = tk.LabelFrame(stats_frame, text=game_name, 
                                     font=('Arial', 12, 'bold'), 
                                     bg=theme['bg'], fg=theme['text'])
            game_frame.pack(fill='x', pady=5, padx=10)
            
            game_stats = stats[game_key]
            
            if 'draws' in game_stats:
                stats_text = f"Wins: {game_stats['wins']} | Losses: {game_stats['losses']} | Draws: {game_stats['draws']}"
                total_games = game_stats['wins'] + game_stats['losses'] + game_stats['draws']
                if total_games > 0:
                    win_rate = (game_stats['wins'] / total_games) * 100
                    stats_text += f"\nWin Rate: {win_rate:.1f}%"
            else:
                stats_text = f"Wins: {game_stats['wins']} | Losses: {game_stats['losses']}"
                total_games = game_stats['wins'] + game_stats['losses']
                if total_games > 0:
                    win_rate = (game_stats['wins'] / total_games) * 100
                    stats_text += f"\nWin Rate: {win_rate:.1f}%"
            
            tk.Label(game_frame, text=stats_text, font=('Arial', 10), 
                    bg=theme['bg'], fg=theme['text']).pack(pady=5)
        
        #buttons
        button_frame = tk.Frame(self.root, bg=theme['bg'])
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Reset Statistics", 
                 bg=theme['accent'], fg=theme['text'], font=('Arial', 10),
                 command=self.reset_stats).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Close", 
                 bg=theme['button'], fg=theme['text'], font=('Arial', 10),
                 command=self.root.destroy).pack(side=tk.LEFT, padx=10)
    
    def reset_stats(self):
        response = messagebox.askyesno("Reset Statistics", 
                                     "Are you sure you want to reset all statistics?")
        if response:
            self.stats_manager.reset_stats()
            messagebox.showinfo("Statistics Reset", "All statistics have been reset!")
            self.root.destroy()

# ---- MAIN MENU -----
class ArcadeHub:
    def __init__(self, root):
        self.root = root
        self.root.title("ArcadeHub - Play Now!")
        self.root.geometry("500x600")
        
        self.theme_manager = ThemeManager()
        self.stats_manager = StatsManager()
        self.player_manager = PlayerManager()
        
        self.apply_theme()
        self.create_menu()

    def apply_theme(self):
        theme = self.theme_manager.get_theme()
        self.root.configure(bg=theme['bg'])

    def create_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        theme = self.theme_manager.get_theme()
        
        #title
        tk.Label(self.root, text="🎮 Welcome to ArcadeHub! 🎮", 
                font=('Arial', 18, 'bold'), bg=theme['bg'], fg=theme['text']).pack(pady=20)
        
        #game buttons
        games = [
            ("Tic Tac Toe", self.launch_ttt, theme['button']),
            ("Connect Four", self.launch_c4, theme['accent']),
            ("Hangman", self.launch_hangman, theme['secondary']),
            ("Rock Paper Scissors", self.launch_rps, theme['button'])
        ]
        
        for game_name, command, color in games:
            btn = tk.Button(self.root, text=game_name, width=20, height=2, 
                           bg=color, fg=theme['text'], font=('Arial', 12),
                           command=command)
            btn.pack(pady=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=theme['button_hover']))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
        
        util_frame = tk.Frame(self.root, bg=theme['bg'])
        util_frame.pack(pady=20)
        
        tk.Button(util_frame, text="Statistics", width=15, height=2, 
                 bg=theme['accent'], fg=theme['text'], font=('Arial', 10),
                 command=self.show_stats).pack(side=tk.LEFT, padx=10)
        
        tk.Button(util_frame, text="Themes", width=15, height=2, 
                 bg=theme['secondary'], fg=theme['text'], font=('Arial', 10),
                 command=self.show_themes).pack(side=tk.LEFT, padx=10)
        
        tk.Button(self.root, text="Exit", width=20, height=2, 
                 bg='#ff6b6b', fg='white', font=('Arial', 12),
                 command=self.root.quit).pack(pady=20)

    def show_themes(self):
        theme_window = tk.Toplevel(self.root)
        theme_window.title("Select Theme")
        theme_window.geometry("300x250")
        
        current_theme = self.theme_manager.get_theme()
        theme_window.configure(bg=current_theme['bg'])
        
        tk.Label(theme_window, text="Choose Theme", 
                font=('Arial', 14, 'bold'), 
                bg=current_theme['bg'], fg=current_theme['text']).pack(pady=10)
        
        themes = [
            ("Default", "default"),
            ("Dark Mode", "dark"),
            ("Ocean Blue", "ocean"),
            ("Sunset Orange", "sunset")
        ]
        
        for theme_name, theme_key in themes:
            tk.Button(theme_window, text=theme_name, width=20,
                     bg=current_theme['button'], fg=current_theme['text'],
                     command=lambda t=theme_key: self.change_theme(t, theme_window)).pack(pady=5)

    def change_theme(self, theme_name, window):
        self.theme_manager.set_theme(theme_name)
        self.apply_theme()
        self.create_menu()
        window.destroy()
        messagebox.showinfo("Theme Changed", f"Theme changed to {theme_name.title()}!")

    def show_stats(self):
        StatsWindow(self.root, self.stats_manager, self.theme_manager)

    def launch_ttt(self):
        TicTacToe(self.root, self.theme_manager, self.stats_manager, self.player_manager)

    def launch_c4(self):
        ConnectFour(self.root, self.theme_manager, self.stats_manager, self.player_manager)

    def launch_hangman(self):
        Hangman(self.root, self.theme_manager, self.stats_manager, self.player_manager)

    def launch_rps(self):
        RockPaperScissors(self.root, self.theme_manager, self.stats_manager, self.player_manager)


if __name__ == "__main__":
    root = tk.Tk()
    app = ArcadeHub(root)
    root.mainloop()

