import cv2 as cv
import json

with open('resources/maps/name_id.json', 'r', encoding='utf-8') as f:
    name_id_map = json.load(f)




def position(screen,map_name):
    map_id = name_id_map[map_name]

    print(map_id)
    pass

position(1,map_name="流云渡 2层")