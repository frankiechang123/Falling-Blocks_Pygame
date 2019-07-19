''' game '''
import random
import string
import pygame
import pygame.draw

#Window & Color config
WIDTH=800
HEIGHT=600
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE=(255,255,255)

#Brick config
brick_pos_y = HEIGHT-100
brick_pos_x = WIDTH/2
brick_pos = [brick_pos_x,brick_pos_y]
BRICK_SIZE=(25,25)
ENEMY_SIZE=(25,25)
CIRCLE_R=10
MOVE_PIXEL=10
ENEMY_SPEED=5
FPS=40
LEVELUPDIFF=1.3
Info_pos=(10,HEIGHT-50)
CountsToLevelUP=5
enemy_count=3
circle_count=1
score=0
level=1

def dropEnemy(Enemylist):
    pos_x=random.randint(0, WIDTH-ENEMY_SIZE[0])
    pos_y=0
    enemy_pos=[pos_x,pos_y]
    Enemylist.append(enemy_pos)

def drawEnemy(Enemylist):
    for enemy in Enemylist:
        pygame.draw.rect(SCREEN, RED, ((enemy[0], enemy[1]), ENEMY_SIZE))
    
Game_Over = False
def detectCollision(enemy_pos,brick_pos):
    if enemy_pos[1]>=brick_pos[1]-ENEMY_SIZE[1] and enemy_pos[1]<=brick_pos[1]+BRICK_SIZE[1] and enemy_pos[0]>=brick_pos[0]-ENEMY_SIZE[0] and enemy_pos[0]<=brick_pos[0]+BRICK_SIZE[0]:
        return True

def EnemyisOut(enemy_pos):
    if enemy_pos[1] >= HEIGHT:
        return True
    else:
        return False

def placeCircle(CircleList):
    pos_x=random.randint(10,WIDTH-2*CIRCLE_R)
    pos_y=random.randint(10,HEIGHT-2*CIRCLE_R)
    CircleList.append([pos_x,pos_y])

def drawCircle(CircleList):
    for circle in CircleList:
        pygame.draw.circle(SCREEN,GREEN,(circle[0],circle[1]),CIRCLE_R)

def eatCircle(circle_pos,brick_pos):
   
    if(brick_pos[0]>=circle_pos[0]-CIRCLE_R-BRICK_SIZE[0] and brick_pos[0]<=circle_pos[0]+CIRCLE_R+BRICK_SIZE[0]\
     and brick_pos[1]>=circle_pos[1]-CIRCLE_R-BRICK_SIZE[0] and brick_pos[1]<=circle_pos[1]+CIRCLE_R+BRICK_SIZE[0]):
        return True 
    else:
        return False


print("Score: %s" %(score))
print("Level: %s" %(level))
pygame.init() 

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Game")

pygame.draw.rect(SCREEN,BLUE,(brick_pos,BRICK_SIZE))
EnemyList=[]
CircleList=[]

clock=pygame.time.Clock()
pygame.key.set_repeat(3,1)
while not Game_Over:

    
    for i in range(len(EnemyList),enemy_count):
        dropEnemy(EnemyList)
    
    while len(CircleList)<circle_count:
        placeCircle(CircleList)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game_Over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if not brick_pos_y <= MOVE_PIXEL:
                    brick_pos_y -= MOVE_PIXEL
            if event.key == pygame.K_a:
                if not brick_pos_x  <= MOVE_PIXEL:
                    brick_pos_x -= MOVE_PIXEL
            if event.key == pygame.K_d:
                if not brick_pos_x+MOVE_PIXEL >= WIDTH:
                    brick_pos_x += MOVE_PIXEL
            if event.key == pygame.K_s:
                if not brick_pos_y+MOVE_PIXEL >=HEIGHT:
                    brick_pos_y += MOVE_PIXEL

            brick_pos=(brick_pos_x,brick_pos_y)
    SCREEN.fill((0,0,0))
    text="LEVEL: %s  SCORE: %s" %(level,score)
    Info=pygame.font.Font(None,30)
    Info_image=Info.render(text,True,WHITE)
    SCREEN.blit((Info_image), Info_pos)
    pygame.draw.rect(SCREEN,BLUE,(brick_pos,BRICK_SIZE))
    drawCircle(CircleList)
    drawEnemy(EnemyList)
    pygame.display.flip()

    for enemy in EnemyList:
        enemy[1] += ENEMY_SPEED
        if EnemyisOut(enemy):
            EnemyList.remove(enemy)
            dropEnemy(EnemyList)
        if detectCollision([enemy[0],enemy[1]],brick_pos):
            Game_Over = True
    
    for circle in CircleList:
        if eatCircle(circle,brick_pos):
            score+=1
            CircleList.remove(circle)
            placeCircle(CircleList)
        
            if score > 0 and score % CountsToLevelUP == 0:  #check level up
                level+=1
                ENEMY_SPEED*=LEVELUPDIFF
            print("Score: %s" %(score))
            print("Level: %s" %(level))
    
    if Game_Over:
        pygame.quit()

    clock.tick(FPS)