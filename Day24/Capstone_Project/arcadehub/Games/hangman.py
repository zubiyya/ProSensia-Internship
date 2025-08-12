import tkinter as tk
from tkinter import simpledialog, messagebox  
import random
import os
from arcadehub.core.theme_manager import ThemeManager
from arcadehub.core.stats_manager import StatsManager
from arcadehub.core.player_manager import PlayerManager

#----- HANGMAN -----
class Hangman:
    def __init__(self, root, theme_manager, stats_manager, player_manager):
        self.root = tk.Toplevel(root)
        self.root.title("Hangman")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.theme_manager = theme_manager
        self.stats_manager = stats_manager
        self.player_manager = player_manager
        
        # Fixed word categories (properly indented)
        self.word_categories = {
            "Programming": ["PYTHON", "JAVASCRIPT", "FUNCTION", "VARIABLE", "ALGORITHM"],
            "Animals": ["ELEPHANT", "GIRAFFE", "KANGAROO", "DOLPHIN", "BUTTERFLY"],
            "Countries": ["CANADA", "BRAZIL", "JAPAN", "GERMANY", "AUSTRALIA"]
        }
        print("Categories loaded:", list(self.word_categories.keys()))
        
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
