import math
import os
import sys

import pygame
import requests

server_address = 'https://static-maps.yandex.ru/v1?'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'

l1 = float(input())
l2 = float(input())

spn1 = float(input())
ll_spn = f'll={l1},{l2}&spn={spn1}'
# Готовим запрос.

map_request = f"{server_address}{ll_spn}&apikey={api_key}"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
running = True
cnt = 1
LAT_STEP = 0.008  # Шаги при движении карты по широте и долготе
LON_STEP = 0.002
coord_to_geo_x = 0.0000428  # Пропорции пиксельных и географических координат.
coord_to_geo_y = 0.0000428
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                l1 -= LON_STEP * math.pow(2, 15 - spn1)
                ll_spn = f'll={l1},{l2}&spn={spn1},{spn1}'
                map_request = f"{server_address}{ll_spn}&apikey={api_key}"
                response = requests.get(map_request)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                screen.blit(pygame.image.load(map_file), (0, 0))
            elif event.key == pygame.K_RIGHT:
                l1 += LON_STEP * math.pow(2, 15 - spn1)
                ll_spn = f'll={l1},{l2}&spn={spn1},{spn1}'
                map_request = f"{server_address}{ll_spn}&apikey={api_key}"
                response = requests.get(map_request)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                screen.blit(pygame.image.load(map_file), (0, 0))
            elif event.key == pygame.K_UP:
                l2 += LAT_STEP * math.pow(2, 15 - spn1)
                ll_spn = f'll={l1},{l2}&spn={spn1},{spn1}'
                map_request = f"{server_address}{ll_spn}&apikey={api_key}"
                response = requests.get(map_request)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                screen.blit(pygame.image.load(map_file), (0, 0))
            elif event.key == pygame.K_DOWN:
                l2 -= LAT_STEP * math.pow(2, 15 - spn1)
                ll_spn = f'll={l1},{l2}&spn={spn1},{spn1}'
                map_request = f"{server_address}{ll_spn}&apikey={api_key}"
                response = requests.get(map_request)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()


pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)