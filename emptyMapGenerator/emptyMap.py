import yaml

from dt_maps import Map, MapLayer
from dt_maps.types.tiles import Tile
from dt_maps.types.frames import Frame
from dt_maps.types.watchtowers import Watchtower


def createMain():
    dict_file = {'main': {'frames': 'frames.yaml', 'tiles': 'tiles.yaml', 'tile_maps': 'tiles_maps.yaml'}}
    return dict_file


def fb(a,b):
    return {f'map_0/tile_{a}_{b}': {'relative_to': 'map_0', 'pose': {'x': a, 'y': b,'z': 0, 'roll': 0, 'pitch': 0, 'yaw': 0 }}}

def fl(size):
    my_dict = {}

    for i in range(0, size):
        for j in range(0, size):
            my_dict.update(fb(i, j))


    return my_dict

def fr():
     frames = fl(size)
     adding_part = {'map_0': {'relative_to': None, 'pose': {'x': 1.0, 'y': 2.0, 'z': 0.0, 'roll': 0, 'pitch': 0, 'yaw': 0}}}
     frames.update(adding_part)
     result = frames
     return result

# def createFrames():
#     dict_file = fr()
#     return dict_file


def createTileMaps():
    dict_file = {'map_0': {'tile_size': {'x': 0.585, 'y': 0.585}}}
    return dict_file
#
#
# def cr(a, b):
#     return {f'map_0/tile_{a}_{b}': {'i': a, 'j': b, 'type': 'floor'}}
#
# def cl(size):
#     my_dict = {}
#     for i in range(0,size):
#         for j in range(0,size):
#             my_dict.update(cr(i,j))
#
#     return my_dict
#
# def mp():
#     my_map = cl(size)
#     return my_map
#
# def createTiles():
#     dict_file = mp()
#     return dict_file

def createBlockFrames(relative_to, x, y, z, roll, pitch, yaw):
    add_new_obj(M, frames_layer, "frames", 'map_0', {'relative_to': relative_to, 'pose': None})
    frames_layer.write("map_0", 'pose', {'x': x, 'y': y, 'z': z, 'roll': roll, 'pitch': pitch, 'yaw': yaw})

def createMapTileBlock(tile_x, tile_y, relative_to, x, y, z, roll, pitch, yaw):
    add_new_obj(M, frames_layer, "frames", f'map_0/tile_{tile_x}_{tile_y}', {'relative_to': relative_to, 'pose': None})
    frames_layer.write(f'map_0/tile_{tile_x}_{tile_y}', 'pose', {'x': x, 'y': y, 'z': z, 'roll': roll, 'pitch': pitch, 'yaw': yaw})

def createFrames():
    createBlockFrames(None, 1.0, 2.0, 0, 0, 0, 0)
    for tile_y in range(0,size):
        for tile_x in range(0, size):
            createMapTileBlock(tile_x, tile_y, None, tile_x, tile_y, 0, 0, 0, 0)


def createTiles(type = 'floor'):
    for i in range(0, size):
        for j in range(0, size):
            add_new_obj(M, tiles_layer, "tiles", f'map_0/tile_{i}_{j}', {'i': i, 'j': j, 'type': type})
            # tiles_layer.write('', f'map_0/tile_{i}_{j}', {'i': i, 'j': j, 'type': 'floor'})

REGISTER = {
    "frames": Frame,
    "watchtowers": Watchtower,
    "tiles": Tile,
}

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
    size = 3
    # frames_layer.write("map_0", ['pose', 'pitch'], 1)
    # frames_layer.write("a", ['b', 'c'], 1)
    tile_maps_content = createTileMaps()

    M = Map("map_0", "./my_map")


    frames_layer = MapLayer(M, "frames")
    createFrames()

    tiles_layer = MapLayer(M, "tiles")
    createTiles()

    tile_maps_layer = MapLayer(M, "tile_maps", tile_maps_content)

    # populate map
    M.layers.__dict__["frames"] = frames_layer
    M.layers.__dict__["tiles"] = tiles_layer
    M.layers.__dict__["tile_maps"] = tile_maps_layer

    print(list(M.layers.items()))
    M.to_disk()