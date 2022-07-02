import yaml
import dt_maps


def createMain():
    dict_file = {'main': {'frames': 'frames.yaml', 'tiles': 'tiles.yaml', 'tile_maps': 'tiles_maps.yaml'}}

    # with open(r'./map/main.yaml', 'w') as file:
    #     documents = yaml.dump(dict_file, file)

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
     result = {'frames': frames}
     return result

def createFrames():
    dict_file = fr()
    return dict_file
    # with open(r'./map/frames.yaml', 'w') as file:
    #     documents = yaml.dump(dict_file, file)

def createTileMaps():
    dict_file = {'tile_maps': {'map_0': {'tile_size': {'x': 0.585, 'y': 0.585}}}}

    # with open(r'./map/tile_maps.yaml', 'w') as file:
    #     documents = yaml.dump(dict_file, file)

def cr(a, b):
    return {f'map_0/tile_{a}_{b}': {'i': a, 'j': b, 'type': 'floor'}}

def cl(size):
    my_dict = {}
    for i in range(0,size):
        for j in range(0,size):
            my_dict.update(cr(i,j))

    return my_dict

def mp():
    my_map = {'tiles': cl(size)}
    return my_map

def createTiles():
    dict_file = mp()
    return dict_file
    # with open(r'./map/tiles.yaml', 'w') as file:
    #     documents = yaml.dump(dict_file, file)


# def createEmptyMap():
#     createMain()
#    # createFrames()
#     createTileMaps()
    #createTiles()


if __name__ == '__main__':
    size = 5
    # createEmptyMap()
    # q_map = dt_maps.Map.from_disk("map_0", "./map")
    # q_map._path = "./new_map"
    # print(list(q_map.layers.items()))
    # q_map.to_disk()

    # M = dt_maps.Map("map_0", "./my_map")
    frames_content = createFrames()
    tiles_content = createTiles()

    # print(M.layers.has("frames"))
    # M.to_disk()

    M = dt_maps.Map("map_0", "./my_map")

    frames_layer = dt_maps.MapLayer(M, "frames", frames_content)
    tiles_layer = dt_maps.MapLayer(M, "tiles", tiles_content)
    # M.layers.frames = frames_content

    # populate map
    M._layers.__dict__["frames"] = frames_layer

    print(list(M.layers.items()))
    M.to_disk()