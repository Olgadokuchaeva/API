import math
import os
import sys
import pygame
import requests

server_address = 'https://static-maps.yandex.ru/v1?'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'

l1 = float(input())
l2 = float(input())
spn1 = int(input())

def get_image(l1, l2, spn1, theme):
    ll_spn = f'll={l1},{l2}&z={spn1}&size=600,450&theme={theme}'

    map_request = f"{server_address}{ll_spn}&apikey={api_key}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file



pygame.init()
screen = pygame.display.set_mode((800, 450))
map_file = get_image(l1, l2, spn1, "light")
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
running = True
cnt = 1
LAT_STEP = 0.008  # Шаги при движении карты по широте и долготе
LON_STEP = 0.002
coord_to_geo_x = 0.0000428  # Пропорции пиксельных и географических координат.
coord_to_geo_y = 0.0000428

theme_but = pygame.rect.Rect(610, 10, 180, 50)
theme = "light"

while running:

    pygame.draw.rect(screen, "white", theme_but)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                l1 -= LON_STEP * math.pow(2, 15 - spn1)
            elif event.key == pygame.K_RIGHT:
                l1 += LON_STEP * math.pow(2, 15 - spn1)
            elif event.key == pygame.K_UP:
                l2 += LAT_STEP * math.pow(2, 15 - spn1)
            elif event.key == pygame.K_DOWN:
                l2 -= LAT_STEP * math.pow(2, 15 - spn1)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            if spn1 < 21:  # Page_UP
                spn1 += 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            if spn1 > 0:  # Page_DOWN
                spn1 -= 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if theme_but.collidepoint(pygame.mouse.get_pos()):
                if theme == "light":
                    theme = "dark"
                elif theme == "dark":
                    theme = "light"
        map_file = get_image(l1, l2, spn1, theme)
        screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

pygame.quit()
os.remove(map_file)
