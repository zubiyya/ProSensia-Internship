from tkinter import simpledialog

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