import pygame
import sys
import random

#display a random torch from the torch's list.
def create_torch():
    random_torch_pos = random.choice(torch_heights)
    new_torch = torch_image.get_rect(midtop= (width-100, random_torch_pos))
    return new_torch

#keep the torches to move accordingly with the screen
def move_torch(torch_list):
    for torch in torch_list:
        torch.centerx -= 4
    return torch_list

# display the torches on the screen
def draw_torch (torch_list):
    for torch in torch_list:
        screen.blit(torch_image,torch)
# check if there was collision with a torch or if the chicken went too high.
def game_over_check (torch_list):
    for torch in torch_list:
        if rect_chicken.colliderect(torch):
            return False
    if rect_chicken.top <= -100 or rect_chicken.bottom >= height+100:
        return False
    return True

#display the score and the game over screen with the highest score
def display_text(game_status):
    if game_status == "game_active":
        score_image = font.render("Score: " +str(int(score)), True, (255,255,255))
        rect_score = score_image.get_rect(center = ((width/2)-200,100))
        screen.blit(score_image, rect_score)
    if game_status == "game_over":
        score_image = font.render("Score: " +str(int(score)), True, (255,255,255))
        rect_score = score_image.get_rect(center = ((width/2)-200,100))
        screen.blit(score_image, rect_score)

        high_score_image = font.render("High Score: " +str(int(high_score)), True, (255,255,255))
        high_rect_score = high_score_image.get_rect(center = ((width/2)+200,100))
        screen.blit(high_score_image, high_rect_score)

        game_over_image = font.render("Press Space To Play", True, (255,255,255))
        game_over_rect = game_over_image.get_rect(center = ((width/2),height/2))
        screen.blit(game_over_image, game_over_rect)

#check and update in case a new high score has achieved 
def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score    

#setting the screen size
width = 950
height = 650
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Super Chicken")  #name of the window
clock = pygame.time.Clock()
font = pygame.font.SysFont ("Times New Roman, Arial", 30) #uploading the font type

#uploading the background image
bg_image = pygame.image.load("assets/hell.jpg").convert()
bg_image=pygame.transform.scale(bg_image,(width, height))

#uploading the chicken image as a rectangle
chicken_image=pygame.image.load("assets/super_chicken.png").convert_alpha()
chicken_image=pygame.transform.scale(chicken_image, (80, 80))
rect_chicken=chicken_image.get_rect(center=(300,100))

#uploading the torch image
torch_image=pygame.image.load("assets/torch.png").convert_alpha()
torch_image=pygame.transform.scale(torch_image, (100, 550))

#playing a bakground music
bg_sound = pygame.mixer.Sound("assets/bg_music.wav")


#variables
gravity = 0.25  
chicken_place = 0
game_active = True
score = 0
high_score = 0

#rect_chicken=chicken_image.get_rect(center=(100,height/2))
torch_list=[]
spwantorch=pygame.USEREVENT
pygame.time.set_timer(spwantorch,600)
torch_heights = [100,130,140,150,160,170,180,190,200,220,250,280,300,310,320,350]

while True:
    for event in pygame.event.get():
        #exit the game
        if event.type == pygame.QUIT:
            pygame.quit()                   
            sys.exit()
        if event.type ==pygame.KEYDOWN:
            #when pressing "space" chicken is jumping     
            if event.key == pygame.K_SPACE and game_active: 
                chicken_place = 0
                chicken_place -= 7
            #pressing space after game over will restart the game
            if event.key == pygame.K_SPACE and game_active == False:  
                game_active = True
                torch_list.clear()
                rect_chicken.center = (300,100)  
                chicken_place = 0  
                score = 0   
        if event.type == spwantorch:
            torch_list.append(create_torch())  

    #display the background image
    screen.blit(bg_image, (0,0))

    if game_active:
        
        #constantly take the chicken down
        chicken_place += gravity     
        rect_chicken.centery += chicken_place
        
        game_active= game_over_check(torch_list)

        #Display the chicken as a rectangle
        screen.blit(chicken_image,rect_chicken)

        torch_list = move_torch(torch_list)
        draw_torch(torch_list)

        score += 0.01
        display_text("game_active")
    else:
        high_score = update_high_score(score,high_score)
        display_text("game_over")    

    #playing background music
    bg_sound.play(-1)     
    pygame.display.update()
    #90 frames per second.
    clock.tick(90) 
