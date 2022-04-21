import pygame
import random
import time

pygame.init()

def tile_num(tile_y, tile_x):

    global y_indent, x_indent, W, H
    
    tile_x -= x_indent
    tile_y -= y_indent
    if tile_x % (tile_size + between) > tile_size or tile_y % (tile_size + between) > tile_size:
        return -1, -1
    if 0 < tile_x < W - 2 * x_indent and 0 < tile_y < H - 2 * y_indent:
        y = tile_y // (tile_size + between)
        x = tile_x // (tile_size + between)
        return y, x
    else:
        return -1, -1
def resize():
    
    global x_l, x_r, y_u, y_d, mid_x, mid_y
    global Matrix

    x_len = x_r - x_l + 1
    y_len = y_d - y_u + 1

    if (y_len >= x_len or y_u < 1) and x_l >= 1: #resizing by Ox
        x_l -= 1
        x_r += 1
    elif y_u >= 1:#resizing by Oy
        y_u -= 1
        y_d += 1
        
    for i in range(y_u, y_d + 1):
        for j in range(x_l, x_r + 1):
            Matrix[i][j] = "on"
def show_start():
    
    st_background = [251, 248, 241]
    #surf.fill(st_background)
    surf.blit(Background2, (0, 0))
    surf.blit(QUESTION, (0, 0))
    y = int(EASY.get_height() * min(max(2 / w_k, 2 // 3), 1))
    x = W // 2 - EASY.get_width() // 2
    surf.blit(EASY, (x, y))
    y += int(MEDIUM.get_height() + between * 2.5)
    surf.blit(MEDIUM, (x, y))
    y += int(HARD.get_height() + between * 2.5)
    surf.blit(HARD, (x, y))
    screen.blit(surf, (0, 0))
    pygame.display.update()
def show_matrix():
    
    global Matrix
    
    flag = True

    for y in range(Y):
        for x in range(X):
            
            cur_x = x_indent + x * (between + tile_size)
            cur_y = y_indent + y * (between + tile_size)
            if Matrix[y][x] == "on":
                surf.blit(tile_surf, (cur_x, cur_y))
            if Matrix[y][x] == "wrong":
                surf.blit(tile_surf, (cur_x, cur_y))
                surf.blit(cross_surf, (cur_x, cur_y))
                flag = False
            if Matrix[y][x] == "colored":
                surf.blit(colored_tile_surf, (cur_x, cur_y))
            
    screen.blit(surf, (0, 0))
    return flag    
def game_over(score):
    
    menu_background = [251, 248, 241]
    #surf.fill(menu_background)
    surf.blit(Background2, (0, 0))
    lose_sys = pygame.font.SysFont('calibri', int(180 // w_k))
    score_sys = pygame.font.SysFont('calibri', int(90 // w_k))
    BLACK = [0, 0, 0]
    sign1 = lose_sys.render("GAME OVER!", 1, BLACK, menu_background)
    sign2 = score_sys.render("Your score: " + str(score), 1, BLACK, menu_background)
    pos1 = sign1.get_rect(center = (W // 2, int(250 // w_k)))
    pos2 = sign2.get_rect(center = (W // 2, int( 250 // w_k + 90 // w_k + 8)))
    surf.blit(sign1, pos1)
    surf.blit(sign2, pos2)
    retr_pos = reload_button.get_rect(center = (W // 2 - 20 - reload_button.get_width(), H // 2))
    cont_pos = continue_button.get_rect(center = (W // 2 + 20 + continue_button.get_width(), H // 2))
    surf.blit(reload_button, retr_pos)
    surf.blit(continue_button, cont_pos)
    #print(retr_pos)
    #print(cont_pos)
    x_retr, y_retr, a, b = retr_pos
    x_cont, y_cont, a, b = cont_pos
    screen.blit(surf, (0, 0))
    pygame.display.update()
    button_size = reload_button.get_width()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x_cont <= x <= x_cont + button_size and y_cont <= y <= y_cont + button_size:
                    return True
                elif x_retr <= x <= x_retr + button_size and y_retr <= y <= y_retr + button_size:
                    return False
        clock.tick(FPS)

def end():
    
    menu_background = [251, 248, 241]
    #surf.fill(menu_background)
    surf.blit(Background2, (0, 0))
    win_sys = pygame.font.SysFont('calibri', int(180 // w_k))
    BLACK = [0, 0, 0]
    sign1 = win_sys.render("YOU WIN!", 1, BLACK, menu_background)
    pos1 = sign1.get_rect(center = (W // 2, int(150 // w_k)))
    surf.blit(sign1, pos1)
    pos2 = cake.get_rect(center = (W // 2, int(150 // w_k + sign1.get_height() // 2 + cake.get_height() // 2 // w_k)))
    x, y, a, b = pos2
    x3 = W // 2 - reload_button.get_width() // 2
    y3 = y + cake.get_height() + 16
    surf.blit(cake, pos2)
    surf.blit(reload_button, (x3, y3))
    screen.blit(surf, (0, 0))
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x3 <= x <= x3 + reload_button.get_width() and y3 <= y <= y3 + reload_button.get_height():
                    return
        clock.tick(FPS)
def fill_matrix():
    
    global Rand_Matrix
    
    for i in range(Y):
        for j in range(X):
            Rand_Matrix[i][j] = -1
    k = 0
    for y in range(y_u, y_d + 1):
        for x in range(x_l, x_r + 1):
            Rand_Matrix[y][x] = random.randint(0, 2) % 2
            k += Rand_Matrix[y][x]
    return k

cfg = open("cfg.txt").readlines()
res = cfg[0].replace("resolution:", "").replace("\n", "")
FPS = int(cfg[1].replace("FPS:", "").replace("\n", ""))
W, H = map(int, res.split('*'))
#W = pygame.display.Info().current_w
#H = pygame.display.Info().current_h
w_k = 1920 / W
h_k = 1080 / H
tile_surf = pygame.image.load("textures/tile2.png")
tile_surf = pygame.transform.scale(tile_surf, (tile_surf.get_width() / w_k, tile_surf.get_height() / h_k))
cross_surf = pygame.image.load("textures/cross2.png")
cross_surf = pygame.transform.scale(cross_surf, (cross_surf.get_width() / w_k, cross_surf.get_height() / h_k))
#check_mark_surf = pygame.image.load("textures/check_mark.png")
colored_tile_surf = pygame.image.load("textures/colored_tile2.png")
colored_tile_surf = pygame.transform.scale(colored_tile_surf, (colored_tile_surf.get_width() / w_k, colored_tile_surf.get_height() / h_k))
QUESTION = pygame.image.load("textures/QUESTION.png")
QUESTION = pygame.transform.scale(QUESTION, (QUESTION.get_width() / w_k, QUESTION.get_height() / h_k))
EASY = pygame.image.load("textures/EASY.png")
EASY = pygame.transform.scale(EASY, (EASY.get_width() / w_k, EASY.get_height() / h_k))
MEDIUM = pygame.image.load("textures/MEDIUM.png")
MEDIUM = pygame.transform.scale(MEDIUM, (EASY.get_width(), EASY.get_height()))
HARD = pygame.image.load("textures/HARD.png")
HARD = pygame.transform.scale(HARD, (EASY.get_width(), EASY.get_height()))
rules = pygame.image.load("textures/rules.png")
rules = pygame.transform.scale(rules, (rules.get_width() / w_k, rules.get_height() / h_k))
reload_button = pygame.image.load("textures/reload-button.png")
reload_button = pygame.transform.scale(reload_button, (192 / w_k, 192 / h_k))
continue_button = pygame.image.load("textures/continue-button.png")
continue_button = pygame.transform.scale(continue_button, (192 / w_k, 192 / h_k))
GAMEOVER = pygame.image.load("textures/GAMEOVER.png")
GAMEOVER = pygame.transform.scale(GAMEOVER, (702 / w_k, 96 / h_k))
cake = pygame.image.load("textures/cake.png")
cake = pygame.transform.scale(cake, (cake.get_width() / w_k, cake.get_height() / h_k))
Background2 = pygame.image.load("textures/background2.png")
Background2 = pygame.transform.scale(Background2, (W, H))
Background = pygame.image.load("textures/background.png")
Background = pygame.transform.scale(Background, (W, H))
#print(W, H)
#print(w_k, h_k)
#W //= 2
#H //= 2

#768, 432

screen = pygame.display.set_mode((W, H))

#sc = pygame.display.set_mode((W, H))

pygame.display.set_caption("Memory-matrix")
background = [187, 173, 160]

#pygame.display.set_icon(pygame.image.load("имя файла.bmp"))

clock = pygame.time.Clock()
surf = pygame.Surface((W, H))
#surf.fill(background)
surf.blit(Background, (0, 0))
tile_size = tile_surf.get_width()
wait_time = 3
tile_surf.set_colorkey(background)
between = 8 / min(w_k * 2, 1) 
X = (W - (tile_size + between)) // (tile_size + between - 1)
x_indent = 32 + ((W - (tile_size + between)) % (tile_size + between - 1)) // 2
if X % 2 == 0:
    X -= 1
    x_indent += (tile_size + between - 1) // 2
Y = (H - (tile_size + between)) // (tile_size + between - 1)
y_indent = 32 + ((H - (tile_size + between)) % (tile_size + between - 1)) // 2
if Y % 2 == 0:
    Y -= 1
    y_indent += (tile_size + between - 1) // 2
####### START ########
resize_chance = 0
def START():
    global resize_chance, wait_time
    A = [[0 for i in range(2)] for j in range(3)]
    y = int(EASY.get_height() * min(max(2 / w_k, 2 // 3), 1))
    x = W // 2 - EASY.get_width() // 2
    A[0][0] = x
    A[0][1] = y
    y += int(MEDIUM.get_height() + between * 2.5)
    A[1][0] = x
    A[1][1] = y
    y += int(HARD.get_height() + between * 2.5)
    A[2][0] = x
    A[2][1] = y
    start = True
    resize_chance = 0
    show_start()
    while start:
        for event in pygame.event.get():  
            #### events processing
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                #print(x, y)
                if max(x, y) < QUESTION.get_width():
                    surf.blit(rules, (0, 0))
                    screen.blit(surf, (0, 0))
                    pygame.display.update()
                    reading = True
                    while reading:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                show_start()
                                reading = False
                            if event.type == pygame.QUIT:
                                exit()
                        clock.tick(FPS)
                elif A[0][0] <= x <= A[0][0] + EASY.get_width() and A[0][1] <= y <= A[0][1] + EASY.get_height():
                    wait_time = 4
                    resize_chance = 30
                    start = False
                elif A[1][0] <= x <= A[1][0] + MEDIUM.get_width() and A[1][1] <= y <= A[1][1] + MEDIUM.get_height():
                    wait_time = 3
                    resize_chance = 50 
                    start = False
                elif A[2][0] <= x <= A[2][0] + HARD.get_width() and A[2][1] <= y <= A[2][1] + HARD.get_height():
                    wait_time = 1.5
                    resize_chance = 70
                    start = False    
            ####
        
        clock.tick(FPS)
    inp = cfg[2].replace("rezice_chance, wait_time:", "").replace("\n", "")
    if inp != "":
        resize_chance, wait_time = map(float, cfg[2].replace("rezice_chance, wait_time:", "").replace("\n", "").split())
        resize_chance = int(resize_chance)
#######START########
START()
screen.blit(surf, (0, 0))  #(x, y)
pygame.display.update()
Y = int(Y)
X = int(X)
Matrix = []
Rand_Matrix = []
for i in range(Y):
    Rand_Matrix.append([-1] * X)
#print("Y, X =", Y, X)
for i in range(Y):
    Matrix.append(["off"] * X)

Matrix[Y // 2][X // 2] = "on"

mid_x = X // 2
mid_y = Y // 2

x_l = x_r = mid_x
y_u = y_d = mid_y

#surf.fill(background)
surf.blit(Background, (0, 0))

resize()
resize()

#print("indents =", y_indent, x_indent)
level_ended = True
k = 0
start = False
playing = True
score = 0
print(resize_chance)
while True:
    if start:
        START()
        playing = True
        Matrix = []
        Rand_Matrix = []
        for i in range(Y):
            Rand_Matrix.append([-1] * X)
        #print("Y, X =", Y, X)
        for i in range(Y):
            Matrix.append(["off"] * X)

        Matrix[Y // 2][X // 2] = "on"

        mid_x = X // 2
        mid_y = Y // 2

        x_l = x_r = mid_x
        y_u = y_d = mid_y
        resize()
        resize()
        score = 0
    while playing:
        surf.blit(Background, (0, 0))
        #surf.fill(background)
        if level_ended:
            #### level start
            k = fill_matrix()
            for i in range(Y):
                for j in range(X):
                    if Rand_Matrix[i][j] == -1:
                        Matrix[i][j] = "off"
                        ###Matrix[i][j] = "on"
                    if Rand_Matrix[i][j] == 0:
                        Matrix[i][j] = "on"
                    if Rand_Matrix[i][j] == 1:
                        Matrix[i][j] = "colored"
            show_matrix()
            pygame.display.update()
            for i in range(int(wait_time * 60)):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                clock.tick(FPS)

            for i in range(Y):
                for j in range(X):
                    if Rand_Matrix[i][j] == 0 or Rand_Matrix[i][j] == 1:
                        Matrix[i][j] = "on"
                    else:
                        Matrix[i][j] = "off"
            level_ended = False
            show_matrix()
            pygame.display.update()
            ####
        for event in pygame.event.get():  
            #### events processing  
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                y, x = map(int, tile_num(y, x))
                if y == -1:
                    continue
                if Rand_Matrix[y][x] == 1:
                    Matrix[y][x] = "colored"
                    k -= 1
                if Rand_Matrix[y][x] == 0:
                    Matrix[y][x] = "wrong"
            ####
        if show_matrix() == False:
            pygame.display.update()
            flag = game_over(score)
            #print("entered")
            if flag:
                score //= 2
                level_ended = True
                surf.blit(Background, (0, 0))
                #surf.fill(background)
            else:
                start = True
                playing = False
                level_ended = True
        pygame.display.update()
        if k == 0:
            if (random.randint(0, 100) < resize_chance):
                resize()
                score += 1
                score += 4
            level_ended = True
            for i in range(30):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                clock.tick(FPS)
        if score == 10:
            end()
            playing = False
            start = True
            
    clock.tick(FPS)