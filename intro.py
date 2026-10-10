import pygame
import random
import math

def run_intro():

    pygame.init()
    screen = pygame.display.set_mode((500,600))
    pygame.display.set_caption("Virtual Companion")

    #это код который делает всегда любую картинку нужного размера
    def scale_to_fit(img, max_w, max_h):
        w, h = img.get_size()
        scale = min(max_w / w, max_h / h)
        new_size = (int(w * scale), int(h * scale))
        return pygame.transform.scale(img,new_size)

    #####  КАРТИНКИ   #####
    #icon=pygame.image.load("images/icon.png")потом сделай иконку,когда нарисуешь
    #pygame.display.set_icon(icon)
    bg = pygame.image.load("images/bg_03.png").convert()#рисунок фона
    bg = pygame.transform.scale(bg, (500,600))

    pot = pygame.image.load("images/pot_01.png").convert_alpha()
    pot = scale_to_fit(pot, 300, 300)
    pot_x = 500 #старт за экраном справа
    pot_y = 310 #высота
    pot_speed = 3 #скорость
    pot_moving = False #о времени появления горшка с руками

    pot_2 = pygame.image.load("images/pot_02.png").convert_alpha()#горшок без рук
    pot_2 = scale_to_fit(pot_2, 270, 270)
    show_pot2 = False

    plant_01 = pygame.image.load("images/plant_01.png").convert_alpha()#листочек 1 
    plant_01 = scale_to_fit(plant_01, 180, 180)
    plant_02 = pygame.image.load("images/plant_02.png").convert_alpha()#листочек 2
    plant_02 = scale_to_fit(plant_02, 180, 180)
    plant_03 = pygame.image.load("images/plant_03.png").convert_alpha()#листочек 3
    plant_03 = scale_to_fit(plant_03, 180, 180)
    plant_04 = pygame.image.load("images/plant_04.png").convert_alpha()#листочек 4
    plant_04 = scale_to_fit(plant_04, 180, 180)
    plant_05 = pygame.image.load("images/plant_05.png").convert_alpha()#листочек 5
    plant_05 = scale_to_fit(plant_05, 180, 180)
    plant_06 = pygame.image.load("images/plant_06.png").convert_alpha()#листочек 6
    plant_06 = scale_to_fit(plant_06, 180, 180)
    plant_07 = pygame.image.load("images/plant_07.png").convert_alpha()#листочек 7
    plant_07 = scale_to_fit(plant_07, 180, 180)
    plant_08 = pygame.image.load("images/plant_08.png").convert_alpha()#листочек 8
    plant_08 = scale_to_fit(plant_08, 180, 180)
    plant_09 = pygame.image.load("images/plant_09.png").convert_alpha()#листочек 9
    plant_09 = scale_to_fit(plant_09, 180, 180)
    plant_10 = pygame.image.load("images/plant_10.png").convert_alpha()#листочек 10
    plant_10 = scale_to_fit(plant_10, 300, 300)
    plant_11 = pygame.image.load("images/plant_11.png").convert_alpha()#листочек 11
    plant_11 = scale_to_fit(plant_11, 290, 290)
    plant_12 = pygame.image.load("images/plant_12.png").convert_alpha()#листочек 12
    plant_12 = scale_to_fit(plant_12, 290, 290)
    plant_13 = pygame.image.load("images/plant_13.png").convert_alpha()#листочек 13
    plant_13 = scale_to_fit(plant_13, 290, 290)
    plant_14 = pygame.image.load("images/plant_14.png").convert_alpha()#листочек 14
    plant_14 = scale_to_fit(plant_14, 440, 440)
    plant_15 = pygame.image.load("images/plant_15.png").convert_alpha()#листочек 15
    plant_15 = scale_to_fit(plant_15, 280, 280)
    plant_16 = pygame.image.load("images/plant_16.png").convert_alpha()#листочек 16
    plant_16 = scale_to_fit(plant_16, 300, 300)
    plant_17 = pygame.image.load("images/plant_17.png").convert_alpha()#листочек 17
    plant_17 = scale_to_fit(plant_17, 300, 300)
    plant_18 = pygame.image.load("images/plant_18.png").convert_alpha()#листочек 18
    plant_18 = scale_to_fit(plant_18, 300, 300)
    plant_19 = pygame.image.load("images/plant_19.png").convert_alpha()#листочек 19
    plant_19 = scale_to_fit(plant_19, 305, 305)
    plant_20 = pygame.image.load("images/plant_20.png").convert_alpha()#листочек 20
    plant_20 = scale_to_fit(plant_20, 310, 310)
    plant_21 = pygame.image.load("images/plant_21.png").convert_alpha()#листочек 21
    plant_21 = scale_to_fit(plant_21, 310, 310)
    plant_26 = pygame.image.load("images/plant_26.png").convert_alpha()#листочек 26
    plant_26 = scale_to_fit(plant_26, 300, 300)
    plant_37 = pygame.image.load("images/plant_37.png").convert_alpha()#листочек 37
    plant_37 = scale_to_fit(plant_37, 320, 320)
    plant_38 = pygame.image.load("images/plant_38.png").convert_alpha()#листочек 26
    plant_38 = scale_to_fit(plant_38, 280, 280)

    clock = pygame.time.Clock() #чтобы не перегружать процессор

    #####   ЗВУКИ #####
    door_sound = pygame.mixer.Sound("sounds/door.mp3")#дверь открывается
    start_time = pygame.time.get_ticks()#звук двери через время после старта
    door_played = False

    boots_sound = pygame.mixer.Sound("sounds/boots.mp3")#звук шагов
    boots_played = False

    ceramik_sound = pygame.mixer.Sound("sounds/ceramic.mp3")#звук поставил горшок
    ceramik_played = False
    ceramik_time = 0

    boots2_sound = pygame.mixer.Sound("sounds/boots.mp3")#шаги посе поставленого горшка
    boots2_played = False

    door2_played = False #двери закрывает

    birds_sound = pygame.mixer.Sound("sounds/birds.mp3")#звук птичек после закрытия двери
    birds_played = False

    magic_sound = pygame.mixer.Sound("sounds/magic.mp3")#звук магии
    magic_played = False
    magic_time = 0

    #СВЕТЛЯЧКИ
    fireflies = []
    fireflies_started = False
    firefly_color = (180, 255, 80)

    ###################цикл
    running = True
    while running:

        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()#звук двери через 3 секунды после плей

        if not door_played and current_time - start_time> 3000:#3 секунды
            door_sound.play()
            door_played = True #чтобы звук не повторялся

        #шаги(через 3 сек + 8 сек = 11сек)
        if door_played and not boots_played and current_time> 11000:
            boots_sound.play()
            boots_played = True

        #горшок с руками
        if current_time - start_time> 17000:
            pot_moving = True
        if pot_moving and pot_x> 110: #110 центр
            pot_x -= pot_speed
        
        #звук поставил горшок
        if not ceramik_played and pot_x <= 180:#чем больше число,тем раньше звук
            ceramik_sound.play()
            ceramik_played = True
            ceramik_time = current_time
        #горшок без рук
        if ceramik_played and current_time - ceramik_time >= 4000:#посе звука
    #поставил горшок, появляется картинка горшок без рук 
            show_pot2 = True
        if show_pot2:
            screen.blit(pot_2, (115, 310))#110(муньше=левее),310(меньше=выше)
        else:
            screen.blit(pot, (pot_x, pot_y))
        if magic_played:
            frames = [      #после магии истик 1.2.3
                (plant_01, (190, pot_y - 50)),
                (plant_02, (190, pot_y - 50)),#190-ширина 50 высота
                (plant_03, (190, pot_y - 50)),
                (plant_02, (190, pot_y - 50)),
                (plant_01, (190, pot_y - 50)),
                (plant_03, (190, pot_y - 50)),
                (plant_04, (165, pot_y - 40)),
                (plant_05, (165, pot_y - 40)),
                (plant_06, (165, pot_y - 40)),
                (plant_05, (165, pot_y - 40)),
                (plant_04, (165, pot_y - 40)),
                (plant_06, (165, pot_y - 40)),
                (plant_07, (165, pot_y - 50)),
                (plant_08, (165, pot_y - 50)),
                (plant_09, (165, pot_y - 50)),
                (plant_08, (165, pot_y - 50)),
                (plant_07, (165, pot_y - 50)),
                (plant_09, (165, pot_y - 50)),
                (plant_10, (100, pot_y - 110)),
                (plant_11, (105, pot_y - 110)),
                (plant_12, (105, pot_y - 105)),
                (plant_11, (105, pot_y - 110)),
                (plant_10, (100, pot_y - 110)),
                (plant_12, (105, pot_y - 105)),
                (plant_13, (105, pot_y - 217)),
                (plant_14, (35, pot_y - 215)),
                (plant_15, (118, pot_y - 223)),
                (plant_14, (35, pot_y - 215)),
                (plant_13, (105, pot_y - 217)),
                (plant_15, (118, pot_y - 223)),
                (plant_16, (85, pot_y - 223)),
                (plant_17, (85, pot_y - 230)),
                (plant_18, (113, pot_y - 243)),
                (plant_17, (85, pot_y - 230)),
                (plant_16, (85, pot_y - 223)),
                (plant_18, (113, pot_y - 243)),
                (plant_19, (80, pot_y - 235)),
                (plant_20, (77, pot_y - 235)),
                (plant_21, (77, pot_y - 235)),
                (plant_20, (77, pot_y - 235)),
                (plant_19, (80, pot_y - 235)),
                (plant_20, (77, pot_y - 235)),            
                (plant_26, (105, pot_y - 245)),]
            frame_duration = 500 #чтобы плавно менялись картинки
            fade_duration = 250
            t = current_time - magic_time
            total_duration = len(frames) * frame_duration
            if t >= total_duration:
                loop_frames = [
                    (plant_37, (90, pot_y - 255)),
                    (plant_38, (105, pot_y - 230)),
                    (plant_26, (105, pot_y - 245)),]
                loop_duration = 400
                t_loop = (
                    current_time - magic_time - total_duration)%(
                        len(loop_frames)*loop_duration)
                index = t_loop // loop_duration
                img, pos = loop_frames[index]
                x,y = pos
                screen.blit(img, (x, y))
            else:
                index = t //frame_duration
                local_t = t % frame_duration
                img1, pos1 = frames[index]
                x1, y1 = pos1
                screen.blit(img1, (x1, y1))
                if index<len(frames)-1 and local_t>=frame_duration-fade_duration:
                    alpha = int(255 *
        (local_t -(frame_duration - fade_duration))/fade_duration)
                    img2, pos2 = frames[index + 1]
                    x2, y2 = pos2
                    img2_copy = img2.copy()
                    img2_copy.set_alpha(alpha)
                    screen.blit(img2_copy, (x2, y2))
            
        #звук шагов после поставленного горшка
        if not boots2_played and current_time - start_time > 24000:
            boots2_sound.play()
            boots2_played = True
        #двери закрывает
        if not door2_played and current_time - start_time > 30000:
            door_sound.play()
            door2_played = True
        #звук птичек после закрытия двери
        if not birds_played and current_time - start_time > 38000:
            birds_sound.play()
            birds_played = True
        #звук магии одновременно с птичками
        if not magic_played and current_time - start_time > 40000:
            magic_sound.play()
            magic_played = True
            fireflies_started = True #светячки
            magic_time = current_time

        #СВЕТЛЯЧКИ
        if fireflies_started:#создаём их
            while len (fireflies) <14:
                big = random.choice([True,False])
                if big:
                    r = random.randint(3,4)
                else:
                    r = random.randint(1,2)
                fireflies.append({"x": random.randint(220, 280),
                                "y": random.randint(-80,0),
                                "speed": random.uniform(1.2, 2.4),
                                "r": r,
                                "phase": random.randint(0, 1000),
                                "jitter": 1.5})
        for f in fireflies:#рисуем их
            f["y"] += f["speed"]
            alpha = 120 + 100 * math.sin((current_time + f["phase"])* 0.01)
            alpha = max(60, min(255,int(alpha)))
            dx = random.uniform(-f["jitter"], f["jitter"])
            dy = random.uniform(-f["jitter"], f["jitter"])
            r = f["r"]
            size = 20 * r
            glow = pygame.Surface((size,size), pygame.SRCALPHA)
            center = size//2
            pygame.draw.circle(glow,(*firefly_color, int(alpha * 0.15)),
    (center, center), int(r * 4))
            pygame.draw.circle(glow,(*firefly_color, int(alpha * 0.35)),
    (center, center), int(r * 2))
            pygame.draw.circle(glow,(*firefly_color, alpha), (center, center), r)
            screen.blit(glow,(f["x"] - center + dx, f["y"] - center + dy))
            if f["y"] > 600:
                fireflies.remove(f)

        # интро заканчивается через 67 секунд
        if current_time - start_time >= 67000:
            print("интро закончено")
            running = False
        
        pygame.display.update()
        clock.tick(60)#чтобы не перегружать процессор
       
if __name__=="__main__":#если я запустила intro/py сама,проиграй интро. но если меня
    #подключил main.py,ничего самостоятельно не начинай, жди вызова run_intro()
    run_intro()
    pygame.quit()

            
