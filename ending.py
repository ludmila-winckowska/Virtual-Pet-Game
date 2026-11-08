import pygame
import random# random numbers (for movement, effects, and randomness)
import math# math (sin, cos for smooth motion and oscillations)

def run_ending():
    pygame.init()
    screen = pygame.display.set_mode((500,600))
    pygame.display.set_caption("Virtual Pet Game")

    def scale_to_fit(img, max_w, max_h):
        w, h = img.get_size()
        scale = min(max_w / w, max_h / h)
        new_size = (int(w * scale), int(h * scale))
        return pygame.transform.scale(img,new_size)

    bg = pygame.image.load("images/bg_03.png").convert()# background image
    bg = pygame.transform.scale(bg, (500,600))

    pot_2 = pygame.image.load("images/pot_02.png").convert_alpha()# pot without arms
    pot_2 = scale_to_fit(pot_2, 270, 270)
    show_pot2 = False

    # images
    plant_29 = pygame.image.load("images/plant_29.png").convert_alpha()# leaf 29
    plant_29 = scale_to_fit(plant_29, 320, 320)
    plant_39 = pygame.image.load("images/plant_39.png").convert_alpha()
    plant_39 = scale_to_fit(plant_39, 360, 360)
    plant_40 = pygame.image.load("images/plant_40.png").convert_alpha()
    plant_40 = scale_to_fit(plant_40, 370,370)
    plant_41 = pygame.image.load("images/plant_41.png").convert_alpha()
    plant_41 = scale_to_fit(plant_41, 350,350)
    plant_42 = pygame.image.load("images/plant_42.png").convert_alpha()
    plant_42 = scale_to_fit(plant_42, 370,370)
    beach = pygame.image.load("images/beach_01.png").convert()
    beach = pygame.transform.scale(beach,(500,600))
    plant_43 = pygame.image.load("images/plant_43.png").convert_alpha()
    plant_43 = scale_to_fit(plant_43, 350,350)
    plant_38 = pygame.image.load("images/plant_38.png").convert_alpha()
    plant_38 = scale_to_fit(plant_38, 350,350)
    plant_26 = pygame.image.load("images/plant_26.png").convert_alpha()
    plant_26 = scale_to_fit(plant_26, 350,350)
    plant_20 = pygame.image.load("images/plant_20.png").convert_alpha()
    plant_20 = scale_to_fit(plant_20, 360,360)
    plant_20_02 = pygame.image.load("images/plant_20_02.png").convert_alpha()
    plant_20_02 = scale_to_fit(plant_20_02, 360,360)
    plant_37 = pygame.image.load("images/plant_37.png").convert_alpha()
    plant_37 = scale_to_fit(plant_37, 350,350)
    plant_43_02 = pygame.image.load("images/plant_43_02.png").convert_alpha()
    plant_43_02 = scale_to_fit(plant_43_02, 350,350)
    longe = pygame.image.load("images/lounge.png").convert_alpha()
    longe = scale_to_fit(longe, 350, 350)
    umbrella = pygame.image.load("images/umbrella.png").convert_alpha()
    umbrella = scale_to_fit(umbrella, 380, 380)
    glasses = pygame.image.load("images/glasses.png").convert_alpha()
    glasses = scale_to_fit(glasses, 200, 200)
    coconut = pygame.image.load("images/coconut.png").convert_alpha()
    coconut = scale_to_fit(coconut, 200, 200)
    necklace = pygame.image.load("images/necklace.png").convert_alpha()
    necklace = scale_to_fit(necklace, 200, 200)
    plant_44 = pygame.image.load("images/plant_44.png").convert_alpha()
    plant_44 = scale_to_fit(plant_44, 560,560)
    plant_44_02 = pygame.image.load("images/plant_44_02.png").convert_alpha()
    plant_44_02 = scale_to_fit(plant_44_02, 560,560)
    plant_45 = pygame.image.load("images/plant_45.png").convert_alpha()
    plant_45 = scale_to_fit(plant_45, 560,560)
    plant_45_02 = pygame.image.load("images/plant_45_02.png").convert_alpha()
    plant_45_02 = scale_to_fit(plant_45_02, 560,560)
    plant_46 = pygame.image.load("images/plant_46.png").convert_alpha()
    plant_46 = scale_to_fit(plant_46, 560,560)
    plant_46_02 = pygame.image.load("images/plant_46_02.png").convert_alpha()
    plant_46_02 = scale_to_fit(plant_46_02, 560,560)
    plant_47 = pygame.image.load("images/plant_47.png").convert_alpha()
    plant_47 = scale_to_fit(plant_47, 560,560)
    plant_47_02 = pygame.image.load("images/plant_47_02.png").convert_alpha()
    plant_47_02 = scale_to_fit(plant_47_02, 560,560)
    plant_48 = pygame.image.load("images/plant_48.png").convert_alpha()
    plant_48 = scale_to_fit(plant_48, 560,560)
    plant_48_02 = pygame.image.load("images/plant_48_02.png").convert_alpha()
    plant_48_02 = scale_to_fit(plant_48_02, 560,560)
    plant_49 = pygame.image.load("images/plant_49.png").convert_alpha()
    plant_49 = scale_to_fit(plant_49, 560,560)
    plant_49_02 = pygame.image.load("images/plant_49_02.png").convert_alpha()
    plant_49_02 = scale_to_fit(plant_49_02, 560,560)
    plant_50 = pygame.image.load("images/plant_50.png").convert_alpha()
    plant_50 = scale_to_fit(plant_50, 570,570)
    plant_50_02 = pygame.image.load("images/plant_50_02.png").convert_alpha()
    plant_50_02 = scale_to_fit(plant_50_02, 570,570)
    beach_02 = pygame.image.load("images/beach_02.png").convert()
    beach_02 = pygame.transform.scale(beach_02, (500,600))
    end = pygame.image.load("images/end.png").convert()
    end = pygame.transform.scale(end,(500,600))
    gull = pygame.image.load("images/gull.png").convert_alpha()
    gull = pygame.transform.scale(gull,(200,200))

    magic_time = pygame.time.get_ticks()

    clock = pygame.time.Clock()
    pot_x = 115
    pot_y = 310

    longe_y = -350
    longe_x = 20
    longe_falling = False

    umbrella_x = 40
    umbrella_y = -380
    umbrella_falling = False

    glasses_x = 150
    glasses_y = -200
    glasses_falling = False
    glasses_done = False

    coconut_x = 200
    coconut_y = -300
    coconut_falling = False
    coconut_done = False

    necklace_x = 150
    necklace_y = -300
    necklace_falling = False
    necklace_done = False

    beach_end_time = 43000# beach scene ends
    final_end_time = 48000# final end screen begins

    gull_x = 500
    gull_y = -30# height
    gull_speed = 1# speed

    # room fireflies
    fireflies = []
    fireflies_started = False
    fireflies_start_time = 0
    firefly_color = (206, 255, 199)# red-orange
    # beach fireflies
    beach_fireflies = []
    beach_fireflies_started = False
    beach_fireflies_start_time = 0
    beach_firefly_color = (255, 245, 180)

    # music
    birds_sound = pygame.mixer.Sound("sounds/birds.mp3")
    birds_played = False
    birds_stopped = False # stop the sound after the background changes

    magic_sound = pygame.mixer.Sound("sounds/magic.mp3")
    magic_played = False
    magic_start_time = 0 # used to stop the sound if needed; see the loop
    magic_items_played = False# flag for stopping the sound at a specific moment

    magical_sound = pygame.mixer.Sound("sounds/magical_02.mp3")
    magical_played = False

    seagulls_sound = pygame.mixer.Sound("sounds/seagulls.wav")
    seagulls_played = False

    beach_magic_sound = pygame.mixer.Sound("sounds/magic.mp3")
    beach_magic_played = False
    beach_magic_stopped = False

    beach_magical_sound = pygame.mixer.Sound("sounds/magical_02.mp3")
    beach_magical_played = False

    hawaii_sound = pygame.mixer.Sound("sounds/hawaii.mp3")
    hawaii_played = False


    # light flash in the room
    flash_started = False
    flash_start_time = 0
    # flash on the beach
    beach_flash_started = False
    beach_flash_start_time = 0

    ending_start_time = pygame.time.get_ticks()
    ##############################################
    # loop
    running = True
    while running:

        current_time = pygame.time.get_ticks()# current Pygame time
        ending_time = current_time - ending_start_time# elapsed time 
                                                      # since the ending began

        if ending_time > final_end_time:
            screen.blit(end, (0, 0))
            screen.blit(gull, (gull_x, gull_y))
            gull_x -= gull_speed
            if gull_x < -200:# restart when the seagull flies off-screen
                gull_x = 500
        elif ending_time > beach_end_time:
            screen.blit(beach_02, (0,0))
        elif flash_started and current_time - flash_start_time >3800:
            screen.blit(beach, (0,0))
        else:
            screen.blit(bg, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.stop()
                pygame.quit()
                raise SystemExit
                
        
        show_pot2 = True
        if not (flash_started and current_time - flash_start_time > 3800):
            screen.blit(pot_2, (115, 310))
        
    # plant in the room
        t = pygame.time.get_ticks() - magic_time
        if t < 1000:
            screen.blit(plant_29, (95, pot_y - 255))# width and height
        elif t < 1300:
            screen.blit(plant_29, (95, pot_y - 255))
            alpha = int(255 * (t - 1000) / 300)
            plant_39_copy = plant_39.copy()
            plant_39_copy.set_alpha(alpha)
            screen.blit(plant_39_copy, (65, pot_y - 290))
            
        elif t < 7300:
            loop_frames = [
                (plant_39, (65, pot_y - 290)),
                (plant_40, (67, pot_y - 295)),
                (plant_41, (75, pot_y - 280)),
                (plant_42, (70, pot_y - 290)),]
            loop_duration = 300
            t_loop = (t - 1300)% (
                len(loop_frames)* loop_duration)
            index = t_loop // loop_duration
            img, pos = loop_frames[index]
            x,y = pos
            screen.blit(img, (x,y))

        if ending_time <= beach_end_time:# stop drawing these elements after 43 seconds        
    # umbrella
            if not umbrella_falling and ending_time> 23000:
                umbrella_falling = True
            if umbrella_falling:
                if umbrella_y < 200:
                    umbrella_y += 2
                screen.blit(umbrella, (umbrella_x, umbrella_y))
    # lounge chair
            if not longe_falling and ending_time> 21000:# appearance time
                longe_falling = True
            if longe_falling:# rendering
                if longe_y < 300:
                    longe_y += 2
                screen.blit(longe, (longe_x, longe_y))

    # plant on the beach
            if beach_flash_started:
                beach_plant_frames = [
                    (plant_43, (70, 190)),
                    (plant_38, (60, 185)),
                    (plant_26, (60, 185)),
                    (plant_26, (60, 185)),
                    (plant_38, (60, 185)),
                    (plant_26, (60, 185)),
                    (plant_38, (60, 185)),
                    (plant_26, (60, 185)),
                    (plant_38, (60, 185)),
                    (plant_26, (60, 185)),
                    (plant_43, (70, 190)),
                    (plant_43_02, (70, 190)),
                    (plant_43, (70, 190)),
                    (plant_43_02, (70, 190)),
                    (plant_43, (70, 190)),
                    (plant_43_02, (70, 190)),
                    (plant_43, (70, 190)),
                    (plant_43_02, (70, 190)),
                    (plant_38, (60, 185)),
                    (plant_26, (60, 185)),
                    (plant_43, (70, 190)),
                    (plant_43_02, (70, 190)),
                    (plant_44, (-50, 180)),
                    (plant_44_02, (-50, 180)),
                    (plant_45, (-45, 180)),
                    (plant_45_02, (-45, 180)),
                    (plant_46, (-45, 180)),
                    (plant_46_02, (-45, 180)),
                    (plant_47, (-50, 180)),
                    (plant_47_02, (-50, 180)),
                    (plant_48, (-40, 180)),
                    (plant_48_02, (-40, 180)),
                    (plant_47, (-50, 180)),
                    (plant_49, (-40, 180)),
                    (plant_49_02, (-40, 180)),
                    (plant_50, (-40, 180)),
                    (plant_50_02, (-40, 180)),
                    (plant_49, (-40, 180)),
                    (plant_49_02, (-40, 180)),
                    (plant_50, (-40, 180)),
                    (plant_50_02, (-40, 180)),
                    (plant_49, (-40, 180)),
                    (plant_49_02, (-40, 180)),
                    (plant_50, (-40, 180)),
                    (plant_50_02, (-40, 180)),
                    (plant_50, (-40, 180)),
                    (plant_50_02, (-40, 180)),
                    (plant_50, (-40, 180)),
                    (plant_50_02, (-40, 180)),
                    (plant_50, (-40, 180)),
                    ]
                frame_duration = 500
                fade_duration = 100
                if ending_time > 18000:
                    t_beach_plant = ending_time - 18000
                    total_duration = len (beach_plant_frames)*frame_duration
                    if t_beach_plant >= total_duration:
                        last_img, last_pos = beach_plant_frames[-1]
                        last_x, last_y = last_pos
                        screen.blit(last_img, (last_x, last_y))
                    else:
                        index = t_beach_plant // frame_duration
                        local_t = t_beach_plant % frame_duration
                        img1, pos1 = beach_plant_frames[index]
                        x1, y1 = pos1
                        screen.blit(img1, (x1, y1))
                        if (
                        index < len(beach_plant_frames) - 1
                            and local_t >= frame_duration -
            fade_duration):
                            alpha = int(255 * (
                                local_t - (frame_duration - fade_duration)
                            ) /fade_duration)
                            img2, pos2 = beach_plant_frames[index + 1]
                            x2, y2 = pos2
                            img2_copy = img2.copy()
                            img2_copy.set_alpha(alpha)
                            screen.blit(img2_copy, (x2, y2))
    # sunglasses
            if not glasses_falling and not glasses_done and ending_time> 26000:
                glasses_falling = True
                glasses_y = -200
            if glasses_falling:
                if glasses_y < 200:
                    glasses_y += 2
                    screen.blit(glasses, (glasses_x, glasses_y))
                else:
                    glasses_falling = False# stop and no longer draw the sunglasses
                    glasses_done = True

    # necklace
            if not necklace_falling and not necklace_done and ending_time> 30000:
                necklace_falling = True
                necklace_y = -300
                beach_magic_sound.stop()# stop the magic sound while the necklace falls
            if necklace_falling:
                if necklace_y < 300:
                    necklace_y += 2
                    screen.blit(necklace, (necklace_x, necklace_y))
                else:
                    necklace_falling = False# stop and no longer draw the necklace
                    necklace_done = True            
    # coconut
            if not coconut_falling and not coconut_done and ending_time> 29800:
                coconut_falling = True
                coconut_y = -300
            if coconut_falling:
                if coconut_y < 300:
                    coconut_y += 2
                    screen.blit(coconut, (coconut_x, coconut_y))
                else:
                    coconut_falling = False# stop and no longer draw the coconut
                    coconut_done = True
            
    # fireflies
        if not fireflies_started and ending_time > 2000:# fireflies appear after 2 seconds
            fireflies_started = True
            fireflies_start_time = current_time
        if fireflies_started and current_time - fireflies_start_time < 7000:
            while len(fireflies) < 20:# number of fireflies
                big = random.choice([True, False])
                if big:
                    r = random.randint(2,3)# firefly size
                else:
                    r = random.randint(1,2)
                fireflies.append({
                    "x": random.randint(50, 400),# firefly coordinates
                    "y": random.randint(100, 400),
                    "speed": random.uniform(1.0, 2.0),
                    "r": r,
                    "phase": random.randint(0,1000),
                    "jitter": 2,
                    "drift": random.uniform(-1, 1)})
            for f in fireflies[:]:
                f ["y"] -= f["speed"]
                f ["x"] += math.sin((current_time + f["phase"])*10)*1 + f[
                        "drift"]
                alpha = 120 + 100 * math.sin((current_time + f[
                        "phase"])* 0.01)
                alpha = max(80, min(255, int(alpha)))
                dx = random.uniform(-f["jitter"],f["jitter"])
                dy = random.uniform(-f["jitter"],f["jitter"])
                r = f["r"]
                size = 50 * r
                glow = pygame.Surface((size, size), pygame.SRCALPHA)
                center = size // 2
                pygame.draw.circle(glow,(*firefly_color, int(alpha*0.15)),
                                    (center,center),int(r*4))
                pygame.draw.circle(glow,(*firefly_color, int(alpha * 0.35)),
                                    (center,center), int(r*2))
                pygame.draw.circle(glow,(*firefly_color, alpha), (center,
                                                                    center),r)
                screen.blit(glow, (f["x"] - center + dx, f["y"] - center + dy))
                if f["y"] < -50:
                        fireflies.remove(f)
    # fireflies on the beach
        if 13000 < ending_time < 19000:
            while len(beach_fireflies) < 18:
                big = random.choice([True,False])
                if big:
                    r = random.randint(2, 3)
                else:
                    r = random.randint(1, 2)
                beach_fireflies.append({
                    "x": random.randint(80, 420),
                    "y": random.randint(430,520),# height (decrease the value to move them higher)
                    "speed": random.uniform(1.0, 2.0),
                    "r": r,
                    "phase": random.randint(0,1000),
                    "jitter": 1.5,
                    "drift": random.uniform(-0.8, 0.8)})
            for f in beach_fireflies[:]:
                f["y"] -= f["speed"]
                f["x"] += math.sin((current_time + f["phase"]) *
                                        0.01) * 0.8 + f["drift"]
                alpha = 120 + 100 * math.sin((current_time + f["phase"]) * 0.01)
                alpha = max(70, min(255, int(alpha)))
                dx = random.uniform(-f["jitter"], f["jitter"])
                dy = random.uniform(-f["jitter"], f["jitter"])
                r = f["r"]
                size = 20 * r
                glow = pygame.Surface((size,size), pygame.SRCALPHA)
                center = size // 2
                pygame.draw.circle(glow,
                                    (*beach_firefly_color,int(alpha*0.15)), (
                                        center,center), int(r*4))
                pygame.draw.circle(glow,(*beach_firefly_color, int (
                        alpha * 0.35)), (center,center), int(r*2))
                pygame.draw.circle(glow,(*beach_firefly_color, alpha),(
                        center,center), r)
                screen.blit(glow, (f["x"] - center + dx, f["y"] - center + dy))
                if f ["y"] < -50:
                    beach_fireflies.remove(f)
                if ending_time >= 19000:
                    beach_fireflies = []
                                    
                                        
                    
        # music
        if not birds_played: # start the sound immediately
            birds_sound.play()
            birds_played = True
        if (      # stop the birds after the background changes
            flash_started and current_time -
            flash_start_time > 3800
            and not birds_stopped):
            birds_sound.stop()
            birds_stopped = True
        if not magic_played and ending_time > 2000:# start the sound after 2 seconds
            magic_sound.play()
            magic_played = True
            magic_start_time = current_time
        if (
            flash_started and current_time-
            flash_start_time > 3800 and not seagulls_played):
            seagulls_sound.play(-1)
            seagulls_played = True
        if magic_played and current_time - magic_start_time > 4000:# stops after 4 seconds
            magic_sound.stop()
        if not magical_played and ending_time > 7000:
            magical_sound.play()
            magical_played = True
        if not beach_magic_played and ending_time >13000:
            beach_magic_sound.play()
            beach_magic_played = True
        if not beach_magic_stopped and ending_time >= 19000:
            beach_magic_sound.stop()
            beach_magic_stopped = True
        if not magic_items_played and ending_time > 21000:
            beach_magic_sound.play(-1)
            magic_items_played = True
        if not hawaii_played and ending_time > 24000:
            hawaii_sound.play(-1)# loop the sound
            hawaii_played = True

    # flash in the room
        if not flash_started and ending_time > 7000:# appears at the 5th second
            flash_started = True
            flash_start_time = current_time
        if flash_started:# render the flash
            flash_time = current_time - flash_start_time
            if flash_time <800:
                alpha = int(255 * flash_time / 800)
                flash = pygame.Surface((500,600), pygame.SRCALPHA)
                flash.fill((255,255,255, alpha))
                screen.blit(flash, (0,0))
    # flash on the beach
        if not beach_flash_started and ending_time > 17000:# appearance time
            beach_flash_started = True
            beach_flash_start_time = current_time
            if not beach_magical_played:# sound for the flash
                beach_magical_sound.play()
                beach_magical_played = True
        if beach_flash_started:
            beach_flash_time = current_time - beach_flash_start_time
            if beach_flash_time < 1200:
                alpha = int(255 * beach_flash_time / 1200)
                beach_flash = pygame.Surface((500,600),pygame.SRCALPHA)
                beach_flash.fill((255,255,255, alpha))
                screen.blit(beach_flash, (0,0))
                        
        pygame.display.update()
        clock.tick(60)# avoid overloading the CPU
    pygame.mixer.stop()

if __name__ == "__main__":
    run_ending()
    pygame.quit()
            

