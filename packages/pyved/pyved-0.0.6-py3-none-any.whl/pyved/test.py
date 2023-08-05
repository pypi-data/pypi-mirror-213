import pygame
from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int
    height: float
    email: str


mec = Person('thomas', 99, 1.85, 'thomas.iw@kata.games')
print('hello world')
gameover = False
surf = pygame.display.set_mode((640, 480))

while not gameover:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            gameover = True
    surf.fill('pink')
    pygame.display.flip()

print('bye', mec.name, 'see you when you turn', mec.age+1)
