import json
from matplotlib import pyplot as plt
from Layer_3.navigation.map import Map
from Layer_3.navigation.metric_position import MetricPosition
from Layer_3.navigation.navigator import Navigator
#from Layer_1.driver.different_speed import *
import subprocess

class NavigationSystem:
    def __init__(self, map_file, point_cloud_file, target_x, target_y, threshold=0.8):
        # Initialize the map
        self.map = Map(map=map_file)
        plt.imsave('map.png', self.map.data, cmap='Greys')
        
        # Load the point cloud
        with open(point_cloud_file, 'r') as file:
            self.point_cloud = json.load(file)['data']
        
        # Initialize the navigator
        self.navigator = Navigator(path_map=self.map, point_cloud_polar=self.point_cloud, 
                                   position_map=self.map, target=MetricPosition(target_x, target_y, 0, 0), 
                                   threshold=threshold)

    def get_path(self):
        return self.navigator.get_path()

    def get_orientation(self):
        return self.navigator.get_orientation()

    def get_position(self):
        return self.navigator.get_position()

    def run_different_speed_script(self):
        subprocess.Popen(['python', 'different_speed.py'])

    # Optional: A method to visualize the path, if needed
    def visualize_path(self):
        plt.imshow(self.navigator._astar.path_matrix)
        plt.show()

# Usage example with your specified parameters:
navigation_system = NavigationSystem(
map_file='maps/map6_small.json',
point_cloud_file='maps/map6_small_225_297_0.json',
target_x=29.2,
target_y=63.0
)

print(f'get_path(): {navigation_system.get_path()}')
print(f'get_orientation(): {navigation_system.get_orientation()}')
print(f'get_position(): {navigation_system.get_position()}')

#subprocess.Popen(['python3','different_speed.py']
# To run the different_speed.py script
# navigation_system.run_different_speed_script()

# If you want to visualize the path uncomment the following line
#navigation_system.visualize_path()

