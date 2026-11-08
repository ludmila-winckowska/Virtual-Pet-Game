import pygame # Imported Pygame
import json
from datetime import datetime
import os
from intro import run_intro
from game import run_game
from ending import run_ending
# Game Over scene
from game_over import run_game_over

pygame.init() # Initialize Pygame
pygame.mixer.init()
WIDTH = 500 # Window width
HEIGHT = 600 # Window height

screen = pygame.display.set_mode((WIDTH,HEIGHT)) # Create the game window
pygame.display.set_caption("Virtual Pet Game") # Game title in the window title bar

bg_11 = pygame.image.load("images/bg_11.png").convert()
bg_11 = pygame.transform.smoothscale(bg_11, (WIDTH, HEIGHT))

error_sound = pygame.mixer.Sound("sounds/error_sound.mp3")
menu_music_sound = pygame.mixer.Sound("sounds/menu_music.mp3")
menu_music_sound.set_volume(0.3)

clock = pygame.time.Clock()

menu_music_sound.play(-1)# -1 means loop indefinitely

new_game_button = pygame.Rect(167, 426, 164, 41)# Button highlight rectangle coordinates
continue_button = pygame.Rect(167, 472, 164, 41)
exit_button = pygame.Rect(167, 518, 164, 41)

SAVE_FILE = "sawe_data.json"

# Create a new game
def create_new_game():
    start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "start_datetime":start_datetime
    }
    with open(SAVE_FILE, "w",encoding="utf-8") as file:# "w" overwrites an existing save
                                           # because the player selected New Game
              json.dump(data, file, ensure_ascii=False, indent=4)
              print("Новая игра создана:", start_datetime)

def has_valid_save():
    if not os.path.exists(SAVE_FILE):# Return False if the save file does not exist
        return False
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)# Try to read the JSON file
            start_datetime = data.get("start_datetime")# Look for start_datetime
            if not start_datetime:
                return False
            datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")# Validate the date format
            return True # Return True if the save is valid

    except (json.JSONDecodeError, OSError, ValueError, TypeError):
        return False # Return False if the save is invalid

# Delete the save after Game Over
def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)    
        


#################################main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:# The player clicked the mouse button
            if new_game_button.collidepoint(event.pos):
                menu_music_sound.stop()
                create_new_game()
                run_intro()
                result = run_game()
                if result == "ending":
                    delete_save()
                    run_ending()
                if result == "game_over":
                    delete_save()
                    run_game_over()
                menu_music_sound.play(-1)
            if continue_button.collidepoint(event.pos):
                if has_valid_save():# Check whether the save is valid
                    menu_music_sound.stop()
                    result = run_game()# If the save file sawe_data.json
                                       # exists, run run_game()
                    if result == "game_over":
                        delete_save()
                        run_game_over()
                    if result == "ending":
                        delete_save()
                        run_ending()
                    menu_music_sound.play(-1)
                else: error_sound.play()

            if exit_button.collidepoint(event.pos):# Check whether the mouse was
                                                   # inside the Exit button area when clicked
                menu_music_sound.stop()
                running = False # If so, stop the main loop

    screen.blit(bg_11, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    if new_game_button.collidepoint(mouse_pos):# Button hover highlight
        pygame.draw.rect(
            screen,(255, 255, 180),
            new_game_button, 3, 
            border_radius = 20)
    if continue_button.collidepoint(mouse_pos):# Button hover highlight
        pygame.draw.rect(
            screen,(255, 255, 180),
            continue_button,3,
            border_radius = 20)
    if exit_button.collidepoint(mouse_pos):# Button hover highlight
        pygame.draw.rect(
            screen,(255, 255, 180),
            exit_button,3,
            border_radius = 20)
    pygame.display.update()
    clock.tick(60)
pygame.quit()