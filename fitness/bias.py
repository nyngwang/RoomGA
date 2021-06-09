from typing import Tuple
from main import RoomMap, RoomCell
from main import W, H, get_size_mapitem

Value = int
Weight = int


def is_chair(room_cell: RoomCell) -> bool:
    for i in range(get_size_mapitem()):
        if i == 6 or i == 14 or i == 8:  # Mod Chair, Dining Chair, Chair (Simple).
            if room_cell[i] == 1:
                return True
    return False


def fitness(room_map: RoomMap, h: int, w: int) -> Tuple[Value, Weight]:
    value = 0
    weight = 0
    hot_index = -1
    for i, hot in enumerate(room_map[h][w]):
        if hot == 1:
            hot_index = i
            break

    if hot_index == -1:
        return value, weight
    elif hot_index == 0:  # Whiteboard = 2x2,
        if h <= H//2:
            value = 100
            weight = 10
        else:
            value = 20
            weight = 50
    elif hot_index == 1:  # Projector Screen
        if h <= H//2:
            value = 100
            weight = 10
        else:
            value = 10
            weight = 50
    elif hot_index == 2:  # Chippendale Table (2x3)
        weight = 100
        if 2 <= h <= H-4 and 1 <= w <= W-4:
            value = 100
            for _w in range(w, w + 3):
                if is_chair(room_map[h + 2][_w]):
                    value += 100
                if is_chair(room_map[h - 1][_w]):
                    value += 100
            for _x in range(h, h + 1):
                if is_chair(room_map[_x][w + 3]):
                    value += 100
                if is_chair(room_map[_x][w - 1]):
                    value += 100
    elif hot_index == 3:  # TV (Flatscreen)
        if h == 0 and w <= W-2:
            value = 200
            weight = 50
        else:
            value = 10
            weight = 100
    elif hot_index == 4:  # Bookshelf (2x4)
        if h == 0 and 0 <= w <= W-4:
            value = 100
            weight = 50
        else:
            value = 20
            weight = 100
    elif hot_index == 5:  # Potted Plant (Spikey), Lucky Bamboo
        if h == 0 or h == H-1:
            weight = 100
        elif w == 0 or w == W-1:
            value = 100
            weight = 20
        else:
            value = 50
            weight = 100
    elif hot_index == 6 or hot_index == 14:  # Mod Chair, Dining Chair (Square)
        weight = 40
    elif hot_index == 7:  # Captain’s Chair
        if 1 <= h <= H//2:
            value = 150
            weight = 50
        else:
            value = 20
            weight = 100
    elif hot_index == 8:  # Chair (Simple)
        weight = 120
        if 2 <= h <= H//2 and 1 <= w <= W-2:
            value = 120
            for _w in range(1, W-2):
                if _w != w:
                    value += 1000
                    break
    elif hot_index == 9:  # Chippendale Table (3x3)
        weight = 200
        if 2 <= h <= H-5 and 1 <= w <= W-5:
            value = 400
            for _w in range(w, w + 3):
                if is_chair(room_map[h + 3][_w]):
                    value += 120
                if is_chair(room_map[h - 1][_w]):
                    value += 120
            for _x in range(h, h + 2):
                if is_chair(room_map[_x][w + 3]):
                    value += 120
                if is_chair(room_map[_x][w - 1]):
                    value += 120
    elif hot_index == 10:  # Bookshelf [Tall] (1x2)
        if h == 0:
            value = 120
            weight = 50
    elif hot_index == 11:  # Laptop
        pass
    elif hot_index == 12:  # Microphone
        pass
    return value, weight
