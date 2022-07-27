from advancedMap.advancedMap import advancedMap, Pose, add_new_obj

from dt_maps import MapLayer


class DuckietownMap(object):
    DEFAULT_TILE_SIZE = 0.585

    NEW_CELLS = {  # type, yaw
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

        self._map = [[''] * state.width for _ in range(state.height)]

        for i in range(state.height):
            for j in range(state.width):
                self._map[i][j] = self.NEW_CELLS[state.map[i][j]]

        self._data = {
            'tiles': self._map,
            'objects': self._objects,
            'tile_size': self.DEFAULT_TILE_SIZE
        }
        return self

    def print_map(self, state):
        old_map = state.map
        # old_map =tuple(zip(*old_map[::-1])) #rotate to 90 degree
        print("map=", old_map)
        for i in range(state.height):
            for j in range(state.width):
                if old_map[i][j] != 0:
                    print("#", end=' ')
                else:
                    print("0", end=' ')
            print('\n', end='')

    def is_near_road(self, state, cells: list):
        old_map = state.map
        near_road_floor = []
        wt_list = []
        for i in range(0, len(cells)):
            cell = cells[i]
            a = cell[0]
            b = cell[1]

            if old_map[a + 1][b] in (5, 10, 7, 11, 13, 14):
                near_road_floor.append(cell)
                wt_list.append([a, b, 90])  # сверху

            if old_map[a - 1][b] in (5, 10, 7, 11, 13, 14):
                near_road_floor.append(cell)
                wt_list.append([a, b, 270])  # снизу

            if old_map[a][b + 1] in (5, 10, 7, 11, 13, 14):
                near_road_floor.append(cell)
                wt_list.append([a, b, 0])  # слева

            if old_map[a][b - 1] in (5, 10, 7, 11, 13, 14):
                near_road_floor.append(cell)
                wt_list.append([a, b, 180])  # справа

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
            for j in range(1, width - 1):
                if old_map[i][j] == 0:
                    floor_list.append([i, j])

        flor_near_road, watchtowers_list = self.is_near_road(state, floor_list)
        return watchtowers_list

    def save_new_architecture(self):

        state = self._generator.get_state()
        save_path = self._generator.get_save_path()
        old_map = state.map
        a_map = advancedMap(state.width, state.height, storage_location=save_path)

        frames_layer = MapLayer(a_map.map, "frames")
        tiles_layer = MapLayer(a_map.map, "tiles")
        tile_maps_layer = MapLayer(a_map.map, "tile_maps", a_map.createTileMaps())

        add_new_obj(a_map.map, frames_layer, "frames", 'map_0', {'relative_to': None, 'pose': None})
        frames_layer['map_0']['pose'] = Pose(1.0, 2.0).get_pose()

        for height in range(0, state.width):
            for width in range(0, state.height):
                old_cell = old_map[width][height]
                new_cell = self.NEW_CELLS[old_cell]
                pose = Pose(x=width, y=height, yaw=new_cell[1])
                a_map.createMapTileBlock(a_map.map, frames_layer, width, height, None, pose)
                add_new_obj(a_map.map, tiles_layer, "tiles", f'map_0/tile_{width}_{height}',
                            {'i': width, 'j': height, 'type': new_cell[0]})

        watchtower_layer = MapLayer(a_map.map, "watchtowers")
        watchtowers_list = self.get_watchtowers_place(state)
        a_map.createWatchtowers(a_map.map, frames_layer, watchtower_layer, watchtowers_list)

        a_map.map.layers.__dict__["watchtowers"] = watchtower_layer
        a_map.map.layers.__dict__["frames"] = frames_layer
        a_map.map.layers.__dict__["tiles"] = tiles_layer
        a_map.map.layers.__dict__["tile_maps"] = tile_maps_layer
        a_map.map.to_disk()

    def save(self):
        self.save_new_architecture()  # reload to new arch map
