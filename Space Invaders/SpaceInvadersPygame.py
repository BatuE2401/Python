import pygame
from pygame.locals import *
import sys
import random

GREEN = (52, 255, 0)
WHITE = (255, 255, 255)

class Space_Invaders:
    def __init__(self):
        self.score = 0
        self.lives = 2

        #Set up of the screen
        pygame.font.init()
        self.small_font = pygame.font.Font("imports/space_invaders.ttf", 15)
        self.big_font = pygame.font.Font("imports/space_invaders.ttf", 100)
        self.screen = pygame.display.set_mode((800,600))

        self.animation_frame = 0

        # A variable to alternate the direction the enemies move towards.
        # 1 is for right, -1 is for left
        self.direction = 1


        # A variable for the player's bullet. There can only be one player's
        # bullet at one time in this game. This limits the firing rate.
        self.bullet = None
        # A variable for the enemies bullets.
        self.bullets = []
        self.bullet_speed = 15


        ### Enemies:
        #import image files for different types of enemies:
        self.enemy_sprites = {
                1:[pygame.image.load("imports/a1_0.png").convert(),
                    pygame.image.load("imports/a1_1.png").convert()],
                2:[pygame.image.load("imports/a2_0.png").convert(),
                    pygame.image.load("imports/a2_1.png").convert()],
                3:[pygame.image.load("imports/a3_0.png").convert(),
                    pygame.image.load("imports/a3_1.png").convert()]
        }
        #Place the enemies on a rectangular coordinate system on the board
        enemy_wave = [
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2],
            [3,3,3,3,3,3,3,3,3,3],
            [3,3,3,3,3,3,3,3,3,3],
        ]
        self.enemies = []
        start_X = 50
        start_Y = 50
        for (row, enemy_lane) in enumerate(enemy_wave):
            for (column, enemy_type) in enumerate(enemy_lane):
                self.enemies.append(
                    (enemy_type,
                     pygame.Rect(start_X * column, start_Y * row + 60, 35, 35)
                    )
                )

        # A variable to limit the rate of movement of enemies
        self.last_enemy_move = 0
        # Variables to control the speed of enemies movement
        self.enemy_speed_x = 20
        self.enemy_speed_y = 20


        ### The Barriers:
        #Barrier Design
        barrier_design = [
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,1,1,1,1,1,0,0,0],
                [0,0,1,1,1,1,1,1,1,0,0],
                [0,1,1,1,1,1,1,1,1,1,0],
                [1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,0,0,0,1,1,1,1],
                [1,1,1,0,0,0,0,0,1,1,1],
                [1,1,1,0,0,0,0,0,1,1,1]
        ]
        #Place the barrier blocks at the lower end of the screen
        barrier_X = 50
        barrier_Y = 400
        space = 100
        self.barrier_particles = []
        for offset in range(1,5):
            for row in barrier_design:
                for particule in row:
                    if particule != 0:
                        x = barrier_X + (space * offset) - 15
                        y = barrier_Y
                        self.barrier_particles.append(pygame.Rect(x, y, 8,6))
                    barrier_X += 8
                barrier_X = 50 * offset
                barrier_Y += 6
            barrier_Y = 400


        ### The Player:
        #import image of player:
        self.player = pygame.image.load("imports/shooter.png").convert() #import image of player
        self.player_X = 400 -  (self.player.get_width()/2)
        self.player_Y = 550



    def move_enemies_down(self):
        for (enemy_type, enemy_rectangle) in self.enemies:
            enemy_rectangle.y += self.enemy_speed_y

    def player_action_right(self):
        if self.player_X < 800 - self.player.get_width():
            self.player_X += 5 #move right 5 pixels
    def player_action_left(self):
        if self.player_X > 0:
            self.player_X -= 5 #move left 5 pixels
    def player_action_fire(self):
        if not self.bullet:
            gun_barrel_X = self.player_X + (self.player.get_width() / 2) - 2
            gun_barrel_Y = self.player_Y - 15
            self.bullet = pygame.Rect(gun_barrel_X, gun_barrel_Y, 5, 10)

    def xxx(self): #Assign movement to player by key-clicks
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            self.player_action_right()
        elif key[K_LEFT]:
            self.player_action_left()
        if key[K_SPACE]:
            self.player_action_fire()

    def player_rect(self):
        x = self.player_X
        y = self.player_Y
        w = self.player.get_width()
        h = self.player.get_height()
        return pygame.Rect(x, y, w, h)

    def bullet_update(self):
        for i, enemy in enumerate(self.enemies):
            enemy = enemy[1]
            if self.bullet and enemy.colliderect(self.bullet):
                #colliderect checks if two rectangls overalep
                self.enemies.pop(i) #remove enemy from enemies list using pop function
                self.bullet = None #hide bullet
                self.score += 100 #score 100 points for every kill

        #make bullets move up whe fired by changing their y location
        if self.bullet:
            self.bullet.y -= self.bullet_speed
            if self.bullet.y < 0:
                self.bullet = None #bullets disappear when reach the end of screen
            if self.bullet:
                barrier_collision = self.bullet.collidelist(self.barrier_particles)
                if barrier_collision != -1:
                    self.barrier_particles.pop(barrier_collision)
                    self.bullet = None
                    self.score -= 10


        # Make enemy bullets move down
        for bullet in self.bullets:
            bullet.y += self.bullet_speed
            if bullet.y > 600:
                self.bullets.remove(bullet)
            # when bullet hits player, remove life and reset
            if bullet.colliderect(self.player_rect()):
                self.lives -= 1
                self.bullets.remove(bullet)
                self.reset_player()
            barrier_collision = bullet.collidelist(self.barrier_particles)
            if barrier_collision != -1: # when there is a collision
                self.barrier_particles.pop(barrier_collision)
                self.bullets.remove(bullet)
                self.score += 10


    def enemy_AI(self, enemy):
        (enemy_type, enemy_rect) = enemy
        enemy_rect.x += self.enemy_speed_x * self.direction
        chance = random.randint(0,1000) #Generate a random number between 0 and 1000
        #if player is NOT underneath a barrier:
        ranges = [
              range(0, 135),
              range (215 - self.player.get_width(), 285),
              range (365 - self.player.get_width(), 435),
              range (515 - self.player.get_width(), 585),
              range (665 - self.player.get_width(), 800),
        ]
        player_unprotected = False
        for r in ranges:
            if self.player_X in r:
                player_unprotected = True
        if player_unprotected:
            #and if this random number is greater than 960 (4% chance)
            if chance > 960:
                #fire enemy bullet
                self.bullets.append(pygame.Rect(enemy_rect.x, enemy_rect.y, 5, 10))
                self.score += 5
        else: #fire even if player is protected
            if chance > 990:
                #fire enemy bullet if random number greater than 990 (1% chance)
                self.bullets.append(pygame.Rect(enemy_rect.x, enemy_rect.y, 5, 10))
                self.score += 5


    def cycle_animation_frame(self):
        if self.animation_frame == 0:
            self.animation_frame = 1
        elif self.animation_frame == 1:
            self.animation_frame = 0



    def enemy_update(self):
        if self.last_enemy_move > 0:
            self.last_enemy_move -= 1
        else:
            self.last_enemy_move = 24
            self.cycle_animation_frame()

            # Check if the aliens are on the side and move accordingly
            bump_on_side = False
            for (enemy_type, enemy_rect) in self.enemies:
                if enemy_rect.x >= 750 or enemy_rect.x < 0:
                    bump_on_side = True
            if bump_on_side:
                self.direction = -1 * self.direction
                self.move_enemies_down()

            for (enemy_type, enemy_rect) in self.enemies:
                if enemy_rect.colliderect(self.player_rect()):
                    self.lives -= 1
                    self.reset_player()
                enemy_rect.x += self.enemy_speed_x * self.direction

            for enemy in self.enemies:
                self.enemy_AI(enemy)


    def reset_player(self): #puts player back in the middle of the screen
        self.player_X = 400 - (self.player.get_width()/2)

    def run(self):
        while True:

            t0 = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == QUIT: #Exits the game
                    sys.exit()

            #Game Play:
            if self.lives > 0: #if you still have lives left update all game elements
                self.bullet_update()
                self.enemy_update()
                self.player_update()



            #Drawing: blank the screen, draw everything
            self.screen.fill((0,0,0))
            #Draw the enemies onto the board
            for enemy in self.enemies:
                enemy_sprite = pygame.transform.scale(
                        self.enemy_sprites[enemy[0]][self.animation_frame],
                        (35,35)
                )
                self.screen.blit(enemy_sprite, (enemy[1].x, enemy[1].y))
            #Draw the player on the board
            self.screen.blit(self.player, (self.player_X, self.player_Y))
            # Draw bullets
            if self.bullet:
                pygame.draw.rect(self.screen, GREEN, self.bullet)
            for bullet in self.bullets:
                pygame.draw.rect(self.screen, WHITE, bullet)
            for i in self.barrier_particles:
                pygame.draw.rect(self.screen, GREEN, i)
            #Lives on screen
            lives_text = "Lives: {}".format(self.lives)
            lives_message = self.small_font.render(lives_text, -1, WHITE)
            self.screen.blit(lives_message, (20, 10))
            #Display Score
            score_text = "Score: {}".format(self.score)
            score_message = self.small_font.render(score_text, -1, WHITE)
            self.screen.blit(score_message, (400, 10))
            #Draw winning message if there are no enemies
            if self.enemies == []: #if no more enemies left
                win_message = self.big_font.render("You Win!", -1, GREEN)
                self.screen.blit(win_message, (100, 200))
            if self.lives == 0: #if no more lives left
                lose_message = self.big_font.render("You Lose!", -1, GREEN)
                self.screen.blit(lose_message, (100, 200))

            pygame.display.flip() #Update screen


            # wait for what is left of 40ms
            t1 = pygame.time.get_ticks()
            pygame.time.wait(40 - (t1 - t0))



if __name__ == "__main__":
    Space_Invaders().run()
