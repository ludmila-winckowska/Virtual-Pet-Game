import pygame
import random #randomly select a lightning variant

#resize an image while preserving its aspect ratio
def scale_to_fit(img, max_w, max_h):
    w, h = img.get_size()
    scale = min(max_w/w, max_h/h)
    new_size = (int(w*scale), int(h*scale))
    return pygame.transform.scale(img, new_size)

def run_game_over():
    pygame.init() #initialize Pygame
    pygame.mixer.init() #initialize the audio mixer

    screen = pygame.display.set_mode((500,600))
    pygame.display.set_caption("Virtual Pet Game")

    clock = pygame.time.Clock()

    bg_12 = pygame.image.load("images/bg_12.png").convert()#background
    bg_12 = pygame.transform.scale(bg_12,(500, 600))
    bg_13 = pygame.image.load("images/bg_13.png").convert()
    bg_13 = pygame.transform.scale(bg_13, (500, 600))
    bg_14 = pygame.image.load("images/bg_14.png").convert()
    bg_14 = pygame.transform.scale(bg_14,(500, 600))
    bg_15 = pygame.image.load("images/bg_15.png").convert()
    bg_15 = pygame.transform.scale(bg_15, (500, 600))
    bg_16 = pygame.image.load("images/bg_16.png").convert()
    bg_16 = pygame.transform.scale(bg_16, (500, 600))

    #buttons
    btn_food = pygame.image.load("images/btn_food.png").convert_alpha()#button
    btn_food = pygame.transform.scale(btn_food,(120, 99))
    btn_fun = pygame.image.load("images/btn_fun.png").convert_alpha()
    btn_fun = pygame.transform.scale(btn_fun,(110, 45))
    btn_sleep = pygame.image.load("images/btn_sleep.png").convert_alpha()
    btn_sleep = pygame.transform.scale(btn_sleep, (120, 93))
    btn_care = pygame.image.load("images/btn_care.png").convert_alpha()
    btn_care = pygame.transform.scale(btn_care, (120, 90))
    btn_continue = pygame.image.load("images/btn_continue.png").convert_alpha()#Continue button
    btn_continue = pygame.transform.scale(btn_continue, (120, 90))
    btn_main_menu = pygame.image.load("images/btn_main_menu.png").convert_alpha()#button to return to the main menu
    btn_main_menu = pygame.transform.scale(btn_main_menu, (180, 110))
    btn_exit = pygame.image.load("images/btn_exit.png").convert_alpha()
    btn_exit = pygame.transform.scale(btn_exit, (155, 75)) 

    #final Game Over screen
    bg_17 = pygame.image.load("images/bg_17.png").convert()
    bg_17 = pygame.transform.scale(bg_17, (500, 600))

    #Continue button sound
    back_sound = pygame.mixer.Sound("sounds/back.mp3")

    #error sound
    error_sound = pygame.mixer.Sound("sounds/error_sound.mp3")

    pot_02 = pygame.image.load("images/pot_02.png").convert_alpha()#flowerpot
    pot_02 = scale_to_fit(pot_02, 270, 270)

    plant_76 = pygame.image.load("images/plant_76.png").convert_alpha()#dead plant
    plant_76 = scale_to_fit(plant_76, 270, 270)

    ui_05 = pygame.image.load("images/ui_05.png").convert_alpha()#Game Over sign
    ui_05 = scale_to_fit(ui_05, 120, 120)

    #rain sound
    rain_sound = pygame.mixer.Sound("sounds/rain.mp3") 
    rain_sound.play(-1)#-1 loops the sound indefinitely
    #thunder
    thunder_sound = pygame.mixer.Sound("sounds/thunder.mp3")
    thunder_sound.play(-1)
    #music for the final screen
    cloud_sound = pygame.mixer.Sound("sounds/cloud.mp3")

    bg_state = 0
    bg_12_start_time = pygame.time.get_ticks()#lightning animation
    lightning_time = 0
    lightning_variant = 1 #which lightning variant appears next 

    pot_x = 115
    pot_y = 310

    #button positions
    food_rect = btn_food.get_rect(topleft=(1, pot_y + 152))
    fun_rect = btn_fun.get_rect(topleft=(130, pot_y + 175))
    sleep_rect = btn_sleep.get_rect(topleft=(250, pot_y + 154))
    care_rect = btn_care.get_rect(topleft=(375, pot_y + 154))
    #Continue button position
    continue_rect = btn_continue.get_rect(topleft=(365, 516))
    #final screen button positions
    main_menu_rect = btn_main_menu.get_rect(center=(140, 545))
    exit_rect = btn_exit.get_rect(center=(360, 545))

    food_mask = pygame.mask.from_surface(btn_food)
    fun_mask = pygame.mask.from_surface(btn_fun)
    sleep_mask = pygame.mask.from_surface(btn_sleep)
    care_mask = pygame.mask.from_surface(btn_care)
    continue_mask = pygame.mask.from_surface(btn_continue)
    main_menu_mask = pygame.mask.from_surface(btn_main_menu)
    exit_mask = pygame.mask.from_surface(btn_exit)

    def mask_collide(rect, mask, mouse_pos):
        x = mouse_pos[0] - rect.x
        y = mouse_pos[1] - rect.y

        if 0 <= x < rect.width and 0 <= y < rect.height:
            return mask.get_at((x, y))

        return False

    #Game Over status panel
    def draw_status_panel():
        #Game Over sign
        sign_x = 18
        sign_y = 5
        screen.blit(ui_05, (sign_x, sign_y))

        #semi-transparent gray panel
        panel_width = 125
        panel_height = 140
        panel_x = 15
        panel_y = 75

        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)

        pygame.draw.rect(panel, (180, 180, 180, 150),
                         (0, 0, panel_width, panel_height),
                         border_radius = 25)

        #dark gray status bars
        bar_x = 18
        bar_y = 20 
        bar_width = 90
        bar_height = 14
        bar_gap = 18

        status_values = [0, 0, 0, 0]

        labels = ["Hunger", "Happiness", "Energy", "Health"]
        font = pygame.font.SysFont(None, 18)
        for i in range(4):
            y = bar_y + i * (bar_height + bar_gap)

            pygame.draw.rect(panel, (80, 80, 80, 255),
                             (bar_x, y, bar_width, bar_height), 
                             border_radius=8)

            text = font.render (labels [i], True, (40, 40, 40))
            panel.blit(text, (bar_x, bar_y + i * (bar_height + bar_gap) - 14))

        screen.blit(panel, (panel_x, panel_y))

    #Game Over scene state
    game_over_state = "room"

    running = True

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():#window close event

            if event.type == pygame.QUIT:
                rain_sound.stop()
                thunder_sound.stop()
                cloud_sound.stop()
                pygame.quit()
                raise SystemExit

        #error sound when inactive buttons are clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #error sound when inactive buttons are clicked
                if (game_over_state == "room" and (
                mask_collide(food_rect, food_mask, event.pos)
                or mask_collide(fun_rect, fun_mask, event.pos)
                or mask_collide(sleep_rect, sleep_mask, event.pos)
                or mask_collide(care_rect, care_mask, event.pos))):
                    error_sound.play()

                #switch to the final screen
                if (game_over_state == "room"
                    and mask_collide(continue_rect, continue_mask, event.pos)):
                    back_sound.play()
                    rain_sound.stop()
                    thunder_sound.stop()
                    cloud_sound.play(-1)
                    game_over_state = "cloud"
                #final screen buttons
                elif game_over_state == "cloud":
                    if mask_collide(main_menu_rect, main_menu_mask, event.pos):
                        back_sound.play()
                        cloud_sound.stop()
                        return "main_menu"
                    elif mask_collide(exit_rect, exit_mask, event.pos):
                        back_sound.play()
                        cloud_sound.stop()
                        pygame.quit()
                        raise SystemExit

        #hand cursor when hovering over buttons
        mouse_pos = pygame.mouse.get_pos()
        if game_over_state == "room":
            hover_button = (mask_collide(food_rect, food_mask, mouse_pos)
                            or mask_collide(fun_rect, fun_mask, mouse_pos)
                            or mask_collide(sleep_rect, sleep_mask, mouse_pos)
                            or mask_collide(care_rect, care_mask, mouse_pos)
                            or mask_collide(continue_rect, continue_mask, 
                                            mouse_pos))
        elif game_over_state == "cloud":
            hover_button = (
                mask_collide(main_menu_rect, main_menu_mask, mouse_pos)
                or mask_collide(exit_rect, exit_mask, mouse_pos))
        else:
            hover_button = False
        if hover_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if bg_state == 0:#background and lightning
            screen.blit(bg_12, (0, 0))
            if current_time - bg_12_start_time >= 3000:
                bg_state = 1
                lightning_time = current_time
                lightning_variant = random.choice([1, 2])

        elif bg_state == 1:

            #first lightning stage
            if lightning_variant == 1:
                screen.blit(bg_13, (0, 0))

            else:
                screen.blit(bg_15, (0, 0 ))

            if current_time - lightning_time >= 100:
                bg_state = 2
                lightning_time = current_time

        elif bg_state == 2:

            #full lightning flash
            if lightning_variant == 1:
                screen.blit(bg_14, (0, 0))
            else: 
                screen.blit(bg_16, (0, 0))

            if current_time - lightning_time >= 180:
                bg_state = 0
                bg_12_start_time = current_time

        #draw the flowerpot
        screen.blit(pot_02, (pot_x, pot_y))

        #draw the dead plant
        screen.blit(plant_76, (160, pot_y - 140))

        #draw the Game Over panel
        draw_status_panel()

        #draw the buttons
        screen.blit(btn_food, food_rect)
        screen.blit(btn_fun, fun_rect)
        screen.blit(btn_sleep, sleep_rect)
        screen.blit(btn_care, care_rect)

        #draw the Continue button
        if game_over_state == "room":
            screen.blit(btn_continue, continue_rect)
        #final screen
        if game_over_state == "cloud":
            screen.blit(bg_17, (0, 0))
        #draw the final screen buttons
            screen.blit(btn_main_menu, main_menu_rect)
            screen.blit(btn_exit, exit_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_game_over()
    pygame.quit() 