# ArcadeHub – Multi-Game Desktop App

**ArcadeHub** is a Tkinter-based desktop app that brings together classic logic games in a single clean interface. With AI opponents, multiplayer modes, and interactive GUI elements, it's perfect for quick brain breaks or fun with friends.

---

## Games Included
- **Tic Tac Toe** – with Single / Multiplayer
- **Connect Four** – with Single / Multiplayer
- **Hangman** – Canvas-based drawing for visual feedback
- **Rock Paper Scissors** – Quick reflex-based fun

---

## Folder Structure
capstone_project/
  ├──setup.py
  └──arcade_hub/
    │── main.py # App entry point
    ├── __init__.py

    ├── core/ # Game logic utilities
      ├── __init__.py
      ├── theme_manager.py 
      ├── stats_manager.py 
      └── player_manager.py 

    ├── games/ # Game implementations
      ├── __init__.py
      ├── tic_tac_toe.py
      ├── connect_four.py
      ├── hangman.py
      └── rock_paper_scissors.py

    ├── ui/ # Interface
      ├── __init__.py
      ├── arcade_hub.py 
      └── stats_window.py

    └── screenshots/ # Screenshots, icons
      ├── main_menu.png
      ├── tic_tac_toe.png
      ├── connect_four.png
      ├── rock_paper_scissors.png
      └── hangman.png

---

## How to Run the App

- Install dependencies (if any)
pip install -e .
- Run the app
python arcade_hub/main.py

---

## Features

-**Themed GUI** (Tkinter) with 4 color schemes  
-**AI Opponents**:  
  - Tic Tac Toe: Minimax algorithm  
  - Connect Four: Rule-based logic (win/block/random)  
-**Hangman Animations**: Progressive canvas drawings  
-**Modular OOP Design**: Separated core/games/ui logic  
-**Replay System**: Instant restart option after games  
-**Statistics Tracking**: Persistent win/loss records saved to json file(JSON)  

---
## Dependencies

Python 3.9+
Tkinter (pre-installed with Python)

---

## Team

- Kashaf Qureshi
- Zubia Tanoli
- Umama Jadoon