import tkinter as tk
from tkinter import messagebox
from arcadehub.core.theme_manager import ThemeManager
from arcadehub.core.stats_manager import StatsManager

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