from src.generator import Generator

import random
import math
import yaml

from emptyMapGenerator.emptyMap import emptyMap, Pose, add_new_obj

from dt_maps import Map, MapLayer
from dt_maps.types.tiles import Tile
from dt_maps.types.frames import Frame
from dt_maps.types.watchtowers import Watchtower


class DuckietownMap(object):
    DEFAULT_MAP_NAME = './maps/new_map.yaml'
    DEFAULT_TILE_SIZE = 0.585
    # DEFAULT_TILE_SIZE = 1.0

    NEW_CELLS = { ### type, yaw
        0: ['floor', 0],
        5: ['straight', 0],
        10: ['straight', 90],
        3: ['curve', 0],
        6: ['curve', 90],
        12: ['curve', 180],
        9: ['curve', 270],
        7: ['3way', 0],
        11: ['3way', 270],
        14: ['3way', 90],
        13: ['3way', 180],
        15: ['4way', 0]
    }

    def __init__(self, generator=None):
        self._map = list()
        self._data = {}
        self._objects = []
        self._generator = generator

    def set_generator(self, generator):
        self._generator = generator

    def new(self):
        self._generator.create()
        state = self._generator.get_state()

        self._map = [['straight/W'] * state.width for _ in range(state.height)]

        for i in range(state.height):
            for j in range(state.width):
                self._map[i][j] = self.NEW_CELLS[state.map[i][j]]
                if state.map[i][j] == 14:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j + 0.25, i],'rotate': 45,'static': True})
                if state.map[i][j] == 7:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j, i + 0.25],'rotate': 45,'static': True})
                if state.map[i][j] == 11:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j + 0.25, i + 1],'rotate': 135,'static': True})
                if state.map[i][j] == 13:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j + 1, i + 0.25],'rotate': 315,'static': True})
                if state.map[i][j] == 15:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j + 0.25, i + 0.25],'rotate': 45,'static': True})

                if self._map[i][j] == 'floor':
                    building_type = random.choice(['duckie',
                                                   'tree',
                                                   'house'])

                    if random.randint(0, 3) == 0:
                        if building_type == 'house':
                            self._objects.append({
                                'height': 0.22, 'kind':building_type, 'pos': [j + 0.2925, i + 0.2925], 'rotate': 0
                            })
                        elif building_type == 'tree':
                            for _ in range(random.randint(3, 7)):
                                self._objects.append({
                                    'height': 0.22,
                                    'kind': building_type,
                                    'pos': [j + random.random() * self.DEFAULT_TILE_SIZE, i + random.random() * self.DEFAULT_TILE_SIZE],
                                    'rotate': 0
                                })
                        elif building_type == 'duckie':
                            for _ in range(random.randint(1, 4)):
                                self._objects.append({
                                    'height': 0.04,
                                    'kind': building_type,
                                    'pos': [j + random.random() * self.DEFAULT_TILE_SIZE, i + random.random() * self.DEFAULT_TILE_SIZE],
                                    'rotate': 0
                                })


                if state.map[i][j] == 14:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j + 0.25, i],'rotate': 45,'static': True})
                if state.map[i][j] == 7:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j, i + 0.25],'rotate': 45,'static': True})
                if state.map[i][j] == 11:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j + 0.25, i + 1],'rotate': 135,'static': True})
                if state.map[i][j] == 13:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j + 1, i + 0.25],'rotate': 315,'static': True})
                if state.map[i][j] == 15:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j + 0.25, i + 0.25],'rotate': 45,'static': True})

        self._data = {
            'tiles': self._map,
            'objects': self._objects,
            'tile_size': self.DEFAULT_TILE_SIZE
        }

        return self

    def _create_objects(self):
        for _ in range(random.randint(150, 151)):
            duckie_pos = [1 + random.random(), 3 * random.random()]
            my_pos = [3.5, 1.5]
            vector = [duckie_pos[0] - my_pos[0], -duckie_pos[1] + my_pos[1]]

            self._objects.append({
                'height': 0.06,
                'kind': random.choice(['sign_blank']),
                'pos': duckie_pos,
                'rotate': 160 + math.degrees(math.atan2(vector[1], vector[0])),
                'static': True
            })

        self._objects.append({
            'height': 0.06,
            'kind': random.choice(['bus']),
            'pos': [2.1, 1.5],
            'rotate': 90,
            'static': True
        })

    def print_map(self, state):
        old_map = state.map
        # old_map =tuple(zip(*old_map[::-1])) #rotate to 90 degree
        print("map=",old_map)
        for i in range(state.height):
            for j in range(state.width):
                if old_map[i][j] != 0 :
                    print("#", end=' ')
                else:
                    print("0", end=' ')
            print('\n', end='')


    def is_near_road(self, state, cells: list):
        old_map = state.map
        near_road_floor = []
        wt_list = []
        # print(state.width, state.height)
        for i in range(0, len(cells)):
            cell = cells[i]
            a = cell[0]
            b = cell[1]

            # print(a, b)
            if old_map[a + 1][b] in (5, 10, 7, 11, 13, 14):
                near_road_floor.append(cell)
                wt_list.append([a,b,90]) # сверху

            if old_map[a - 1][b] in (5, 10, 7, 11, 13, 14):
                near_road_floor.append(cell)
                wt_list.append([a,b,270]) # снизу

            if old_map[a][b + 1] in (5, 10, 7, 11, 13, 14):
                near_road_floor.append(cell)
                wt_list.append([a,b,0]) # слева

            if old_map[a][b - 1] in (5, 10, 7, 11, 13, 14):
                near_road_floor.append(cell)
                wt_list.append([a,b,180]) # справа

        list1 = near_road_floor
        list2 = []
        for item in list1:
            if item not in list2:
                list2.append(item)

        near_road_floor = list2
        return near_road_floor, wt_list


    def get_watchtowers_place(self, state):
        old_map = state.map
        width = state.width
        height = state.height

        floor_list = []
        for i in range(1, height - 1):
            for j in range(1,width-1):
                if old_map[i][j] == 0:
                    floor_list.append([i,j])

        # self.print_map(state)
        # print("floor_list", floor_list)
        flor_near_road, watchtowers_list = self.is_near_road(state, floor_list)

        # print("flor_near_road",flor_near_road)
        # print("watchtower_list=",watchtowers_list)
        self.print_map(state)
        return  watchtowers_list

    def save_new_architecture(self):

        state = self._generator.get_state()
        old_map = state.map
        eMap = emptyMap(state.width, state.height)

        frames_layer = MapLayer(eMap.map, "frames")
        tiles_layer = MapLayer(eMap.map, "tiles")
        tile_maps_layer = MapLayer(eMap.map, "tile_maps", eMap.createTileMaps())

        add_new_obj(eMap.map, frames_layer, "frames", 'map_0', {'relative_to': None, 'pose': None})
        frames_layer['map_0']['pose'] = Pose(1.0, 2.0).get_pose()

        for height in range(0, state.width):
            for width in range(0, state.height):
                old_cell = old_map[width][height]
                new_cell = self.NEW_CELLS[old_cell]
                pose = Pose(x=width, y=height, yaw=new_cell[1])
                eMap.createMapTileBlock(eMap.map, frames_layer, width, height, None, pose)
                add_new_obj(eMap.map, tiles_layer, "tiles", f'map_0/tile_{width}_{height}', {'i': width, 'j': height, 'type': new_cell[0]})

        watchtower_layer = MapLayer(eMap.map, "watchtowers")
        watchtowers_list = self.get_watchtowers_place(state)
        eMap.createWatchtowers(eMap.map, frames_layer, watchtower_layer, watchtowers_list)
       # print(old_map)

        eMap.map.layers.__dict__["watchtowers"] = watchtower_layer
        eMap.map.layers.__dict__["frames"] = frames_layer
        eMap.map.layers.__dict__["tiles"] = tiles_layer
        eMap.map.layers.__dict__["tile_maps"] = tile_maps_layer
        eMap.map.to_disk()


    def save(self, file_name=DEFAULT_MAP_NAME):

        self.save_new_architecture()            ### reload to new arch map
        with open(file_name, 'w') as fout:
            fout.write(yaml.dump(self._data))

