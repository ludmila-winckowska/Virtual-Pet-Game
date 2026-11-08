import pygame
import random #Random numbers (movement, effects, random behavior)
import math #Math (sin and cos for smooth movement and oscillations)
from datetime import datetime, timedelta #Allows the game to read the computer clock
import json
import os

def run_game():

    pygame.init()#Initialize Pygame graphics, windows, and input
    pygame.mixer.init()#Initialize the audio mixer separately

    screen = pygame.display.set_mode((500,600))
    pygame.display.set_caption("Virtual Pet Game")

    def scale_to_fit(img, max_w, max_h):
        w, h = img.get_size()
        scale = min(max_w / w, max_h / h)
        new_size = (int(w * scale), int(h * scale))
        return pygame.transform.scale(img,new_size)

    class Button:
        def __init__(
            self,
            image,
            pos,
            hover_scale=1.12,
            hitbox_scale=1.0
        ):
            #Original button image
            self.image = image
            #Button coordinates
            self.pos = pos
            #Button rectangle for clicks and hover
            self.rect = self.image.get_rect(topleft=pos)
            #Smaller mouse interaction area
            self.hit_rect = self.rect.copy()
            self.hit_rect.width = int(self.rect.width * hitbox_scale)
            self.hit_rect.height = int(self.rect.height * hitbox_scale)
            self.hit_rect.center = self.rect.center
            #Original button size
            w, h = self.image.get_size()
            #Enlarged button image on hover
            self.hover_image = pygame.transform.scale(
                self.image,
                (int(w * hover_scale), int(h* hover_scale)))
            #Keep the enlarged button centered on the original
            self.hover_rect = self.hover_image.get_rect(center=self.rect.center)
        def is_hover(self, mouse_pos):
            #Check whether the mouse is over the button
            return self.hit_rect.collidepoint(mouse_pos)
        def is_clicked(self, event):
            #Check whether the button was clicked
            return (event.type == pygame.MOUSEBUTTONDOWN
                    and self.hit_rect.collidepoint(event.pos))
        def draw(self, screen):
            #Mouse position
            mouse_pos = pygame.mouse.get_pos()
            #Draw an enlarged button when hovered
            if self.is_hover(mouse_pos):
                screen.blit(self.hover_image, self.hover_rect)
                #Otherwise draw the original button
            else: screen.blit(self.image, self.rect)
                                                                            
    #Images
    main_bg = pygame.image.load("images/bg_04.png").convert()#Main room background
    main_bg = pygame.transform.scale(main_bg, (500,600))
    main_bg_evening = pygame.image.load("images/bg_07.png").convert()#Evening main room background
    main_bg_evening = pygame.transform.scale(main_bg_evening, (500, 600))
    food_bg = pygame.image.load("images/bg_05.png").convert()#Food room background
    food_bg = pygame.transform.scale(food_bg, (500, 600))
    food_bg_evening = pygame.image.load("images/bg_08.png").convert()#Evening food room background
    food_bg_evening = pygame.transform.scale(food_bg_evening, (500, 600))
    fun_bg = pygame.image.load("images/bg_02.png").convert()#Fun room background
    fun_bg = pygame.transform.scale(fun_bg,(500, 600))
    sleep_bg = pygame.image.load("images/bg_01.png").convert()#Nighttime sleep room background
    sleep_bg = pygame.transform.scale(sleep_bg, (500, 600))
    sleep_bg_day = pygame.image.load("images/bg_09.png").convert()#Daytime sleep room background 
    sleep_bg_day = pygame.transform.scale(sleep_bg_day, (500, 600))
    care_bg = pygame.image.load("images/bg_06.png").convert()#Care room background
    care_bg = pygame.transform.scale(care_bg, (500,600))
    care_bg_evening = pygame.image.load("images/bg_10.png").convert()#Evening care room background
    care_bg_evening = pygame.transform.scale(care_bg_evening, (500,600))

    pot_2 = pygame.image.load("images/pot_02.png").convert_alpha()#Flowerpot without arms
    pot_2 = scale_to_fit(pot_2, 270, 270)
    show_pot2 = False

    plant_26 = pygame.image.load("images/plant_26.png").convert_alpha()#Plant for main room
    plant_26 = scale_to_fit(plant_26, 290, 290)
    plant_38 = pygame.image.load("images/plant_38.png").convert_alpha()#Plant for main room
    plant_38 = scale_to_fit(plant_38, 290, 290)
    plant_26_care = pygame.image.load("images/plant_26.png").convert_alpha()#Plant for care room
    plant_26_care = scale_to_fit(plant_26_care, 260, 260)
    plant_38_care = pygame.image.load("images/plant_38.png").convert_alpha()#Plant for care room
    plant_38_care = scale_to_fit(plant_38_care, 260, 260)

    btn_food = pygame.image.load("images/btn_food.png").convert_alpha()#Food button
    btn_food = pygame.transform.scale (btn_food, (120, 99))
    btn_fun = pygame.image.load("images/btn_fun.png").convert_alpha()#Fun button
    btn_fun = pygame.transform.scale(btn_fun, (110, 45))
    btn_sleep = pygame.image.load("images/btn_sleep.png").convert_alpha()#Sleep button
    btn_sleep = pygame.transform.scale (btn_sleep, (120, 93))
    btn_care = pygame.image.load("images/btn_care.png").convert_alpha()#Care button
    btn_care = pygame.transform.scale (btn_care, (120, 90))

    plant_24 = pygame.image.load("images/plant_24.png").convert_alpha()#Plant for food room
    plant_24 = scale_to_fit(plant_24, 290, 290)
    plant_25 = pygame.image.load("images/plant_25.png").convert_alpha()#Plant for food room
    plant_25 = scale_to_fit(plant_25, 290, 290)
    plant_30 = pygame.image.load("images/plant_30.png").convert_alpha()#Plant for food room
    plant_30 = scale_to_fit(plant_30, 290, 290)
    plant_31 = pygame.image.load("images/plant_31.png").convert_alpha()#Plant for food room
    plant_31 = scale_to_fit(plant_31, 290, 290)

    plant_60 = pygame.image.load("images/plant_60.png").convert_alpha()#Plant for sleep room
    plant_60 = scale_to_fit(plant_60, 290, 290)
    plant_61 = pygame.image.load("images/plant_61.png").convert_alpha()#Plant for sleep room
    plant_61 = scale_to_fit(plant_61, 290, 290)

    plant_62 = pygame.image.load("images/plant_62.png").convert_alpha()#Plant for care room
    plant_62 = scale_to_fit(plant_62, 260, 260)
    plant_63 = pygame.image.load("images/plant_63.png").convert_alpha()#Plant for care room
    plant_63 = scale_to_fit(plant_63, 260, 260)

    plant_64 = pygame.image.load("images/plant_64.png").convert_alpha()#Plant for sleep room
    plant_64 = scale_to_fit(plant_64, 280, 280)
    plant_65 = pygame.image.load("images/plant_65.png").convert_alpha()#Plant for sleep room
    plant_65 = scale_to_fit(plant_65, 280, 280)
    plant_66 = pygame.image.load("images/plant_66.png").convert_alpha()#Plant for sleep room
    plant_66 = scale_to_fit(plant_66, 280, 280)
    plant_67 = pygame.image.load("images/plant_67.png").convert_alpha()#Plant for alarm animation
    plant_67 = scale_to_fit(plant_67, 280, 280)
    plant_68 = pygame.image.load("images/plant_68.png").convert_alpha()#Plant for alarm animation
    plant_68 = scale_to_fit(plant_68, 280, 280)
    plant_69 = pygame.image.load("images/plant_69.png").convert_alpha()#Plant for alarm animation
    plant_69 = scale_to_fit(plant_69, 280, 280)

    plant_53 = pygame.image.load("images/plant_53.png").convert_alpha()#Plant for fun room
    plant_53 = scale_to_fit(plant_53, 280, 280)
    plant_54 = pygame.image.load("images/plant_54.png").convert_alpha()#Plant for fun room
    plant_54 = scale_to_fit(plant_54, 280, 280)
    plant_55 = pygame.image.load("images/plant_55.png").convert_alpha()#Plant for fun room
    plant_55 = scale_to_fit(plant_55, 280, 280)
    plant_56 = pygame.image.load("images/plant_56.png").convert_alpha()#Plant for fun room 
    plant_56 = scale_to_fit(plant_56, 280, 280)
    plant_57 = pygame.image.load("images/plant_57.png").convert_alpha()#Plant for fun room
    plant_57 = scale_to_fit(plant_57, 280, 280)
    plant_58 = pygame.image.load("images/plant_58.png").convert_alpha()#Plant for fun room
    plant_58 = scale_to_fit(plant_58, 280, 280)
    plant_59 = pygame.image.load("images/plant_59.png").convert_alpha()#Plant for fun room
    plant_59 = scale_to_fit(plant_59, 280, 280)

    plant_70 = pygame.image.load("images/plant_70.png").convert_alpha()#Plant for care room
    plant_70 = scale_to_fit(plant_70, 305, 305)#Watering can
    plant_71 = pygame.image.load("images/plant_71.png").convert_alpha()#Plant for care room
    plant_71 = scale_to_fit(plant_71, 305, 305)#Watering can
    plant_72 = pygame.image.load("images/plant_72.png").convert_alpha()#Plant for care room
    plant_72 = scale_to_fit(plant_72, 320, 320)#Leaf misting
    plant_73 = pygame.image.load("images/plant_73.png").convert_alpha()#Plant for care room
    plant_73 = scale_to_fit(plant_73, 310, 310)#Leaf misting
    plant_43 = pygame.image.load("images/plant_43.png").convert_alpha()#Plant for care room
    plant_43 = scale_to_fit(plant_43, 270, 270)#Leaf shine
    plant_43_02 = pygame.image.load("images/plant_43_02.png").convert_alpha()#Plant for care room
    plant_43_02 = scale_to_fit(plant_43_02, 270, 270)#Leaf shine

    plant_51 = pygame.image.load("images/plant_51.png").convert_alpha()#Plant for main room
    plant_51 = scale_to_fit(plant_51, 290, 290)
    plant_52 = pygame.image.load("images/plant_52.png").convert_alpha()#Plant for main room
    plant_52 = scale_to_fit(plant_52, 290, 290)
    plant_74 = pygame.image.load("images/plant_74.png").convert_alpha()#Plant for main room
    plant_74 = scale_to_fit(plant_74, 290, 290)
    plant_75 = pygame.image.load("images/plant_75.png").convert_alpha()#Plant for main room
    plant_75 = scale_to_fit(plant_75, 290, 290)
    plant_74_care = pygame.image.load("images/plant_74.png").convert_alpha()#Plant for main room
    plant_74_care = scale_to_fit(plant_74_care, 260, 260)
    plant_75_care = pygame.image.load("images/plant_75.png").convert_alpha()#Plant for main room
    plant_75_care = scale_to_fit(plant_75_care, 260, 260)

    plant_37 = pygame.image.load("images/plant_37.png").convert_alpha()#Plant for main room
    plant_37 = scale_to_fit(plant_37, 290, 290)
    plant_37_1 = pygame.image.load("images/plant_37_1.png").convert_alpha()#Plant for main room
    plant_37_1 = scale_to_fit(plant_37_1, 290, 290)
    plant_37_care = pygame.image.load("images/plant_37.png").convert_alpha()#Plant for main room
    plant_37_care = scale_to_fit(plant_37_care, 260, 260)
    plant_37_1_care = pygame.image.load("images/plant_37_1.png").convert_alpha()#Plant for main room
    plant_37_1_care = scale_to_fit(plant_37_1_care, 260, 260)

    btn_05 = pygame.image.load("images/btn_05.png").convert_alpha()#Soup
    btn_05 = pygame.transform.scale(btn_05,(150, 130))
    btn_06 = pygame.image.load("images/btn_06.png").convert_alpha()#Fish
    btn_06 = pygame.transform.scale(btn_06,(150, 130))
    btn_07 = pygame.image.load("images/btn_07.png").convert_alpha()#Chicken
    btn_07 = pygame.transform.scale(btn_07,(150, 130))
    btn_08 = pygame.image.load("images/btn_08.png").convert_alpha()#Spaghetti
    btn_08 = pygame.transform.scale(btn_08,(150, 130))
    btn_09 = pygame.image.load("images/btn_09.png").convert_alpha()#Salad
    btn_09 = pygame.transform.scale(btn_09,(150, 130))
    btn_10 = pygame.image.load("images/btn_10.png").convert_alpha()#Cake
    btn_10 = pygame.transform.scale(btn_10,(150, 130))

    btn_12 = pygame.image.load("images/btn_12.png").convert_alpha()#Watering can
    btn_12 = pygame.transform.scale(btn_12,(120, 120))
    btn_13 = pygame.image.load("images/btn_13.png").convert_alpha()#Fertilizer
    btn_13 = pygame.transform.scale(btn_13,(120, 120))
    btn_14 = pygame.image.load("images/btn_14.png").convert_alpha()#Anti-worm treatment
    btn_14 = pygame.transform.scale(btn_14,(120, 120))
    btn_15 = pygame.image.load("images/btn_15.png").convert_alpha()#Leaf misting
    btn_15 = pygame.transform.scale(btn_15,(110, 110))
    btn_16 = pygame.image.load("images/btn_16.png").convert_alpha()#Leaf shine
    btn_16 = pygame.transform.scale(btn_16,(110, 110))

    btn_back = pygame.image.load("images/btn_back.png").convert_alpha()#Back arrow
    btn_back = pygame.transform.scale(btn_back, (60, 60))#Back arrow
    btn_back_big = pygame.transform.scale(btn_back, (70, 70))#Back arrow

    plant_51 = pygame.image.load("images/plant_51.png").convert_alpha()#Plant for fun room
    plant_51 = scale_to_fit(plant_51, 290, 290)
    plant_52 = pygame.image.load("images/plant_52.png").convert_alpha()#Plant for fun room
    plant_52 = scale_to_fit(plant_52, 290, 290)

    btn_02 = pygame.image.load("images/btn_02.png").convert_alpha()#Book button
    btn_02 = pygame.transform.scale(btn_02, (150, 130))
    btn_04 = pygame.image.load("images/btn_04.png").convert_alpha()#Headphones button
    btn_04 = pygame.transform.scale(btn_04, (150, 130))

    btn_03 = pygame.image.load("images/btn_03.png").convert_alpha()#Bed button
    btn_03 = pygame.transform.scale(btn_03, (170, 160))
    btn_11 = pygame.image.load("images/btn_11.png").convert_alpha()#Alarm button
    btn_11 = pygame.transform.scale(btn_11, (130, 120))

    worm_1 = pygame.image.load("images/worm_1.png").convert_alpha()#Worm
    worm_1_normal = pygame.transform.scale(worm_1, (100, 100))#For main, fun, sleep, and food rooms
    worm_1_care = pygame.transform.scale(worm_1,(90,90))#For care room

    worm_2 = pygame.image.load("images/worm_2.png").convert_alpha()#Worm
    worm_2_normal = pygame.transform.scale(worm_2, (110, 110))#For main, fun, sleep, and food rooms
    worm_2_care = pygame.transform.scale(worm_2, (100, 100))#For care room

    ui_01 = pygame.image.load("images/ui_01.png").convert_alpha()#Candle
    ui_01 = pygame.transform.scale(ui_01, (150, 250))
    ui_02 = pygame.image.load("images/ui_02.png").convert_alpha()
    ui_02 = pygame.transform.scale(ui_02, (150, 250))
    ui_03 = pygame.image.load("images/ui_03.png").convert_alpha()
    ui_03 = pygame.transform.scale(ui_03, (150, 250))

    ui_04 = pygame.image.load("images/ui_04.png").convert_alpha()
    ui_04 = scale_to_fit(ui_04, 150, 150)

    #Time of the last game save
    last_save_time = None

    show_first_plant = True
    plant_timer = pygame.time.get_ticks()
    plant_delay = 600 #Frame interval: 600 milliseconds

    pot_x = 115
    pot_y = 310

    #Food room coordinates
    pot_food_x = 115
    pot_food_y = 290

    food_button_rect = btn_food.get_rect(topleft=(1, pot_y + 170))
    food_base_y = 310

    #Fun room coordinates
    pot_fun_x = 115
    pot_fun_y = 290
    fun_base_y = 310

    #Sleep room coordinates
    pot_sleep_x = 130
    pot_sleep_y = 320
    sleep_base_y = 310
    #Sleep animation frame coordinates
    sleep_anim_pos = (130, sleep_base_y - 213)
    #Repeating segment of the sleep animation
    sleep_loop = [
        (plant_64, sleep_anim_pos),
        (plant_65, sleep_anim_pos)]
    #Sleep animation sequence
    sleep_anim_frames = [
        (plant_66, sleep_anim_pos)]+ sleep_loop * 4 + [ (plant_66, sleep_anim_pos)]
    #Wake-up animation frames
    wake_anim_frames = [
        (plant_67, (127, sleep_base_y - 215)),
        (plant_68, (115, sleep_base_y - 215)),
        (plant_69, (135, sleep_base_y - 215)),
        (plant_68, (115, sleep_base_y -215)),
        (plant_67, (127, sleep_base_y - 215))]

    #Animations for 50% and 25% condition 
    main_sad_frames = [
        (plant_51, (110, 222)),
        (plant_52, (105, 222))]
    main_weak_frames = [
        (plant_74, (165, 150)),
        (plant_75, (160, 155))]

    #Variables:

    #Indicates whether an action is currently in progress
    action_in_progress = False

    #Stores the action currently being performed
    current_action= None

    #Real-world time until which the plant stays awake at night
    night_wake_until = None
    #Real-world time until which the plant sleeps during the day
    day_sleep_until = None

    #Filename for saved game data
    SAVE_FILE = "sawe_data.json"

    #Whether a worm is currently active
    worm_active = False

    #Date when a worm last appeared
    worm_spawned_date = None

    #Pet status values
    hunger = 25
    energy = 100
    happiness = 50
    health = 50
    start_datetime = None

    death_condition_start = None 

    #One in-game hour equals one real-world hour
    GAME_HOUR = timedelta(hours=1) #GAME_HOUR represents one real-world hour
    last_hunger_decrease = datetime.now()
    last_happiness_decrease = datetime.now()
    last_health_decrease = datetime.now()

    #Variable used to track the computer time
    last_printed_minute = -1

    #Last displayed time-of-day period
    last_printed_period = None

    #Sleep state
    plant_is_sleeping = False
    #Sleep animation
    sleep_anim_index = 0
    sleep_anim_timer = 0
    sleep_anim_delay = plant_delay
    #Wake-up animation
    wake_anim_playing = False
    wake_anim_index = 0
    wake_anim_timer = 0
    wake_anim_delay = plant_delay

    #Care room coordinates
    pot_care_x = 120
    pot_care_y = 230
    care_base_y = 310

    #Care animation frame coordinates
    watering_can_pos = (120, care_base_y- 330)
    fertilizer_pos_1 = (130, care_base_y - 285)
    fertilizer_pos_2 = (125, care_base_y - 285)
    anti_worm_pos_1 = (130, care_base_y - 285)
    anti_worm_pos_2 = (125, care_base_y - 285)
    leaf_mist_pos_1 = (105, care_base_y - 315)
    leaf_mist_pos_2 = (115, care_base_y - 325)
    leaf_shine_pos_1 = (125, care_base_y - 290)
    leaf_shine_pos_2 = (115, care_base_y - 290)
    #Watering animation
    watering_can_frames = [
        (plant_70, watering_can_pos),
        (plant_71, watering_can_pos)] * 3
    #Fertilizing animation
    fertilizer_frames = [
        (plant_26_care, fertilizer_pos_1),
        (plant_38_care, fertilizer_pos_2)] * 3
    #Anti-worm animation
    anti_worm_frames = [
        (plant_26_care, anti_worm_pos_1),
        (plant_38_care, anti_worm_pos_2)] * 3
    #Misting animation
    leaf_mist_frames = [
        (plant_72, leaf_mist_pos_1),
        (plant_73, leaf_mist_pos_2)] * 3
    #Leaf shine animation
    leaf_shine_frames = [
        (plant_43, leaf_shine_pos_1),
        (plant_43_02, leaf_shine_pos_2)] * 3

    #Book animation frame coordinates
    book_pos = (125, fun_base_y - 240)
    #Repeating segment of the book animation
    book_loop = [
        (plant_56, book_pos),
        (plant_57, book_pos),
        (plant_56, book_pos),
        (plant_57, book_pos),
        (plant_58, book_pos),
        (plant_59, book_pos)]
    #Complete book animation
    book_anim_frames = book_loop * 2 + [
        (plant_56, book_pos),
        (plant_57, book_pos)]
    #Repeating segment of the headphones animation
    headphones_loop = [
        (plant_54, (115, fun_base_y - 235)),
        (plant_55, (110, fun_base_y - 235))]
    #Complete headphones animation
    headphones_anim_frames = [
        (plant_53, (110, fun_base_y - 240))] + headphones_loop * 6 + [
        (plant_53, (110, fun_base_y - 240)) ]

    #Worm coordinates in main room
    worm_main_frames = [(worm_1_normal, (200, pot_y - 27)),
                        (worm_2_normal, (200, pot_y - 38))]
    #Worm coordinates in food menu
    worm_food_frames = [
        (worm_1_normal, (200, food_base_y - 50)),
        (worm_2_normal, (200, food_base_y - 60))]
    #Worm coordinates in fun room
    worm_fun_frames = [ 
        (worm_1_normal, (200, fun_base_y - 50)),
        (worm_2_normal, (200, fun_base_y - 60))]
    #Worm coordinates in sleep room
    worm_sleep_frames = [
        (worm_1_normal, (215, sleep_base_y - 20)),
        (worm_2_normal, (215, sleep_base_y - 30))]
    #Worm coordinates in care room
    worm_care_frames = [
        (worm_1_care, (210, care_base_y - 100)),
        (worm_2_care, (210, care_base_y - 110))]

    #Get the image rectangle for click detection
    btn_back_pos = (435, pot_y - 300)
    btn_back_rect = btn_back.get_rect(topleft=btn_back_pos)

    #Main room buttons
    food_button = Button(btn_food, (1, pot_y + 170))
    fun_button = Button(btn_fun, (130, pot_y +193))
    sleep_button = Button(btn_sleep, (250, pot_y +172))
    care_button = Button(btn_care, (375, pot_y + 172))

    #Food buttons
    soup_button = Button(btn_05, (-20, food_base_y + 100),hitbox_scale=0.55)
    fish_button = Button(btn_06, (35, food_base_y + 160),hitbox_scale=0.55)
    chicken_button = Button(btn_07, (145, food_base_y +110),hitbox_scale=0.55)
    spaghetti_button = Button(btn_08, (225, food_base_y +170),hitbox_scale=0.55)
    salad_button = Button(btn_09, (290, food_base_y + 100),hitbox_scale=0.55)
    cake_button = Button(btn_10, (360, food_base_y + 160),hitbox_scale=0.55)

    #Back button
    back_button = Button(btn_back, btn_back_pos)

    #Fun room buttons
    book_button = Button(btn_02, (90, fun_base_y + 140), hitbox_scale=0.55)
    headphones_button = Button(btn_04, (240, fun_base_y + 140), hitbox_scale=0.55)

    #Sleep room buttons
    bed_button = Button(btn_03, (100, sleep_base_y + 150),hitbox_scale=0.55)
    alarm_button = Button(btn_11, (270, sleep_base_y + 170), hitbox_scale=0.55)

    #Care room buttons
    watering_can_button = Button(btn_12, (40, care_base_y + 170),hitbox_scale=0.55)
    fertilizer_button = Button(btn_13, (130, care_base_y + 170),hitbox_scale=0.55)
    anti_worm_button = Button(btn_14, (205, care_base_y + 170),hitbox_scale=0.55)
    leaf_mist_button = Button(btn_15, (285, care_base_y + 175),hitbox_scale=0.55)
    leaf_shine_button = Button(btn_16, (355, care_base_y + 175),hitbox_scale=0.55)

    #FIREFLIES
    #Care room fireflies
    care_fireflies = []
    care_fireflies_playing = False
    care_fireflies_start_time = 0
    care_fireflies_duration = 3000
    care_firefly_color = (255, 245, 150)
    #Firefly colors
    care_blue = (120, 190, 255)
    care_green = (130, 255, 160)
    care_pink = (255, 150, 220)
    care_cyan = (150, 240, 255)
    care_yellow = (255, 245, 150)

    #List of main room buttons
    main_room_buttons = [
        food_button,
        fun_button,
        sleep_button,
        care_button]
    #List of food room buttons
    food_menu_buttons = [
        soup_button,
        fish_button,
        chicken_button,
        spaghetti_button,
        salad_button,
        cake_button,
        back_button]
    #Food buttons without Back
    food_action_buttons =[
        soup_button,
        fish_button,
        chicken_button,
        spaghetti_button,
        salad_button,
        cake_button]
    #List of fun room buttons
    fun_room_buttons = [
        book_button,
        headphones_button,
        back_button]
    #List of sleep room buttons
    sleep_room_buttons = [
        bed_button,
        alarm_button,
        back_button]
    #List of care room buttons
    care_room_buttons = [
        watering_can_button,
        fertilizer_button,
        anti_worm_button,
        leaf_mist_button,
        leaf_shine_button,
        back_button]

    #Duration of daytime sleep triggered by button
    DAY_SLEEP_DURATION = 60 * 1000
    #Time when daytime sleep ends
    day_sleep_end_time = None
    #Duration of nighttime wake period
    NIGHT_WAKE_DURATION = 5 * 60 * 1000
    #Time when nighttime wake period ends
    night_wake_end_time = None

    #screen_state = "food_menu"
    screen_state = "main_room"

    magic_time = pygame.time.get_ticks()

    clock = pygame.time.Clock()

    #Feeding animation
    food_anim_playing = False
    food_anim_index = 0
    food_anim_timer = 0
    food_anim_delay = 300
    food_anim_frames = [
        plant_30,
        plant_31,
        plant_30,
        plant_31,
        plant_30,
        plant_31]

    #Fun room animation (reading, listening to music)
    fun_anim_playing = False
    fun_anim_index = 0
    fun_anim_timer = 0
    fun_anim_delay = plant_delay
    fun_anim_frames = []

    #Care room animation (all five buttons)
    care_anim_playing = False
    care_anim_index = 0
    care_anim_timer = 0
    care_anim_delay = plant_delay
    care_anim_frames = []


    #Music
    birds_sound = pygame.mixer.Sound("sounds/birds.mp3")
    birds_sound.set_volume(0.3)#Volume
    evening_crickets_sound = pygame.mixer.Sound("sounds/evening_crickets.mp3")
    evening_owl_sound = pygame.mixer.Sound("sounds/evening_owl.mp3")
    psh_sound = pygame.mixer.Sound("sounds/psh.mp3")
    btn_sound = pygame.mixer.Sound("sounds/btn.wav")
    food_sound = pygame.mixer.Sound("sounds/food.mp3")
    action_sound = pygame.mixer.Sound("sounds/action.wav")
    back_sound = pygame.mixer.Sound("sounds/back.mp3")
    back_sound.set_volume(1.0)
    care_sound = pygame.mixer.Sound("sounds/care.wav")
    fireflies_sound = pygame.mixer.Sound("sounds/fireflies.wav")
    read_sound = pygame.mixer.Sound("sounds/read.mp3")
    music1_sound = pygame.mixer.Sound("sounds/music1.mp3")
    music1_sound.set_volume(0.3)#Volume
    music2_sound = pygame.mixer.Sound("sounds/music2.mp3")
    music2_sound.set_volume(0.3)#Volume
    music3_sound = pygame.mixer.Sound("sounds/music3.mp3")
    music3_sound.set_volume(0.3)#Volume
    music_sounds = [music1_sound, music2_sound, music3_sound]#Play tracks in sequence
    current_music_index = 0#Play tracks in sequence
    sleep_sound = pygame.mixer.Sound("sounds/sleep.mp3")
    alarm_sound = pygame.mixer.Sound("sounds/alarm.mp3")
    grumble_sound = pygame.mixer.Sound("sounds/grumble.mp3")
    grumble_sound.set_volume(0.3)
    pour_sound = pygame.mixer.Sound("sounds/pour.mp3")
    sand_sound = pygame.mixer.Sound("sounds/sand.mp3")
    dig_sound = pygame.mixer.Sound("sounds/dig.mp3")
    spray_sound = pygame.mixer.Sound("sounds/spray.mp3")
    error_sound = pygame.mixer.Sound("sounds/error_sound.mp3")


    #FUNCTIONS

    #Function to determine the pet condition
    def get_plant_condition():
        lowest_stat = min(hunger, happiness, health, energy)
        if lowest_stat <= 25:
            return "weak"
        elif lowest_stat <= 50:
            return "sad"
        else:
            return "happy"

    #Function to draw the worm
    def draw_worm(frames):
        if worm_active:
            if show_first_plant:
                worm_img, worm_pos = frames[0]
            else:
                worm_img, worm_pos = frames[1]
            screen.blit(worm_img, worm_pos)

    #Function to draw the main room
    def draw_main_room():
        if 7 <= current_hour < 18:
                screen.blit(main_bg, (0, 0))
        else:
                screen.blit(main_bg_evening, (0, 0))
        if 7<= current_hour <18 :
            screen.blit(ui_01, (46, pot_y -45))
        else:
            if (pygame.time.get_ticks() // 400) % 2 == 0:
                screen.blit(ui_02, (40, pot_y -65))
            else:
                screen.blit(ui_03, (40, pot_y - 65))
        screen.blit(pot_2, (pot_x, pot_y))
        #Hide the plant in the main room while it sleeps
        if not plant_is_sleeping:
            plant_condition = get_plant_condition()
            if plant_condition == "weak":
                if show_first_plant:
                    screen.blit(plant_74, (165, pot_y - 150))
                else:
                    screen.blit(plant_75, (160, pot_y -155))
            elif plant_condition == "sad":
                if show_first_plant:
                    screen.blit(plant_51, (110, pot_y - 222))
                else:
                    screen.blit(plant_52, (105, pot_y - 222))
            else:
                if show_first_plant:
                    screen.blit(plant_26, (107, pot_y - 235))
                else:
                    screen.blit(plant_38, (100, pot_y - 235))
        draw_worm(worm_main_frames)
        #Draw all main room buttons
        for button in main_room_buttons: button.draw(screen)

    #Function to draw the food room
    def draw_food_menu():
        if 7 <= current_hour < 18:
            screen.blit(food_bg, (0, 0))
        else:
            screen.blit(food_bg_evening, (0, 0))
        screen.blit(pot_2, (pot_food_x, pot_food_y))

        if not plant_is_sleeping:#Hide the plant in the food room while it sleeps
            #Plant in the food room
            if food_anim_playing:
                screen.blit(food_anim_frames[
                    food_anim_index],(108, food_base_y - 250))
            else:
                plant_condition = get_plant_condition()
                if plant_condition == "weak":
                    if show_first_plant:
                        screen.blit(plant_74, (160, food_base_y - 170))
                    else:
                        screen.blit(plant_75, (160, food_base_y - 175))
                elif plant_condition == "sad":
                    if show_first_plant:
                        screen.blit(plant_24, (115, food_base_y - 252))
                    else:
                        screen.blit(plant_25, (115, food_base_y - 252))
                else:
                    if show_first_plant:
                        screen.blit(plant_37, (110, food_base_y - 250))
                    else:
                        screen.blit(plant_37_1, (105, food_base_y - 250))
        draw_worm(worm_food_frames)
        #Draw all food room buttons
        for button in food_menu_buttons: button.draw(screen)

    #Function to draw the fun room
    def draw_fun_room():
        screen.blit(fun_bg, (0, 0))
        screen.blit(pot_2, (pot_fun_x, pot_fun_y))
        if not plant_is_sleeping:#Hide the plant in the fun room while it sleeps
            #Plant in the fun room
            if fun_anim_playing:
                plant_img, plant_pos = fun_anim_frames[fun_anim_index]
                screen.blit(plant_img, plant_pos)
            else:
                plant_condition = get_plant_condition()
                if plant_condition == "weak":
                    if show_first_plant:
                        screen.blit(plant_74, (160, fun_base_y - 170))
                    else:
                        screen.blit(plant_75, (160, fun_base_y - 175))
                elif plant_condition == "sad":
                    if show_first_plant:
                        screen.blit(plant_51, (110, fun_base_y - 245))
                    else:
                        screen.blit(plant_52, (105, fun_base_y - 245))
                else:
                    if show_first_plant:
                        screen.blit(plant_37, (110, fun_base_y - 250))
                    else:
                        screen.blit(plant_37_1, (105, fun_base_y - 250))
        draw_worm(worm_fun_frames)
        #Draw all fun room buttons
        for button in fun_room_buttons: button.draw(screen)

    #Function to draw the sleep room
    def draw_sleep_room():
        if 7 <= current_hour <18:
            screen.blit(sleep_bg_day, (0, 0))
        else:
            screen.blit(sleep_bg, (0, 0))
        screen.blit(pot_2, (pot_sleep_x, pot_sleep_y))
        #Plant in the sleep room
        if wake_anim_playing:
            plant_img, plant_pos = wake_anim_frames[wake_anim_index]
            screen.blit(plant_img, plant_pos)
        elif plant_is_sleeping:
            plant_img, plant_pos = sleep_anim_frames[sleep_anim_index]
            screen.blit(plant_img, plant_pos)
        else:
            plant_condition = get_plant_condition()
            if plant_condition == "weak":
                if show_first_plant:
                    screen.blit(plant_74, (175, sleep_base_y - 140))
                else:
                    screen.blit(plant_75, (175, sleep_base_y - 145))
            elif plant_condition == "sad":
                if show_first_plant:
                    screen.blit(plant_60, (123, sleep_base_y - 220))
                else:
                    screen.blit(plant_61, (123, sleep_base_y - 217))
            else:
                if show_first_plant:
                    screen.blit(plant_37, (125, sleep_base_y - 220))
                else:
                    screen.blit(plant_37_1, (120, sleep_base_y - 220))
        draw_worm(worm_sleep_frames)

        #Draw all sleep room buttons
        for button in sleep_room_buttons: button.draw(screen)

    #Function to draw the care room
    def draw_care_room():
        if 7 <= current_hour < 18:
            screen.blit(care_bg, (0, 0))
        else:
            screen.blit(care_bg_evening, (0, 0))
        screen.blit(pot_2, (pot_care_x, pot_care_y))
        if not plant_is_sleeping:#Hide the plant in the care room while it sleeps
            if care_anim_playing:
                plant_img, plant_pos = care_anim_frames[care_anim_index]
                screen.blit(plant_img, plant_pos)
            else:
                plant_condition = get_plant_condition()
                if plant_condition == "weak":
                    if show_first_plant:
                        screen.blit(plant_74_care, (175, care_base_y - 210))
                    else:
                        screen.blit(plant_75_care, (175, care_base_y - 215))
                elif plant_condition == "sad":
                    if show_first_plant:
                        screen.blit(plant_62, (125, care_base_y - 270))
                    else:
                        screen.blit(plant_63, (125, care_base_y - 270))
                else:
                    if show_first_plant:
                        screen.blit(plant_37_care, (130, care_base_y - 280))
                    else:
                        screen.blit(plant_37_1_care, (125, care_base_y - 280))
        draw_worm(worm_care_frames)
        #Fireflies
        draw_care_fireflies(pygame.time.get_ticks())
        #Buttons
        for button in care_room_buttons: button.draw(screen)

    #Fireflies function
    def start_care_fireflies(color):
        nonlocal care_fireflies
        nonlocal care_fireflies_playing
        nonlocal care_fireflies_start_time
        nonlocal care_firefly_color

        care_fireflies = []
        care_fireflies_playing = True
        care_fireflies_start_time = pygame.time.get_ticks()
        care_firefly_color = color

        while len(care_fireflies) < 22:
            big = random.choice([True, False])
            if big:
                r = random.randint(2, 3)
            else:
                r = random.randint(1, 2)

            care_fireflies.append({
                "x": random.randint(70, 430),
                "y": random.randint(190, 520),
                "speed": random.uniform(0.4, 1.2),
                "r": r,
                "phase": random.randint(0, 1000),
                "jitter": 1.5,
                "drift": random.uniform(-0.5, 0.5)})

    def draw_care_fireflies(current_time):
        nonlocal care_fireflies
        nonlocal care_fireflies_playing

        if not care_fireflies_playing:
            return
        if current_time - care_fireflies_start_time > care_fireflies_duration:
            care_fireflies_playing = False
            care_fireflies = []
            return
        for f in care_fireflies[:]:
            f["y"] -= f["speed"]
            f["x"] += math.sin((current_time + f["phase"]) * 0.01)*0.5
            f["x"] += f["drift"]
            
            alpha = 120 + 100 * math.sin(
                (current_time +f["phase"]) * 0.01)
            alpha = max(60, min(255, int(alpha)))
            dx = random.uniform(-f["jitter"], f["jitter"])
            dy = random.uniform(-f["jitter"], f["jitter"])
            r = f["r"]
            size = 20 * r
            glow = pygame.Surface((size, size), pygame.SRCALPHA)
            center = size//2

            pygame.draw.circle(
                glow,
                (*care_firefly_color, int(alpha * 0.15)),
                (center, center),
                int(r * 4))

            pygame.draw.circle(
                glow,
                (*care_firefly_color, int(alpha * 0.35)),
                (center, center),
                int(r * 2))

            pygame.draw.circle(
                glow,
                (*care_firefly_color, alpha),
                (center, center),
                int(r))

            screen.blit(
                glow,(
                    int(f["x"] - center + dx ),
                    int(f["y"] - center + dy)))
            if f ["y"] < -20:
                care_fireflies.remove(f)

    #Function to draw the plant status panel
    def draw_status_panel():
        #Sign showing the plant age
        sign_x = 5
        sign_y = 5
        screen.blit(ui_04, (sign_x, sign_y))
        sign_font = pygame.font.SysFont(None, 24)
        day_text = sign_font.render( f"{game_day}/15", True, (90,60,20))
        screen.blit(day_text,(sign_x + 77, sign_y + 42))
        #Semi-transparent gray panel
        panel_width = 125
        panel_height = 140
        panel_x = 15
        panel_y = 75
        
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        
        pygame.draw.rect(
            panel,
            (180, 180, 180, 150),
            (0, 0, panel_width, panel_height), border_radius=25)
        
        #Dark gray status bars
        bar_x = 18
        bar_y = 20
        bar_width = 90
        bar_height = 14
        bar_gap = 18

        status_values = [hunger, happiness, energy, health] #%
        
        for i in range(4):
            y = bar_y + i * (bar_height + bar_gap)
            #Dark gray bar
            pygame.draw.rect(
                panel,
                (80, 80, 80, 255),
                (bar_x, y, bar_width, bar_height),
                border_radius = 8)
            #Green status indicator
            green_width = int((bar_width -4)* status_values[i] / 100)
            if green_width > 6:
                pygame.draw.rect(
                    panel,(80, 210, 90, 255),
                    (bar_x + 2, y +3, green_width, bar_height - 6),
                    border_radius=6)
            elif green_width >0:
                pygame.draw.rect(panel,(80, 210, 90, 255),
                            (bar_x + 2, y +3, green_width, bar_height - 6),
                            border_radius = 6)

        #Labels for status bars
        font = pygame.font.SysFont(None, 18)
        labels = ["Hunger", "Happiness", "Energy", "Health"]
        for i in range(4):
            text = font.render(labels[i],True,(40, 40, 40))
            panel.blit(text, (bar_x, bar_y + i * (bar_height + bar_gap) - 14))
        
        screen.blit(panel, (panel_x, panel_y))

    #Function to stop care room button sounds
    def stop_care_sounds():
        pour_sound.stop()
        sand_sound.stop()
        dig_sound.stop()
        spray_sound.stop()
        psh_sound.stop()

    #Function to cap a stat at 100%
    def increase_stat(value, amount=25):
        value += amount
        if value > 100:
            value= 100
        return value

    #Function to decrease a stat value
    def decrease_stat (value, amount):
        value -= amount
        if value < 0:
            value = 0
        return value

    #Determine the time-of-day period from the computer clock
    def get_day_period(hour):
        #Day: 07:00 to 17:59
        if 7 <= hour < 18:
            return "day"
        #Evening: 18:00 to 21:59
        elif 18 <= hour < 22:
            return "evening"
        #Night: 22:00 to 02:59
        elif hour >= 22 or hour <3:
            return "night"
        #Deep night / recovery: 03:00 to 06:59
        else:
            return "deep_night"

    #Update energy based on the computer clock
    def update_energy_by_time(hour):
        #Day: 07:00 to 20:59, energy stays at 100%
        if 7 <= hour < 21:
            return 100
        #Evening: 21:00 to 23:59, energy drops 25% per hour
        elif 21 <= hour < 24:
            return 100 - (hour - 20)* 25
        #Night: 00:00 to 02:59, energy is 0%
        elif 0 <= hour < 3:
            return 0
        #Deep night: 03:00 to 06:59, energy recovers 25% per hour
        else:
            return (hour -2)* 25

    #Check whether the plant should sleep based on computer time
    def should_sleep_by_time(hour):
        #From 00:00 to 06:59, the plant sleeps
        if 0 <= hour < 7:
            return True
        #From 07:00 to 22:59, the plant stays awake
        else:
            return False

    #Load saved game data from a file
    def load_save_data():
        #If the save file does not exist yet
        if not os.path.exists(SAVE_FILE):
            return None
        #Try to open the save file
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        #If the file is corrupted or unreadable
        except Exception:
            return None 

    #Save game data to a file
    def save_game_data():
        data = {
            "hunger": hunger,
            "energy": energy,
            "happiness": happiness,
            "health": health,
            "start_datetime": start_datetime,
            "plant_is_sleeping": plant_is_sleeping,
            "worm_active": worm_active,
            "worm_spawned_date": worm_spawned_date,
            "night_wake_until":night_wake_until,
            "day_sleep_until": day_sleep_until,
            "last_hunger_decrease":
            last_hunger_decrease.strftime("%Y-%m-%d %H:%M:%S"),
            "last_happiness_decrease":
            last_happiness_decrease.strftime("%Y-%m-%d %H:%M:%S"),
            "last_health_decrease":
            last_health_decrease.strftime("%Y-%m-%d %H:%M:%S"),
            "last_save_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "death_condition_start": (
                death_condition_start.strftime("%Y-%m-%d %H:%M:%S")
                if death_condition_start is not None
                else None)}
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        #Record the actual time of saving the game

    #Shared Back button for all rooms
    def handle_back(event):
        nonlocal screen_state

        if screen_state not in ("food_menu", "fun_room", "care_room", 
                                "sleep_room"):
            return
        if not back_button.is_clicked(event):
            return

        #Prevent leaving during wake-up animation
        if screen_state == "sleep_room" and wake_anim_playing:
            error_sound.play()
            return

        #Cannot leave while the plant is busy
        if action_in_progress:
            error_sound.play()
            return
        #Stop sounds from the current room
        if screen_state == "food_menu":
            food_sound.stop()
        elif screen_state == "fun_room":
            read_sound.stop()
            for sound in music_sounds:
                sound.stop()
        elif screen_state == "care_room":
            stop_care_sounds()
        elif screen_state == "sleep_room":
            grumble_sound.stop()

        back_sound.play()
        screen_state = "main_room"
            

    #Load saved game data once at startup
    saved_data = load_save_data()
    #If the save file exists and was read successfully
    if saved_data is not None:
        #Load plant status values
        hunger = saved_data.get("hunger", hunger)
        energy = saved_data.get("energy", energy)
        happiness = saved_data.get("happiness", happiness)
        health = saved_data.get("health", health)
        saved_both_zero = hunger == 0 and health == 0
        #Load the game start time
        start_datetime = saved_data.get("start_datetime",
                                    start_datetime)
        plant_is_sleeping = saved_data.get(
        "plant_is_sleeping", plant_is_sleeping
    )

        saved_death_condition_start = saved_data.get(
            "death_condition_start"
        )
        if saved_death_condition_start is not None:
            death_condition_start = datetime.strptime(
                saved_death_condition_start, "%Y-%m-%d %H:%M:%S"
            )
        else:
            death_condition_start = None
        
        #Load worm state
        worm_active = saved_data.get("worm_active", worm_active)
        worm_spawned_date = saved_data.get("worm_spawned_date", worm_spawned_date)
        #Load nighttime wake-up deadline
        night_wake_until = saved_data.get("night_wake_until", night_wake_until)
        day_sleep_until = saved_data.get(
        "day_sleep_until", day_sleep_until
    )
        #Load the last save time from the file
        last_save_time = saved_data.get("last_save_time",last_save_time)
        # Load timestamps of last stat decreases
        saved_hunger_time = saved_data.get("last_hunger_decrease")
        saved_happiness_time = saved_data.get("last_happiness_decrease")
        saved_health_time = saved_data.get("last_health_decrease")
        if saved_hunger_time is not None:
            last_hunger_decrease = datetime.strptime(
                saved_hunger_time, "%Y-%m-%d %H:%M:%S"
            )
        if saved_happiness_time is not None:
            last_happiness_decrease = datetime.strptime(saved_happiness_time, 
            "%Y-%m-%d %H:%M:%S")
        if saved_health_time is not None:
            last_health_decrease = datetime.strptime(
                saved_health_time, "%Y-%m-%d %H:%M:%S"
            )
        # Calculate elapsed real-world time since the last save
        offline_time = timedelta(0)

        if last_save_time is not None:
            try: 
                last_save_datetime = datetime.strptime(last_save_time, "%Y-%m-%d %H:%M:%S")
                offline_time = datetime.now() - last_save_datetime
            except ValueError:
                offline_time = timedelta(0)

    game_start = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")

    print("Игра была выключена:", offline_time)

    #Check whether a nighttime wake period was saved before exit
    if night_wake_until is not None:#This value stores the actual 
                                    #time until which the plant must stay awake
        try:
            wake_until_time = datetime.strptime(
                night_wake_until, "%Y-%m-%d %H:%M:%S")
            #If five minutes have not passed yet
            if datetime.now()<wake_until_time:
                remaining_ms = int(
                    (wake_until_time - datetime.now()).total_seconds()*1000)
                night_wake_end_time = pygame.time.get_ticks()+remaining_ms
                plant_is_sleeping = False
            #If five minutes have already passed
            else:
                night_wake_until = None
                night_wake_end_time = None
        except Exception:
            night_wake_until = None
            night_wake_end_time = None

    #Check whether daytime sleep ended before launch
    if day_sleep_until is not None:
        try:
            sleep_until_time = datetime.strptime(
                day_sleep_until, "%Y-%m-%d %H:%M:%S"
            )

            #If the minute of sleep has not passed yet
            if datetime.now() < sleep_until_time:
                remaining_ms = int(
                    (sleep_until_time - datetime.now()).total_seconds() * 1000
                )

                day_sleep_end_time = (
                    pygame.time.get_ticks() + remaining_ms
                )

                plant_is_sleeping = True

            #If the minute has already passed
            else:
                day_sleep_end_time = None
                day_sleep_until = None
                plant_is_sleeping = False

        except Exception:
            day_sleep_until = None
            day_sleep_end_time = None
            
    ##############################################
    #Main loop
    running = True
    while running:
        #Time
        current_time = pygame.time.get_ticks()
        #Read time from the computer clock
        real_time = datetime.now()
        current_hour = real_time.hour
        current_minute = real_time.minute

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Save game data before quitting
                save_game_data()
                pygame.mixer.stop()
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                #Shared Back-button handling
                handle_back(event)

                #Click in the main room
                if screen_state == "main_room":
                    if food_button.is_clicked(event):
                        btn_sound.play()
                        screen_state = "food_menu"
                    if fun_button.is_clicked(event):
                        btn_sound.play()
                        screen_state = "fun_room"
                    if sleep_button.is_clicked(event):
                        btn_sound.play()
                        screen_state = "sleep_room"
                    if care_button.is_clicked(event):
                        btn_sound.play()
                        screen_state = "care_room"
                #Click on the Back button
                elif screen_state == "food_menu":
                    
                    #Clicking a food button starts the animation
                    for button in food_action_buttons:
                        # Only handle food click if no other action is in progress
                        if (
                            button.is_clicked(event) and not action_in_progress
                            and not plant_is_sleeping
                        ):
                            #Block repeated clicks
                            action_in_progress = True
                            current_action = "food"
                            food_sound.play()
                            action_sound.play()
                            food_anim_playing = True
                            food_anim_index = 0
                            food_anim_timer = pygame.time.get_ticks()
                            break
                        
                elif screen_state == "fun_room":
                    
                    #Clicking Book starts the reading animation
                    if (book_button.is_clicked(event)
                        and not action_in_progress
                        and not plant_is_sleeping):

                        action_in_progress = True
                        current_action = "fun"
                        action_sound.play()

                        for sound in music_sounds:
                            sound.stop()

                        read_sound.play(maxtime=7000)#Sound duration: approximately 8 seconds
                        fun_anim_playing = True
                        fun_anim_frames = book_anim_frames
                        fun_anim_index = 0
                        fun_anim_timer = pygame.time.get_ticks()
                    #Clicking Headphones starts the listening animation
                    elif(
                    headphones_button.is_clicked(event)
                    and not action_in_progress
                    and not plant_is_sleeping):
                        action_in_progress = True
                        current_action = "fun"
                        read_sound.stop()
                        for sound in music_sounds:
                            sound.stop()
                        action_sound.play()
                        music_sounds[current_music_index].play()
                        current_music_index +=1
                        if current_music_index >= len(music_sounds):
                            current_music_index = 0
                        fun_anim_playing = True
                        fun_anim_frames = headphones_anim_frames
                        fun_anim_index = 0
                        fun_anim_timer = pygame.time.get_ticks()

                        
                elif screen_state == "sleep_room":
                    
                    #Bed button puts the plant to sleep
                    if bed_button.is_clicked(event):
                        action_sound.play()
                        grumble_sound.stop()
                        if sleep_sound.get_num_channels() == 0:
                            sleep_sound.play(-1)#-1 means repeat indefinitely...
                                                #...check whether it is nighttime or daytime
                        #Stop the wake-up animation
                        wake_anim_playing = False
                        sleep_anim_index = 0
                        #If the plant is put to bed from 22:00 to 06:59
                        if current_hour >= 22 or current_hour < 7:
                            #Cancel nighttime wake-up
                            night_wake_end_time = None
                            night_wake_until = None
                            #Cancel daytime sleep
                            day_sleep_end_time = None
                            day_sleep_until = None
                            #The plant is sleeping again
                            plant_is_sleeping = True
                        #If it is daytime   
                        else:
                            #Cancel nighttime wake-up
                            night_wake_end_time = None
                            night_wake_until = None
                            #During the day, the plant sleeps for only one minute
                            day_sleep_end_time =(
                                pygame.time.get_ticks() + DAY_SLEEP_DURATION)
                            day_sleep_until = (
                                datetime.now() + timedelta(minutes=1)
                                    ).strftime("%Y-%m-%d %H:%M:%S")
                            plant_is_sleeping = True
                            #Restart the sleep animation from the beginning
                        sleep_anim_index = 0
                        sleep_anim_timer = pygame.time.get_ticks()
                        
                    #Alarm button wakes the plant
                    elif alarm_button.is_clicked(event):
                        #Alarm works only while the plant is asleep
                        if plant_is_sleeping:
                            #From 00:00 to 02:59, wake the plant for five minutes
                            if 0 <= current_hour < 3:
                                action_sound.play()
                                alarm_sound.play()
                                grumble_sound.play()
                                night_wake_end_time = (
                                    pygame.time.get_ticks()+ NIGHT_WAKE_DURATION)
                                #Store the real-world time until which the plant...
                                #...will stay awake
                                night_wake_until = (
                                    datetime.now()+
                                    timedelta(minutes=5)
                                    ).strftime("%Y-%m-%d %H:%M:%S")
                                plant_is_sleeping = False
                                wake_anim_playing = True
                                wake_anim_index = 0
                                wake_anim_timer = pygame.time.get_ticks()
                                sleep_sound.stop()
                                #From 22:00 to 23:59, waking up does not use the five-minute timer
                            elif 22 <= current_hour < 24:
                                action_sound.play()
                                alarm_sound.play()
                                grumble_sound.play()

                                night_wake_end_time = None
                                night_wake_until = None
                                day_sleep_end_time = None
                                day_sleep_until = None

                                plant_is_sleeping = False
                                wake_anim_playing = True
                                wake_anim_index = 0
                                wake_anim_timer = pygame.time.get_ticks()
                                sleep_sound.stop()
                            #From 03:00 to 06:59, the plant cannot be woken up
                            elif 3 <= current_hour <7:
                                pass
                            #During the day, if the plant sleeps after pressing Sleep, it can...
                                #...be woken up immediately
                            else:
                                action_sound.play()
                                alarm_sound.play()
                                grumble_sound.play()
                                day_sleep_end_time = None
                                day_sleep_until = None
                                plant_is_sleeping = False
                                wake_anim_playing = True
                                wake_anim_index = 0
                                wake_anim_timer = pygame.time.get_ticks()
                                sleep_sound.stop()
                        
                elif screen_state == "care_room":
                    
                    #Watering button
                    if watering_can_button.is_clicked(event):
                        if worm_active:
                            error_sound.play()
                        elif not action_in_progress and not plant_is_sleeping:
                            action_in_progress = True
                            current_action = "care"
                            stop_care_sounds()
                            care_sound.play()
                            pour_sound.play(maxtime=4000)
                            fireflies_sound.play()
                            care_anim_playing = True
                            care_anim_frames = watering_can_frames
                            care_anim_index = 0
                            care_anim_timer = pygame.time.get_ticks()
                            start_care_fireflies(care_blue)
                            
                    #Fertilizer button
                    elif fertilizer_button.is_clicked(event):
                        if worm_active:
                            error_sound.play()
                        elif not action_in_progress and not plant_is_sleeping:
                            action_in_progress = True
                            current_action = "care"
                            stop_care_sounds()
                            care_sound.play()
                            sand_sound.play()
                            fireflies_sound.play()
                            care_anim_playing = True
                            care_anim_frames = fertilizer_frames
                            care_anim_index = 0
                            care_anim_timer = pygame.time.get_ticks()
                            start_care_fireflies(care_green)
                    
                    #Anti-worm button
                    elif anti_worm_button.is_clicked(event):
                        if not worm_active:
                            error_sound.play()
                        elif not action_in_progress and not plant_is_sleeping:
                            action_in_progress = True
                            current_action = "anti_worm"
                            stop_care_sounds()
                            care_sound.play()
                            dig_sound.play(maxtime=4000)
                            fireflies_sound.play()
                            care_anim_playing = True
                            care_anim_frames = anti_worm_frames
                            care_anim_index = 0
                            care_anim_timer = pygame.time.get_ticks()
                            start_care_fireflies(care_pink)

                    #Misting button
                    elif leaf_mist_button.is_clicked(event):
                        if worm_active:
                            error_sound.play()
                        elif not action_in_progress and not plant_is_sleeping:
                            action_in_progress = True
                            current_action = "care"
                            stop_care_sounds()
                            care_sound.play()
                            spray_sound.play()
                            fireflies_sound.play()
                            care_anim_playing = True
                            care_anim_frames = leaf_mist_frames
                            care_anim_index = 0
                            care_anim_timer = pygame.time.get_ticks()
                            start_care_fireflies(care_cyan)
                    
                    #Leaf shine button
                    elif leaf_shine_button.is_clicked(event):
                        if worm_active:
                            error_sound.play()
                        elif not action_in_progress and not plant_is_sleeping:
                            action_in_progress = True
                            current_action = "care"
                            stop_care_sounds()
                            care_sound.play()
                            psh_sound.play()
                            fireflies_sound.play()
                            care_anim_playing = True
                            care_anim_frames = leaf_shine_frames
                            care_anim_index = 0
                            care_anim_timer = pygame.time.get_ticks()
                            start_care_fireflies(care_yellow)

        game_age = real_time - game_start
        game_day = game_age.days +1

        #Today's date
        current_date = real_time.strftime("%Y-%m-%d")

        #Check whether a new worm should appear
        if not worm_active:
            if worm_spawned_date is None:
                next_worm_time = real_time.replace(
                hour=15,
                minute=0,
                second=0,
                microsecond=0)
            else:
                last_worm_date = datetime.strptime(
                worm_spawned_date,
                "%Y-%m-%d")
                next_worm_time = last_worm_date + timedelta(days=1)
                next_worm_time = next_worm_time.replace(
                    hour=15,
                    minute=0,
                    second=0)
            if real_time >= next_worm_time:
                worm_active = True
                worm_spawned_date = current_date
                health = 0

        #Update energy based on computer time
        energy = update_energy_by_time(current_hour)

        #Check whether the plant should sleep based on computer time
        auto_sleep = should_sleep_by_time(current_hour)
        #If it is currently nighttime sleep hours
        if auto_sleep:
            # From 03:00 to 06:59, the plant cannot be woken up
            if 3 <= current_hour < 7:
                plant_is_sleeping = True
                night_wake_end_time = None
                night_wake_until = None #Clear any remaining part of the five-minute 
                                        #wake period if it carried over from 02:59
                day_sleep_end_time = None
                day_sleep_until = None
                wake_anim_playing = False #Cancel any wake-up animation 
                                        #still running at exactly 03:00
            #From 00:00 to 02:59, the plant can be woken for five minutes
            else:
                if ( night_wake_end_time is
                not None and current_time < night_wake_end_time):
                    plant_is_sleeping = False
                    sleep_sound.stop()
                else:
                    plant_is_sleeping = True
                    night_wake_end_time = None
                    night_wake_until = None
                    day_sleep_end_time = None
                    day_sleep_until = None
        #If it is not the automatic sleep period
        else:
            night_wake_end_time = None

            #From 22:00 to 23:59, preserve the current state
            #If put to bed, it sleeps; if woken, it stays awake
            if 22 <= current_hour < 24:
                if day_sleep_end_time is not None:
                    if current_time < day_sleep_end_time:
                        plant_is_sleeping = True
                    else:
                        plant_is_sleeping = False
                        sleep_sound.stop()
                        day_sleep_end_time = None
                        day_sleep_until = None

            #From 07:00 to 21:59, daytime sleep lasts one minute
            else:
                #If daytime sleep was started with the button
                if day_sleep_end_time is not None:
                    #If the minute has not passed, the plant stays asleep
                    if current_time < day_sleep_end_time:
                        plant_is_sleeping = True
                    #If the minute has passed, the plant wakes up
                    else:
                        plant_is_sleeping = False
                        sleep_sound.stop()
                        day_sleep_end_time = None
                        day_sleep_until = None
                #If daytime sleep is not enabled, the plant is awake
                else:
                    plant_is_sleeping = False
                    sleep_sound.stop()
                    day_sleep_end_time = None
            
            #Play sleep sound while the plant sleeps
        if plant_is_sleeping:
            if sleep_sound.get_num_channels() == 0:
                sleep_sound.play(-1)
        else:
            sleep_sound.stop()

        #Determine the time-of-day period
        current_period = get_day_period(current_hour)
        #Print the time-of-day period only when it changes
        if current_period != last_printed_period:
            print("Период суток:", current_period)
            last_printed_period = current_period

        if current_minute != last_printed_minute:
            print("сейчас на ноутбуке:",
                current_hour, ":", current_minute)
            last_printed_minute = current_minute


        #Time when a stat reached zero during recalculation
        hunger_zero_time = None
        health_zero_time = None

        #Hunger decreases every real-world hour
        while real_time - last_hunger_decrease >= GAME_HOUR:
            old_hunger = hunger
            hunger = decrease_stat(hunger, 4.2)
            last_hunger_decrease += GAME_HOUR
            if old_hunger > 0 and hunger == 0:
                hunger_zero_time = last_hunger_decrease
        #Happiness decreases every three real-world hours
        while real_time - last_happiness_decrease >= GAME_HOUR * 3:
            happiness = decrease_stat(happiness, 12.5)
            last_happiness_decrease += GAME_HOUR * 3
        #Health decreases every two real-world hours
        while real_time - last_health_decrease >= GAME_HOUR * 2:
            old_health = health
            health = decrease_stat(health, 8.3)
            last_health_decrease += GAME_HOUR * 2 
            if old_health > 0 and health == 0:
                health_zero_time = last_health_decrease

        #Update food animation
        if food_anim_playing:
            if current_time - food_anim_timer > food_anim_delay:
                food_anim_index += 1
                food_anim_timer = current_time
                if food_anim_index >= len (food_anim_frames):
                    # Stop the food animation
                    food_anim_playing = False
                    food_anim_index = 0
                    # If the completed action was eating
                    if current_action == "food":
                        #Increase hunger stat only after chewing ends
                        hunger = increase_stat(hunger)
        # Allow new actions again
                        action_in_progress = False
                        current_action = None

        #Update fun room animation
        if fun_anim_playing:
            if current_time - fun_anim_timer > fun_anim_delay:
                fun_anim_index += 1
                fun_anim_timer = current_time
                if fun_anim_index >= len(fun_anim_frames):
                    fun_anim_playing = False
                    fun_anim_index = 0
                    if current_action == "fun":
                        happiness = increase_stat(happiness)
                        action_in_progress = False
                        current_action = None

        #Update looping sleep animation
        if plant_is_sleeping and not wake_anim_playing:
            if current_time - sleep_anim_timer > sleep_anim_delay:
                sleep_anim_index += 1
                sleep_anim_timer = current_time
                if sleep_anim_index >= len(sleep_anim_frames):
                    sleep_anim_index = 0
        #Update alarm animation
        if wake_anim_playing:
            if current_time - wake_anim_timer > wake_anim_delay:
                wake_anim_index += 1
                wake_anim_timer = current_time
                if wake_anim_index >= len(wake_anim_frames):
                    wake_anim_playing = False
                    plant_is_sleeping = False
                    wake_anim_index = 0

        #Update care room animation
        if care_anim_playing:
            if current_time - care_anim_timer > care_anim_delay:
                care_anim_index += 1
                care_anim_timer = current_time
                if care_anim_index >= len(care_anim_frames):
                    care_anim_playing = False
                    care_anim_index = 0
                    if current_action == "care":
                        if not worm_active:
                            health = increase_stat(health)
                    elif current_action == "anti_worm":
                        if worm_active:
                            worm_active = False
                            health = increase_stat(health, 25)
                    action_in_progress = False
                    current_action = None
        
        if hunger == 0 and health == 0:
            if death_condition_start is None:
                zero_times = [
                    time for time in
                    (hunger_zero_time, health_zero_time)
                    if time is not None]
                if zero_times:
                    death_condition_start = max(zero_times)
                elif saved_both_zero and last_save_time is not None:
                    death_condition_start = datetime.strptime(
                    last_save_time, "%Y-%m-%d %H:%M:%S")
                else:
                    death_condition_start = real_time
        else:
            death_condition_start = None
            saved_both_zero = False

        #Check whether 24 hours have passed before Game Over
        if (death_condition_start is not None
            and real_time - death_condition_start >= timedelta(hours=24)):
            pygame.mixer.stop()
            return "game_over"

        if game_age >= timedelta(days=15):
            pygame.mixer.stop()
            return "ending"
                    
        #Mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        #Hand cursor:
        if screen_state == "main_room":
            active_buttons = main_room_buttons
        elif screen_state == "food_menu":
            active_buttons = food_menu_buttons
        elif screen_state == "fun_room":
            active_buttons = fun_room_buttons
        elif screen_state == "sleep_room":
            active_buttons = sleep_room_buttons
        elif screen_state == "care_room":
            active_buttons = care_room_buttons
        else: active_buttons = []
        
        
        #Check whether the mouse is over an active button
        hover_any_button = False
        for button in active_buttons:
            if button.is_hover(mouse_pos):
                hover_any_button = True
        #Show hand cursor only over buttons
        if hover_any_button: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    #Draw buttons
        if current_time - plant_timer > plant_delay:
            show_first_plant = not show_first_plant
            plant_timer = current_time
        if screen_state == "main_room":
            draw_main_room()
        elif screen_state == "food_menu":
            draw_food_menu()
        elif screen_state == "fun_room":
            draw_fun_room()
        elif screen_state == "sleep_room":
            draw_sleep_room()
        elif screen_state == "care_room":
            draw_care_room()

        draw_status_panel()
        
    #Music
        if 7 <= current_hour < 18:
            if birds_sound.get_num_channels() == 0:
                birds_sound.play(-1)
                evening_crickets_sound.stop()
                evening_owl_sound.stop()
        else:
            birds_sound.stop()
            if evening_crickets_sound.get_num_channels() == 0:
                evening_crickets_sound.play(-1)
            if evening_owl_sound.get_num_channels() == 0:
                evening_owl_sound.play(-1)
            
        pygame.display.update()
        clock.tick(60)#Limit the frame rate to avoid overloading the CPU

    pygame.mixer.stop()

if __name__ == "__main__":
    run_game()
    pygame.quit()
