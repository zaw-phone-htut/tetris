import pygame
import sys
import colors
from game import Game

pygame.init()


title_font = pygame.font.Font(None, 40)
label_font = pygame.font.Font(None, 32)
score_surface = title_font.render("Score", True, (255, 255, 255))
level_surface = title_font.render("Level", True, (255, 255, 255))
next_surface = title_font.render("Next", True, (255, 255, 255))
game_over_surface = title_font.render("GAME OVER", True, (255, 255, 255))
score_rect = pygame.Rect(320, 55, 170, 60)
level_rect = pygame.Rect(320, 450, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)


screen = pygame.display.set_mode((500, 620))  # Set the screen resolution
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()  # Create an object for frame rate
game = Game()  # Create the game object
GAME_EVENT = pygame.USEREVENT  # Create a custom event

# Classic Tetris drop speeds in milliseconds (60 FPS)
classic_drop_speeds = [800, 720, 630, 550, 470, 380, 300, 220, 130, 100]


def get_drop_speed(level):
    if level < len(classic_drop_speeds):
        return classic_drop_speeds[level]
    else:
        return classic_drop_speeds[-1]


pygame.time.set_timer(GAME_EVENT, get_drop_speed(0))

screen_color = (33, 33, 77)

while True:  # Main Game Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Loop Break
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:  # Controls for game
            if game.game_over == True:
                if event.key == pygame.K_r:
                    game.game_over = False
                    game.reset()
                    pygame.time.set_timer(
                        GAME_EVENT, get_drop_speed(game.level))
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
                pygame.time.set_timer(GAME_EVENT, get_drop_speed(game.level))
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
                pygame.time.set_timer(GAME_EVENT, get_drop_speed(game.level))
            if event.key == pygame.K_SPACE and game.game_over == False:
                game.hard_drop()
                pygame.time.set_timer(GAME_EVENT, get_drop_speed(game.level))
        if event.type == GAME_EVENT and game.game_over == False:
            game.move_down()
            pygame.time.set_timer(GAME_EVENT, get_drop_speed(game.level))

    """ Had to declare a variable above cuz this
    lil shit will only accept a single variable """
    screen.fill(screen_color)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))
    screen.blit(level_surface, (365, 420, 50, 50))
    if game.game_over == True:
        screen.blit(game_over_surface, (322, 525, 50, 50))

    score_value_surface = title_font.render(
        str(game.score), True, (255, 255, 255))
    level_value_surface = title_font.render(
        str(game.level), True, (255, 255, 255))

    pygame.draw.rect(screen, colors.Colors().darkgrey, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(
        centerx=score_rect.centerx, centery=score_rect.centery))
    pygame.draw.rect(screen, colors.Colors().darkgrey, level_rect, 0, 10)
    screen.blit(level_value_surface, level_value_surface.get_rect(
        centerx=level_rect.centerx, centery=level_rect.centery))
    pygame.draw.rect(screen, colors.Colors().darkgrey, next_rect, 0, 10)
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)  # Setting Frame rate
