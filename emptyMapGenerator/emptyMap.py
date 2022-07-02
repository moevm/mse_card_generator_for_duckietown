import yaml
import dt_maps


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

def createFrames():
    dict_file = fr()
    return dict_file


def createTileMaps():
    dict_file = {'map_0': {'tile_size': {'x': 0.585, 'y': 0.585}}}
    return dict_file


def cr(a, b):
    return {f'map_0/tile_{a}_{b}': {'i': a, 'j': b, 'type': 'floor'}}

def cl(size):
    my_dict = {}
    for i in range(0,size):
        for j in range(0,size):
            my_dict.update(cr(i,j))

    return my_dict

def mp():
    my_map = cl(size)
    return my_map

def createTiles():
    dict_file = mp()
    return dict_file


if __name__ == '__main__':
    size = 3
    frames_content = createFrames()
    tiles_content = createTiles()
    tile_maps_content = createTileMaps()

    M = dt_maps.Map("map_0", "./my_map")

    frames_layer = dt_maps.MapLayer(M, "frames", frames_content)
    frames_layer.write("map_0", ['pose', 'pitch'], 1)
    tiles_layer = dt_maps.MapLayer(M, "tiles", tiles_content)
    tile_maps_layer = dt_maps.MapLayer(M, "tile_maps", tile_maps_content)

    # populate map
    M.layers.__dict__["frames"] = frames_layer
    M.layers.__dict__["tiles"] = tiles_layer
    M.layers.__dict__["tile_maps"] = tile_maps_layer
    # M.layers.frames["map_0/tile_0_0"].pose.pitch = 1

    print(list(M.layers.items()))
    M.to_disk()