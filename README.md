# Project description
Personal project based on the final lab assignment in the Spring 2022 iteration of MIT's 6.009: Fundamentals of Programming. The course provided the server, tests, and UI, and I implemented lab.py, which is the core game logic.

The goal is to recreate a version of [Baba Is You](https://www.youtube.com/watch?v=z3_yA4HTJfs&ab_channel=NintendoofAmerica), a 2D puzzle video game in which the player can change the rules of the game as they are playing by moving the text objects that dictate gameplay rules. 

**Graphical objects** (such as a "snek" which is rendered as a snake icon) can be walked on top of, pushed, pulled, or result in defeat depending on the rules of the game defined by **text objects**.

**Text objects** can be a:
- **noun**: e.g., "ROCK" which refers to all graphical objects represented by "rock"
- **property**: e.g., a behavior such as "YOU", "PUSH", or "DEFEAT"
- **verb**: the key to forming gameplay rule. e.g., a connector object that assigns the PROPERTY behavior to all graphical objects represented by NOUN
- **conjunction**: a mechanism for chaining nouns or properties in a rule

For example:
- "SNEK IS YOU" means that you control snake objects. If you push a "ROCK" text object to replace the "SNEK" text object to create the rule "ROCK IS YOU", you now control rock graphical objects instead of snakes.
- "FLAG IS WIN" means that you need to touch the flag objects to win. You can replace "FLAG" with "ROCK" (= "ROCK IS WIN") to mean that touching any rock object results in victory.


## Demo

Gameplay demos using 6.009's provided GUI.

### Basic gameplay

![snek_basic_game_demo](https://github.com/dorl9039/snek-is-you/assets/121260645/64728783-b399-4bcd-bf8d-4e20def85e25)

In this example, the player controls the snake ("SNEK IS YOU"), and the win condition is touching the flag ("FLAG IS WIN"). The snake can push computers out of the way ("COMPUTER IS PUSH") but the walls block all movements ("WALL IS STOP").


### Interactions between objects

![snek_push_pull_demo](https://github.com/dorl9039/snek-is-you/assets/121260645/cc1d4578-bd40-42ae-9f9c-49bc1db7b0a5)

Here, the player can pull and push computers. The correct gameplay requires resolving how each computer can also be pulled by and push the other. This logic extends to arbitrarily long sequences of objects as well.

### Rewriting rules

![snek_rules_change_demo](https://github.com/dorl9039/snek-is-you/assets/121260645/119bcada-f677-46d3-b334-b6b185d0e615)

In this example, the player achieves the win condition using the following steps:
- Breaks the rule that prevents the player from traversing walls ("WALL IS STOP")
- Sets the win condition to flag objects ("FLAG IS WIN")
- Changes the player from controlling snake objects to walls ("WALL IS YOU")
- Moves the player to the win condition (wall touches flag).
