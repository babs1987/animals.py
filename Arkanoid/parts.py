from random import randint
from enum import Enum
from dataclasses import dataclass
from Arcanoid import Game


class Direction(Enum):
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"


@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int

    def to_pygame(self):
        return [self.x, self.y, self.width, self.height]


@dataclass
class SetBall:
    x: int
    y: int
    radius: int

    def to_pygame(self):
        return [self.x, self.y, self.radius]


@dataclass
class Color:
    r: int
    g: int
    b: int

    def to_pygame(self):
        return self.r, self.g, self.b


class Ball:
    def __init__(self):
        self.color = Color(255, 0, 0)
        self.pos = SetBall(x=60, y=450, radius=10)
        self.direction_x = Direction.RIGHT
        self.direction_y = Direction.UP
        self.speed = 10

    def ball_direction_changer(self, platform: 'Platform', game: 'Game'):
        self.block_collapse(game,platform)
        if self.direction_x == Direction.LEFT:
            self.pos.x -= self.speed
        if self.direction_y == Direction.UP:
            self.pos.y -= self.speed
        if self.direction_x == Direction.RIGHT:
            self.pos.x += self.speed
        if self.direction_y == Direction.DOWN:
            self.pos.y += self.speed
        if self.pos.x <= 10:
            self.direction_x = Direction.RIGHT
        if self.pos.x > 630:
            self.direction_x = Direction.LEFT
        if self.pos.y <= 10:
            self.direction_y = Direction.DOWN

        if self.pos.y > 445 and platform.pos.x < self.pos.x + 6 and self.pos.x < platform.pos.x + platform.pos.width:
            self.direction_y = Direction.UP
        elif self.pos.y >= 460:
            self.speed = 0
            game.game_over()
            # game.texts()
            game.is_running = False

    def make_harder(self,game:'Game',platform:'Platform'):
        randcol = Color(randint(0, 255), randint(0, 255), randint(0, 255))
        for x in game.blocks:
            x.color = randcol
        self.speed+=1
        platform.pos.width-=5
        game.level+=1


    def block_collapse(self, game: 'Game',platform:'Platform'):
        if not game.blocks:
            game.is_running = False
        for block in game.blocks:
            if block.pos.y + 20 >= self.pos.y-5 and block.pos.x<=self.pos.x+5 and block.pos.x+block.pos.width>=self.pos.x:
                game.blocks.remove(block)
                self.make_harder(game,platform)

                print(len(game.blocks))
                #block.color=Color(0,255,0)
                self.direction_y = Direction.DOWN


class Block:
    def __init__(self, color: 'Color', position: 'Rect'):
        self.color = color
        self.pos = position

    def __str__(self):
        return f"{self.pos.x}:{self.pos.y}:{self.color}"

class Platform(Block):
    def __init__(self):
        # super().__init__()
        self.color = Color(0, 200, 100)
        self.pos = Rect(x=0, y=460, width=400, height=20)
        self.is_running = False
        self.direction = 'right'
        self.speed = 20




    def platform_limiter(self):
        if self.pos.x <= 0:
            return "no_left"
        elif self.pos.x + self.pos.width >= 640:
            return "no_right"
