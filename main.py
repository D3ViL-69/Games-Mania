#os import
import os 

#pygame import
import pygame
from pygame.locals import *

#TODO: TKINTER INIIALIZATION
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import tkinter.font as tkFont
from tkinter import messagebox

root = Tk()
root.title("Games Mania")

# #TODO: Mysql initializaton
# import mysql.connector
# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "root", 
#     password = "",
#     database = "games"
# )
import sqlite3
mydb = sqlite3.connect("database.db")
mycursor = mydb.cursor()

# TODO: VARIABLES
win_width = 1280
win_height = 720
uservalue = StringVar()
passvalue = StringVar()

new_uservalue = StringVar()
new_mobvalue = StringVar()
new_passvalue = StringVar()
re_passvalue = StringVar() 

s_ques = StringVar()
s_ans = StringVar()

font1 = tkFont.Font(family = "Rockwell Extra Bold", size = 40, weight = "bold", underline = 1)
font2 = tkFont.Font(family = "Sans Serif", size = 14, weight = "bold")
font3 = tkFont.Font(family = "Rockwell Extra Bold", size = 20, weight = "bold", underline = 1)
font4 = tkFont.Font(family = "Algerian", size=30, weight = "bold", underline=2)
font5 = tkFont.Font(family = "Algerian", size=20, weight = "bold", underline=2)
font6 = tkFont.Font(family = "Sans Serif", size = 18, weight = "bold")

current_user = ""

#TODO: Image variables
logo = Image.open("pictures/logo.jpg")
logo = ImageTk.PhotoImage(logo)

bg0 = Image.open("pictures/menu.png")
bg0 = bg0.resize((win_width-12, win_height-12))
bg0 = ImageTk.PhotoImage(bg0)

bg1 = Image.open("pictures/background.png")
bg1 = bg1.resize((win_width, win_height))
bg1 = ImageTk.PhotoImage(bg1)

bg2 = Image.open("pictures/fruit_fg.jpg")
bg2 = bg2.resize((win_width, win_height))
bg2 = ImageTk.PhotoImage(bg2)

bg3 = Image.open("pictures/tank_fg.jpg")
bg3 = bg3.resize((win_width, win_height))
bg3 = ImageTk.PhotoImage(bg3)

bg4 = Image.open("pictures/car_fg.jpg")
bg4 = bg4.resize((win_width, win_height))
bg4 = ImageTk.PhotoImage(bg4)


# Dimensions of the window 
root.geometry(f"{win_width}x{win_height}")
root.minsize(win_width, win_height)
root.maxsize(win_width, win_height)
root.iconphoto(False, logo)


#TODO: FUCNTIONS 

