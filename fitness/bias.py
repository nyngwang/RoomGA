from typing import Tuple
from main import RoomMap, RoomCell
from main import W, H
from main import id_to_mapitemname

Value = int
Weight = int


def is_chair(room_cell: RoomCell) -> bool:
    for i in range(len(id_to_mapitemname)):
        if i == 6 or i == 14 or i == 8:  # Mod Chair, Dining Chair, Chair (Simple).
            if room_cell[i] == 1:
                return True
    return False


def fitness(hot_index: int, room_map: RoomMap, x: int, y: int) -> Tuple[Value, Weight]:
    value = 0
    weight = 0
    if hot_index == 0:  # Whiteboard = 2x2,
        if y == W-1 or x == H-1:
            weight = 100
        if x == 0:
            value = 20
        elif x <= H//2:
            value = 10
    if hot_index == 1:  # Projector Screen
        if y >= W-2 or x >= H//2:
            weight = 100
        if x == 0:
            value = 20
        elif x <= H//2:
            value = 10
        else:
            value = 0
    if hot_index == 2:  # Chippendale Table (2x3)
        if 2 <= x <= H-4 and 1 <= y <= W-4:
            value = 100
            for _y in range(y, y + 3):
                if is_chair(room_map[x + 2][_y]):
                    value += 100
                if is_chair(room_map[x - 1][_y]):
                    value += 100
            for _x in range(x, x + 1):
                if is_chair(room_map[_x][y + 3]):
                    value += 100
                if is_chair(room_map[_x][y - 1]):
                    value += 100
        else:
            value = 0
        weight = 20
    if hot_index == 3:  # TV (Flatscreen)
        if x == 0 and y <= W-2:
            value = 20
            weight = 5
        else:
            value = 0
            weight = 10
    if hot_index == 4:  # Bookshelf (2x4)
        if x == 0 and 0 <= y <= W-4:
            value = 10
            if room_map[x][y+1][4]\
                or room_map[x][y+2][4]\
                or room_map[x][y+3][4]:
                weight = 10
        else:
            value = 5
            weight=30
    if hot_index == 5:  # Potted Plant (Spikey), Lucky Bamboo
        if x == 0 or x == H-1:
            weight = 100
        else:
            if y == 0 or y == W-1:
                value = 10
                weight = 5
            else:
                value = 10
                weight = 15
    if hot_index == 6 or hot_index == 14:  # Mod Chair, Dining Chair (Square)
        weight = 5
    if hot_index == 7:  # Captain’s Chair
        if 1 <= x <= H//2:
            value = 50
            weight = 10
    if hot_index == 8:  # Chair (Simple)
        if 2 <= x <= H-3 and 1 <= y <= W-2:
            value = 20
            for _y in range(1, W-1):
                if _y != y:
                    value = 100
                    break
            weight = 10
        else:
            weight = 40
    if hot_index == 9:  # Chippendale Table (3x3)
        if 2 <= x <= H-5 and 1 <= y <= W-5:
            value = 120
            for _y in range(y, y+3):
                if is_chair(room_map[x+3][_y]):
                    value += 100
                if is_chair(room_map[x-1][_y]):
                    value += 100
            for _x in range(x, x+2):
                if is_chair(room_map[_x][y+3]):
                    value += 100
                if is_chair(room_map[_x][y-1]):
                    value += 100
        else:
            value = 0
        weight = 30
    if hot_index == 10:  # Bookshelf [Tall] (1x2)
        if x == 0:
            value = 50
            weight = 10
    if hot_index == 11:  # Laptop
        pass
    if hot_index == 12:  # Microphone
        pass
    return value, weight
