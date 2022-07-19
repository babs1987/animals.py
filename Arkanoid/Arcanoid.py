import pygame
from parts import *
from enum import Enum

FRAME_PER_SECOND = 30


class Direction(Enum):
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((640, 480))
        self.level=0
        pygame.display.update()
        pygame.display.set_caption("Арканоид")
        self.platform = Platform()
        self.ball = Ball()
        self.is_running = True
        self.blocks = [Block(Color(255, 0, 0), Rect(x=i, y=j, width=100, height=20)) for i in
                       [0, 108, 216, 323, 431, 539] for j in [0, 25, 50, 75]]

    # def create_blocks(self):

    def render(self):

        self.ball.ball_direction_changer(self.platform, self)
        if self.platform.direction == Direction.LEFT and self.platform.is_running:
            if self.platform.platform_limiter() != "no_left":
                self.platform.pos.x -= self.platform.speed

        elif self.platform.direction == Direction.RIGHT and self.platform.is_running:
            if self.platform.platform_limiter() != "no_right":
                self.platform.pos.x += self.platform.speed
        self.display.fill((0, 0, 0))

        self.texty()
        if self.is_running is False:
            self.game_over()
        pygame.draw.rect(self.display, self.platform.color.to_pygame(), self.platform.pos.to_pygame())

        pygame.draw.circle(self.display, self.ball.color.to_pygame(), (self.ball.pos.x, self.ball.pos.y),
                           self.ball.pos.radius)
        for i in self.blocks:
            pygame.draw.rect(self.display, i.color.to_pygame(), i.pos.to_pygame())

        pygame.display.update()

    # @staticmethod
    def game_over(self):
        font = pygame.font.Font(None, 40)
        if len(self.blocks):
            game_over_text = font.render(f"GAME OVER!", True, (0, 255, 0))
        else:
            game_over_text = font.render(f"YOU WIN", True, (0, 255, 0))
        self.display.blit(game_over_text, (200, 200))


    def texty(self):

        font = pygame.font.Font(None, 40)
        coord_text = font.render(f"Level:{self.level}", True, (0, 255, 0))
        self.display.blit(coord_text, (300, 300))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # and self.platform_limiter() != "no_left":
                    self.platform.is_running = True
                    self.platform.direction = Direction.LEFT

                elif event.key == pygame.K_RIGHT:  # and self.platform_limiter() != "no_right":
                    print("tertertertet")
                    self.platform.is_running = True
                    self.platform.direction = Direction.RIGHT

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.platform.is_running = False
                    self.platform.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.platform.is_running = False
                    self.platform.direction = Direction.RIGHT

    def run(self):
        while self.is_running:
            pygame.time.delay(1000 // FRAME_PER_SECOND)

            self.handle_events()

            self.render()

    def stop(self):
        pygame.quit()


def main():
    game = Game()
    game.run()

    pygame.time.delay(1000)
    game.stop()


if __name__ == '__main__':
    main()
