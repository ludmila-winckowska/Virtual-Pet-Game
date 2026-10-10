import pygame # подключила Pygame
import json
from datetime import datetime
from intro import run_intro
from game import run_game

pygame.init() # запустила модуль
WIDTH = 500 # размер окна
HEIGHT = 600 # размер окна

screen = pygame.display.set_mode((WIDTH,HEIGHT)) # создаёт само окно
pygame.display.set_caption("Virtual Pet Game") # название игры на верху окна

bg_11 = pygame.image.load("images/bg_11.png").convert()
bg_11 = pygame.transform.smoothscale(bg_11, (WIDTH, HEIGHT))

clock = pygame.time.Clock()

new_game_button = pygame.Rect(167, 426, 164, 41)#координаты для рамки кнопок подсветка
continue_button = pygame.Rect(167, 472, 164, 41)
exit_button = pygame.Rect(167, 518, 164, 41)

SAVE_FILE = "sawe_data.json"

#создание новой игры
def create_new_game():
    start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "start_datetime":start_datetime
    }
    with open(SAVE_FILE, "w",encoding="utf-8") as file:# "w" если там было старое прохождение, 
                                           #файл перезапишется,потому что игрок нажал New Game
              json.dump(data, file, ensure_ascii=False, indent=4)
              print("Новая игра создана:", start_datetime)

#################################цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:#пользователь нажал кнопку мыши
            if new_game_button.collidepoint(event.pos):
                create_new_game()
                run_intro()
                run_game()
            if continue_button.collidepoint(event.pos):
                print("Continue")
            if exit_button.collidepoint(event.pos):#проверь:находилась ли мышка 
                                                   #в нашей области exit в момент клика
                running = False#если да(верхнее), то running

    screen.blit(bg_11, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    if new_game_button.collidepoint(mouse_pos):#рамка кнопок подстветка
        pygame.draw.rect(
            screen,(255, 255, 180),
            new_game_button, 3, 
            border_radius = 20)
    if continue_button.collidepoint(mouse_pos):# рамка кнопок подстветка
        pygame.draw.rect(
            screen,(255, 255, 180),
            continue_button,3,
            border_radius = 20)
    if exit_button.collidepoint(mouse_pos):#рамка кнопок подстветка
        pygame.draw.rect(
            screen,(255, 255, 180),
            exit_button,3,
            border_radius = 20)
    pygame.display.update()
    clock.tick(60)
pygame.quit()