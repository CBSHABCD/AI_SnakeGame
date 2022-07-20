import pygame
import os
import random
import numpy as np
import pickle

FPS = 10
SCREEN_SIZE = 40
PIXEL_SIZE = 20
LINE_WIDTH = 1

DIRECTIONS = np.array([
    (0, -1),  # UP
    (1, 0),  # RIGHT
    (0, 1),  # DOWN
    (-1, 0)  # LEFT
])


class Snake():
    snake, fruit = None, None

    def __init__(self, s, genome1, genome2):
        # P1(AI)
        self.genome1 = genome1
        self.score1 = 0
        self.snake1 = np.array([[15, 26], [15, 27], [15, 28], [15, 29]])
        self.direction1 = 0  # UP
        self.fitness1 = 0.
        self.last_dist1 = np.inf
        self.last_fruit_time1 = 0
        # p2
        self.genome2 = genome2
        self.score2 = 0
        self.snake2 = np.array([[25, 26], [25, 27], [25, 28], [25, 29]])
        self.direction2 = 0  # UP
        self.fitness2 = 0.
        self.last_dist2 = np.inf
        self.last_fruit_time2 = 0

        self.s = s
        self.timer = 0
        self.place_fruit()

    def place_fruit(self, coord=None):
        if coord:
            self.fruit = np.array(coord)
            return

        while True:
            x = random.randint(0, SCREEN_SIZE-1)
            y = random.randint(0, SCREEN_SIZE-1)
            if list([x, y]) not in self.snake1.tolist() and list([x, y]) not in self.snake2.tolist():
                break
        self.fruit = np.array([x, y])

    def step1(self, direction):
        old_head = self.snake1[0]
        movement = DIRECTIONS[direction]
        new_head = old_head + movement
        if (new_head[0] < 0 or
                new_head[0] >= SCREEN_SIZE or
                new_head[1] < 0 or
                new_head[1] >= SCREEN_SIZE
                ) :
            print('p1 out of box')
            return False

        if new_head.tolist() in self.snake1.tolist():
            # self.fitness1 -= FPS/2
            print('p1 suicide')
            return False
        
        if new_head.tolist() in self.snake2.tolist():
            # self.fitness1 -= FPS/2
            print('p1 hit p2')
            return False

        # eat fruit
        if all(new_head == self.fruit):
            self.last_fruit_time1 = self.timer
            self.score1 += 1
            self.fitness1 += 10
            self.place_fruit()
        else:
            tail = self.snake1[-1]
            self.snake1 = self.snake1[:-1, :]

        self.snake1 = np.concatenate([[new_head], self.snake1], axis=0)
        return True

    def step2(self, direction):
        old_head = self.snake2[0]
        movement = DIRECTIONS[direction]
        new_head = old_head + movement
        if (new_head[0] < 0 or
                new_head[0] >= SCREEN_SIZE or
                new_head[1] < 0 or
                new_head[1] >= SCREEN_SIZE
                ) :
            print('p2 out of box')
            return False

        if new_head.tolist() in self.snake2.tolist():
            # self.fitness1 -= FPS/2
            print('p2 suicide')
            return False
        
        if new_head.tolist() in self.snake1.tolist():
            # self.fitness1 -= FPS/2
            print('p2 hit p1')
            return False

        # eat fruit
        if all(new_head == self.fruit):
            self.last_fruit_time2 = self.timer
            self.score2 += 1
            self.fitness2 += 10
            self.place_fruit()
        else:
            tail = self.snake2[-1]
            self.snake2 = self.snake2[:-1, :]

        self.snake2 = np.concatenate([[new_head], self.snake2], axis=0)
        return True

    def get_inputs1(self):
        head = self.snake1[0]
        result = [1., 1., 1., 0., 0., 0.]

        # check forward, left, right
        possible_dirs = [
            DIRECTIONS[self.direction1],  # straight forward
            DIRECTIONS[(self.direction1 + 3) % 4],  # left
            DIRECTIONS[(self.direction1 + 1) % 4]  # right
        ]

        # 0 - 1 ... danger - safe
        for i, p_dir in enumerate(possible_dirs):
            # sensor range = 5
            for j in range(5):
                guess_head = head + p_dir * (j + 1)
                if (
                    guess_head[0] < 0 or
                    guess_head[0] >= SCREEN_SIZE or
                    guess_head[1] < 0 or
                    guess_head[1] >= SCREEN_SIZE or
                    guess_head.tolist() in self.snake1.tolist() or
                    guess_head.tolist() in self.snake2.tolist()
                ):
                    result[i] = j * 0.2
                    break

        # finding fruit
        # heading straight forward to fruit
        if np.any(head == self.fruit) and np.sum(head * possible_dirs[0]) <= np.sum(self.fruit * possible_dirs[0]):
            result[3] = 1
        # fruit is on the left side
        if np.sum(head * possible_dirs[1]) < np.sum(self.fruit * possible_dirs[1]):
            result[4] = 1
        # fruit is on the right side
        # if np.sum(head * possible_dirs[2]) < np.sum(self.fruit * possible_dirs[2]):
        else:
            result[5] = 1

        return np.array(result)
    
    def get_inputs2(self):
        head = self.snake2[0]
        result = [1., 1., 1., 0., 0., 0.]

        # check forward, left, right
        possible_dirs = [
            DIRECTIONS[self.direction2],  # straight forward
            DIRECTIONS[(self.direction2 + 3) % 4],  # left
            DIRECTIONS[(self.direction2 + 1) % 4]  # right
        ]

        # 0 - 1 ... danger - safe
        for i, p_dir in enumerate(possible_dirs):
            # sensor range = 5
            for j in range(5):
                guess_head = head + p_dir * (j + 1)
                if (
                    guess_head[0] < 0 or
                    guess_head[0] >= SCREEN_SIZE or
                    guess_head[1] < 0 or
                    guess_head[1] >= SCREEN_SIZE or
                    guess_head.tolist() in self.snake2.tolist()
                ):
                    result[i] = j * 0.2
                    break

        # finding fruit
        # heading straight forward to fruit
        if np.any(head == self.fruit) and np.sum(head * possible_dirs[0]) <= np.sum(self.fruit * possible_dirs[0]):
            result[3] = 1
        # fruit is on the left side
        if np.sum(head * possible_dirs[1]) < np.sum(self.fruit * possible_dirs[1]):
            result[4] = 1
        # fruit is on the right side
        # if np.sum(head * possible_dirs[2]) < np.sum(self.fruit * possible_dirs[2]):
        else:
            result[5] = 1

        return np.array(result)

    def run(self):
        self.fitness1 = 0
        self.fitness2 = 0

        prev_key = pygame.K_UP

        font = pygame.font.Font('NanumBarunGothic.ttf', 20)
        font.set_bold(True)
        appleimage = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        appleimage.fill((0, 255, 0))
        img = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        img.fill((255, 0, 0))
        clock = pygame.time.Clock()

        while True:
            self.timer += 0.1
            if __name__ != '__main__':
                if self.fitness1 < -FPS/2 or self.timer - self.last_fruit_time1 > 0.1 * FPS * 5:
                    # self.fitness1 -= FPS/2
                    print('Terminate!')
                    break
                # if self.fitness2 < -FPS/2 or self.timer - self.last_fruit_time2 > 0.1 * FPS * 5:
                #     # self.fitness1 -= FPS/2
                #     print('Terminate!')
                #     break

            clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.KEYDOWN:
                    # QUIT
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    # PAUSE
                    if e.key == pygame.K_SPACE:
                        pause = True
                        while pause:
                            for ee in pygame.event.get():
                                if ee.type == pygame.QUIT:
                                    pygame.quit()
                                elif ee.type == pygame.KEYDOWN:
                                    if ee.key == pygame.K_SPACE:
                                        pause = False
                    if __name__ == '__main__':
                        # CONTROLLER
                        if prev_key != pygame.K_DOWN and e.key == pygame.K_UP:
                            self.direction2 = 0
                            prev_key = e.key
                        elif prev_key != pygame.K_LEFT and e.key == pygame.K_RIGHT:
                            self.direction2 = 1
                            prev_key = e.key
                        elif prev_key != pygame.K_UP and e.key == pygame.K_DOWN:
                            self.direction2 = 2
                            prev_key = e.key
                        elif prev_key != pygame.K_RIGHT and e.key == pygame.K_LEFT:
                            self.direction2 = 3
                            prev_key = e.key

            # action
            #p1    
            inputs1 = self.get_inputs1()
            outputs1 = self.genome1.forward(inputs1)
            outputs1 = np.argmax(outputs1)

            if outputs1 == 0:  # straight
                pass
            elif outputs1 == 1:  # left
                self.direction1 = (self.direction1 + 3) % 4
            elif outputs1 == 2:  # right
                self.direction1 = (self.direction1 + 1) % 4
                
            if __name__ != '__main__':
                #p2
                inputs2 = self.get_inputs2()
                outputs2 = self.genome2.forward(inputs2)
                outputs2 = np.argmax(outputs2)

                if outputs2 == 0:  # straight
                    pass
                elif outputs2 == 1:  # left
                    self.direction2 = (self.direction2 + 3) % 4
                elif outputs2 == 2:  # right
                    self.direction2 = (self.direction2 + 1) % 4
            #p1
            if not self.step1(self.direction1):
                break
            #p2
            if not self.step2(self.direction2):
                break
            
            # compute fitness
            #p1
            current_dist1 = np.linalg.norm(self.snake1[0] - self.fruit)
            if self.last_dist1 > current_dist1:
                self.fitness1 += 1.
            else:
                self.fitness1 -= 1.5
            self.last_dist1 = current_dist1
            #p2
            current_dist2 = np.linalg.norm(self.snake2[0] - self.fruit)
            if self.last_dist2 > current_dist2:
                self.fitness2 += 1.
            else:
                self.fitness2 -= 1.5
            self.last_dist2 = current_dist2

            self.s.fill((0, 0, 0))
            pygame.draw.rect(self.s, (255, 255, 255), [
                             0, 0, SCREEN_SIZE*PIXEL_SIZE, LINE_WIDTH])
            pygame.draw.rect(self.s, (255, 255, 255), [
                             0, SCREEN_SIZE*PIXEL_SIZE-LINE_WIDTH, SCREEN_SIZE*PIXEL_SIZE, LINE_WIDTH])
            pygame.draw.rect(self.s, (255, 255, 255), [
                             0, 0, LINE_WIDTH, SCREEN_SIZE*PIXEL_SIZE])
            pygame.draw.rect(self.s, (255, 255, 255), [
                             SCREEN_SIZE*PIXEL_SIZE-LINE_WIDTH, 0, LINE_WIDTH, SCREEN_SIZE*PIXEL_SIZE+LINE_WIDTH])
            #p1
            for bit1 in self.snake1:
                self.s.blit(img, (bit1[0] * PIXEL_SIZE, bit1[1] * PIXEL_SIZE))
            #p2
            for bit2 in self.snake2:
                self.s.blit(img, (bit2[0] * PIXEL_SIZE, bit2[1] * PIXEL_SIZE))
            #fruit
            self.s.blit(
                appleimage, (self.fruit[0] * PIXEL_SIZE, self.fruit[1] * PIXEL_SIZE))
            #p1            
            score_ts1 = font.render(str(self.score1), False, (255, 255, 255))
            self.s.blit(score_ts1, (5, 5))
            #p2            
            score_ts2 = font.render(str(self.score2), False, (255, 255, 255))
            self.s.blit(score_ts1, (35, 5))
            
            pygame.display.update()

        return self.fitness1, self.score1


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    s = pygame.display.set_mode(
        (SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
    pygame.display.set_caption('Snake')

    with open('Gen#12_Fit-884.0.p', 'rb') as file:
        GENOME = pickle.load(file)

    while True:
        # snake = Snake(s, genome=GENOME)
        snake = Snake(s,genome1=GENOME ,genome2=None)
        fitness, score = snake.run()

        print('Fitness: %s, Score: %s' % (fitness, score))
