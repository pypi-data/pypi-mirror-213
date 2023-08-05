import math
import inspect
import pygame
import pygame.font

class Enemy:
    _object = []
    typ = "Enemy"

    def __init__(self, _x, _y, _h, _w, _update):
        self._object.append(self)
        self.x = _x
        self.y = _y
        self.h = _h
        self.w = _w
        self.update = _update

    def delete(self, sure):
        if sure:
            self._object.remove(self)

    def hide(self):
        self.typ = "NoN"

    def visible(self, typ):
        self.typ = typ

    def cash(self):
        text = []

        text.append("Enemy\n")
        text.append("x = " + self.x + "\n")
        text.append("y = " + self.y + "\n")
        text.append("h = " + self.h + "\n")
        text.append("w = " + self.w + "\n")
        text.append("func update = " + inspect.getsource(self.update).replace("\n", "/../+o+/../") + "\n")
        text.append("init @x @y @h @w @update\n")
        text.append(";")

        return "".join(text)


class FakeEnemy:
    typ = "Enemy"
    x = 0
    y = 0
    h = 0
    w = 0
    update = lambda: print()

    def __init__(self, _x, _y, _h, _w, _update):
        self.x = _x
        self.y = _y
        self.h = _h
        self.w = _w
        self.update = _update

    def hide(self):
        self.typ = "NoN"

    def visible(self, typ):
        self.typ = typ

    def cash(self):
        text = []

        text.append("FakeEnemy\n")
        text.append("x = " + self.x + "\n")
        text.append("y = " + self.y + "\n")
        text.append("h = " + self.h + "\n")
        text.append("w = " + self.w + "\n")
        text.append("func update = " + inspect.getsource(self.update).replace("\n", "/../+o+/../") + "\n")
        text.append("init @x @y @h @w @update\n")
        text.append(";")

        return "".join(text)


class Player(Enemy):
    typ = "EnemyPlayer"
    speed = 5

    def __init__(self, _x, _y, _h, _w, _update, speed):
        super().__init__(_x, _y, _h, _w, _update)
        self.speed = speed

    def addMove(self, up, down, left, right, obj):
        speed = self.speed
        keys = pygame.key.get_pressed()
        if keys[left]:
            obj.x -= speed
        if keys[right]:
            obj.x += speed
        if keys[up]:
            obj.y -= speed
        if keys[down]:
            obj.y += speed

    def addMoveWithBorder(self, up, down, left, right, obj, w, h):
        speed = self.speed
        keys = pygame.key.get_pressed()
        if keys[left] and obj.x >= self.w:
            obj.x -= speed
        if keys[right] and obj.x <= w - self.w:
            obj.x += speed
        if keys[up] and obj.y >= self.h:
            obj.y -= speed
        if keys[down] and obj.y <= h - self.h:
            obj.y += speed

    def cash(self):
        text = []

        text.append("Player\n")
        text.append("x = " + str(self.x) + "\n")
        text.append("y = " + str(self.y) + "\n")
        text.append("h = " + str(self.h) + "\n")
        text.append("w = " + str(self.w) + "\n")
        text.append("speed = " + str(self.speed) + "\n")
        text.append("func update = " + inspect.getsource(self.update).replace("\n", "/../+o+/../") + "\n")
        text.append("init @x @y @h @w @speed @update\n")
        text.append(";")

        return "".join(text)

class Text(Enemy):
    def __init__(self, x, y, text, font_name, font_size, color):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(font_name, font_size)
        self.color = color

    def set_text(self, text):
        self.text = text

    def set_font(self, font_name, font_size):
        self.font = pygame.font.Font(font_name, font_size)

    def set_color(self, color):
        self.color = color

    def draw(self, window):
        text_surface = self.font.render(self.text, True, self.color)
        window.blit(text_surface, (self.x, self.y))

class MathMap:
    h = 0
    w = 0

    def __init__(self, height, width):
        self._h = height
        self._w = width

    def Distance(x, y, x1, y1):
        distance = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
        return distance

    def Side(x, y, x1, y1):
        if x1 > x:
            return "right"
        elif x1 < x:
            return "left"
        elif y1 > y:
            return "bottom"
        elif y1 < y:
            return "top"
        else:
            return "center"

    def isTouch(self, obj):
        for obj2 in obj._object:
            if obj != obj2:
                if obj.x < obj2.x + obj2.w and obj.x + obj.w > obj2.x and obj.y < obj2.y + obj2.h and obj.y + obj.h > obj2.y:
                    return True
        return False

    def getTouch(self, obj):
        for obj2 in obj._object:
            if obj != obj2:
                if obj.x < obj2.x + obj2.w and obj.x + obj.w > obj2.x and obj.y < obj2.y + obj2.h and obj.y + obj.h > obj2.y:
                    return obj2
        return None


class Map:
    def __init__(self, window, drawingMap):
        self.map = drawingMap
        self.window = window

    def draw(self, map):
        drawMap = self.map

        for card in map:
            if not type(card) == "tuple":
                drawMap[card](self.window, "NoN")
            else:
                for subCard in card:
                    drawMap[subCard](self.window, card)


# class Bank:
#     def __init__(self, src):
#         self.src = src
#
#     def cash(self):
#         text = []
#         for obj in Enemy._object:
#             text.append(obj.cash())
#
#
#         with open(self.src, "w") as file:
#             file.write("\n".join(text))
#
#     def casher(self):
#         with open(self.src, "r") as file:
#             texts = file.read().split(";")
#
#             i = 0
#             while i<len(texts):
#                 text = texts[i].split("\n")
#
#                 y = 0
#
#                 while y < len(text):
#                     line = text[y].replace("^\s+", "").split(" ")
#                     var = dict()
#                     com = line[0]
#                     if com == "func":
#                         pass
#                     else:
#                         if len(line) == 1:
#                             pass
#                         else:
#                             if line[1] == "=":
#                                 var[com] = " ".join(line[2:len(line)])
#                             else:
#                                 print("Unknown value '"+com+"' in cache '"+self.src+"'")
#                     y += 1
#                     print(var)
#                 i += 1

class RunLopster:
    _fps = 16

    def __init__(self, window_size, title, icon, update, fps):
        self._window_size = window_size
        self._title = title
        self._update = update
        self._fps = fps
        self._icon = icon

    def run(self):
        window_size = self._window_size
        title = self._title
        update = self._update
        fps = self._fps
        icon = self._icon

        pygame.init()
        window = pygame.display.set_mode(window_size)

        pygame.display.set_caption(title)

        pygame.display.set_icon(pygame.image.load(icon))

        is_run = True

        while is_run:
            update(window)

            pygame.time.delay(1000 // fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_run = False

            for obj in Enemy._object:
                if obj.typ != "NoN":
                    obj.update(window, obj)

            pygame.display.update()

        pygame.quit()


__all__ = ['Enemy', 'FakeEnemy', 'Player', 'MathMap', 'Map', 'RunLopster']