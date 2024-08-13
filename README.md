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

![Screenshot_1](https://github.com/user-attachments/assets/69c10ca2-3df1-482c-b5de-0e9fc595d530)
![Screenshot_2](https://github.com/user-attachments/assets/b556b403-fb2b-490e-b8ef-4d3f004bac00)

### **elixir_screen.py**

#### *Setup*
- Each player is allocated the same amount of coins to purchase elixirs.
- 5 elixirs with varying costs and power values are available.

#### *Mechanics*
- Players aim to collect elixirs with the highest power within their budget.
- Ash selects elixirs with user assistance.
- Team Rocket uses a genetic algorithm with tournament selection for optimal elixir collection. Tournament selection picks the best-performing elixirs for each generation.
- Final elixir collections are used in Pokémon battles to recover health points.

![Screenshot_3](https://github.com/user-attachments/assets/615d21c1-bfe5-4205-aaa5-2588ef666fc0)
![Screenshot_4](https://github.com/user-attachments/assets/dbe47bec-3af1-44c0-aa74-bb2b77f160f7)
![Screenshot_5](https://github.com/user-attachments/assets/2e6ce47c-6282-46ea-9bd2-6fdc57b026e8)
![Screenshot_6](https://github.com/user-attachments/assets/bdb62e0b-2160-4bdd-8a69-d099b7b35cd3)

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

![Screenshot_7](https://github.com/user-attachments/assets/8428f720-ff7a-410e-9fae-0590a83101ab)
![Screenshot_8](https://github.com/user-attachments/assets/2329ba46-bdbf-4efe-82fb-9deaebe0a6d5)
![Screenshot_9](https://github.com/user-attachments/assets/70b636a9-ac3f-42ea-82fc-b170f3c707ca)
![Screenshot_10](https://github.com/user-attachments/assets/0bddb3d8-7246-4aff-a644-14728202e5b4)

## **Contributing**

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests. Please adhere to the project's coding standards and guidelines.

## **Contact**

If you need help or want to share feedback, feel free to reach out at [israttasnimesha1046@gmail.com](mailto:israttasnimesha1046@gmail.com).

## Authors

- **Israt Tasnim Esha** (1907090)
- **Tasfia Tasnim** (1907102)

**CSE 4110	- Artificial Intelligence Laboratory**  
*Department of Computer Science and Engineering*  
*Khulna University of Engineering and Technology*
