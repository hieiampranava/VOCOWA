import pygame, pygame.locals
from PIL import Image

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# in cm, using standard Cartesian Coordinates
botY = 60
botX = 60
size = [800, 600]


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, [(size[0] - botX) / 2, (size[1] - botY) / 2, botX, botY])
    pygame.display.update()

    done = False
    mouse_pressed = False
    while not done:

        # This will limit the loop to 10 times per sec
        # comment this and program will use all CPU it can
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False
            elif event.type == pygame.MOUSEMOTION and mouse_pressed:
                pygame.draw.circle(screen, BLACK, event.pos, 2)

        # to update screen. This must happen after all commands
        pygame.display.flip()

    # saving two images, with and without bot
    pygame.image.save(screen, 'img.jpg')
    pygame.draw.rect(screen, WHITE, [(size[0] - botX) / 2, (size[1] - botY) / 2, botX, botY])
    pygame.display.update()
    pygame.image.save(screen, 'map.jpg')  # we'll use this for calculations
    im = Image.open('map.jpg')
    im = im.convert('1')
    im.save('map.jpg')  # saving it as  pure BW

    # being IDLE friendly
    pygame.quit()


if __name__ == '__main__':
    main()
