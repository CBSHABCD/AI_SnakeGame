import pygame
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
network = []


class Snake():
    def __init__(self, s):
        # P1(AI)
        with open('#Gen#25_Fit-1138.5.p', 'rb') as file:
            GENOME = pickle.load(file)
        self.genome1 = GENOME
        self.score1 = 0
        self.snake1 = np.array([[15, 26], [15, 27], [15, 28], [15, 29]])
        self.direction1 = 0  # UP
        self.fitness1 = 0.
        self.last_dist1 = np.inf
        self.last_fruit_time1 = 0
        # p2
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
            ):
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
            ):
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

    def message(self, msg, color, xy):
        font = pygame.font.Font('NanumBarunGothic.ttf', 40)
        font.set_bold(True)
        mesg = font.render(msg, True, color)
        s.blit(mesg, xy)

    def run(self):
        self.fitness1 = 0
        self.fitness2 = 0

        prev_key = pygame.K_UP

        font = pygame.font.Font('NanumBarunGothic.ttf', 40)
        time_font = pygame.font.Font('NanumBarunGothic.ttf', 30)
        font.set_bold(True)
        appleimage = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        appleimage.fill((0, 255, 0))
        img1 = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        img1.fill((255, 255, 255))
        img2 = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        img2.fill((255, 0, 0))
        clock = pygame.time.Clock()

        while True:
            self.timer += 0.1
            if self.timer > 60:
                msg1 = "AI : Human"
                msg2 = f"{self.score1} : {self.score2}"
                msg3 = "AI Win"
                msg4 = "Human Win"
                msg5 = "Draw"
                msg6 = "Press C to restart"
                msg7 = "Press ESC to quit"
                s.fill((0, 0, 0))
                if self.score1 > self.score2:
                    print("AI win")
                    self.message(msg1, (255, 255, 255), (290, 250))
                    self.message(msg2, (255, 255, 255), (290, 300))
                    self.message(msg3, (255, 255, 255), (290, 350))
                    self.message(msg6, (255, 255, 255), (210, 420))
                    self.message(msg7, (255, 255, 255), (210, 480))

                elif self.score1 < self.score2:
                    print("Human win")
                    self.message(msg1, (255, 255, 255), (290, 250))
                    self.message(msg2, (255, 255, 255), (290, 300))
                    self.message(msg4, (255, 255, 255), (290, 350))
                    self.message(msg6, (255, 255, 255), (210, 420))
                    self.message(msg7, (255, 255, 255), (210, 480))

                else:
                    print("Draw")
                    self.message(msg1, (255, 255, 255), (290, 250))
                    self.message(msg2, (255, 255, 255), (290, 300))
                    self.message(msg5, (255, 255, 255), (290, 350))
                    self.message(msg6, (255, 255, 255), (210, 420))
                    self.message(msg7, (255, 255, 255), (210, 480))

                while True:
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_c:
                                self.score1 = 0
                                self.snake1 = np.array(
                                    [[15, 26], [15, 27], [15, 28], [15, 29]])
                                self.direction1 = 0  # UP
                                self.fitness1 = 0.
                                self.last_dist1 = np.inf
                                self.last_fruit_time1 = 0
                                # p2
                                self.score2 = 0
                                self.snake2 = np.array(
                                    [[25, 26], [25, 27], [25, 28], [25, 29]])
                                self.direction2 = 0  # UP
                                self.fitness2 = 0.
                                self.last_dist2 = np.inf
                                self.last_fruit_time2 = 0
                                self.timer = 0
                                self.run()
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                exit()
            clock.tick(FPS)

            # action
            # p1
            inputs1 = self.get_inputs1()
            outputs1 = self.genome1.forward(inputs1)

            outputs1 = np.argmax(outputs1)

            if outputs1 == 0:  # straight
                pass
            elif outputs1 == 1:  # left
                self.direction1 = (self.direction1 + 3) % 4
            elif outputs1 == 2:  # right
                self.direction1 = (self.direction1 + 1) % 4

            # p1
            if not self.step1(self.direction1):
                # break
                self.snake1 = np.array(
                    [[15, 26], [15, 27], [15, 28], [15, 29]])
                self.score1 -= 1
                self.direction1 = 0  # UP

            # p2
            if not self.step2(self.direction2):
                # break
                self.snake2 = np.array(
                    [[25, 26], [25, 27], [25, 28], [25, 29]])
                self.score2 -= 1
                self.direction2 = 0  # UP
                prev_key = pygame.K_UP

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.KEYDOWN:

                    # PAUSE
                    if e.key == pygame.K_SPACE:
                        pause = True
                        while pause:
                            for ee in pygame.event.get():
                                if ee.type == pygame.QUIT:
                                    pygame.quit()
                                elif ee.type == pygame.KEYDOWN:
                                    # QUIT
                                    if ee.key == pygame.K_ESCAPE:
                                        pygame.quit()
                                        exit()
                                    if ee.key == pygame.K_SPACE:
                                        pause = False
                                    if ee.key == pygame.K_c:
                                        self.score1 = 0
                                        self.snake1 = np.array(
                                            [[15, 26], [15, 27], [15, 28], [15, 29]])
                                        self.direction1 = 0  # UP
                                        self.fitness1 = 0.
                                        self.last_dist1 = np.inf
                                        self.last_fruit_time1 = 0
                                        # p2
                                        self.score2 = 0
                                        self.snake2 = np.array(
                                            [[25, 26], [25, 27], [25, 28], [25, 29]])
                                        self.direction2 = 0  # UP
                                        self.fitness2 = 0.
                                        self.last_dist2 = np.inf
                                        self.last_fruit_time2 = 0
                                        self.timer = 0
                                        self.run()
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

            # compute fitness
            # p1
            current_dist1 = np.linalg.norm(self.snake1[0] - self.fruit)
            if self.last_dist1 > current_dist1:
                self.fitness1 += 1.
            else:
                self.fitness1 -= 1.5
            self.last_dist1 = current_dist1
            # p2
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
            # p1
            for bit1 in self.snake1:
                self.s.blit(img1, (bit1[0] * PIXEL_SIZE, bit1[1] * PIXEL_SIZE))
            # p2
            for bit2 in self.snake2:
                self.s.blit(img2, (bit2[0] * PIXEL_SIZE, bit2[1] * PIXEL_SIZE))
            # fruit
            self.s.blit(
                appleimage, (self.fruit[0] * PIXEL_SIZE, self.fruit[1] * PIXEL_SIZE))
            # p1
            score_ts1 = font.render(
                "AI "+str(self.score1), False, (255, 255, 255))
            self.s.blit(score_ts1, (5, 5))
            # p2
            score_ts2 = font.render(
                "Human "+str(self.score2), False, (255, 0, 0))
            self.s.blit(score_ts2, (560, 5))
            # time
            time = time_font.render(str(round(self.timer, 1)) +
                               '초', False, (255, 255, 255))
            self.s.blit(time, (300, 5))

            pygame.display.update()

        return self.fitness1, self.score1


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    s = pygame.display.set_mode(
        (SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
    pygame.display.set_caption('Snake Game')

    # while True:
    snake = Snake(s)
    fitness, score = snake.run()
    # print('Fitness: %s, Score: %s' % (fitness, score))
