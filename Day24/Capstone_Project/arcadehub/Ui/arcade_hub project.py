import tkinter as tk
from tkinter import messagebox 
from arcadehub.core.theme_manager import ThemeManager  
from arcadehub.core.stats_manager import StatsManager
from arcadehub.core.player_manager import PlayerManager
from arcadehub.games.tic_tac_toe import TicTacToe
from arcadehub.games.connect_four import ConnectFour
from arcadehub.games.hangman import Hangman
from arcadehub.games.rock_paper_scissors import RockPaperScissors
from arcadehub.ui.stats_window import StatsWindow

#---- MAIN MENU -----
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


