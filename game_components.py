import sys, pygame
from globals import screen, font, background
from constants import *

class GameText:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.rect = pygame.Rect(pos, font.render(self.text, True, (0, 0, 255)).get_size())

    def erase(self):
        screen.blit(background, self.rect, self.rect)

class PlainText(GameText):
    def __init__(self, text, pos):
        super().__init__(text, pos)

    def draw(self):
        self.erase()
        screen.blit(font.render(self.text, True, LIGHT_PINK), self.pos)

class ButtonText(GameText):
    def __init__(self, text, pos):
        super().__init__(text, pos)

    def draw(self, hover = False):
        screen.blit(background, self.rect, self.rect)
        color = BLUE if hover else LIGHT_BLUE
        screen.blit(font.render(self.text, True, color), self.pos)

    def is_hovering(self, pos):
        return self.rect.collidepoint(pos)


class Piece:
    def __init__(self, color, cell_i, cell_j, pos_rect):
        self.color = color
        self.cell_i = cell_i
        self.cell_j = cell_j
        self.pos_rect = pos_rect

        self.image = pygame.Surface(CELL_SIZE)
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, color, (CELL_LENGTH/2, CELL_LENGTH/2), PIECE_RADIUS)

    def draw(self):
        screen.blit(self.image, self.pos_rect)

    def is_inside(self, pos):
        return self.pos_rect.collidepoint(pos)

    def go_to(self, destination):
        src_color = LIGHT_CREAM if (self.cell_i+self.cell_j)%2 == 0 else DARK_CREAM
        pygame.draw.rect(screen, src_color, self.pos_rect)

        cur_surface = pygame.Surface(GAME_SIZE)
        cur_surface.blit(screen, ORIGIN)

        dest_x, dest_y = destination
        speed = [0, 0]

        if self.pos_rect.left < dest_x:
            speed[0] = 4
        elif self.pos_rect.left > dest_x:
            speed[0] = -4

        if self.pos_rect.top < dest_y:
            speed[1] = 4
        elif self.pos_rect.top > dest_y:
            speed[1] = -4

        while self.pos_rect.left != dest_x or self.pos_rect.top != dest_y:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(-1, flush = True)
                    sys.exit()

            screen.blit(cur_surface, ORIGIN)

            self.pos_rect = self.pos_rect.move(speed)
            screen.blit(self.image, self.pos_rect)
            pygame.display.update()
