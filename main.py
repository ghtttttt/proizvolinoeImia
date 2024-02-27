import pygame
import requests
import os

longitude = 2.29444
latitude = 48.85806
howclose = 17
ty = "map"
step_lr = 0.01
step_ud = 0.005


def makemap(lo, la, z, t):
    map_r = f"http://static-maps.yandex.ru/1.x/?ll={(str(lo) + ',' + str(la))}&z={z}&l={t}"
    res = requests.get(map_r)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(res.content)
    return map_file


def main():
    try:
        global howclose, latitude, longitude, ty
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        font = pygame.font.Font(None, 32)
        input_box = pygame.Rect(100, 100, 140, 32)
        color_inactive = pygame.Color('black')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    if event.button == 3:
                        if howclose != 1:
                            howclose -= 1
                    elif event.button == 1:
                        if howclose != 21:
                            howclose += 1
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

                if event.key == pygame.K_LEFT:
                    longitude -= step_lr * 2 ** (15 - howclose)
                elif event.key == pygame.K_RIGHT:
                    longitude += step_lr * 2 ** (15 - howclose)
                elif event.key == pygame.K_UP:
                    latitude += step_ud * 2 ** (15 - howclose)
                elif event.key == pygame.K_DOWN:
                    latitude -= step_ud * 2 ** (15 - howclose)
                elif event.key == pygame.K_1:
                    ty = 'map'
                elif event.key == pygame.K_2:
                    ty = 'sat'
                elif event.key == pygame.K_3:
                    ty = 'sat,skl'
            mp = makemap(longitude, latitude, howclose, ty)
            pygame.display.flip()
            screen.fill((30, 30, 30))
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(pygame.transform.scale(pygame.image.load(mp), (800, 600)), (0, 0))
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)
        pygame.quit()
        os.remove(mp)
    except:
        pass


if __name__ == "__main__":
    main()