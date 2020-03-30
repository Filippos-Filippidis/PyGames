# Pygame Development
import pygame

# Size of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Candy Rush'
# Colours according to RGB codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
# Clock used to update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

class Game:

    # Typical rate of 60 equivalent to FPS
    TICK_RATE = 60

    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        # Create the window of specified size in white to display the game
        self.game_screen = pygame.display.set_mode((width, height))
        # Set the game window color to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level_speed):
        is_game_over = False
        did_win = False
        direction = 0

        player = PlayerCharacter('/Users/continuous_inputs/Documents/PyCharm/PyGames/BW_Game/Images/player.png', 415, 700, 50, 50)
        enemy = NonPlayerCharacter('/Users/continuous_inputs/Documents/PyCharm/PyGames/BW_Game/Images/enemy.png', 20, 470, 50, 50)
        treasure = GameObject('/Users/continuous_inputs/Documents/PyCharm/PyGames/BW_Game/Images/treasure.png', 415, 135, 50, 50)
        enemy.SPEED *= level_speed

        enemy1 = NonPlayerCharacter('/Users/continuous_inputs/Documents/PyCharm/PyGames/BW_Game/Images/enemy.png', self.width-40, 315, 50, 50)
        enemy1.SPEED *= level_speed

        enemy2 = NonPlayerCharacter('/Users/continuous_inputs/Documents/PyCharm/PyGames/BW_Game/Images/enemy.png', 20, 200, 50, 50)
        enemy2.SPEED *= level_speed


        # Main game loop, used to update all gameplay such as movement, check, graphics
        # Runs until is_game_over = True
        while not is_game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1
                    elif event.key ==pygame.K_DOWN:
                        direction = -1
                elif event.type ==pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                print(event)

            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image, (0,0))

            treasure.draw(self.game_screen)

            player.move(direction, self.height)
            player.draw(self.game_screen)

            enemy.move(self.width)
            enemy.draw(self.game_screen)

            if level_speed > 2:
                enemy1.move(self.width)
                enemy1.draw(self.game_screen)
            if level_speed > 4:
                enemy2.move(self.width)
                enemy2.draw(self.game_screen)


            if player.detect_collision(enemy):
                is_game_over = True
                did_win = False
                text = font.render('You Lose :(', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break
            if player.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('You Win :)', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break

            # Update all game graphics
            pygame.display.update()
            # Tick the clock to update everything within the game
            clock.tick(self.TICK_RATE)

        if did_win:
            self.run_game_loop(level_speed + 0.5)
        else:
            return

class GameObject:

    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width, height))
        self.width = width
        self.height = height
        self.x_pos = x
        self.y_pos = y

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

class PlayerCharacter(GameObject):

    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, direction, maxHeight):
        #self.y_pos += direction * SPEED
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction <0:
            self.y_pos += self.SPEED
        if self.y_pos >= maxHeight - 20:
            self.y_pos = maxHeight - 20

    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False

        return True

class NonPlayerCharacter(GameObject):

    # How many tiles the character moves per second
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # Move function will move character right once it hits the far left of the
    # screen and left once it hits the far right of the screen
    def move(self, max_width):
        if self.x_pos <= 80:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 150:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

pygame.init()
new_game = Game('/Users/continuous_inputs/Documents/PyCharm/PyGames/BW_Game/Images/background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)

# Quit pygame and the program
pygame.quit()
quit()

