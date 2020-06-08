import pygame
from random import randrange


high_score = 0
with open('Resources/Data/high.txt') as f:
    high_score = int(f.read())
#initialize stuff
pygame.init()
screen = pygame.display.set_mode((600,150))
pygame.display.set_caption('Google Dinosaur')

#get images
dino_img_left = pygame.image.load('Resources/Images/d1.png')
dino_img_right = pygame.image.load('Resources/Images/d2.png')
dino_img_jump = pygame.image.load('Resources/Images/dino_jump.png')
dino_img_left = pygame.transform.scale(dino_img_left, (40, 42))
dino_img_right = pygame.transform.scale(dino_img_right, (40, 42))
dino_img_jump = pygame.transform.scale(dino_img_jump, (40, 42))
tree_img = pygame.image.load('Resources/Images/tree.png')
tree_img = pygame.transform.scale(tree_img, (30, 42))
ground_img = pygame.image.load('Resources/Images/ground.png')
bird_img_up = pygame.image.load('Resources/Images/bird_up.png')
bird_img_down = pygame.image.load('Resources/Images/bird_down.png')
bird_img_up = pygame.transform.scale(bird_img_up, (30, 30))
bird_img_down = pygame.transform.scale(bird_img_down, (30, 30))

#get coordinates
dino_x = 30
dino_y = 90
tree_y = 90
ground_x = 0
bird_x = 615
bird_y = 50
bird_y_choices = [50, 70, 90]

#get velocity
dino_y_vel = 0
tree_x_vel = 0
bird_x_vel = 0
#set physics
gravity = 0


#Tree list
trees_x = []
gap_max = 300
gap_min = 200
trees_x.append(600)
last = 600
for i in range(4):
    gap = randrange(gap_min,gap_max)
    last +=gap
    trees_x.append(last)
run = True
clock = pygame.time.Clock()
jump = False
gameOver = True
font = pygame.font.Font('freesansbold.ttf', 36)
new_font = pygame.font.Font('freesansbold.ttf', 12)
count_dino= -1
dino_random_count = 0
bird_random_count = 0
bird_count = 0
score = 0
increment = 0
min_dist = 0
max_dist = 0
bird_allow = False

collison_allow = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if gameOver:
                tree_x_vel = -7
                dino_y_vel = 0
                gravity = 1.75
                count_dino= 1
                gameOver = False
                trees_x = []
                gap_max = 300
                bird_x_vel = -5
                gap_min = 200
                trees_x.append(600)
                last = 600
                bird_x = 615
                min_dist = 500
                max_dist = 600
                bird_allow = False
                for i in range(4):
                    gap = randrange(gap_min,gap_max)
                    last +=gap
                    trees_x.append(last)
                score = 0
                increment = 0
            if event.key == pygame.K_SPACE and not jump:
                jump = True
                count_dino= -1
                dino_y_vel = -18
            if event.key == pygame.K_q:
                collison_allow = not collison_allow
    dino_y+=dino_y_vel
    dino_y_vel += gravity
    if bird_allow:
        bird_x+=bird_x_vel
    if dino_y > 90:
        dino_y = 90
        jump = False
        if count_dino==-1:
            count_dino= 0
    ground_x += tree_x_vel
    if ground_x < -600:
        ground_x = 0
    screen.fill((217, 217, 217))
    screen.blit(ground_img, (ground_x,120))
    if count_dino<0:
        screen.blit(dino_img_jump, (dino_x,dino_y))
    elif count_dino%2==0:
        screen.blit(dino_img_left, (dino_x,dino_y))
    else:
        screen.blit(dino_img_right, (dino_x,dino_y))
    if count_dino>=0:
        if dino_random_count%5==0:
            count_dino+=1
    dino_random_count+=1
    if bird_allow:
        bird_random_count+=1
        if bird_random_count%5==0:
            bird_count+=1
        if bird_count%2==0:
            screen.blit(bird_img_up, (bird_x,bird_y))
        else:
            screen.blit(bird_img_down, (bird_x,bird_y))
        if bird_x < -30:
            bird_x = randrange(1000,2000)
            bird_y = bird_y_choices[randrange(3)]
    for i in range(len(trees_x)):
        trees_x[i] += tree_x_vel
        if collison_allow:
            if trees_x[i] <= dino_x+30 and trees_x[i]+20 >= dino_x:
                if dino_y+40 >= tree_y:
                    tree_x_vel = 0
                    dino_y_vel = 0
                    gravity = 0
                    count_dino= -1
                    gameOver = True
                    bird_x_vel = 0
            if bird_x <= dino_x+25 and bird_x+20 >= dino_x:
                if dino_y+40 >= bird_y and dino_y<=bird_y+30:
                    tree_x_vel = 0
                    dino_y_vel = 0
                    gravity = 0
                    count_dino= -1
                    gameOver = True
                    bird_x_vel = 0

        if trees_x[i] < -30:
            trees_x[i] = max(trees_x) + randrange(min_dist,max_dist)
        screen.blit(tree_img, (trees_x[i],tree_y))
    if gameOver and score != 0:
        text = font.render("Game Over", True, (0,0,0))
        screen.blit(text, (205,60))

    if not collison_allow:
        new_text = new_font.render('Score: None', True, (0,0,0))
    else:
        new_text = new_font.render('Score: ' + str(score), True, (0,0,0))
    high_score_text = new_font.render('High Score : ' + str(high_score), True, (0,0,0))
    screen.blit(new_text, (10,10))
    if score > high_score:
        high_score = score
    screen.blit(high_score_text, (490,10))
    if not gameOver:
        score+=1
        increment+=1
        if increment == 1000:
            tree_x_vel -= 0.5
            increment = 0
            bird_allow = True
            min_dist -=50
            max_dist -=50
            if min_dist <= 200:
                min_dist = 200
                max_dist = 300
    pygame.display.update()
with open('Resources/Data/high.txt', 'w') as f:
    f.write(str(high_score))
