from typing import Type

class Beat:
    def __init__(self, text: str, choices: list, children: list, status: bool = True):
        self.text = text           #text to be printed for player
        self.choices = choices     #options for player to select from
        self.children = children   #next beat based on children
        self.status = status       #if true, game is still active, if false, game over


class Choice:
    def __init__(self, text: str, recap: str):
        self.text = text
        self.recap = recap

e1 = Beat("You kept walking and continued your day like normal.", [], [], False)
c1a = Choice("Pick up the\nNecklace", "You picked up the Necklace")
c1b = Choice("Leave the Necklace\nwhere it is", "You left the Necklace on the ground")
b1 = Beat("You are walking through a park one afternoon. The weather is warm, the sun is out, and the grass is green. Something shiny catches the corner of your eye. You look over and see something silver in the grass nearby. You walk toward it to see it’s a chain necklace with some sort of bird as the pendant. You’re not quite sure why, but something about the necklace seems to be attracting you toward it, as if it’s calling out to you in somehow…", [c1a, c1b], [None, e1], True)
