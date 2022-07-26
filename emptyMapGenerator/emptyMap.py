import yaml

from dt_maps import Map, MapLayer
from dt_maps.types.tiles import Tile
from dt_maps.types.frames import Frame
from dt_maps.types.watchtowers import Watchtower

REGISTER = {
    "frames": Frame,
    "watchtowers": Watchtower,
    "tiles": Tile,
}

class Pose():
    def __init__(self, x=0.0, y=0.0, z=0.0, pitch=0.0, roll=0.0, yaw=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw

    def get_pose(self):
       return {'x': self.x, 'y': self.y, 'z': self.z, 'roll': self.roll, 'pitch': self.pitch,
                                                             'yaw': self.yaw}

class emptyMap:
    def __init__(self, width, height, map_name="map_0", storage_location="./"):
        self.width = width
        self.height = height
        self.map_name = map_name
        self.storage_location = storage_location
        self.map = Map(map_name, storage_location)

    def createMapTileBlock(self, M, frames_layer, tile_x, tile_y, relative_to, pose: Pose):
        add_new_obj(M, frames_layer, "frames", f'map_0/tile_{tile_x}_{tile_y}',
                    {'relative_to': relative_to, 'pose': None})
        frames_layer[f'map_0/tile_{tile_x}_{tile_y}']['pose'] = pose.get_pose()

    def createBlockFrames(self, M, frames_layer, relative_to, pose: Pose):
        add_new_obj(M, frames_layer, "frames", 'map_0', {'relative_to': relative_to, 'pose': None})
        frames_layer["map_0"]['pose'] = pose.get_pose()

    def createFrames(self, frames_layer):
        self.createBlockFrames(self.map, frames_layer, None, Pose(x=1.0, y=2.0))
        for tile_y in range(0, self.height):
            for tile_x in range(0, self.width):
                pose = Pose(x=tile_x, y=tile_y)
                self.createMapTileBlock(self.map, frames_layer, tile_x, tile_y, None, pose)

    def createTiles(self, tiles_layer, type='floor'):
        for i in range(0, self.width):
            for j in range(0, self.height):
                add_new_obj(self.map, tiles_layer, "tiles", f'map_0/tile_{i}_{j}', {'i': i, 'j': j, 'type': type})

    def createTileMaps(self):
        # add_new_obj(M, tile_maps_layer, "tile_maps", 'map_0', {'tile_size': {'x': 0.585, 'y': 0.585}})
        return {'map_0': {'tile_size': {'x': 0.585, 'y': 0.585}}}

    '''
    Main creation doesnt work
    '''
    # def createMain():
    #     dict_file = {'main': {'frames': 'frames.yaml', 'tiles': 'tiles.yaml', 'tile_maps': 'tiles_maps.yaml'}}
    #     return dict_file

    def calc_xy_wt(self, elem: list):
        x = elem[0]
        y = elem[1]
        direction = elem[2]
        if direction == 0:
            return x + 0.4, y + 0.6
        if direction == 90:
            return x + 0.6, y - (1 - 0.585)
        if direction == 180:
            return x + 0.4, y - 0.6
        if direction == 270:
            return x - 0.6, y - (1 - 0.585)

    def createWatchtowers(self, M, frames_layer, watchtowers_layer, wt_list: list):
        counter = 0
        for elem in wt_list:
            x, y = self.calc_xy_wt(elem)
            z = 0
            pitch = 0
            roll = 0
            yaw = elem[2]
            pose = Pose(x=x, y=y, yaw=yaw)

            counter += 1
            add_new_obj(M, watchtowers_layer, "watchtowers", f"map_0/watchtower{counter}", {"configuration": "WT18"})
            add_new_obj(M, frames_layer, "frames", f'map_0/watchtower{counter}', {'relative_to': None, 'pose': None})
            frames_layer[f'map_0/watchtower{counter}']['pose'] = pose.get_pose()

    def createEmptyMap(self):
        frames_layer = MapLayer(self.map, "frames")
        self.createFrames(frames_layer)

        tiles_layer = MapLayer(self.map, "tiles")
        self.createTiles(tiles_layer)

        tile_maps_layer = MapLayer(self.map, "tile_maps", self.createTileMaps())

        # populate map
        self.map.layers.__dict__["frames"] = frames_layer
        self.map.layers.__dict__["tiles"] = tiles_layer
        self.map.layers.__dict__["tile_maps"] = tile_maps_layer

        # print(list(M.layers.items()))
        self.map.to_disk()


def add_new_obj(dm: Map,
                layer: MapLayer,
                layer_name: str, obj_name: str, default_conf: dict) -> None:
    layer[obj_name] = default_conf
    layer = MapLayer(dm, layer_name, layer)
    dm._layers.__dict__[layer_name] = layer
    register = lambda l, t: dm.layers.get(l).register_entity_helper(
        t) if dm.layers.has(l) else 0
    register(layer_name, REGISTER[layer_name])


if __name__ == '__main__':
    eMap = emptyMap(width=9, height=8)
    eMap.createEmptyMap()