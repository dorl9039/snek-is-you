# Project description
Final lab assignment in MIT's 6.009: Fundamentals of Programming. The course provided the server, tests, and UI, and I implemented lab.py, which is the core game logic.

The goal is to recreate a version of [Baba Is You](https://www.youtube.com/watch?v=z3_yA4HTJfs&ab_channel=NintendoofAmerica), a 2D puzzle video game in which the player can change the rules of the game as they are playing by moving the text objects that dictate gameplay rules. 

**Graphical objects** (such as a "snek" which is rendered as a snake icon) can be walked on top of, pushed, pulled, or result in defeat depending on the rules of the game defined by **text objects**.

**Text objects** can be a:
- **noun**: e.g., "ROCK" which refers to all graphical objects represented by "rock"
- **property**: e.g., a behavior such as "YOU", "PUSH", or "DEFEAT"
- **verb**: the key to forming gameplay rule. e.g., a connector object that assigns the PROPERTY behavior to all graphical objects represented by NOUN
- **conjunction**: a mechanism for chaining nouns or properites in a rule

For example:
- "SNEK" "IS" "YOU" means that you control snek objects. But if you push a "ROCK" text object to replace the "SNEK" text object to create the rule "ROCK" "IS" "YOU", you now control rock graphical objects instead of sneks.

- "FLAG" "IS "WIN" means that you need to touch the flag objects to win. You can replace "FLAG" with "ROCK" to mean that touching any rock object results in victory. Meanwhile, "FLAG" "IS" "YOU" "AND" "WIN" is an automatic win condition.


## Demo
https://github.com/dorl9039/snek-is-you/assets/121260645/e63a8615-347b-468c-ba70-805d9de00212


Gameplay demonstration using 6.009's provided GUI

## Challenges
- Handling the sheer scope of the game. I broke down the challenges into smaller problems and started off by hard-coding certain rules. This helped me fully understand the basic game logic and figure out what helper functions I wanted to create.
- Figuring out how to recursively handle PULL and PUSH actions, especially when a graphical object can have both PUSH and PULL properties at the same tiem (e.g., "COMPUTER" "IS" "PUSH" "AND" "PULL")
