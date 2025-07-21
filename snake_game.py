import pygame
import random
import numpy as np
from enum import Enum

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGameAI:
    def __init__(self, w=640, h=480, block_size=20, vision_radius=3):
        self.w = w
        self.h = h
        self.block_size = block_size
        self.vision_radius = vision_radius
        
        # init display - créer une surface au lieu d'une fenêtre
        self.display = pygame.Surface((self.w, self.h))
        self.clock = pygame.time.Clock()
        
        # init colors
        self.WHITE = (255, 255, 255)
        self.RED = (200, 0, 0)
        self.BLUE1 = (0, 0, 255)
        self.BLUE2 = (0, 100, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        
        self.reset()
        
    def reset(self):
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = [self.w//2, self.h//2]
        self.snake = [self.head,
                      [self.head[0]-self.block_size, self.head[1]],
                      [self.head[0]-(2*self.block_size), self.head[1]]]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        
    def _place_food(self):
        x = random.randint(0, (self.w-self.block_size)//self.block_size)*self.block_size
        y = random.randint(0, (self.h-self.block_size)//self.block_size)*self.block_size
        self.food = [x, y]
        if self.food in self.snake:
            self._place_food()
            
    def play_step(self, action):
        self.frame_iteration += 1
        
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(60)
        
        # 6. return game over and score
        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt[0] > self.w - self.block_size or pt[0] < 0 or pt[1] > self.h - self.block_size or pt[1] < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(self.BLACK)
        
        # Dessiner le snake avec un design moderne
        for i, pt in enumerate(self.snake):
            if i == 0:  # Tête du snake
                # Tête avec gradient et effet glow
                head_color = (0, 255, 100)  # Vert brillant
                shadow_color = (0, 150, 50)  # Ombre
                
                # Ombre de la tête
                pygame.draw.rect(self.display, shadow_color, 
                               pygame.Rect(pt[0]+2, pt[1]+2, self.block_size, self.block_size))
                # Tête principale
                pygame.draw.rect(self.display, head_color, 
                               pygame.Rect(pt[0], pt[1], self.block_size, self.block_size))
                # Highlight sur la tête
                pygame.draw.rect(self.display, (150, 255, 200), 
                               pygame.Rect(pt[0]+3, pt[1]+3, self.block_size-6, self.block_size-6))
                
                # Yeux du snake
                eye_size = 3
                pygame.draw.circle(self.display, self.WHITE, 
                                 (pt[0] + 6, pt[1] + 6), eye_size)
                pygame.draw.circle(self.display, self.WHITE, 
                                 (pt[0] + 14, pt[1] + 6), eye_size)
                pygame.draw.circle(self.display, self.BLACK, 
                                 (pt[0] + 6, pt[1] + 6), 1)
                pygame.draw.circle(self.display, self.BLACK, 
                                 (pt[0] + 14, pt[1] + 6), 1)
            else:  # Corps du snake
                # Gradient du corps selon la position
                fade = max(0.3, 1 - (i * 0.1))  # Effet de fondu
                body_color = (int(0 * fade), int(200 * fade), int(255 * fade))
                shadow_color = (int(0 * fade), int(100 * fade), int(150 * fade))
                
                # Ombre du corps
                pygame.draw.rect(self.display, shadow_color, 
                               pygame.Rect(pt[0]+1, pt[1]+1, self.block_size, self.block_size))
                # Corps principal
                pygame.draw.rect(self.display, body_color, 
                               pygame.Rect(pt[0], pt[1], self.block_size, self.block_size))
                # Highlight intérieur
                pygame.draw.rect(self.display, (int(100 * fade), int(220 * fade), int(255 * fade)), 
                               pygame.Rect(pt[0]+2, pt[1]+2, self.block_size-4, self.block_size-4))
        
        # Nourriture avec effet brillant
        food_colors = [(255, 100, 100), (255, 150, 150), (255, 200, 200)]
        
        # Animation de la nourriture (effet pulsation)
        import time
        pulse = abs(int(time.time() * 10) % 6 - 3)  # Oscillation entre 0 et 3
        
        # Ombre de la nourriture
        pygame.draw.rect(self.display, (150, 50, 50), 
                        pygame.Rect(self.food[0]+2, self.food[1]+2, self.block_size, self.block_size))
        
        # Nourriture principale avec pulsation
        pygame.draw.rect(self.display, food_colors[0], 
                        pygame.Rect(self.food[0], self.food[1], self.block_size, self.block_size))
        
        # Effet de brillance
        pygame.draw.rect(self.display, food_colors[1], 
                        pygame.Rect(self.food[0]+2+pulse, self.food[1]+2+pulse, 
                                   self.block_size-4-pulse*2, self.block_size-4-pulse*2))
        
        # Petit highlight central
        pygame.draw.rect(self.display, food_colors[2], 
                        pygame.Rect(self.food[0]+6, self.food[1]+6, 8, 8))
        
        # Score avec style
        text = pygame.font.Font(None, 25).render("Score: " + str(self.score), True, self.WHITE)
        # Ombre du texte
        shadow_text = pygame.font.Font(None, 25).render("Score: " + str(self.score), True, (100, 100, 100))
        self.display.blit(shadow_text, [2, 2])
        self.display.blit(text, [0, 0])
        
    def _move(self, action):
        # [straight, right, left]
        
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head[0]
        y = self.head[1]
        if self.direction == Direction.RIGHT:
            x += self.block_size
        elif self.direction == Direction.LEFT:
            x -= self.block_size
        elif self.direction == Direction.DOWN:
            y += self.block_size
        elif self.direction == Direction.UP:
            y -= self.block_size
            
        self.head = [x, y]
    
    def get_state(self):
        head = self.snake[0]
        point_l = [head[0] - self.block_size, head[1]]
        point_r = [head[0] + self.block_size, head[1]]
        point_u = [head[0], head[1] - self.block_size]
        point_d = [head[0], head[1] + self.block_size]
        
        dir_l = self.direction == Direction.LEFT
        dir_r = self.direction == Direction.RIGHT
        dir_u = self.direction == Direction.UP
        dir_d = self.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and self.is_collision(point_r)) or 
            (dir_l and self.is_collision(point_l)) or 
            (dir_u and self.is_collision(point_u)) or 
            (dir_d and self.is_collision(point_d)),

            # Danger right
            (dir_u and self.is_collision(point_r)) or 
            (dir_d and self.is_collision(point_l)) or 
            (dir_l and self.is_collision(point_u)) or 
            (dir_r and self.is_collision(point_d)),

            # Danger left
            (dir_d and self.is_collision(point_r)) or 
            (dir_u and self.is_collision(point_l)) or 
            (dir_r and self.is_collision(point_u)) or 
            (dir_l and self.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            self.food[0] < self.head[0],  # food left
            self.food[0] > self.head[0],  # food right
            self.food[1] < self.head[1],  # food up
            self.food[1] > self.head[1]   # food down
            ]

        return np.array(state, dtype=int) 