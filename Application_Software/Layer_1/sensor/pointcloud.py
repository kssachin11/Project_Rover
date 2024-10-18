

import matplotlib.pyplot as plt

# Assuming points is a list of (X, Y) coordinates
points = [(100, 130),(110, 140),(130, 150)]

# Extract X and Y coordinates for plotting
X, Y = zip(*points)

# Plot the points
plt.scatter(X, Y, s=5, c='b', marker='o')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('2D Point Cloud from Laser Data')
plt.show()
