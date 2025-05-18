import os
import sys
import pygame
import requests


def get_image(l1, l2, spn1, dark=False):
    ll_spn = f'll={l1},{l2}&spn={spn1}'
    theme = '&theme=dark' if dark else ''
    map_request = f"{server_address}{ll_spn}{theme}&apikey={api_key}"
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


def draw_theme_button():
    button_text = "Тёмная тема" if not dark_theme else "Светлая тема"
    text_surface = font.render(button_text, True, (255, 255, 255))
    button_rect = pygame.Rect(450, 10, 140, 30)
    pygame.draw.rect(screen, (50, 50, 50), button_rect)
    screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 5))
    return button_rect

# Настройки API
server_address = 'https://static-maps.yandex.ru/v1?'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'

# Получение параметров от пользователя
l1 = float(input())
l2 = float(input())
spn1 = int(input())

pygame.init()
screen = pygame.display.set_mode((600, 450))
font = pygame.font.SysFont('Arial', 20)
dark_theme = False
map_file = get_image(l1, l2, spn1, dark_theme)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if theme_button.collidepoint(mouse_pos):
                    dark_theme = not dark_theme
                    map_file = get_image(l1, l2, spn1, dark_theme)
    screen.blit(pygame.image.load(map_file), (0, 0))
    theme_button = draw_theme_button()
    pygame.display.flip()

pygame.quit()
os.remove(map_file)