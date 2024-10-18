import json
from matplotlib import pyplot as plt
from Layer_3.navigation.map import Map
from Layer_3.navigation.metric_position import MetricPosition
from Layer_3.navigation.navigator import Navigator
#from Layer_1.driver.different_speed import *
#from Layer_1.driver.roboclaw_3 import Roboclaw
import subprocess


map = Map(map='maps\map6_small.json')
plt.imsave('map.png', map.data, cmap='Greys')

with open('maps\map6_small_225_297_0.json', 'r') as file:
    point_cloud = json.load(file)['data']
    
navigator = Navigator(path_map=map, point_cloud_polar=point_cloud, position_map=map, target=MetricPosition(29.2, 63.0, 0, 0), threshold=0.8)

print(f'get_path(): {navigator.get_path()}')

print(f'get_orientation(): {navigator.get_orientation()}')

print(f'get_position(): {navigator.get_position()}')


#plt.imshow(navigator._astar.path_matrix)
#plt.show()
subprocess.Popen(['python', 'different_speed.py'])