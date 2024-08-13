# **Pokémon Battle Adventure**

Welcome to **Pokémon Battle Adventure**! This game brings the magical world of Pokémon to life, where you can step into the shoes of Ash and embark on an exciting journey to gather your Pokémon and engage in strategic battles against Team Rocket.

## **Table of Contents**
- [Introduction](#introduction)
  - [Background](#background)
  - [Objectives and Goals](#objectives-and-goals)
- [Methodology](#methodology)
  - [pokemon_find_screen.py](#pokemon_find_screenpy)
  - [elixir_screen.py](#elixir_screenpy)
  - [play_screen.py](#play_screenpy)
- [UML Class Diagram](#uml-class-diagram)
- [Result](#result)
- [Contributing](#contributing)
- [Contact](#contact)
- [Authors](#authors)

## **Introduction**

### **Background**

Welcome to the magical world of Pokémon, where childhood dreams come alive and adventures await at every corner. In **Pokémon Battle Adventure**, you relive the excitement of Ash's journey, battling alongside Pikachu, and outsmarting Team Rocket. In this thrilling adventure, you take on the role of Ash, gathering your Pokémon, and preparing for epic battles against Team Rocket, who is always up to their mischievous ways.

### **Objectives and Goals**
- *Recreate the Magic*: Capture the wonder and excitement of the Pokémon series in a Python-based game.
- *Strategic Gameplay*: Implement strategic elements that allow players to choose and manage their Pokémon wisely.
- *Engaging Adventure*: Create a captivating adventure for Ash to retrieve his Pokémon, adding depth and excitement to the gameplay.
- *Epic Battles*: Simulate Pokémon battles with attack, defense, and elixir moves, bringing the thrill of the series to life.
- *Dynamic Swapping*: Allow players to swap Pokémon during battles, adding a layer of strategy and unpredictability.
- *Victory Conditions*: Define clear win/lose conditions based on the health status of all Pokémon, ensuring a fair and exciting competition.

## **Methodology**

### **pokemon_find_screen.py**

#### *Setup*
- Ash, Team Rocket, and their respective Pokémon are randomly assigned to different Pokémon Centers and starting locations.
- Ash knows the location of Pikachu, while Team Rocket knows the location of Meowth.
- After catching Pikachu, Nurse Joy reveals the location of Charmander, followed by Squirtle. Team Rocket follows a similar sequence with Meowth, Weezing, and Wobbuffet.

#### *Mechanics*
- Each player has a fuel limit of 15 liters to catch each Pokémon and a total of 1 minute to catch all Pokémon.
- A player is eliminated if they exceed the fuel limit or fail to catch all Pokémon within 1 minute.
- Ash's movements are controlled by the player, while Team Rocket's movements are guided by an A* algorithm.

### **elixir_screen.py**

#### *Setup*
- Each player is allocated the same amount of coins to purchase elixirs.
- 5 elixirs with varying costs and power values are available.

#### *Mechanics*
- Players aim to collect elixirs with the highest power within their budget.
- Ash selects elixirs with user assistance.
- Team Rocket uses a genetic algorithm with tournament selection for optimal elixir collection. Tournament selection picks the best-performing elixirs for each generation.
- Final elixir collections are used in Pokémon battles to recover health points.

### **play_screen.py**

#### *Setup*
- Each player has 3 Pokémon, each starting with 100 health points.
- Battles are turn-based, with two types of actions: attack and defense.

#### *Mechanics*
- Pokémon and field types affect damage output:
  - *Type matches* between Pokémon and field increase damage to the opponent.
  - *Type advantages*: Fire > Electric, Electric > Water, Water > Fire.
- Players can swap Pokémon if the health points of the swapped Pokémon are not 0.
- Elixirs can be used to boost health points.

#### *Decision Making*
- Ash takes user input for actions, elixir usage, and Pokémon swaps.
- Team Rocket uses the minimax algorithm to choose actions, with fuzzy logic aiding in deciding when to use elixirs or swap Pokémon.

## **UML Class Diagram**

- ![Insert UML Class Diagram Image Here](#)

## **Result**

In this section, we showcase the features of our application along with corresponding screenshots.

- **Fig 3.1**: `announcement_screen.py` (for `pokemon_field_screen.py`)
- **Fig 3.2**: `pokemon_field_screen.py`
- **Fig 3.3**: `announcement_screen.py` (for `player_1_elixir_screen.py`)
- **Fig 3.4**: `player_1_elixir_screen.py`
- **Fig 3.5**: `announcement_screen.py` (for `player_0_elixir_screen.py`)
- **Fig 3.6**: `player_0_elixir_screen.py`
- **Fig 3.7**: `announcement_screen.py` (for `play_screen.py`)
- **Fig 3.8**: `play_screen.py` (Electric Field, Team Rocket using defense, Ash using attack)
- **Fig 3.9**: `play_screen.py` (Fire Field, Team Rocket using attack, Ash using defense)
- **Fig 3.10**: `play_screen.py` (Water Field, Team Rocket using attack, Ash using attack)

## **Contributing**

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests. Please adhere to the project's coding standards and guidelines.

## **Contact**

If you need help or want to share feedback, feel free to reach out at [israttasnimesha1046@gmail.com](mailto:israttasnimesha1046@gmail.com).

## **Authors**

- **Israt Tasnim Esha**
- **Hasibul Hasan Hasib**

*Department of Computer Science and Engineering*  
*Khulna University of Engineering and Technology*

---

This README is now formatted using Markdown elements such as `*`, `**`, and `-`, making it suitable for a GitHub project page.
