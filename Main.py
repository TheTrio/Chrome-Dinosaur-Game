import pygame
from random import randrange

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
#get coordinates
dino_x = 30
dino_y = 90
tree_y = 90
ground_x = 0

#get velocity
dino_y_vel = 0
tree_x_vel = -7
#set physics
gravity = 2


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
gameOver = False
font = pygame.font.Font('freesansbold.ttf', 36)
new_font = pygame.font.Font('freesansbold.ttf', 12)
c = 1
d = 0
score = 0
increment = 0
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if gameOver:
                tree_x_vel = -7
                dino_y_vel = 0
                gravity = 2
                c = 1
                gameOver = False
                trees_x = []
                gap_max = 300
                gap_min = 200
                trees_x.append(600)
                last = 600
                for i in range(4):
                    gap = randrange(gap_min,gap_max)
                    last +=gap
                    trees_x.append(last)
                score = 0
                increment = 0
            if event.key == pygame.K_SPACE and not jump:
                jump = True
                c = -1
                dino_y_vel = -18
    dino_y+=dino_y_vel
    dino_y_vel += gravity
    if dino_y_vel == 0:
        dino_y_vel = gravity
    if dino_y > 90:
        dino_y = 90
        jump = False
        if c==-1:
            c = 0
    ground_x += tree_x_vel
    if ground_x < -600:
        ground_x = 0
    screen.fill((217, 217, 217))
    screen.blit(ground_img, (ground_x,120))
    if c<0:
        screen.blit(dino_img_jump, (dino_x,dino_y))
    elif c%2==0:
        screen.blit(dino_img_left, (dino_x,dino_y))
    else:
        screen.blit(dino_img_right, (dino_x,dino_y))
    if c >=0:
        if d%5==0:
            c+=1
    d+=1
    for i in range(len(trees_x)):
        trees_x[i] += tree_x_vel
        if trees_x[i] <= dino_x+30 and trees_x[i]+20 >= dino_x:
            if dino_y+40 >= tree_y:
                tree_x_vel = 0
                dino_y_vel = 0
                gravity = 0
                c = -1
                gameOver = True

        if trees_x[i] < -30:
            trees_x[i] = max(trees_x) + randrange(200,300)
        screen.blit(tree_img, (trees_x[i],tree_y))
    if gameOver:
        text = font.render("Game Over", True, (0,0,0))
        screen.blit(text, (205,60))

    new_text = new_font.render('Score: ' + str(score), True, (0,0,0))
    screen.blit(new_text, (10,10))
    if not gameOver:
        score+=1
        increment+=1
        if increment == 300:
            tree_x_vel -= 1
            increment = 0
    pygame.display.update()
