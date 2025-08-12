import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os
from arcadehub.core.theme_manager import ThemeManager
from arcadehub.core.stats_manager import StatsManager
from arcadehub.core.player_manager import PlayerManager

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