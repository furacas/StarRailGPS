import json

from star_rail_gps.utils.resources import resource_path

with open(resource_path('maps/name_id.json'), 'r', encoding='utf-8') as f:
    name_id_map = json.load(f)


def position(screen, map_name=None):
    map_id = name_id_map[map_name]

    print(map_id)


position(1, map_name="流云渡 2层")
