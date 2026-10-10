import pygame
import random #случайные числа (для движения, эффектов, рандома)
import math #математика (sin, cos дя павных движений, колебаний)
from datetime import datetime, timedelta #чтобы игра видела время на ноутбуке
import json
import os

def run_game():

    pygame.init()#включаем графику, окна и кнопки
    pygame.mixer.init()#отдельно запускаем "движок" для звука

    screen = pygame.display.set_mode((500,600))
    pygame.display.set_caption("Virtual Companion")

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
            #обычная картинка кнопки
            self.image = image
            #координаты кнопки
            self.pos = pos
            #прямоугольник кнопки для клика и наведения
            self.rect = self.image.get_rect(topleft=pos)
            #маленькая зона реакции мышки
            self.hit_rect = self.rect.copy()
            self.hit_rect.width = int(self.rect.width * hitbox_scale)
            self.hit_rect.height = int(self.rect.height * hitbox_scale)
            self.hit_rect.center = self.rect.center
            #размер обычной кнопки
            w, h = self.image.get_size()
            #увеиченная картинка кнопки при наведении
            self.hover_image = pygame.transform.scale(
                self.image,
                (int(w * hover_scale), int(h* hover_scale)))
            #увеичение кнопки рисуется из центральной обычной
            self.hover_rect = self.hover_image.get_rect(center=self.rect.center)
        def is_hover(self, mouse_pos):
            #проверка:мышка наведена на кнопку
            return self.hit_rect.collidepoint(mouse_pos)
        def is_clicked(self, event):
            #проверка:по кнопке кликнули мышкой
            return (event.type == pygame.MOUSEBUTTONDOWN
                    and self.hit_rect.collidepoint(event.pos))
        def draw(self, screen):
            #позиция мышки
            mouse_pos = pygame.mouse.get_pos()
            #если мышка наведена - рисуем увеличенную кнопку
            if self.is_hover(mouse_pos):
                screen.blit(self.hover_image, self.hover_rect)
                #иначе рисуем обычную кнопку
            else: screen.blit(self.image, self.rect)
                                                                            
    #картинки
    main_bg = pygame.image.load("images/bg_04.png").convert()#фон главное меню
    main_bg = pygame.transform.scale(main_bg, (500,600))
    main_bg_evening = pygame.image.load("images/bg_07.png").convert()#фон вечернего меню
    main_bg_evening = pygame.transform.scale(main_bg_evening, (500, 600))
    food_bg = pygame.image.load("images/bg_05.png").convert()#фон еда
    food_bg = pygame.transform.scale(food_bg, (500, 600))
    food_bg_evening = pygame.image.load("images/bg_08.png").convert()#фон вечернего меню еда
    food_bg_evening = pygame.transform.scale(food_bg_evening, (500, 600))
    fun_bg = pygame.image.load("images/bg_02.png").convert()#фон развлечения
    fun_bg = pygame.transform.scale(fun_bg,(500, 600))
    sleep_bg = pygame.image.load("images/bg_01.png").convert()#фон для ночи спальни
    sleep_bg = pygame.transform.scale(sleep_bg, (500, 600))
    sleep_bg_day = pygame.image.load("images/bg_09.png").convert()#фон для дневной спальной 
    sleep_bg_day = pygame.transform.scale(sleep_bg_day, (500, 600))
    care_bg = pygame.image.load("images/bg_06.png").convert()#фон для ухода
    care_bg = pygame.transform.scale(care_bg, (500,600))
    care_bg_evening = pygame.image.load("images/bg_10.png").convert()#фон для вечернего ухода
    care_bg_evening = pygame.transform.scale(care_bg_evening, (500,600))

    pot_2 = pygame.image.load("images/pot_02.png").convert_alpha()#горшок без рук
    pot_2 = scale_to_fit(pot_2, 270, 270)
    show_pot2 = False

    plant_26 = pygame.image.load("images/plant_26.png").convert_alpha()#раст.mein_r.
    plant_26 = scale_to_fit(plant_26, 290, 290)
    plant_38 = pygame.image.load("images/plant_38.png").convert_alpha()#раст.mein_r.
    plant_38 = scale_to_fit(plant_38, 290, 290)
    plant_26_care = pygame.image.load("images/plant_26.png").convert_alpha()#раc.care
    plant_26_care = scale_to_fit(plant_26_care, 260, 260)
    plant_38_care = pygame.image.load("images/plant_38.png").convert_alpha()#рас.care
    plant_38_care = scale_to_fit(plant_38_care, 260, 260)

    btn_food = pygame.image.load("images/btn_food.png").convert_alpha()#кнопка еда
    btn_food = pygame.transform.scale (btn_food, (120, 99))
    btn_fun = pygame.image.load("images/btn_fun.png").convert_alpha()#кноп.развлечения
    btn_fun = pygame.transform.scale(btn_fun, (110, 45))
    btn_sleep = pygame.image.load("images/btn_sleep.png").convert_alpha()#кн.спать
    btn_sleep = pygame.transform.scale (btn_sleep, (120, 93))
    btn_care = pygame.image.load("images/btn_care.png").convert_alpha()#кн.полив
    btn_care = pygame.transform.scale (btn_care, (120, 90))

    plant_24 = pygame.image.load("images/plant_24.png").convert_alpha()#растениеfood
    plant_24 = scale_to_fit(plant_24, 290, 290)
    plant_25 = pygame.image.load("images/plant_25.png").convert_alpha()#растениеfood
    plant_25 = scale_to_fit(plant_25, 290, 290)
    plant_30 = pygame.image.load("images/plant_30.png").convert_alpha()#растениеfood
    plant_30 = scale_to_fit(plant_30, 290, 290)
    plant_31 = pygame.image.load("images/plant_31.png").convert_alpha()#растениеfood
    plant_31 = scale_to_fit(plant_31, 290, 290)

    plant_60 = pygame.image.load("images/plant_60.png").convert_alpha()#раст. sleep
    plant_60 = scale_to_fit(plant_60, 290, 290)
    plant_61 = pygame.image.load("images/plant_61.png").convert_alpha()#раст. sleep
    plant_61 = scale_to_fit(plant_61, 290, 290)

    plant_62 = pygame.image.load("images/plant_62.png").convert_alpha()#растениеcare
    plant_62 = scale_to_fit(plant_62, 260, 260)
    plant_63 = pygame.image.load("images/plant_63.png").convert_alpha()#растениеcare
    plant_63 = scale_to_fit(plant_63, 260, 260)

    plant_64 = pygame.image.load("images/plant_64.png").convert_alpha()#раст. sleep
    plant_64 = scale_to_fit(plant_64, 280, 280)
    plant_65 = pygame.image.load("images/plant_65.png").convert_alpha()#раст. sleep
    plant_65 = scale_to_fit(plant_65, 280, 280)
    plant_66 = pygame.image.load("images/plant_66.png").convert_alpha()#раст. sleep
    plant_66 = scale_to_fit(plant_66, 280, 280)
    plant_67 = pygame.image.load("images/plant_67.png").convert_alpha()#раст. alarm
    plant_67 = scale_to_fit(plant_67, 280, 280)
    plant_68 = pygame.image.load("images/plant_68.png").convert_alpha()#раст. alarm
    plant_68 = scale_to_fit(plant_68, 280, 280)
    plant_69 = pygame.image.load("images/plant_69.png").convert_alpha()#раст. alarm
    plant_69 = scale_to_fit(plant_69, 280, 280)

    plant_53 = pygame.image.load("images/plant_53.png").convert_alpha()#растение fun
    plant_53 = scale_to_fit(plant_53, 280, 280)
    plant_54 = pygame.image.load("images/plant_54.png").convert_alpha()#растение fun
    plant_54 = scale_to_fit(plant_54, 280, 280)
    plant_55 = pygame.image.load("images/plant_55.png").convert_alpha()#растение fun
    plant_55 = scale_to_fit(plant_55, 280, 280)
    plant_56 = pygame.image.load("images/plant_56.png").convert_alpha()#растение fun 
    plant_56 = scale_to_fit(plant_56, 280, 280)
    plant_57 = pygame.image.load("images/plant_57.png").convert_alpha()#растение fun
    plant_57 = scale_to_fit(plant_57, 280, 280)
    plant_58 = pygame.image.load("images/plant_58.png").convert_alpha()#растение fun
    plant_58 = scale_to_fit(plant_58, 280, 280)
    plant_59 = pygame.image.load("images/plant_59.png").convert_alpha()#растение fun
    plant_59 = scale_to_fit(plant_59, 280, 280)

    plant_70 = pygame.image.load("images/plant_70.png").convert_alpha()#раст.care
    plant_70 = scale_to_fit(plant_70, 305, 305)#поливалка
    plant_71 = pygame.image.load("images/plant_71.png").convert_alpha()#раст.care
    plant_71 = scale_to_fit(plant_71, 305, 305)#поливалка
    plant_72 = pygame.image.load("images/plant_72.png").convert_alpha()#раст.care
    plant_72 = scale_to_fit(plant_72, 320, 320)#орошение
    plant_73 = pygame.image.load("images/plant_73.png").convert_alpha()#раст.care
    plant_73 = scale_to_fit(plant_73, 310, 310)#орошение
    plant_43 = pygame.image.load("images/plant_43.png").convert_alpha()#раст.care
    plant_43 = scale_to_fit(plant_43, 270, 270)#блеск для листьев
    plant_43_02 = pygame.image.load("images/plant_43_02.png").convert_alpha()#раст.care
    plant_43_02 = scale_to_fit(plant_43_02, 270, 270)#блеск для листьев

    plant_51 = pygame.image.load("images/plant_51.png").convert_alpha()#раст.main_room
    plant_51 = scale_to_fit(plant_51, 290, 290)
    plant_52 = pygame.image.load("images/plant_52.png").convert_alpha()#раст.main_room
    plant_52 = scale_to_fit(plant_52, 290, 290)
    plant_74 = pygame.image.load("images/plant_74.png").convert_alpha()#раст.main_room
    plant_74 = scale_to_fit(plant_74, 290, 290)
    plant_75 = pygame.image.load("images/plant_75.png").convert_alpha()#раст.main_room
    plant_75 = scale_to_fit(plant_75, 290, 290)
    plant_74_care = pygame.image.load("images/plant_74.png").convert_alpha()#раст.main_room
    plant_74_care = scale_to_fit(plant_74_care, 260, 260)
    plant_75_care = pygame.image.load("images/plant_75.png").convert_alpha()#раст.main_room
    plant_75_care = scale_to_fit(plant_75_care, 260, 260)

    plant_37 = pygame.image.load("images/plant_37.png").convert_alpha()#раст.main_room
    plant_37 = scale_to_fit(plant_37, 290, 290)
    plant_37_1 = pygame.image.load("images/plant_37_1.png").convert_alpha()#раст.main_room
    plant_37_1 = scale_to_fit(plant_37_1, 290, 290)
    plant_37_care = pygame.image.load("images/plant_37.png").convert_alpha()#раст.main_room
    plant_37_care = scale_to_fit(plant_37_care, 260, 260)
    plant_37_1_care = pygame.image.load("images/plant_37_1.png").convert_alpha()#раст.main_room
    plant_37_1_care = scale_to_fit(plant_37_1_care, 260, 260)

    btn_05 = pygame.image.load("images/btn_05.png").convert_alpha()#суп
    btn_05 = pygame.transform.scale(btn_05,(150, 130))
    btn_06 = pygame.image.load("images/btn_06.png").convert_alpha()#рыба
    btn_06 = pygame.transform.scale(btn_06,(150, 130))
    btn_07 = pygame.image.load("images/btn_07.png").convert_alpha()#курица
    btn_07 = pygame.transform.scale(btn_07,(150, 130))
    btn_08 = pygame.image.load("images/btn_08.png").convert_alpha()#спагетти
    btn_08 = pygame.transform.scale(btn_08,(150, 130))
    btn_09 = pygame.image.load("images/btn_09.png").convert_alpha()#салат
    btn_09 = pygame.transform.scale(btn_09,(150, 130))
    btn_10 = pygame.image.load("images/btn_10.png").convert_alpha()#торт
    btn_10 = pygame.transform.scale(btn_10,(150, 130))

    btn_12 = pygame.image.load("images/btn_12.png").convert_alpha()#поливалка
    btn_12 = pygame.transform.scale(btn_12,(120, 120))
    btn_13 = pygame.image.load("images/btn_13.png").convert_alpha()#удобрение
    btn_13 = pygame.transform.scale(btn_13,(120, 120))
    btn_14 = pygame.image.load("images/btn_14.png").convert_alpha()#анти-червяк
    btn_14 = pygame.transform.scale(btn_14,(120, 120))
    btn_15 = pygame.image.load("images/btn_15.png").convert_alpha()#орошение
    btn_15 = pygame.transform.scale(btn_15,(110, 110))
    btn_16 = pygame.image.load("images/btn_16.png").convert_alpha()#блеск для листьев
    btn_16 = pygame.transform.scale(btn_16,(110, 110))

    btn_back = pygame.image.load("images/btn_back.png").convert_alpha()#стрекавозвр.
    btn_back = pygame.transform.scale(btn_back, (60, 60))#стрека возврата
    btn_back_big = pygame.transform.scale(btn_back, (70, 70))#стрека возврата

    plant_51 = pygame.image.load("images/plant_51.png").convert_alpha()#раст. fun_room
    plant_51 = scale_to_fit(plant_51, 290, 290)
    plant_52 = pygame.image.load("images/plant_52.png").convert_alpha()#раст. fun_room
    plant_52 = scale_to_fit(plant_52, 290, 290)

    btn_02 = pygame.image.load("images/btn_02.png").convert_alpha()#кнопка книга
    btn_02 = pygame.transform.scale(btn_02, (150, 130))
    btn_04 = pygame.image.load("images/btn_04.png").convert_alpha()#кнопка наушники
    btn_04 = pygame.transform.scale(btn_04, (150, 130))

    btn_03 = pygame.image.load("images/btn_03.png").convert_alpha()#кнопка кровать
    btn_03 = pygame.transform.scale(btn_03, (170, 160))
    btn_11 = pygame.image.load("images/btn_11.png").convert_alpha()#кнопка будильник
    btn_11 = pygame.transform.scale(btn_11, (130, 120))

    worm_1 = pygame.image.load("images/worm_1.png").convert_alpha()#червяк
    worm_1_normal = pygame.transform.scale(worm_1, (100, 100))#для main,fun,slip,food-room
    worm_1_care = pygame.transform.scale(worm_1,(90,90))#для care-room

    worm_2 = pygame.image.load("images/worm_2.png").convert_alpha()#червяк
    worm_2_normal = pygame.transform.scale(worm_2, (110, 110))#для main,fun,slip,food-room
    worm_2_care = pygame.transform.scale(worm_2, (100, 100))#для care-room

    ui_01 = pygame.image.load("images/ui_01.png").convert_alpha()#свеча
    ui_01 = pygame.transform.scale(ui_01, (150, 250))
    ui_02 = pygame.image.load("images/ui_02.png").convert_alpha()
    ui_02 = pygame.transform.scale(ui_02, (150, 250))
    ui_03 = pygame.image.load("images/ui_03.png").convert_alpha()
    ui_03 = pygame.transform.scale(ui_03, (150, 250))

    ui_04 = pygame.image.load("images/ui_04.png").convert_alpha()
    ui_04 = scale_to_fit(ui_04, 150, 150)

    #время последнего сохранения игры
    last_save_time = None

    show_first_plant = True
    plant_timer = pygame.time.get_ticks()
    plant_delay = 600 #скорость смены картинки 600 милисекунд

    pot_x = 115
    pot_y = 310

    #координаты комнаты еда
    pot_food_x = 115
    pot_food_y = 290

    food_button_rect = btn_food.get_rect(topleft=(1, pot_y + 170))
    food_base_y = 310

    #координаты комнаты fun
    pot_fun_x = 115
    pot_fun_y = 290
    fun_base_y = 310

    #координаты комнаты sleep
    pot_sleep_x = 130
    pot_sleep_y = 320
    sleep_base_y = 310
    #координаты кадров сна
    sleep_anim_pos = (130, sleep_base_y - 213)
    #повторяющийся кусок сна
    sleep_loop = [
        (plant_64, sleep_anim_pos),
        (plant_65, sleep_anim_pos)]
    #бусконечная анимация сна
    sleep_anim_frames = [
        (plant_66, sleep_anim_pos)]+ sleep_loop * 4 + [ (plant_66, sleep_anim_pos)]
    #кадры пробуждения
    wake_anim_frames = [
        (plant_67, (127, sleep_base_y - 215)),
        (plant_68, (115, sleep_base_y - 215)),
        (plant_69, (135, sleep_base_y - 215)),
        (plant_68, (115, sleep_base_y -215)),
        (plant_67, (127, sleep_base_y - 215))]

    #анимация для 50% и 25% состояния 
    main_sad_frames = [
        (plant_51, (110, 222)),
        (plant_52, (105, 222))]
    main_weak_frames = [
        (plant_74, (165, 150)),
        (plant_75, (160, 155))]

    #переменные:

    #показывает, выполняется и сейчас какое-то действие
    action_in_progress = False

    #запоминает, какое именно действие выполняется
    current_action= None

    #реаьное времяб до которого растение разбужено ночью
    night_wake_until = None
    #реальное время, до которого растение спит днём
    day_sleep_until = None

    #имя файла, куда игра будет сохранять память
    SAVE_FILE = "sawe_data.json"

    #есть ли сейчас червяк в игре
    worm_active = False

    #дата, когда червяк уже появлялся
    worm_spawned_date = None

    #состояние питомца
    hunger = 100
    energy = 100
    happiness = 100
    health = 100
    start_datetime = None

    #тестовая скорость времени
    GAME_HOUR = timedelta(hours=1) #G.H. буквально означает один реальный час
    last_hunger_decrease = datetime.now()
    last_happiness_decrease = datetime.now()
    last_health_decrease = datetime.now()

    #переменная для чтения времени с ноутбука
    last_printed_minute = -1

    #последний выведенный период суток
    last_printed_period = None

    #состояние сна
    plant_is_sleeping = False
    #анимация сна
    sleep_anim_index = 0
    sleep_anim_timer = 0
    sleep_anim_delay = plant_delay
    #анимация пробуждения
    wake_anim_playing = False
    wake_anim_index = 0
    wake_anim_timer = 0
    wake_anim_delay = plant_delay

    #координаты комнаты care
    pot_care_x = 120
    pot_care_y = 230
    care_base_y = 310

    #координаты кадров care-анимаций
    watering_can_pos = (120, care_base_y- 330)
    fertilizer_pos_1 = (130, care_base_y - 285)
    fertilizer_pos_2 = (125, care_base_y - 285)
    anti_worm_pos_1 = (130, care_base_y - 285)
    anti_worm_pos_2 = (125, care_base_y - 285)
    leaf_mist_pos_1 = (105, care_base_y - 315)
    leaf_mist_pos_2 = (115, care_base_y - 325)
    leaf_shine_pos_1 = (125, care_base_y - 290)
    leaf_shine_pos_2 = (115, care_base_y - 290)
    #анимация полива
    watering_can_frames = [
        (plant_70, watering_can_pos),
        (plant_71, watering_can_pos)] * 3
    #анимация удобрения
    fertilizer_frames = [
        (plant_26_care, fertilizer_pos_1),
        (plant_38_care, fertilizer_pos_2)] * 3
    #анимация анти-червяк
    anti_worm_frames = [
        (plant_26_care, anti_worm_pos_1),
        (plant_38_care, anti_worm_pos_2)] * 3
    #анимация распылителя
    leaf_mist_frames = [
        (plant_72, leaf_mist_pos_1),
        (plant_73, leaf_mist_pos_2)] * 3
    #анимация блеск листьев
    leaf_shine_frames = [
        (plant_43, leaf_shine_pos_1),
        (plant_43_02, leaf_shine_pos_2)] * 3

    #координаты кадров книги
    book_pos = (125, fun_base_y - 240)
    #повторяющийся кусок анимации книги
    book_loop = [
        (plant_56, book_pos),
        (plant_57, book_pos),
        (plant_56, book_pos),
        (plant_57, book_pos),
        (plant_58, book_pos),
        (plant_59, book_pos)]
    #полная анимация книги
    book_anim_frames = book_loop * 2 + [
        (plant_56, book_pos),
        (plant_57, book_pos)]
    #повторяющийся кусок aнимации наушников
    headphones_loop = [
        (plant_54, (115, fun_base_y - 235)),
        (plant_55, (110, fun_base_y - 235))]
    #полная анимация наушников
    headphones_anim_frames = [
        (plant_53, (110, fun_base_y - 240))] + headphones_loop * 6 + [
        (plant_53, (110, fun_base_y - 240)) ]

    #координаты червяка в main-room
    worm_main_frames = [(worm_1_normal, (200, pot_y - 27)),
                        (worm_2_normal, (200, pot_y - 38))]
    #координаты червяка в food-menu
    worm_food_frames = [
        (worm_1_normal, (200, food_base_y - 50)),
        (worm_2_normal, (200, food_base_y - 60))]
    #координаты червяка в fun_room
    worm_fun_frames = [ 
        (worm_1_normal, (200, fun_base_y - 50)),
        (worm_2_normal, (200, fun_base_y - 60))]
    #координаты червяка в sleep-room
    worm_sleep_frames = [
        (worm_1_normal, (215, sleep_base_y - 20)),
        (worm_2_normal, (215, sleep_base_y - 30))]
    #координаты червяка в care-room
    worm_care_frames = [
        (worm_1_care, (210, care_base_y - 100)),
        (worm_2_care, (210, care_base_y - 110))]

    #просим у картинки прямоугольник для клика
    btn_back_pos = (435, pot_y - 300)
    btn_back_rect = btn_back.get_rect(topleft=btn_back_pos)

    #кнопки главной комнаты
    food_button = Button(btn_food, (1, pot_y + 170))
    fun_button = Button(btn_fun, (130, pot_y +193))
    sleep_button = Button(btn_sleep, (250, pot_y +172))
    care_button = Button(btn_care, (375, pot_y + 172))

    #кнопка еды
    soup_button = Button(btn_05, (-20, food_base_y + 100),hitbox_scale=0.55)
    fish_button = Button(btn_06, (35, food_base_y + 160),hitbox_scale=0.55)
    chicken_button = Button(btn_07, (145, food_base_y +110),hitbox_scale=0.55)
    spaghetti_button = Button(btn_08, (225, food_base_y +170),hitbox_scale=0.55)
    salad_button = Button(btn_09, (290, food_base_y + 100),hitbox_scale=0.55)
    cake_button = Button(btn_10, (360, food_base_y + 160),hitbox_scale=0.55)

    #кнопка возврата
    back_button = Button(btn_back, btn_back_pos)

    #кнопки комнаты fun
    book_button = Button(btn_02, (90, fun_base_y + 140), hitbox_scale=0.55)
    headphones_button = Button(btn_04, (240, fun_base_y + 140), hitbox_scale=0.55)

    #кнопки комнаты sleep
    bed_button = Button(btn_03, (100, sleep_base_y + 150),hitbox_scale=0.55)
    alarm_button = Button(btn_11, (270, sleep_base_y + 170), hitbox_scale=0.55)

    #кнопки комнаты care
    watering_can_button = Button(btn_12, (40, care_base_y + 170),hitbox_scale=0.55)
    fertilizer_button = Button(btn_13, (130, care_base_y + 170),hitbox_scale=0.55)
    anti_worm_button = Button(btn_14, (205, care_base_y + 170),hitbox_scale=0.55)
    leaf_mist_button = Button(btn_15, (285, care_base_y + 175),hitbox_scale=0.55)
    leaf_shine_button = Button(btn_16, (355, care_base_y + 175),hitbox_scale=0.55)

    #СВЕТЛЯЧКИ
    #светлички care_room
    care_fireflies = []
    care_fireflies_playing = False
    care_fireflies_start_time = 0
    care_fireflies_duration = 3000
    care_firefly_color = (255, 245, 150)
    #цвет светячков
    care_blue = (120, 190, 255)
    care_green = (130, 255, 160)
    care_pink = (255, 150, 220)
    care_cyan = (150, 240, 255)
    care_yellow = (255, 245, 150)

    #список кнопок главной комнаты
    main_room_buttons = [
        food_button,
        fun_button,
        sleep_button,
        care_button]
    #список кнопок комнаты еды
    food_menu_buttons = [
        soup_button,
        fish_button,
        chicken_button,
        spaghetti_button,
        salad_button,
        cake_button,
        back_button]
    #кнопки еды без back
    food_action_buttons =[
        soup_button,
        fish_button,
        chicken_button,
        spaghetti_button,
        salad_button,
        cake_button]
    #список кнопок комнаты fun
    fun_room_buttons = [
        book_button,
        headphones_button,
        back_button]
    #список кнопок комнаты sleep
    sleep_room_buttons = [
        bed_button,
        alarm_button,
        back_button]
    #список кнопок комнаты care
    care_room_buttons = [
        watering_can_button,
        fertilizer_button,
        anti_worm_button,
        leaf_mist_button,
        leaf_shine_button,
        back_button]

    #длительность дневного сна по кнопке
    DAY_SLEEP_DURATION = 60 * 1000
    #время, когда закончится дневной сон
    day_sleep_end_time = None
    #длительность ночного пробуждения
    NIGHT_WAKE_DURATION = 5 * 60 * 1000
    #время окончания ночного пробуждения
    night_wake_end_time = None

    #screen_state = "food_menu"
    screen_state = "main_room"

    magic_time = pygame.time.get_ticks()

    clock = pygame.time.Clock()

    #анимация кормления
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

    #aнимация комнаты fun (чистаю, слушаю музыку)
    fun_anim_playing = False
    fun_anim_index = 0
    fun_anim_index = 0
    fun_anim_timer = 0
    fun_anim_delay = plant_delay
    fun_anim_frames = []

    #анимация care_room(все 5 кнопок)
    care_anim_playing = False
    care_anim_index = 0
    care_anim_timer = 0
    care_anim_delay = plant_delay
    care_anim_frames = []


    #музыка
    birds_sound = pygame.mixer.Sound("sounds/birds.mp3")
    birds_sound.set_volume(0.3)#громкость
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
    music1_sound.set_volume(0.3)#громкость
    music2_sound = pygame.mixer.Sound("sounds/music2.mp3")
    music2_sound.set_volume(0.3)#громкость
    music3_sound = pygame.mixer.Sound("sounds/music3.mp3")
    music3_sound.set_volume(0.3)#громкость
    music_sounds = [music1_sound, music2_sound, music3_sound]#чтобы играла поОчереди
    current_music_index = 0#чтобы играла по очереди
    sleep_sound = pygame.mixer.Sound("sounds/sleep.mp3")
    alarm_sound = pygame.mixer.Sound("sounds/alarm.mp3")
    grumble_sound = pygame.mixer.Sound("sounds/grumble.mp3")
    grumble_sound.set_volume(0.3)
    pour_sound = pygame.mixer.Sound("sounds/pour.mp3")
    sand_sound = pygame.mixer.Sound("sounds/sand.mp3")
    dig_sound = pygame.mixer.Sound("sounds/dig.mp3")
    spray_sound = pygame.mixer.Sound("sounds/spray.mp3")
    error_sound = pygame.mixer.Sound("sounds/error_sound.mp3")


    #ФУНКЦИИ

    #функция выбора состояния
    def get_plant_condition():
        lowest_stat = min(hunger, happiness, health, energy)
        if lowest_stat <= 25:
            return "weak"
        elif lowest_stat <= 50:
            return "sad"
        else:
            return "happy"

    #функция рисует червяка
    def draw_worm(frames):
        if worm_active:
            if show_first_plant:
                worm_img, worm_pos = frames[0]
            else:
                worm_img, worm_pos = frames[1]
            screen.blit(worm_img, worm_pos)

    #функция главной комнаты main_room
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
        #если растение спит, не показывать в main_room
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
        #рисуем все кнопки главной комнаты
        for button in main_room_buttons: button.draw(screen)

    #функция комнтаы food
    def draw_food_menu():
        if 7 <= current_hour < 18:
            screen.blit(food_bg, (0, 0))
        else:
            screen.blit(food_bg_evening, (0, 0))
        screen.blit(pot_2, (pot_food_x, pot_food_y))

        if not plant_is_sleeping:#если растение спит, не показывать в food
            #растение в комнате еды
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
        #рисуем все кнопки комнаты еды
        for button in food_menu_buttons: button.draw(screen)

    #функция комнаты fun
    def draw_fun_room():
        screen.blit(fun_bg, (0, 0))
        screen.blit(pot_2, (pot_fun_x, pot_fun_y))
        if not plant_is_sleeping:#если растение спит, не показывать в fun
            #растение в комнате fun
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
        #рисуем все кнопки комнаты fun
        for button in fun_room_buttons: button.draw(screen)

    #функция комнаты sleep
    def draw_sleep_room():
        if 7 <= current_hour <18:
            screen.blit(sleep_bg_day, (0, 0))
        else:
            screen.blit(sleep_bg, (0, 0))
        screen.blit(pot_2, (pot_sleep_x, pot_sleep_y))
        #растение в комнате sleep
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

        #рисуем все кнопки комнаты sleep
        for button in sleep_room_buttons: button.draw(screen)

    #функция комнаты care
    def draw_care_room():
        if 7 <= current_hour < 18:
            screen.blit(care_bg, (0, 0))
        else:
            screen.blit(care_bg_evening, (0, 0))
        screen.blit(pot_2, (pot_care_x, pot_care_y))
        if not plant_is_sleeping:#если растение спит, не показывать в care
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
        #светлячки
        draw_care_fireflies(pygame.time.get_ticks())
        #кнопки
        for button in care_room_buttons: button.draw(screen)

    #функция светячков
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

    #функция для панели состояния растения
    def draw_status_panel():
        #дощечка с возрастом растения
        sign_x = 5
        sign_y = 5
        screen.blit(ui_04, (sign_x, sign_y))
        sign_font = pygame.font.SysFont(None, 24)
        day_text = sign_font.render("3/15", True, (90,60,20))
        screen.blit(day_text,(sign_x + 77, sign_y + 42))
        #серая полупрозрачная панель
        panel_width = 125
        panel_height = 140
        panel_x = 15
        panel_y = 75
        
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        
        pygame.draw.rect(
            panel,
            (180, 180, 180, 150),
            (0, 0, panel_width, panel_height), border_radius=25)
        
        #тёмно-серые полоски состояния
        bar_x = 18
        bar_y = 20
        bar_width = 90
        bar_height = 14
        bar_gap = 18

        status_values = [hunger, happiness, energy, health] #%
        
        for i in range(4):
            y = bar_y + i * (bar_height + bar_gap)
            #тёмно-серая полоска
            pygame.draw.rect(
                panel,
                (80, 80, 80, 255),
                (bar_x, y, bar_width, bar_height),
                border_radius = 8)
            #зулёная шкала состояния
            green_width = int((bar_width -4)* status_values[i] / 100)
            if green_width > 6:
                pygame.draw.rect(
                    panel,(80, 210, 90, 255),
                    (bar_x + 2, y +3, green_width, bar_height - 6),
                    border_radius=6)
            elif green_width >0:
                pygame.draw.rect(panel,(80, 210, 90, 255),
                            (bar_x + 2, y +3, green_width - 4, bar_height - 6),
                            border_radius = 6)

        #подписи к шкалам
            font = pygame.font.SysFont(None, 18)
            labels = ["Hunger", "Happiness", "Energy", "Health"]
            for i in range(4):
                text = font.render(labels[i],True,(40, 40, 40))
                panel.blit(text, (bar_x, bar_y + i * (bar_height + bar_gap) - 14))
        
            screen.blit(panel, (panel_x, panel_y))

    #функция остановки звука кнопок комнаты care-room
    def stop_care_sounds():
        pour_sound.stop()
        sand_sound.stop()
        dig_sound.stop()
        spray_sound.stop()
        psh_sound.stop()

    #функция ограничение состояния до 100%
    def increase_stat(value, amount=25):
        value += amount
        if value > 100:
            value= 100
        return value

    #функция уменьшения времени
    def decrease_stat (value, amount):
        value -= amount
        if value < 0:
            value = 0
        return value

    #функция определяетпериод суток по часу ноутбука
    def get_day_period(hour):
        #день: с 07:00 до 18:59
        if 7 <= hour < 19:
            return "day"
        #вечер: с 19:00 до 22:59
        elif 19 <= hour < 23:
            return "evening"
        #ночь: с 23:00 до 02:59
        elif hour >= 23 or hour <3:
            return "night"
        #глубокая ночь. восстановление: с 03:00 до 06:59
        else:
            return "deep_night"

    #функция обновляет энергию по времени ноутбука
    def update_energy_by_time(hour):
        #день: с 07:00 до 20:59 энергия всегда 100%
        if 7 <= hour < 21:
            return 100
        #вечер: с 21:00 до 23:59 энергия постепенно падает по 25% в час
        elif 21 <= hour < 24:
            return 100 - (hour - 20)* 25
        #ночь: с 00:00 до 02:59 энергия 0%
        elif 0 <= hour < 3:
            return 0
        #глубокая ночь: с 03:00 до 06:59 энергия восстанавливается на 25% в час
        else:
            return (hour -2)* 25

    #функция проверяет, должно ли растение спать по времени ноутбука
    def should_sleep_by_time(hour):
        #с 00:00 до 6:59 растение спит
        if 0 <= hour < 7:
            return True
        #с 7:00 до 22:59 растение не спит
        else:
            return False

    #функция загружает память игры из файла
    def load_save_data():
        #если файла памяти ещё нет
        if not os.path.exists(SAVE_FILE):
            return None
        #пробуем открыть файл памяти
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        #если фай сломан или не читается
        except Exception:
            return None 

    #функция сoхраняет память игры в файл
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
            "last_save_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S") }
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        #записываем реаьное время закрытия игры
            

    #загружаем память игры один раз при запуске
    saved_data = load_save_data()
    #если файл памяти существует и нормально прочитался
    if saved_data is not None:
        #загружаем показатели растения
        hunger = saved_data.get("hunger", hunger)
        energy = saved_data.get("energy", energy)
        happiness = saved_data.get("happiness", happiness)
        health = saved_data.get("health", health)
        #загружаем время начала игры
        start_datetime = saved_data.get("start_datetime",
                                    start_datetime)
        plant_is_sleeping = saved_data.get(
        "plant_is_sleeping", plant_is_sleeping
    )
        #загружаем данныепро червяка
        worm_active = saved_data.get("worm_active", worm_active)
        worm_spawned_date = saved_data.get("worm_spawned_date", worm_spawned_date)
        #загружаем время ночного пробуждения
        night_wake_until = saved_data.get("night_wake_until", night_wake_until)
        day_sleep_until = saved_data.get(
        "day_sleep_until", day_sleep_until
    )
        #загружаем время последнего сохранения из памяти
        last_save_time = saved_data.get("last_save_time",last_save_time)
        # загружаем время последнего уменьшения показателей
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
        # считаем, сколько реального времени игра была включена
        offline_time = timedelta(0)

        if last_save_time is not None:
            try: 
                last_save_datetime = datetime.strptime(last_save_time, "%Y-%m-%d %H:%M:%S")
                offline_time = datetime.now() - last_save_datetime
            except ValueError:
                offline_time = timedelta(0)

    print("Игра была выключена:", offline_time)

    #проверяем, не было и ночного пробуждения до закрытия игры
    if night_wake_until is not None:#строка сохраняет настоящий 
                                    #момент, до которого растение должно бодрствовать
        try:
            wake_until_time = datetime.strptime(
                night_wake_until, "%Y-%m-%d %H:%M:%S")
            #если 5 минут ещё не прошли
            if datetime.now()<wake_until_time:
                remaining_ms = int(
                    (wake_until_time - datetime.now()).total_seconds()*1000)
                night_wake_end_time = pygame.time.get_ticks()+remaining_ms
                plant_is_sleeping = False
            #если 5 минут уже прошли
            else:
                night_wake_until = None
                night_wake_end_time = None
        except Exception:
            night_wake_until = None
            night_wake_end_time = None

    #проверяем, не закончился ли дневной сон до запуска игры
    if day_sleep_until is not None:
        try:
            sleep_until_time = datetime.strptime(
                day_sleep_until, "%Y-%m-%d %H:%M:%S"
            )

            #если минута сна ещё не прошла
            if datetime.now() < sleep_until_time:
                remaining_ms = int(
                    (sleep_until_time - datetime.now()).total_seconds() * 1000
                )

                day_sleep_end_time = (
                    pygame.time.get_ticks() + remaining_ms
                )

                plant_is_sleeping = True

            #если минута уже прошла
            else:
                day_sleep_end_time = None
                day_sleep_until = None
                plant_is_sleeping = False

        except Exception:
            day_sleep_until = None
            day_sleep_end_time = None
            
    ##############################################
    #цикл
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #сохранять память игры перед закрытием
                save_game_data()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                #клик в главной комнате
                if screen_state == "main_room":
                    btn_sound.play()
                    if food_button.is_clicked(event):screen_state = "food_menu"
                    if fun_button.is_clicked(event):screen_state = "fun_room"
                    if sleep_button.is_clicked(event):screen_state = "sleep_room"
                    if care_button.is_clicked(event):screen_state = "care_room"
                #клик на кнопку back
                elif screen_state == "food_menu":
                    if back_button.is_clicked(event):
                        food_sound.stop()
                        back_sound.play()
                        screen_state = "main_room"
                    #еси нажать любую кнопку еды - запускается анимация
                    for button in food_action_buttons:
                        # если нажать кнопку еды и сейчас не идёт другое действие
                        if (
                            button.is_clicked(event) and not action_in_progress
                            and not plant_is_sleeping
                        ):
                            #блокируем повторные клики
                            action_in_progress = True
                            current_action = "food"
                            food_sound.play()
                            action_sound.play()
                            food_anim_playing = True
                            food_anim_index = 0
                            food_anim_timer = pygame.time.get_ticks()
                            break
                        
                elif screen_state == "fun_room":
                    if back_button.is_clicked(event):
                        read_sound.stop()
                        for sound in music_sounds:
                            sound.stop()
                        back_sound.play()
                        screen_state = "main_room"
                    #если нажать кнопку книга, включается анимация чтения
                    elif (
                        book_button.is_clicked(event)
                        and not action_in_progress
                        and not plant_is_sleeping
                    ):
                        action_in_progress = True
                        current_action = "fun"
                        action_sound.play()
                        for sound in music_sounds:
                            sound.stop()
                        read_sound.play(maxtime=7000)#звучит 8 сек 6 мили секунд
                        fun_anim_playing = True
                        fun_anim_frames = book_anim_frames
                        fun_anim_index = 0
                        fun_anim_timer = pygame.time.get_ticks()
                    #если нажать кнопку наушники, включается анимация слушать музыку
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
                    if back_button.is_clicked(event):#кнопака back
                        grumble_sound.stop()
                        back_sound.play()
                        screen_state = "main_room"
                    #кнопка кровати - растение засыпает
                    elif bed_button.is_clicked(event):
                        action_sound.play()
                        grumble_sound.stop()
                        sleep_sound.play(-1)#-1 повтор бесконечно...
                                                #...проверяем, ночь сейчас или день
                        #останавливаем аним. пробуждения
                        wake_anim_playing = False
                        sleep_anim_index = 0
                        #если растение укладывают с 22:00 до 06:59
                        if current_hour >= 22 or current_hour < 7:
                            #отменяем ночное пробуждение
                            night_wake_end_time = None
                            night_wake_until = None
                            #отменяем дневной сон
                            day_sleep_end_time = None
                            day_sleep_until = None
                            #растение снова спит
                            plant_is_sleeping = True
                        #если сейчас день   
                        else:
                            #отменяем ночное пробуждение
                            night_wake_end_time = None
                            night_wake_until = None
                            #днём растение засыпает только на 1 минуту
                            day_sleep_end_time =(
                                pygame.time.get_ticks() + DAY_SLEEP_DURATION)
                            day_sleep_until = (
                                datetime.now() + timedelta(minutes=1)
                                    ).strftime("%Y-%m-%d %H:%M:%S")
                            plant_is_sleeping = True
                            #запускаем анимацию сна сначала
                        sleep_anim_index = 0
                        sleep_anim_timer = pygame.time.get_ticks()
                        
                    #кнопка будильника - растение просыпается
                    elif alarm_button.is_clicked(event):
                        #будильник работает только если растение сейчас спит
                        if plant_is_sleeping:
                            #с 00:00 до 02:59 можно разбудить на 5 минут
                            if 0 <= current_hour < 3:
                                action_sound.play()
                                alarm_sound.play()
                                grumble_sound.play()
                                night_wake_end_time = (
                                    pygame.time.get_ticks()+ NIGHT_WAKE_DURATION)
                                #запоминать реальное время, до которого растение...
                                #...будет бодрствовать
                                night_wake_until = (
                                    datetime.now()+
                                    timedelta(minutes=5)
                                    ).strftime("%Y-%m-%d %H:%M:%S")
                                plant_is_sleeping = False
                                wake_anim_playing = True
                                wake_anim_index = 0
                                wake_anim_timer = pygame.time.get_ticks()
                                sleep_sound.stop()
                                #c 22:00 до 23:59 можно разбудить без таймера 5 минут
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
                            #с 03:00 до 06:59 растение нельзя разбудить
                            elif 3 <= current_hour <7:
                                pass
                            #днём, если растение спит после кнопки "спать", можно...
                                #...разбудить сразу
                            else:
                                action_sound.play()
                                alarm_sound.play()
                                grumble_sound.play()
                                day_sleep_end_time = None
                                plant_is_sleeping = False
                                wake_anim_playing = True
                                wake_anim_index = 0
                                wake_anim_timer = pygame.time.get_ticks()
                                sleep_sound.stop()
                        
                elif screen_state == "care_room":
                    if back_button.is_clicked(event):#кнопка back
                        stop_care_sounds()
                        back_sound.play()
                        screen_state = "main_room"
                    #кнопка полива
                    elif watering_can_button.is_clicked(event):
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
                            
                    #кнопка удобрения
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
                    
                    #кнопка анти-червяк
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

                    #кнопка распылителя
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
                    
                    #кнопка блеска истьев
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
                    
                        
        current_time = pygame.time.get_ticks()#время

        #игра видит время на ноутбуке
        real_time = datetime.now()
        current_hour = real_time.hour
        current_minute = real_time.minute
        #сегодняшняя дата
        current_date = real_time.strftime("%Y-%m-%d")

        #после 15:00 червяк появляется один раз в день
        if current_hour >= 15 and worm_spawned_date != current_date: 
            worm_active = True
            worm_spawned_date = current_date
            health = 0

        #обновляем энергию по времени ноутбука
        energy = update_energy_by_time(current_hour)

        #проверяем, должно ли растение спать по времени ноутбука
        auto_sleep = should_sleep_by_time(current_hour)
        #если сейчас ночное время сна
        if auto_sleep:
            # с 03:00 до 06:59 растение нельзя разбудить
            if 3 <= current_hour < 7:
                plant_is_sleeping = True
                night_wake_end_time = None
                night_wake_until = None #убирает остаток пятиминутного 
                                        #пробуждения, если оно ещё тянулось с 02:59
                day_sleep_end_time = None
                day_sleep_until = None
                wake_anim_playing = False #отменяет анимацию пробуждения, 
                                        #если ровно в 03:00 она ещё вдруг шла
            #с 00:00 до 02:59 растение можно разбудить на 5 минут
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
        #если сейчас не время автоматического сна
        else:
            night_wake_end_time = None

            #с 22:00 до 23:59 сохраняем текущее состояние
            #если уложили - спит, если разбудили - бодрствует
            if 22 <= current_hour < 24:
                if day_sleep_end_time is not None:
                    if current_time < day_sleep_end_time:
                        plant_is_sleeping = True
                    else:
                        plant_is_sleeping = False
                        sleep_sound.stop()
                        day_sleep_end_time = None
                        day_sleep_until = None

            #с 07:00 до 21:59 работает дневной сон на 1 минуту
            else:
                #если включён дневной сон по кнопке
                if day_sleep_end_time is not None:
                    #если минута ещё не прошла, растение спит
                    if current_time < day_sleep_end_time:
                        plant_is_sleeping = True
                    #если минута прошла, растение просыпается
                    else:
                        plant_is_sleeping = False
                        sleep_sound.stop()
                        day_sleep_end_time = None
                #если дневной сон не включён, растение не спит
                else:
                    plant_is_sleeping = False
                    sleep_sound.stop()
                    day_sleep_end_time = None
            
            #звук сна, когда растение спит
        if plant_is_sleeping:
            if sleep_sound.get_num_channels() == 0:
                sleep_sound.play(-1)
        else:
            sleep_sound.stop()

        #определяем период суток
        current_period = get_day_period(current_hour)
        #выводим период суток только когда он изменился
        if current_period != last_printed_period:
            print("Период суток:", current_period)
            last_printed_period = current_period

        if current_minute != last_printed_minute:
            print("сейчас на ноутбуке:",
                current_hour, ":", current_minute)
            last_printed_minute = current_minute

        #голод уменьшается каждый реальный час
        if real_time - last_hunger_decrease >= GAME_HOUR:
            hunger = decrease_stat(hunger, 4.2)
            last_hunger_decrease += GAME_HOUR
        #счастье уменьшается каждые 3 реальных часа
        if real_time - last_happiness_decrease >= GAME_HOUR * 3:
            happiness = decrease_stat(happiness, 12.5)
            last_happiness_decrease += GAME_HOUR * 3
        #уход уменьшается каждые 2 реальных часа
        if real_time - last_health_decrease >= GAME_HOUR * 2:
            health = decrease_stat(health, 8.3)
            last_health_decrease += GAME_HOUR * 2 

        #обновление анимации food
        if food_anim_playing:
            if current_time - food_anim_timer > food_anim_delay:
                food_anim_index += 1
                food_anim_timer = current_time
                if food_anim_index >= len (food_anim_frames):
                    # останавливаем анимацию еды
                    food_anim_playing = False
                    food_anim_index = 0
                    # если закончилось именно действие еды
                    if current_action == "food":
                        #повышаем сытость только после окончания жевания
                        hunger = increase_stat(hunger)
        # разблокируем новые действия
                        action_in_progress = False
                        current_action = None

        #обновление анимации комнаты fun
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

        #обновление бесконечной анимации sleep
        if plant_is_sleeping and not wake_anim_playing:
            if current_time - sleep_anim_timer > sleep_anim_delay:
                sleep_anim_index += 1
                sleep_anim_timer = current_time
                if sleep_anim_index >= len(sleep_anim_frames):
                    sleep_anim_index = 0
        #обновение анимации будильник
        if wake_anim_playing:
            if current_time - wake_anim_timer > wake_anim_delay:
                wake_anim_index += 1
                wake_anim_timer = current_time
                if wake_anim_index >= len(wake_anim_frames):
                    wake_anim_playing = False
                    plant_is_sleeping = False
                    wake_anim_index = 0

        #обновление анимации care_room
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
                    
        #позиция мышки
        mouse_pos = pygame.mouse.get_pos()
        
        #мышка-пальчик:
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
        
        
        #проверяем, наведена ли мышка на любую активную кнопку
        hover_any_button = False
        for button in active_buttons:
            if button.is_hover(mouse_pos):
                hover_any_button = True
        #паьчик только над кнопками
        if hover_any_button: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    #рисуем кнопки
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
        
    #музыка
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
        clock.tick(60)#чтобы не перегружать процессор

if __name__ == "__main__":
    run_game()
    pygame.quit()
