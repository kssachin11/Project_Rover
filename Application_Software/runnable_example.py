import json
from matplotlib import pyplot as plt
from Layers.L1_App.navigation.map import Map
from Layers.L1_App.navigation.metric_position import MetricPosition
from Layers.L1_App.navigation.navigator import Navigator


map = Map(map='maps\map6_small.json')
plt.imsave('map.png', map.data, cmap='Greys')

with open('maps\map6_small_225_297_0.json', 'r') as file:
    point_cloud = json.load(file)['data']
    
navigator = Navigator(path_map=map, point_cloud_polar=point_cloud, position_map=map, target=MetricPosition(29.2, 63.0, 0, 0), threshold=0.8)

print(f'get_path(): {navigator.get_path()}')

print(f'get_orientation(): {navigator.get_orientation()}')

print(f'get_position(): {navigator.get_position()}')


plt.imshow(navigator._astar.path_matrix)
plt.show()