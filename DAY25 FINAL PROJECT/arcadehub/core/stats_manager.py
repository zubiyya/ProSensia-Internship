import json
import os

class StatsManager:
    def __init__(self):
        self.stats_file = os.path.join(os.path.dirname(__file__), 'game_stats.json')  # Fixed path
        print(f"Stats file location: {self.stats_file}")  # Debug line
        self.stats = self.load_stats()
    
    def load_stats(self):
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading stats: {e}")  # Debug line
        
        # Default stats structure
        return {
            'tic_tac_toe': {'wins': 0, 'losses': 0, 'draws': 0},
            'connect_four': {'wins': 0, 'losses': 0, 'draws': 0},
            'hangman': {'wins': 0, 'losses': 0},
            'rock_paper_scissors': {'wins': 0, 'losses': 0, 'draws': 0}
        }
    
    def save_stats(self):
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=4)  # Pretty print
            print("Stats saved successfully!")  # Debug line
        except Exception as e:
            print(f"Error saving stats: {e}")  # Debug line
    
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