#fruit ninja
def fruit_ninja(who):

    import pygame, sys
    import os
    import random
    # import mysql.connector
    # mydb = mysql.connector.connect(
    #     host = "localhost",
    #     user = "root", 
    #     password = "",
    #     database = "games"
    # )
    # mycursor = mydb.cursor()

    player_lives = 3                                                #keep track of lives
    score = 0                                                       #keeps track of score
    fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']    #entities in the game

    # initialize pygame and create window
    WIDTH = 800
    HEIGHT = 500
    FPS = 15                                                 #controls how often the gameDisplay should refresh. In our case, it will refresh every 1/12th second
    pygame.init()
    pygame.display.set_caption('Fruit-Ninja Game')
    gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))   #setting game display size
    clock = pygame.time.Clock()

    # Define colors
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)

    background = pygame.image.load('back.jpg')                                  #game background
    font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
    score_text = font.render('Score : ' + str(score), True, (255, 255, 255))    #score display
    lives_icon = pygame.image.load('images/white_lives.png')                    #images that shows remaining lives

    # Generalized structure of the fruit Dictionary
    def generate_random_fruits(fruit):
        fruit_path = "images/" + fruit + ".png"
        data[fruit] = {
            'img': pygame.image.load(fruit_path),
            'x' : random.randint(100,500),          #where the fruit should be positioned on x-coordinate
            'y' : 800,
            'speed_x': random.randint(-10,10),      #how fast the fruit should move in x direction. Controls the diagonal movement of fruits
            'speed_y': random.randint(-80, -60),    #control the speed of fruits in y-directionn ( UP )
            'throw': False,                         #determines if the generated coordinate of the fruits is outside the gameDisplay or not. If outside, then it will be discarded
            't': 0,                                 #manages the
            'hit': False,
        }

        if random.random() >= 0.75:     #Return the next random floating point number in the range [0.0, 1.0) to keep the fruits inside the gameDisplay
            data[fruit]['throw'] = True
        else:
            data[fruit]['throw'] = False

    # Dictionary to hold the data the random fruit generation
    data = {}
    for fruit in fruits:
        generate_random_fruits(fruit)

    def hide_cross_lives(x, y):
        gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))

    # Generic method to draw fonts on the screen
    font_name = pygame.font.match_font('comic.ttf')
    def draw_text(display, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        gameDisplay.blit(text_surface, text_rect)

    # draw players lives
    def draw_lives(display, x, y, lives, image) :
        for i in range(lives) :
            img = pygame.image.load(image)
            img_rect = img.get_rect()       #gets the (x,y) coordinates of the cross icons (lives on the the top rightmost side)
            img_rect.x = int(x + 35 * i)    #sets the next cross icon 35pixels awt from the previous one
            img_rect.y = y                  #takes care of how many pixels the cross icon should be positioned from top of the screen
            display.blit(img, img_rect)

    # show game over display & front display
    def show_gameover_screen():
        gameDisplay.blit(background, (0,0))
        draw_text(gameDisplay, "FRUIT NINJA!", 90, WIDTH / 2, HEIGHT / 4)
        if not game_over :
            draw_text(gameDisplay,"Score : " + str(score), 50, WIDTH / 2, HEIGHT /2)
        draw_text(gameDisplay, "Press a key to begin!", 64, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYUP:
                    waiting = False
        
    # Game Loop
    first_round = True
    game_over = True        #terminates the game While loop if more than 3-Bombs are cut
    game_running = True     #used to manage the game loop

    mycursor.execute("SELECT * from `user` WHERE username = ?", (who, ))
    myresult = mycursor.fetchone()
    highscore = myresult[5]
    
    while game_running :
        if game_over :
            if first_round :
                show_gameover_screen()
                first_round = False
            game_over = False
            player_lives = 3
            draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')
            score = 0

        for event in pygame.event.get():
            # checking for closing window
            if event.type == pygame.QUIT:
                game_running = False

        gameDisplay.blit(background, (0, 0))
        gameDisplay.blit(score_text, (0, 0))
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')

        for key, value in data.items():
            if value['throw']:
                value['x'] += value['speed_x']          #moving the fruits in x-coordinates
                value['y'] += value['speed_y']          #moving the fruits in y-coordinate
                value['speed_y'] += (1 * value['t'])    #increasing y-corrdinate
                value['t'] += 1                         #increasing speed_y for next loop

                if value['y'] <= 800:
                    gameDisplay.blit(value['img'], (value['x'], value['y']))    #displaying the fruit inside screen dynamically
                else:
                    generate_random_fruits(key)

                current_position = pygame.mouse.get_pos()   #gets the current coordinate (x, y) in pixels of the mouse

                if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+60 \
                        and current_position[1] > value['y'] and current_position[1] < value['y']+60:
                    if key == 'bomb':
                        player_lives -= 1
                        if player_lives == 0:
                            
                            hide_cross_lives(690, 15)
                        elif player_lives == 1 :
                            hide_cross_lives(725, 15)
                        elif player_lives == 2 :
                            hide_cross_lives(760, 15)
                        #if the user clicks bombs for three time, GAME OVER message should be displayed and the window should be reset
                        if player_lives < 0 :
                            show_gameover_screen()
                            
                            game_over = True

                        half_fruit_path = "images/explosion.png"
                    else:
                        half_fruit_path = "images/" + "half_" + key + ".png"

                    value['img'] = pygame.image.load(half_fruit_path)
                    value['speed_x'] += 10
                    if key != 'bomb' :
                        score += 1
                    score_text = font.render('Score : ' + str(score), True, (255, 255, 255))

                    if int(highscore)>int(score):    
                        sql = f"UPDATE `user` SET `fruit-score` = '{highscore}' WHERE `user`.`username` = '{who}'"
                        mycursor.execute(sql)
                        mydb.commit()
                    elif highscore<score:
                        sql = f"UPDATE `user` SET `fruit-score` = '{score}' WHERE `user`.`username` = '{who}'"
                        mycursor.execute(sql)
                        mydb.commit() 
                    
                    value['hit'] = True
            else:
                generate_random_fruits(key)

        pygame.display.update()
        clock.tick(FPS)      # keep loop running at the right speed (manages the frame/second. The loop should update afer every 1/12th pf the sec
                            

    pygame.quit()
    return


#pocket tanks
def pocket_tanks():
    import pygame
    import random

    pygame.init()

    display_width = 800
    display_height = 600

    game_layout_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Tanks Game')

    Resources = pygame.image.load("game_background.png")
    pygame.display.set_icon(Resources)


    wheat = (245, 222, 179)

    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (0, 0, 255)

    red = (200, 0, 0)
    light_red = (255, 0, 0)

    yellow = (200, 200, 0)
    light_yellow = (255, 255, 0)

    green = (34, 177, 76)
    light_green = (0, 255, 0)


    clock = pygame.time.Clock()

    tnk_width = 40
    tnk_height = 20

    tur_width = 5
    whl_width = 5

    grnd_height = 35

    s_font = pygame.font.SysFont("Times New Roman", 25)
    m_font = pygame.font.SysFont("Times New Roman", 50)
    l_font = pygame.font.SysFont("Times New Roman", 85)
    vs_font = pygame.font.SysFont("Times New Roman", 25)


    def Score(Score):
            txt = s_font.render("Score: " + str(Score), True, white)
            game_layout_display.blit(txt, [0, 0])


    def txt_object(txt, color, size="small"):
        if size == "small":
            txtSrfc = s_font.render(txt, True, color)
        if size == "medium":
            txtSrfc = m_font.render(txt, True, color)
        if size == "large":
            txtSrfc = l_font.render(txt, True, color)
        if size == "vsmall":
            txtSrfc = vs_font.render(txt, True, color)

        return txtSrfc, txtSrfc.get_rect()


    def txt_btn(message, color, btnx, btny, btnwidth, btnheight, size="vsmall"):
        txtSrf, textRect = txt_object(message, color, size)
        textRect.center = ((btnx + (btnwidth / 2)), btny + (btnheight / 2))
        game_layout_display.blit(txtSrf, textRect)

    # function for texts that has to appear over screen
    def msg_screen(message, color, y_displace=0, size="small"):
        txtSrf, textRect = txt_object(message, color, size)
        textRect.center = (int(display_width / 2), int(display_height / 2) + y_displace)
        game_layout_display.blit(txtSrf, textRect)


    def tank(x, y, turret_position):
        x = int(x)
        y = int(y)

        pos_Turrets = [(x - 27, y - 2),
                           (x - 26, y - 5),
                           (x - 25, y - 8),
                           (x - 23, y - 12),
                           (x - 20, y - 14),
                           (x - 18, y - 15),
                           (x - 15, y - 17),
                           (x - 13, y - 19),
                           (x - 11, y - 21)
                           ]

        pygame.draw.circle(game_layout_display, blue, (x, y), int(tnk_height / 2))
        pygame.draw.rect(game_layout_display, blue, (x - tnk_height, y, tnk_width, tnk_height))

        pygame.draw.line(game_layout_display, blue, (x, y), pos_Turrets[turret_position], tur_width)

        pygame.draw.circle(game_layout_display, blue, (x - 15, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x - 10, y + 20), whl_width)

        pygame.draw.circle(game_layout_display, blue, (x - 15, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x - 10, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x - 5, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x + 5, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x + 10, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x + 15, y + 20), whl_width)

        return pos_Turrets[turret_position]


    def computer_tank(x, y, turret_position):
        x = int(x)
        y = int(y)

        pos_Turrets = [(x + 27, y - 2),
                           (x + 26, y - 5),
                           (x + 25, y - 8),
                           (x + 23, y - 12),
                           (x + 20, y - 14),
                           (x + 18, y - 15),
                           (x + 15, y - 17),
                           (x + 13, y - 19),
                           (x + 11, y - 21)
                           ]

        pygame.draw.circle(game_layout_display, blue, (x, y), int(tnk_height / 2))
        pygame.draw.rect(game_layout_display, blue, (x - tnk_height, y, tnk_width, tnk_height))

        pygame.draw.line(game_layout_display, blue, (x, y), pos_Turrets[turret_position], tur_width)

        pygame.draw.circle(game_layout_display, blue, (x - 15, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x - 10, y + 20), whl_width)

        pygame.draw.circle(game_layout_display, blue, (x - 15, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x - 10, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x - 5, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x + 5, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x + 10, y + 20), whl_width)
        pygame.draw.circle(game_layout_display, blue, (x + 15, y + 20), whl_width)

        return pos_Turrets[turret_position]


    def game_ctrls():
        gameControl = True

        while gameControl:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()

            game_layout_display.fill(black)
            msg_screen("Controls", white, -100, size="large")
            msg_screen("Fire: Spacebar", wheat, -30)
            msg_screen("Move Turret: Up and Down arrows", wheat, 10)
            msg_screen("Move Tank: Left and Right arrows", wheat, 50)
            msg_screen("Press D to raise Power % AND Press A to lower Power % ", wheat, 140)
            msg_screen("Pause: P", wheat, 90)

            btn("Play", 150, 500, 100, 50, green, light_green, action="play")
            btn("Main", 350, 500, 100, 50, yellow, light_yellow, action="main")
            btn("Quit", 550, 500, 100, 50, red, light_red, action="quit")

            pygame.display.update()

            clock.tick(15)


    def btn(txt, x, y, width, height, inactive_color, active_color, action=None,size=" "):
        cursor = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(click)
        if x + width > cursor[0] > x and y + height > cursor[1] > y:
            pygame.draw.rect(game_layout_display, active_color, (x, y, width, height))
            if click[0] == 1 and action != None:
                if action == "quit":
                    pygame.quit()


                if action == "controls":
                    game_ctrls()

                if action == "play":
                    gameLoop()

                if action == "main":
                    game_intro()

        else:
            pygame.draw.rect(game_layout_display, inactive_color, (x, y, width, height))

        txt_btn(txt, black, x, y, width, height)


    def pause():
        paused = True
        msg_screen("Paused", white, -100, size="large")
        msg_screen("Press C to continue playing or Q to quit", wheat, 25)
        pygame.display.update()
        while paused:
            # game_layout_display.fill(black)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        

            clock.tick(5)


    def barrier(x_loc, ran_height, bar_width):
        pygame.draw.rect(game_layout_display, green, [x_loc, display_height - ran_height, bar_width, ran_height])


    def explosion(x, y, size=50):

        exp = True

        while exp:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    

            startPoint = x, y

            choice_colors = [red, light_red, yellow, light_yellow]

            mgntde = 1

            while mgntde < size:
                exploding_bit_x = x + random.randrange(-1 * mgntde, mgntde)
                exploding_bit_y = y + random.randrange(-1 * mgntde, mgntde)

                pygame.draw.circle(game_layout_display, choice_colors[random.randrange(0, 4)], (exploding_bit_x, exploding_bit_y),
                                   random.randrange(1, 5))
                mgntde += 1

                pygame.display.update()
                clock.tick(100)

            exp = False


    def playerfireShell(xy, tankx, tanky, turPost, gun_power, xloc, bar_width, ranHeight, eTankX, eTankY):

        fire = True
        damage = 0

        startShell = list(xy)

        print("FIRE!", xy)

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    

            # print(startShell[0],startShell[1])
            pygame.draw.circle(game_layout_display, red, (startShell[0], startShell[1]), 5)

            startShell[0] -= (12 - turPost) * 2

            # y = x**2
            startShell[1] += int(
                (((startShell[0] - xy[0]) * 0.015 / (gun_power / 50)) ** 2) - (turPost + turPost / (12 - turPost)))

            if startShell[1] > display_height - grnd_height:
                print("Last shell:", startShell[0], startShell[1])
                hit_x = int((startShell[0] * display_height - grnd_height) / startShell[1])
                hit_y = int(display_height - grnd_height)
                print("Impact:", hit_x, hit_y)

                if eTankX + 10 > hit_x > eTankX - 10:
                    print("Critical Hit!")
                    damage = 25
                elif eTankX + 15 > hit_x > eTankX - 15:
                    print("Hard Hit!")
                    damage = 18
                elif eTankX + 25 > hit_x > eTankX - 25:
                    print("Medium Hit")
                    damage = 10
                elif eTankX + 35 > hit_x > eTankX - 35:
                    print("Light Hit")
                    damage = 5

                explosion(hit_x, hit_y)
                fire = False

            check_x_1 = startShell[0] <= xloc + bar_width
            check_x_2 = startShell[0] >= xloc

            check_y_1 = startShell[1] <= display_height
            check_y_2 = startShell[1] >= display_height - ranHeight

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                print("Last shell:", startShell[0], startShell[1])
                hit_x = int((startShell[0]))
                hit_y = int(startShell[1])
                print("Impact:", hit_x, hit_y)
                explosion(hit_x, hit_y)
                fire = False

            pygame.display.update()
            clock.tick(60)
        return damage


    def computerfireShell(xy, tankx, tanky, turPost, gun_power, xloc, bar_width, ranHeight, ptankx, ptanky):

        damage = 0
        cPower = 1
        pow_found = False

        while not pow_found:
            cPower += 1
            if cPower > 100:
                pow_found = True
            # print(currentPower)

            fire = True
            startShell = list(xy)

            while fire:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        

                # pygame.draw.circle(game_layout_display, red, (startShell[0],startShell[1]),5)

                startShell[0] += (12 - turPost) * 2
                startShell[1] += int(
                    (((startShell[0] - xy[0]) * 0.015 / (cPower / 50)) ** 2) - (turPost + turPost / (12 - turPost)))

                if startShell[1] > display_height - grnd_height:
                    hit_x = int((startShell[0] * display_height - grnd_height) / startShell[1])
                    hit_y = int(display_height - grnd_height)
                    # explosion(hit_x,hit_y)
                    if ptankx + 15 > hit_x > ptankx - 15:
                        print("target acquired!")
                        pow_found = True
                    fire = False

                check_x_1 = startShell[0] <= xloc + bar_width
                check_x_2 = startShell[0] >= xloc

                check_y_1 = startShell[1] <= display_height
                check_y_2 = startShell[1] >= display_height - ranHeight

                if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                    hit_x = int((startShell[0]))
                    hit_y = int(startShell[1])
                    # explosion(hit_x,hit_y)
                    fire = False

        fire = True
        startShell = list(xy)
        print("FIRE!", xy)

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    

            pygame.draw.circle(game_layout_display, red, (startShell[0], startShell[1]), 5)

            startShell[0] += (12 - turPost) * 2



            gun_power = random.randrange(int(cPower * 0.90), int(cPower * 1.10))

            startShell[1] += int(
                (((startShell[0] - xy[0]) * 0.015 / (gun_power / 50)) ** 2) - (turPost + turPost / (12 - turPost)))

            if startShell[1] > display_height - grnd_height:
                print("last shell:", startShell[0], startShell[1])
                hit_x = int((startShell[0] * display_height - grnd_height) / startShell[1])
                hit_y = int(display_height - grnd_height)
                print("Impact:", hit_x, hit_y)

                if ptankx + 10 > hit_x > ptankx - 10:
                    print("Critical Hit!")
                    damage = 25
                elif ptankx + 15 > hit_x > ptankx - 15:
                    print("Hard Hit!")
                    damage = 18
                elif ptankx + 25 > hit_x > ptankx - 25:
                    print("Medium Hit")
                    damage = 10
                elif ptankx + 35 > hit_x > ptankx - 35:
                    print("Light Hit")
                    damage = 5

                explosion(hit_x, hit_y)
                fire = False

            check_x_1 = startShell[0] <= xloc + bar_width
            check_x_2 = startShell[0] >= xloc

            check_y_1 = startShell[1] <= display_height
            check_y_2 = startShell[1] >= display_height - ranHeight

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                print("Last shell:", startShell[0], startShell[1])
                hit_x = int((startShell[0]))
                hit_y = int(startShell[1])
                print("Impact:", hit_x, hit_y)
                explosion(hit_x, hit_y)
                fire = False

            pygame.display.update()
            clock.tick(60)
        return damage


    def power(level):
        text = s_font.render("Power: " + str(level) + "%", True, wheat)
        game_layout_display.blit(text, [display_width / 2, 0])


    def game_intro():
        intro = True

        while intro:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        intro = False
                    elif event.key == pygame.K_q:

                        pygame.quit()
                        

            game_layout_display.fill(black)
            msg_screen("Welcome to Tanks War!", white, -100, size="large")
            msg_screen("The goal is to shoot and destroy", wheat, 15)
            msg_screen("the enemy tank before they destroy you.", wheat, 60)
            msg_screen("The more enemies you destroy, the highest score you get.", wheat, 110)
            msg_screen("Enjoy Playing", wheat, 280)
            # msg_screen("Press C to play, P to pause or Q to quit",black,180)


            btn("Play", 150, 500, 100, 50, wheat, light_green, action="play",size="vsmall")
            btn("Controls", 350, 500, 100, 50, wheat, light_yellow, action="controls",size="vsmall")
            btn("Quit", 550, 500, 100, 50, wheat, light_red, action="quit",size="vsmall")

            pygame.display.update()

            clock.tick(15)


    def game_over():
        game_over = True

        while game_over:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()

            game_layout_display.fill(black)
            msg_screen("Game Over", white, -100, size="large")
            msg_screen("You died.", wheat, -30)

            btn("Play Again", 150, 500, 150, 50, wheat, light_green, action="play")
            btn("Controls", 350, 500, 100, 50, wheat, light_yellow, action="controls")
            btn("Quit", 550, 500, 100, 50, wheat, light_red, action="quit")

            pygame.display.update()

            clock.tick(15)


    def you_win():
        win = True

        while win:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()

            game_layout_display.fill(black)
            msg_screen("You won!", white, -100, size="large")
            msg_screen("Congratulations!", wheat, -30)

            btn("play Again", 150, 500, 150, 50, wheat, light_green, action="play")
            btn("controls", 350, 500, 100, 50, wheat, light_yellow, action="controls")
            btn("quit", 550, 500, 100, 50, wheat, light_red, action="quit")

            pygame.display.update()

            clock.tick(15)

    def health_bars(p_health, e_health):
        if p_health > 75:
            p_health_color = green
        elif p_health > 50:
            p_health_color = yellow
        else:
            p_health_color = red

        if e_health > 75:
            e_health_color = green
        elif e_health > 50:
            e_health_color = yellow
        else:
            e_health_color = red

        pygame.draw.rect(game_layout_display, p_health_color, (680, 25, p_health, 25))
        pygame.draw.rect(game_layout_display, e_health_color, (20, 25, e_health, 25))


    def gameLoop():
        gExit = False
        gOver = False
        FPS = 15

        p_health = 100
        e_health = 100

        bar_width = 50

        mTankX = display_width * 0.9
        mTankY = display_height * 0.9
        tnkMove = 0
        curTurPost = 0
        changeTurs = 0

        eTankX = display_width * 0.1
        eTankY = display_height * 0.9

        f_power = 50
        p_change = 0

        xloc = (display_width / 2) + random.randint(-0.1 * display_width, 0.1 * display_width)
        ranHeight = random.randrange(display_height * 0.1, display_height * 0.6)

        while not gExit:

            if gOver == True:
                # gameDisplay.fill(white)
                msg_screen("Game Over", red, -50, size="large")
                msg_screen("Press C to play again or Q to exit", black, 50)
                pygame.display.update()
                while gOver == True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            gExit = True
                            gOver = False

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_c:
                                gameLoop()
                            elif event.key == pygame.K_q:

                                gExit = True
                                gOver = False

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    gExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        tnkMove = -5

                    elif event.key == pygame.K_RIGHT:
                        tnkMove = 5

                    elif event.key == pygame.K_UP:
                        changeTurs = 1

                    elif event.key == pygame.K_DOWN:
                        changeTurs= -1

                    elif event.key == pygame.K_p:
                        pause()

                    elif event.key == pygame.K_SPACE:

                        damage = playerfireShell(gun, mTankX, mTankY, curTurPost, f_power, xloc, bar_width,
                                           ranHeight, eTankX, eTankY)
                        e_health -= damage

                        posMovement = ['f', 'r']
                        moveInd = random.randrange(0, 2)

                        for x in range(random.randrange(0, 10)):

                            if display_width * 0.3 > eTankX > display_width * 0.03:
                                if posMovement[moveInd] == "f":
                                    eTankX += 5
                                elif posMovement[moveInd] == "r":
                                    eTankX -= 5

                                game_layout_display.fill(black)
                                health_bars(p_health, e_health)
                                gun = tank(mTankX, mTankY, curTurPost)
                                e_gun = computer_tank(eTankX, eTankY, 8)
                                f_power += p_change

                                power(f_power)

                                barrier(xloc, ranHeight, bar_width)
                                game_layout_display.fill(green,
                                                 rect=[0, display_height - grnd_height, display_width, grnd_height])
                                pygame.display.update()

                                clock.tick(FPS)

                        damage = computerfireShell(e_gun, eTankX, eTankY, 8, 50, xloc, bar_width,
                                             ranHeight, mTankX, mTankY)
                        p_health -= damage

                    elif event.key == pygame.K_a:
                        p_change = -1
                    elif event.key == pygame.K_d:
                        p_change = 1

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        tnkMove = 0

                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        changeTurs = 0

                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        p_change = 0

            mTankX += tnkMove

            curTurPost += changeTurs

            if curTurPost > 8:
                curTurPost = 8
            elif curTurPost < 0:
                curTurPost = 0

            if mTankX - (tnk_width / 2) < xloc + bar_width:
                mTankX += 5

            game_layout_display.fill(black)
            health_bars(p_health, e_health)
            gun = tank(mTankX, mTankY, curTurPost)
            e_gun = computer_tank(eTankX, eTankY, 8)

            f_power += p_change

            if f_power > 100:
                f_power = 100
            elif f_power < 1:
                f_power = 1

            power(f_power)

            barrier(xloc, ranHeight, bar_width)
            game_layout_display.fill(green, rect=[0, display_height - grnd_height, display_width, grnd_height])
            pygame.display.update()

            if p_health < 1:
                game_over()
            elif e_health < 1:
                you_win()
            clock.tick(FPS)

        pygame.quit()
        #quit()
        return

    game_intro()
    gameLoop()

#car racing
def car_racing(who):
    import pygame
    import time
    import random
    import os
    # ector
    # mydb = mysql.connector.connect(
    #     host = "localhost",
    #   import mysql.conn  user = "root", 
    #     password = "",
    #     database = "games"
    # )
    # mycursor = mydb.cursor()


    pygame.init()

    screen_width = 400
    screen_height = 600

    btn_starting_x = 75
    nw_gm_y = 400
    exit_y = 460
    btn_width = 242
    btn_height = 50

    black_color = (0, 0, 0)
    white_color = (255, 255, 255)
    red_color = (255, 0, 0)
    redLight_color = (255, 21, 21)
    gray_color = (112, 128, 144)
    green_color = (0, 255, 0)
    greenLight_color = (51, 255, 51)
    blue_color = (0, 0, 255)

    game_layout_display= pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('F1 Race Road Game')
    time_clock=pygame.time.Clock()

    car_photo = pygame.image.load(os.getcwd() + '\\images/car.png')
    left_c = pygame.image.load(os.getcwd() + '\\images/car_left.png')
    right_c = pygame.image.load(os.getcwd() + '\\images/car_right.png')
    photo_obstacle = pygame.image.load(os.getcwd() + '\\images/obstacle.png')
    texture_photo = pygame.image.load(os.getcwd() + '\\images/texture.png')
    (c_width, c_height) = car_photo.get_rect().size
    (c_left_width, c_left_height) = left_c.get_rect().size
    (c_right_width, c_right_height) = right_c.get_rect().size
    (t_width, t_height) = photo_obstacle.get_rect().size
    (txtwidth, txtheight) = texture_photo.get_rect().size

    icon = pygame.image.load(os.getcwd() + '\\images/logo.png')
    pygame.display.set_icon(icon)

    image_background = pygame.image.load(os.getcwd() + '\\images/background.png')
    image_background_still = pygame.image.load(os.getcwd() + '\\images/background_inv.png')
    bckgrndRect = image_background.get_rect()

    #welcome_1 = pygame.mixer.Sound(os.getcwd() + '\\audio/intro1.wav')
    #welcome_2 = pygame.mixer.Sound(os.getcwd() + '\\audio/intro2.wav')
    #audio_crash = pygame.mixer.Sound(os.getcwd() + '\\audio/car_crash.wav')
    #audio_ignition = pygame.mixer.Sound(os.getcwd() + '\\audio/ignition.wav')
    #pygame.mixer.music.load(os.getcwd()+'\\audio/running.wav')

    def things_dodged(counting, highest_score, everything_speed):
            fnt = pygame.font.SysFont(None, 25)
            score = fnt.render("Dodged: " + str(counting), True, green_color)
            h_score = fnt.render("High Score: " + str(highest_score), True, green_color)
            speed = fnt.render("Speed: " + str(everything_speed) + "Km/h", True, green_color)
            game_layout_display.blit(score, (10, 0))
            game_layout_display.blit(h_score, (10, 27))
            game_layout_display.blit(speed, (screen_width - 125, 0))

    def high_score_update(dodged):
            high_scores = open(os.getcwd()+'\\textfile/high_score.txt', 'w')
            temperd = str(dodged)
            high_scores.write(temperd)

    def things(th_x, th_y):
            game_layout_display.blit(photo_obstacle, (th_x, th_y))

    def car(x, y, direction):
            if direction==0:
                    game_layout_display.blit(car_photo, (x, y))
            if direction==-1:
                    game_layout_display.blit(left_c, (x, y))
            if direction==1:
                    game_layout_display.blit(right_c, (x, y))

    def text_objects(text, font, color):
            txtSurf = font.render(text, True, color)
            return txtSurf, txtSurf.get_rect()

    def message_display_screen(txt, sh_x, sh_y, color, time_sleeping):
            lar_txt = pygame.font.Font('freesansbold.ttf',50)
            txtSurf, TxtRect = text_objects(txt, lar_txt, color)
            TxtRect.center = ((screen_width / 2 - sh_x), (screen_height / 2 - sh_y))
            game_layout_display.blit(txtSurf, TxtRect)
            pygame.display.update()
            time.sleep(time_sleeping)

    def title_message_display(sh_x, sh_y, color):
            lar_txt = pygame.font.Font('freesansbold.ttf',60)
            txtSurf, TxtRect = text_objects("F1 RaceRoad", lar_txt, color)
            TxtRect.center = ((screen_width / 2 - sh_x), (screen_height / 3 - sh_y))
            game_layout_display.blit(txtSurf, TxtRect)
            time.sleep(0.15)
            pygame.display.update()

    def title_msg():
            animation_height=screen_height
            #pygame.mixer.Sound.play(welcome_1)
            while animation_height > -600:
                    game_layout_display.fill(white_color)
                    things(screen_width / 2 - t_width / 2, animation_height)
                    animation_height-=1.5
                    pygame.display.update()
            title_message_display(0, 0, black_color)
            time.sleep(0.1)
            #pygame.mixer.Sound.play(welcome_2)

    def motion_texture(th_starting):
            game_layout_display.blit(texture_photo, (0, th_starting - 400))
            game_layout_display.blit(texture_photo, (0, th_starting))
            game_layout_display.blit(texture_photo, (0, th_starting + 400))

    def crash_function():
            #pygame.mixer.music.stop()
            #pygame.mixer.Sound.play(audio_crash)
            message_display_screen("YOU CRASHED", 0, 0, red_color, 0)
            while True:
                    playAgain = button("Play Again", btn_starting_x, nw_gm_y, btn_width, btn_height, greenLight_color, green_color)
                    exit_game = button("Quit", btn_starting_x, exit_y, btn_width, btn_height, redLight_color, red_color)
                    for event in pygame.event.get():
                            if event.type == pygame.QUIT or exit_game == 1 or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                    pygame.quit()
                                    return
                            if playAgain== 1 or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                                    looping_gameplay()
                    pygame.display.update()
                    time_clock.tick(15)

    def button(messages, x, y, wid, hei, in_act_color, act_color, action=None):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x + wid > mouse[0] > x and y+hei > mouse[1] > y:
                    pygame.draw.rect(game_layout_display, act_color, (x, y, wid, hei))
                    if click[0] == 1:
                            return 1
            else:
                    pygame.draw.rect(game_layout_display, in_act_color, (x, y, wid, hei))

            small_txt = pygame.font.Font('freesansbold.ttf',20)
            TxtSurf, TxtRect = text_objects(messages, small_txt, white_color)
            TxtRect.center = ((x + wid / 2), (y + hei / 2))
            game_layout_display.blit(TxtSurf, TxtRect)

    def welcome_gameplay():
            welcome = True
            game_layout_display.fill(white_color)
            title_msg()
            exit_game=0
            while welcome:
                    for event in pygame.event.get():
                            if event.type == pygame.QUIT or exit_game == 1 or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                    pygame.quit()
                                    
                    playGame = button("New game", btn_starting_x, nw_gm_y, btn_width, btn_height, greenLight_color, green_color)
                    exit_game = button("Quit", btn_starting_x, exit_y, btn_width, btn_height, redLight_color, red_color)
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                    exit_game = 1
                    if playGame or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                            welcome = False

                    pygame.display.update()
                    time_clock.tick(15)

    def counting_three_two_one():
            counting = 3
            #pygame.mixer.music.pause()
            #pygame.mixer.Sound.play(audio_ignition)
            while counting >= 0:
                    game_layout_display.blit(image_background, bckgrndRect)
                    car(screen_width * 0.40, screen_height * 0.6, 0)
                    if counting == 0:
                            message_display_screen ("GO!", 0, 0, green_color, 0.75)
                            #pygame.mixer.music.play(-1)
                    else:
                            message_display_screen (str(counting), 0, 0, red_color, 0.75)
                    counting -= 1
            time_clock.tick(15)

    def gameplay_paused():
            #pygame.mixer.music.pause()
            pause = True
            while pause:
                    for event in pygame.event.get():
                            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):  ###############or quit_game == 1
                                    pygame.quit()
                                    
                            message_display_screen("pause", 0, 0, blue_color, 1.5)
                            if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:
                                            #pygame.mixer.music.unpause()
                                            return
                    pygame.display.update()
                    time_clock.tick(15)

    def looping_gameplay():
            #pygame.mixer.music.play(-1)
            display = 0
            width_x=(screen_width * 0.4)
            height_y=(screen_height * 0.6)
            ch_x=0

            th_st_x = random.randrange(8, screen_width - t_width - 8)
            th_st_y = -600
            th_speed = 5

            tracking_y = 0
            tracking_speed = 25

            dodg=0
            direction = 0

            highest_score_txtfile = open(os.getcwd()+'/textfile/high_score.txt','r')
            high_score = highest_score_txtfile.read()

            gameExit = False
            counting_three_two_one()

            mycursor.execute("SELECT * from `user` WHERE username = ?", (who, ))
            myresult = mycursor.fetchone()
            Highscore = myresult[6]

            while not gameExit:
                    for event in pygame.event.get():
                            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                    pygame.quit()
                                    
                            if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                            ch_x = -10
                                            direction = -1
                                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                            ch_x = 10
                                            direction = 1
                                    if event.key == pygame.K_SPACE:
                                            gameplay_paused()
                            if event.type == pygame.KEYUP:
                                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                                            ch_x = 0
                                            direction = 0
                    width_x+=ch_x
                    game_layout_display.blit(image_background, bckgrndRect)

                    motion_texture(th_st_y)
                    things(th_st_x, th_st_y)
                    th_st_y += th_speed
                    car(width_x,height_y,direction)

                    things_dodged(dodg, high_score, th_speed)
                    if width_x > screen_width - c_width or width_x < 0:
                            crash_function()
                    if th_st_y > screen_height:
                            th_st_y = 0 - t_height
                            th_st_x = random.randrange(0, screen_width)
                            dodg += 1
                            th_speed += 1

                    if Highscore>dodg:
                        sql = f"UPDATE `user` SET `car-score` = '{Highscore}' WHERE `user`.`username` = '{who}'"
                        mycursor.execute(sql)
                        mydb.commit()
                    elif Highscore<dodg:
                        sql = f"UPDATE `user` SET `car-score` = '{dodg}' WHERE `user`.`username` = '{who}'"
                        mycursor.execute(sql)
                        mydb.commit()
                            
                    if dodg > int(high_score):
                            high_score_update(dodg)
                    if height_y < th_st_y+t_height-15 and width_x > th_st_x-c_width-5 and width_x < th_st_x+t_width-5:
                            crash_function()

                    pygame.display.update()
                    time_clock.tick(60)

    welcome_gameplay()
    looping_gameplay()
    pygame.quit()
    return

# to hide a widget
def hide_widget(*Widget):
    for item in Widget:
        item.place_forget()

# to show a widget
def show_widget(*Widget):
    for item in Widget:
        item.place(anchor = "c", relx = 0.5, rely = 0.5)

# function to clear the entry area after user inputs
def clear_entry(*boxes):
    for item in boxes:
        item.delete(0, END)

# To show register box and disappear login box
def appear_register(widget1, widget2, canvas):
    global change_button, change_text, change_message
    hide_widget(widget1)
    show_widget(widget2)
    canvas.delete(change_button, change_text, change_message)
    change_text = canvas.create_text(640, 180, text = "REGISTER", fill="#00FFFF", font = font3)
    change_message = canvas.create_text(650, 550, text = "Have account? ", fill="#00FFFF", font = font2)
    change_button = canvas.create_window(860, 550, window = Button(canvas, text = "Login", font = font2, bg = "#FFFF00", command = lambda : appear_login(login_box, register_box, canvas)))

#To show login box and dissapear register box
def appear_login(widget1, widget2, canvas):
    global change_button, change_text, change_message
    hide_widget(widget2)
    show_widget(widget1)
    canvas.delete(change_button, change_text, change_message)
    change_text = canvas.create_text(640, 200, text = "LOGIN", fill="#00FFFF", font = font3)
    change_message = canvas.create_text(700, 500, text = "New user ?", fill="#00FFFF", font = font2)
    change_button = canvas.create_window(840, 500, window = Button(canvas, text = "Sign Up", font = font2, bg = "#FFFF00", command = lambda : appear_register(login_box, register_box, canvas)))

'''#To show forgot box and disappear login box
def appear_forgot(widget1, widget2, canvas):
    global change_button, change_text, change_message
    hide_widget(widget1)
    show_widget(widget2)
    canvas.delete(change_button, change_text, change_message)
    change_text = canvas.create_text(640, 200, text = "FORGOT PASSWORD?", fill="#00FFFF", font = font3)
    change_message = canvas.create_text(500, 500, text = "Got Password?", fill="#00FFFF", font = font2)
    change_button = canvas.create_window(860, 500, window = Button(canvas, text = "Login", font = font2, bg = "#FFFF00", command = lambda : appear_login(login_box, register_box, canvas)))'''
    

#Function to feed the information of register to the database 
def register():
    global current_user
    user, phn, pas, re_pass, sq, sa = new_userentry.get().strip(), new_mobentry.get().strip(), new_passentry.get().strip(), re_passentry.get().strip(), s_ques.get(), s_ans.get().upper()
    invalid_register.grid_forget()
    if user and phn and pas and re_pass:
        if pas != re_pass:
            invalid_register.grid(row = 2, column = 2)
            return
        else:
            if s_ans != "":
                sql = "SELECT username FROM user"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                result = [i[0] for i in myresult]
                if user not in result:
                    sql = "INSERT INTO user (username, phone, password, squestion, sanswer) VALUES (?, ?, ?, ?, ?)"
                    val = (user, int(phn), pas, sq, sa) 
                    mycursor.execute(sql, val)
                    mydb.commit()
                    current_user = user
                    menu()
                else:
                    invalid_register.grid(row = 0, column = 2)
            else:
                invalid_register.grid(row = 4, column = 2)
    else:
        invalid_register.grid(row = 0, column = 2)
        
    clear_entry(new_userentry, new_mobentry, new_passentry, re_passentry)

# Funcion to Check Login related querry
def login():
    global current_user
    invalid_user.grid_forget()
    user, pas = userentry.get().strip(), passentry.get().strip()
    if user and pas:
        sql = "SELECT username, password FROM user"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        userlist = [i[0] for i in myresult]
        passwordlist = [i[1] for i in myresult]
        if user in userlist:
            index = userlist.index(user)
            if pas == passwordlist[index]:
                current_user = user
                menu()
            else:
                invalid_user.grid(row = 1, column = 2)

        elif user=="admin" and pas=="12345":
            # import mysql.connector
            import tkinter  as tk
            from PIL import ImageTk, Image
            
            my_w = tk.Tk()
            my_w.title("Admin Panel")
            my_w.geometry("400x250")
            my_w['bg']="#00FF00"
            # my_connect = mysql.connector.connect(
            #     host="localhost",
            #     user="root", 
            #     passwd="",
            #     database="games"
            #     )
            # my_conn = my_connect.cursor()
            ####### end of connection ####

            # e=Label(my_w,width=20,text='id',borderwidth=2, relief='ridge',anchor='w',bg='#FFFF00')
            e=Label(my_w,width=15,text='Username',borderwidth=2, relief='ridge',anchor='w',bg='#FFFF00', fg="#FF0000")
            e.grid(row=0,column=0)
            e=Label(my_w,width=15,text='Password',borderwidth=2, relief='ridge',anchor='w',bg='#FFFF00', fg="#FF0000")
            e.grid(row=0,column=1)
            e=Label(my_w,width=15,text='Mobile No.',borderwidth=2, relief='ridge',anchor='w',bg='#FFFF00', fg="#FF0000")
            e.grid(row=0,column=2)
            e=Label(my_w,width=15,text='Question',borderwidth=2, relief='ridge',anchor='w',bg='#FFFF00', fg="#FF0000")
            e.grid(row=0,column=3)
            e=Label(my_w,width=15,text='Answer',borderwidth=2, relief='ridge',anchor='w',bg='#FFFF00', fg="#FF0000")
            e.grid(row=0,column=4)
            e=Label(my_w,width=15,text='Fruit Score',borderwidth=2, relief='ridge',anchor='w',bg='#FFFF00', fg="#FF0000")
            e.grid(row=0,column=5)
            e=Label(my_w,width=15,text='Car Score',borderwidth=2, relief='ridge',anchor='w',bg='#FFFF00', fg="#FF0000")
            e.grid(row=0,column=6)
            e=Label(my_w,width=15,text='Date',borderwidth=2, relief='ridge',anchor='w',bg='#FFFF00', fg="#FF0000")
            e.grid(row=0,column=7)
            e=Label(my_w,width=15,text='Time',borderwidth=2, relief='ridge',anchor='w',bg='#FFFF00', fg="#FF0000")
            e.grid(row=0,column=8)

            my_conn = mycursor
            my_conn.execute("SELECT * FROM user limit 0,10")
            i=1
            for student in my_conn: 
                for j in range(len(student)):
                    e = Entry(my_w, width=18, fg='blue')
                    e.configure({"background": "#FFA1FF"})
                    e.grid(row=i, column=j) 
                    e.insert(END, student[j])
                i=i+1
            my_w.mainloop()
            
                
        else:
            invalid_user.grid(row = 0, column = 2)
    clear_entry(userentry, passentry)

def forget():
    def change(name, pas, ans, inp):
        if inp.upper() == ans.upper():
            mycursor.execute(f"update user set password = '{pas.get()}' where username = '{name.get()}'")
            mydb.commit()
            messagebox.showinfo(" ", f"Password changed! {name.get()}  {pas.get()}") 
            register_screen.destroy()
        else:
            messagebox.showinfo(" ", "Please enter correct answer.")

    def go_check(rs, name, phone):
        answer = StringVar()
        password = StringVar()
        a = mycursor.execute(f"select * from user where username = '{name.get()}' and phone = '{phone.get()}'").fetchone()
        if a:
            ques = a[3]
            ans = a[4]
            Label(rs,text=f"What is your favourite {ques}").pack(pady = 10)
            pass2=Entry(rs,textvariable=answer).pack()
            
            Label(rs, text = "Enter new password *").pack()
            ent = Entry(rs, textvariable = password, show = "*").pack(pady = 10)

            Button(rs,text="Change",bg="purple",fg="white",command= lambda : change(name, password, ans, answer.get())).pack(pady = 10)
        else:
            messagebox.showinfo("ERROR", "Wrong username or phone number! ")

    name=StringVar()
    email = StringVar()
    register_screen=Toplevel(root)
    register_screen.title("Forgot Password Screen")
    register_screen.geometry("300x450")
    Label(register_screen,text="Forgot Password",height="2",width="300").pack()
    Label(text="").pack()
    Label(register_screen,text="User Name *").pack()
    name2=Entry(register_screen,textvariable=name)
    name2.pack(pady = 10)
    Label(register_screen,text="Mobile *").pack()
    pass2=Entry(register_screen,textvariable=email)
    pass2.pack(pady = 10)
    Button(register_screen,text="GO",bg="purple",fg="white",command= lambda : go_check(register_screen, name, email)).pack(pady = 10)



def menu():
    canvas.pack_forget()
    hide_widget(login_box, register_box)
    
    box = Frame(root )
    box.pack(fill = BOTH, expand = 1)

    def switch_window(From, To):
        From.grid_forget()
        To()

    #---------------------------------SELECT RELATED STUFF---------------------------------------------
    def select_func():
        select_box = Canvas(box, width = win_width-10, height = win_height-10, borderwidth = 4, relief = SUNKEN)
        select_box.grid(row = 0, column = 0)
        select_box.create_image((5, 5), image = bg0, anchor = "nw")
        play_fruit = select_box.create_window(1000, 150, window = Button(select_box, text = 'START', font = font3, bg = 'brown', borderwidth = 0, width = 10, fg = 'orange', command = lambda : switch_window(select_box, fruit_func)))
        play_tank = select_box.create_window(1000, 360, window = Button(select_box, text = 'START', font = font3, bg = '#bc1616', borderwidth = 0, width = 10, fg = '#030931', command = lambda : switch_window(select_box, tank_func)))
        play_car = select_box.create_window(1000, 600, window = Button(select_box, text = 'START', font = font3, bg = '#0000FF', borderwidth = 0, width = 10, fg = '#00FFFF', command = lambda : switch_window(select_box, car_func)))
        #head_1 = select_box.create_text((100, 100), text = "FRUIT NINJA", font = font3, fill = "#0c2920")
        #head_2 = select_box.create_text((350, 100), text = "POCKET TANKS", font = font3, fill = "#0c2920")
        head_3 = select_box.create_text((150, 600), text = "CAR\n RACING", font = font3, fill = "#00FFFF")

    #---------------------------------FRUIT RELATED STUFF----------------------------------------------

    def fruit_func():
        fruit = Canvas(box, width = win_width-10, height = win_height-10, borderwidth = 4, relief = SUNKEN)
        fruit.grid(row = 0, column = 0)
        fruit.create_image((5, 5) , image = bg2, anchor = "nw")
        play_fruit = fruit.create_window(500, 600, window = Button(fruit, text = "PLAY", font = font3, bg = '#bc1616', borderwidth = 0, width = 10, fg = '#030931', command = lambda : fruit_ninja(current_user))) 
        fruit.create_text((50, 50), text = "Instructions: \n*Use your mouse \n(hover the mouse) \nto slice the fruits \non the screen.*", font = font6, fill = "white", anchor = "nw")
        mycursor.execute("SELECT `username`, `fruit-score` FROM `user` ORDER BY `fruit-score` DESC")
        myresult = mycursor.fetchall()
        my_fruit_score = None
        #fruit_content = Label(fruit, relief = SUNKEN, borderwidth = 4)
        #fruit_v = Scrollbar(fruit_content)
        #fruit_v.pack(side = RIGHT, fill = Y)
        #fruit_t = Text(fruit_content, width = 22, height = 16, wrap = NONE, yscrollcommand = fruit_v.set, bg = "silver")
        #fruit_t.insert(END, "*****LEADERBOARD*****\n")
        #fruit_t.insert(END, "NAME\t\tSCORE\
        for name , score in myresult:
            #fruit_t.insert(END, f"{name}\t\t{score}\n")
            if name == current_user:
                my_fruit_score = score
        #fruit_t.pack(side = TOP, fill = X)
       # fruit_v.config(command = fruit_t.yview)
       # fruit.create_window(800, 170, window = fruit_content)
        fruit.create_text((1000, 100), text = f"Hello {current_user}, \nyour highscore is: {my_fruit_score}", font = font4, fill = "black", anchor = 'c')
        go_back_fruit = fruit.create_window(830, 600, window = Button(fruit, text = 'BACK', font = font3, bg = 'brown', borderwidth = 0, width = 10, fg = 'orange', command = lambda : switch_window(fruit, select_func)))



    #---------------------------------TANK RELATED STUFF----------------------------------------------
    def tank_func():
        tank = Canvas(box, width = win_width-10, height = win_height - 10, borderwidth = 5, relief = SUNKEN)
        tank.grid(row = 1, column = 0)
        tank.create_image((5, 5) , image = bg3, anchor = "nw")
        play_tank = tank.create_window(500, 600, window = Button(tank, text = 'PLAY', font = font3, bg = '#bc1616', borderwidth = 0, width = 10, fg = '#030931', command = lambda : pocket_tanks()))
        tank.create_text((50, 50), text = "Press play button to play and \nuse up,down,left,right arrow keys \n to move the tank and it's turret.", font = font6, fill = "white", anchor = "nw")
        mycursor.execute("SELECT `username` , `date` , `time` FROM user ORDER BY `date` DESC")
        myresult = mycursor.fetchall()
        #my_tank_score = 0
        #tank_content = Label(tank, relief = SUNKEN, borderwidth = 4)
        #tank_v = Scrollbar(tank_content)
        #tank_v.pack(side = RIGHT, fill = Y)
        #tank_t = Text(tank_content, width = 22, height = 16, wrap = NONE, yscrollcommand = flappy_v.set, bg = "silver")
        #tank_t.insert(END, "*****LEADERBOARD*****\n")
        #tank_t.insert(END, "NAME\t\tSCORE\n")
        for name , date , time in myresult:
           # tank_t.insert(END, f"{name}\t\t{score}\n")
            if name == current_user:
                DATE = date
                TIME = time
        #tank_t.pack(side = TOP, fill = X)
        #tank_v.config(command = tank_t.yview)
        #tank.create_window(800, 170, window = tank_content)
        tank.create_text((1000, 100), text = f"Hello {current_user} \nHope you \nenjoy", font = font5, fill = "#FFFFFF", anchor = 'c')
        #, \nthe last time you played \nwas on %s \n at %s %(DATE,TIME)
        go_back_tank = tank.create_window(830, 600, window = Button(tank, text = 'BACK', font = font3, bg = 'brown', borderwidth = 0, width = 10, fg = 'orange', command = lambda : switch_window(tank, select_func)))


   #--------------------------------CAR RELATED STUFF----------------------------------------------
    def car_func():
        car = Canvas(box, width = win_width-10, height = win_height-10, borderwidth = 5, relief = SUNKEN)
        car.grid(row = 2, column = 0)
        car.create_image((5, 5) , image = bg4, anchor = "nw")
        play_car = car.create_window(500, 600, window = Button(car, text = "PLAY", font = font3, bg = '#0a195c', borderwidth = 0, width = 10, fg = '#d02b7b', command = lambda : car_racing(current_user))) 
        car.create_text((40, 150), text = "INSTRUCTIONS: \nUse Left/Right arrow keys or \nA/S alphabet \nkeys to move your car sideways. \nAvoid crashing with other cars \n to gain more points.*", font = font6, fill = "#00fba7", anchor = "nw")
        mycursor.execute("SELECT `username` , `car-score` FROM `user` ORDER BY `car-score` ASC")
        myresult = mycursor.fetchall()
        my_car_score = None
        #car_content = Label(car, relief = SUNKEN, borderwidth = 4)
        #car_v = Scrollbar(car_content)
        #car_v.pack(side = RIGHT, fill = Y)
        #car_t = Text(car_content, width = 22, height = 16, wrap = NONE, yscrollcommand = car_v.set, bg = "silver")
        #car_t.insert(END, "*****LEADERBOARD*****\n")
        #car_t.insert(END, "NAME\t\tSCORE\n")
        #car_t.insert(END, "\n")
        for name, score in myresult:
         #   car_t.insert(END, f"{name}\t\t{score}\n")
            if name == current_user:
                my_car_score = score 
        #car_t.pack(side = TOP, fill = X)
        #car_v.config(command = car_t.yview)
        #car.create_window(800, 170, window = car_content)
        car.create_text((1000, 100), text = f"Hello {current_user}, \nyour score is: {my_car_score}", font = font4, fill = "black", anchor = 'c')
        go_back_car = car.create_window(830, 600, window = Button(car, text = 'BACK', font = font3, bg = 'brown', borderwidth = 0, width = 10, fg = 'orange', command = lambda : switch_window(car, select_func)))
    
    select_func()

#-------------------------------------------------------INTRO PAGE---------------------------------------------------------------------

bg1 = Image.open("pictures/background.png")
bg1 = ImageTk.PhotoImage(bg1)
canvas = Canvas(root, width = win_width, height = win_height, bg = "white" )
canvas.pack(fill = "both")
canvas.create_image(0, 0, image = bg1, anchor = "nw")
canvas.create_text(640, 60, text = "Games Mania", fill="#FAFA33", font = font1)
change_text = canvas.create_text(640, 200, text = "LOGIN", fill="#00FFFF", font = font3)
change_message = canvas.create_text(700, 500, text = "New user ?", fill="#00FFFF", font = font2)
change_button = canvas.create_window(840, 500, window = Button(canvas, text = "Sign Up", font = font2, bg = "#FFFF00", command = lambda : appear_register(login_box, register_box, canvas)))

#login box
login_box = Frame(root, width = 500, height = 200, borderwidth = 5, relief = SUNKEN ,bg="#FFC0CB")
login_box.place(anchor = "c", relx = 0.5, rely = 0.5)

username = Label(login_box, text = "Username", fg="#0000FF", font = "Sans 15 bold", padx = 10, pady = 40 ,bg="#FFC0CB")
password = Label(login_box, text = "Password", fg="#0000FF", font = "Sans 15 bold", padx = 10 ,bg="#FFC0CB") 
userentry = Entry(login_box, textvariable = uservalue, width = 40, fg = "#312e2e", font = "consolas 10")
passentry = Entry(login_box, textvariable = passvalue, width = 40, fg = "#312e2e", show = "*", font = "consolas 10" )

username.grid(row = 0, column = 0)
password.grid(row = 1, column = 0)
userentry.grid(row = 0, column = 1, padx = 10)
passentry.grid(row = 1, column = 1, padx = 10)

Button(login_box, text = "Login", font = font2, bg = "#FFA500", command = login ).grid(row = 2 , column = 2, pady = 10, padx = 2)
Button(login_box, text = "Forgot Password", font = font2, bg = "#FFA500", command = forget ).grid(row = 2 , column = 0, pady = 10, padx = 2)

# TODO: TO PRINT INVALID MESSAGE WHEN USER INPUT WRONG DATA 
invalid_user = Label(login_box, text = "*invalid", font = "Sans 10", fg = "red")
# invalid.grid(row = 0, column = 2)


# Register box
register_box = Frame(root, width = 500, height = 200, borderwidth = 5, relief = SUNKEN, bg="#FFC0CB")
#register_box.place(anchor = "c", relx = 0.5, rely = 0.5)

new_username = Label(register_box, text = "Username", fg="#0000FF", font = "Sans 15 bold", padx = 10, pady = 40, bg="#FFC0CB")
new_mob=Label(register_box, text= "Mobile no.", fg="#0000FF", font = "Sans 15 bold", padx=10, bg="#FFC0CB")
new_password = Label(register_box, text = "Password", fg="#0000FF", font = "Sans 15 bold", padx = 10, bg="#FFC0CB")
re_password = Label(register_box, text = "Confirm password", fg="#0000FF", font = "Sans 15 bold", padx = 10, bg="#FFC0CB")
question = Label(register_box, text = "Security Question", fg = "#0000FF", font = "Sans 15 bold", padx = 10, bg="#FFC0CB")
answer = Label(register_box, text = "Answer", fg = "#0000FF", font = "Sans 15 bold", padx = 10, bg="#FFC0CB")

new_userentry = Entry(register_box, textvariable = new_uservalue, width = 40, fg = "#312e2e", font = "consolas 10")
new_mobentry=Entry(register_box, textvariable = new_mobvalue, width = 40, fg = "#312e2e", font = "consolas 10")
new_passentry = Entry(register_box, textvariable = new_passvalue, width = 40, fg = "#312e2e",  show = "*", font = "consolas 10" )
re_passentry = Entry(register_box, textvariable = re_passvalue, width = 40, fg = "#312e2e", show = "*", font = "consolas 10" )
questions = ['Food', 'Place', 'color', 'Singer', 'Animal', 'Bird', 'Sport']
question_inp = OptionMenu(register_box, s_ques, *questions)
s_ques.set(questions[0])
ans_inp = Entry(register_box, textvariable = s_ans,  width = 40, fg = "#312e2e", show = "*", font = "consolas 10")

new_username.grid(row = 0, column = 0)
new_userentry.grid(row = 0, column = 1, padx = 5)
new_mob.grid(row = 1, column = 0)
new_mobentry.grid(row = 1, column = 1)
new_password.grid(row = 2, column = 0)
new_passentry.grid(row = 2, column = 1, padx = 5)
re_password.grid(row = 3, column = 0)
re_passentry.grid(row = 3, column = 1)
question.grid(row = 4, column = 0)
question_inp.grid(row = 4, column = 1, sticky = E)
Label(register_box, text= "What is your favourite", fg = "black", font = "Sans 12 bold", padx = 10, bg="#FFC0CB").grid(row = 4, column = 1, sticky = W)
answer.grid(row = 5, column = 0)
ans_inp.grid(row = 5, column = 1)

Button(register_box, text = "Sign Up", font = font2, bg = "#FFA500", command = lambda : register()).grid(row = 6 , column = 2, pady = 10, padx = 2)

# TODO: TO PRINT INVALID MESSAGE WHEN USER INPUT WRONG DATA 
invalid_register = Label(register_box, text = "*invalid", font = "Sans 10", fg = "red")
# invalid.grid(row = 0, column = 2)


root.mainloop()







