import pygame
import os
import random
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/character", "run1.png")),
           pygame.image.load(os.path.join("Assets/character", "run2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/character", "jump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/character", "slide.png")),
           pygame.image.load(os.path.join("Assets/character", "slide.png"))]

PUMPKIN = [pygame.image.load(os.path.join("Assets/monsters", "pumpkin.png")),
           pygame.image.load(os.path.join("Assets/monsters", "pumpkin.png")),
           pygame.image.load(os.path.join("Assets/monsters", "pumpkin.png"))]
THOMBSTONE = [pygame.image.load(os.path.join("Assets/monsters", "thombstone.png")),
              pygame.image.load(os.path.join("Assets/monsters", "thombstone.png")),
              pygame.image.load(os.path.join("Assets/monsters", "thombstone.png"))]

WITCH = [pygame.image.load(os.path.join("Assets/monsters", "witch1.png")),
         pygame.image.load(os.path.join("Assets/monsters", "witch2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

class girl:
    X_POS = 80
    Y_POS = 280
    Y_POS_DUCK = 330
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.girl_duck = False
        self.girl_run = True
        self.girl_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.girl_react = self.image.get_rect()
        self.girl_react.x = self.X_POS
        self.girl_react.y = self.Y_POS

    def update(self, userInput):
        if self.girl_duck:
            self.duck()
        if self.girl_run:
            self.run()
        if self.girl_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.girl_jump:
            self.girl_duck = False
            self.girl_run = False
            self.girl_jump = True
        elif userInput[pygame.K_DOWN] and not self.girl_jump:
            self.girl_duck = True
            self.girl_run = False
            self.girl_jump = False
        elif not (self.girl_jump or userInput[pygame.K_DOWN]):
            self.girl_duck = False
            self.girl_run = True
            self.girl_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.girl_react = self.image.get_rect()
        self.girl_react.x = self.X_POS
        self.girl_react.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.girl_react = self.image.get_rect()
        self.girl_react.x = self.X_POS
        self.girl_react.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.girl_jump:
            self.girl_react.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.girl_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.girl_react.x, self.girl_react.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Pumpkin(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 280


class Thombstone(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 280


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 195
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


# Add this function to display the jumpscare
def jumpscare():
    jumpscare_image = pygame.image.load(os.path.join("Assets/character", "dead.jpg"))
    jumpscare_rect = jumpscare_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(jumpscare_image, jumpscare_rect)
    pygame.display.update()
    pygame.time.delay(3000)  # Display the jumpscare for 3 seconds
    return


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = girl()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((0, 0, 0))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(Pumpkin(PUMPKIN))
            elif random.randint(0, 2) == 1:
                obstacles.append(Thombstone(THOMBSTONE))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(WITCH))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.girl_react.colliderect(obstacle.rect):
                jumpscare()
                death_count += 1
                run = False  # Exit the main loop and display the restart menu

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()

    # Restart menu
    menu(death_count)


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((0, 0, 0))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (255, 255, 255))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (255, 255, 255))
            score_text = font.render("Your Score: " + str(points), True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            SCREEN.blit(score_text, score_rect)

        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(text, text_rect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)