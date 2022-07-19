import pygame as pg
import time
import random as rd

pg.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
p1_color = (120, 192, 224)
p2_clor = (68, 157, 209)

dis_width = 800
dis_height = 800

dis = pg.display.set_mode((dis_width, dis_height))
pg.display.set_caption('Snake Game')

clock = pg.time.Clock()

snake_size = 20
snake_speed = 8

font_style = pg.font.SysFont("consolas", 25)
score_font = pg.font.SysFont("consolas", 35)


def display_score(score):
    value = score_font.render(f"Score: {str(score)}", True, white)
    dis.blit(value, [0, 0])


def move_snake(snake_size, snake_list, color):
    for [x, y] in snake_list:
        pg.draw.rect(dis, color, [x, y, snake_size, snake_size])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop():
    game_over = False
    game_close = False

    # p1
    p1_x = dis_width-40
    p1_y = 20

    p1_x_change = 0
    p1_y_change = 0

    p1_snake_List = []
    p1_Length_of_snake = 1

    # p2
    p2_x = 20
    p2_y = dis_height-40

    p2_x_change = 0
    p2_y_change = 0

    p2_snake_List = []
    p2_Length_of_snake = 1

    foodx = round(rd.randrange(0, dis_width - snake_size) /
                  snake_size) * snake_size
    foody = round(rd.randrange(0, dis_height - snake_size) /
                  snake_size) * snake_size

    while not game_over:

        while game_close == True:
            dis.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            display_score(p1_Length_of_snake - 1)
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pg.K_c:
                        gameLoop()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True
            if event.type == pg.KEYDOWN:
                # p1
                if event.key == pg.K_LEFT:
                    p1_x_change = -snake_size
                    p1_y_change = 0
                elif event.key == pg.K_RIGHT:
                    p1_x_change = snake_size
                    p1_y_change = 0
                elif event.key == pg.K_UP:
                    p1_y_change = -snake_size
                    p1_x_change = 0
                elif event.key == pg.K_DOWN:
                    p1_y_change = snake_size
                    p1_x_change = 0
                if p1_Length_of_snake > 1:
                    if [p1_x+p1_x_change, p1_y+p1_y_change] == p1_snake_List[-2]:
                        if p1_x_change == 0:
                            p1_y_change *= -1
                        if p1_y_change == 0:
                            p1_x_change *= -1
                # p2
                if event.key == pg.K_a:
                    p2_x_change = -snake_size
                    p2_y_change = 0
                elif event.key == pg.K_d:
                    p2_x_change = snake_size
                    p2_y_change = 0
                elif event.key == pg.K_w:
                    p2_y_change = -snake_size
                    p2_x_change = 0
                elif event.key == pg.K_s:
                    p2_y_change = snake_size
                    p2_x_change = 0
                if p2_Length_of_snake > 1:
                    if [p2_x+p2_x_change, p2_y+p2_y_change] == p2_snake_List[-2]:
                        if p2_x_change == 0:
                            p2_y_change *= -1
                        if p2_y_change == 0:
                            p2_x_change *= -1
        # p1
        if p1_x >= dis_width or p1_x < 0 or p1_y >= dis_height or p1_y < 0:
            game_close = True
        p1_x += p1_x_change
        p1_y += p1_y_change

        # p2
        if p2_x >= dis_width or p2_x < 0 or p2_y >= dis_height or p2_y < 0:
            game_close = True
        p2_x += p2_x_change
        p2_y += p2_y_change

        dis.fill(black)
        pg.draw.rect(dis, green, [foodx, foody, snake_size, snake_size])

        # p1
        p1_snake_Head = []
        p1_snake_Head.append(p1_x)
        p1_snake_Head.append(p1_y)
        p1_snake_List.append(p1_snake_Head)
        if len(p1_snake_List) > p1_Length_of_snake:
            del p1_snake_List[0]

        for x in p1_snake_List[:-1]:
            if x == p1_snake_Head:
                game_close = True

        move_snake(snake_size, p1_snake_List, p1_color)
        display_score(p1_Length_of_snake - 1)
        for i in range(len(p1_snake_List)):
            print('p1 -', i, ':', p1_snake_List[i])

        # p2
        p2_snake_Head = []
        p2_snake_Head.append(p2_x)
        p2_snake_Head.append(p2_y)
        p2_snake_List.append(p2_snake_Head)
        if len(p2_snake_List) > p2_Length_of_snake:
            del p2_snake_List[0]

        for x in p2_snake_List[:-1]:
            if x == p2_snake_Head:
                game_close = True

        move_snake(snake_size, p2_snake_List, p2_clor)
        display_score(p2_Length_of_snake - 1)
        for i in range(len(p2_snake_List)):
            print('p2-', i, ':', p2_snake_List[i])

        pg.display.update()

        # p1
        if p1_x == foodx and p1_y == foody:
            foodx = round(rd.randrange(
                0, dis_width - snake_size) / snake_size) * snake_size
            foody = round(rd.randrange(
                0, dis_height - snake_size) / snake_size) * snake_size
            p1_Length_of_snake += 1

        # p2
        if p2_x == foodx and p2_y == foody:
            foodx = round(rd.randrange(
                0, dis_width - snake_size) / snake_size) * snake_size
            foody = round(rd.randrange(
                0, dis_height - snake_size) / snake_size) * snake_size
            p2_Length_of_snake += 1
        clock.tick(snake_speed)

    pg.quit()
    quit()


gameLoop()
