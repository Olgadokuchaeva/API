import os
import sys

import pygame
import requests

server_address = 'https://static-maps.yandex.ru/v1?'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'

l1 = float(input())
l2 = float(input())
spn1, spn2 = [float(i) for i in input().split()]


def get_image(l1, l2, spn1, spn2):
    ll_spn = f'll={l1},{l2}&spn={spn1},{spn2}'
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

    return map_file


map_file = get_image(l1, l2, spn1, spn2)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.

while pygame.event.wait().type != pygame.QUIT:
    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()

pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)