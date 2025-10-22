# Benyamin Plaksienko –  Cluedo Game

## Overview

This project is a **text-based Cluedo (Clue) game** implemented in Python for **CS 670 – AI** (Project 2, Part 1).  

Key features:

- **Mansion Layout Generation**  
  - Rooms are nodes in a weighted graph.  
  - Edges represent hallways or secret passages (cost 0).  
  - Graph saved to `mansion_layout.json`.

- **Limited Uniform Cost Search (LUCS)**  
  - Player movement is computed using **Limited Uniform Cost Search**.  
  - LUCS finds all reachable rooms from the current location without exceeding the die roll cost.  
  - Secret passages (edges of cost 0) are handled so they don’t consume die roll cost.  

- **Card Dealing & Solution Selection**  
  - Randomly selects 1 **character**, 1 **weapon**, and 1 **room** as the hidden murder solution.  
  - Remaining cards are shuffled and dealt to active players.  
  - Player hands saved to `hands.json`; solution saved to `solution.json`.

- **Turn-Based Gameplay**  
  - Players roll a die to move across the mansion graph via LUCS.  
  - Entering a room triggers a **suggestion**.  
  - Other players refute in turn order by privately showing one matching card.  
  - **Accusations** can be made at the start or end of a turn:  
    - Correct → Player wins, game ends.  
    - Incorrect → Player eliminated from movement/suggestions but can still refute.

- **Game End**  
  - Game ends when a player makes a correct accusation.  
  - Final solution is revealed.

---
## Running the Game

To start the Cluedo game, run the `game.py` script from the project directory:

```bash
python game.py

```


## Development Environment

This project was developed using **Python 3.11** within a **PyCharm** virtual environment. PyCharm's built-in virtual environment feature was used to manage dependencies and isolate the project environment.

If you use PyCharm, the IDE will automatically create and configure a virtual environment for this project. You can run the game and manage packages within PyCharm’s integrated terminal or Python console.
