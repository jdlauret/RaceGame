import pygame
import random
import os
import time

# directories
top_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(top_dir, 'assets')
image_dir = os.path.join(assets_dir, 'images')

pygame.init()

display_width = 800
display_height = 1000

# colors values (red, green, blue)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

color_list = [
    black,
    red,
    green,
    blue
]

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

#images
car_image_path = os.path.join(image_dir, 'acura-sports-car-vertical-small.png')
car_image = pygame.image.load(car_image_path)
car_rect = car_image.get_rect()
car_center = car_rect.centerx = 25


class ImageObject:

    def __init__(self, params):
        image, x, y = params
        self.x = x
        self.y = y
        self.speed = 0
        self.image = image
        self.size = image.get_rect()
        self.width = self.size.width
        self.height = self.size.height
        self.sides()

    def sides(self):
        self.left = self.x
        self.right = self.x + self.width
        self.top = self.y
        self.bottom = self.y + self.height

    def draw(self):
        game_display.blit(self.image, (self.x, self.y))


class RectObject:
    def __init__(self, params):
        x, y, w, h, color = params
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = color
        self.sides()

    def sides(self):
        self.left = self.x
        self.right = self.x + self.width
        self.top = self.y
        self.bottom = self.y + self.height

    def draw(self):
        self.sides()
        pygame.draw.rect(game_display, self.color, [self.x, self.y, self.width, self.height])


def quit_game():
    pygame.quit()
    quit()


def blocks_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    game_display.blit(text, (0, 0))


def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    text_surf, text_rect = text_objects(text, largeText)
    text_rect.center = ((display_width/2, display_height/2))
    game_display.blit(text_surf, text_rect)

    pygame.display.update()

    time.sleep(2)

    game_loop()

def crash():
    message_display('You Crashed')


def create_obj(block_count):
    # default block parameters

    obj_list = []
    for obj_count in range(block_count):
        block_width = random.randrange(50, 100)
        block_height = random.randrange(50, 100)
        block_color = color_list[random.randrange(0, len(color_list) - 1)]
        block_x_start = random.randrange(0, display_width - block_width)
        block_y_start = random.randrange(-800, -600)
        new_block = RectObject((block_x_start, block_y_start, block_width, block_height, block_color))
        obj_list.append(new_block)
    return obj_list


def game_loop():

    # car starting position
    x = display_width * 0.45
    y = (display_height * 0.8)

    # default location change
    x_change = 0

    # Number of objects that can be on screen
    block_count = 2
    obj_list = create_obj(block_count)

    block_speed = 3
    # dodged block counter
    dodged_counter = 0

    # game loop run variable
    exit_game = False

    # game loop
    while not exit_game:

        # event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT \
                        or event.key == pygame.K_RIGHT:
                    x_change = 0

        # update car position
        x += x_change

        # create background
        game_display.fill(white)

        print(obj_list)
        # draw block
        for obj in obj_list:
            obj.draw()
            # change block location
            obj.y += block_speed

        # draw car
        car = ImageObject((car_image, x, y))
        car.draw()
        blocks_dodged(dodged_counter)

        # reset block once it leaves display
        for obj in obj_list:
            if obj.y > display_height:
                obj.x = random.randrange(0, display_width - obj.width)
                obj.y = random.randrange(-800, -600)
                obj.width = random.randrange(50, 100)
                obj.height = random.randrange(50, 100)
                dodged_counter += 1
                block_speed += 0.25


            # check for collision with block_1
            if car.top < obj.bottom and obj.top < car.bottom:
                    # print('Y Crossover')
                    if obj.left < car.left < obj.right \
                            or obj.left < car.right < obj.right:
                        # print('X Crossover')
                        crash()

        # update frame
        pygame.display.update()

        # frames per second
        clock.tick(60)


if __name__ == '__main__':
    game_loop()
