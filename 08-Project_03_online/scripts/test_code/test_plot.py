import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev

def generate_feasible_path(points, vx_limit, vy_limit):
    # Perform cubic spline interpolation
    tck, u = splprep(np.array(points).T, k=3, s=0)
    
    # Evaluate the spline at more points
    t_eval = np.linspace(0, 1, 100)
    curve_points = np.array(splev(t_eval, tck))

    # Calculate the arc length of the curve
    length = np.sum(np.sqrt(np.sum(np.diff(curve_points, axis=1)**2, axis=0)))

    # Calculate time values based on velocity limits
    time_values = np.linspace(0, length/vx_limit, len(t_eval))
    t_eval = np.linspace(0, 1, math.ceil(length/vx_limit*1.2))
    curve_points = np.array(splev(t_eval, tck))

    arc_length = np.sqrt(np.sum(np.diff(curve_points, axis=1)**2, axis=0))
    arc_xy = np.diff(curve_points, axis=1)
    # Adjust velocity along the curve to maintain limits
    # vx_values = np.gradient(curve_points[0], time_values)
    # vy_values = np.gradient(curve_points[1], time_values)
    # vx_values = np.clip(vx_values, 0-vx_limit, vx_limit)
    # vy_values = np.clip(vy_values, 0-vy_limit, vy_limit)

    # Plot the result
    plt.plot(curve_points[0], curve_points[1], label='Spline Curve')
    # plt.plot(t_eval, curve_points[0], label='Spline X')
    # plt.plot(t_eval, curve_points[1], label='Spline X')
    # plt.plot([0,7 ], [0.5]*2, label='Baseline')
    # plt.plot(curve_points[0][:-1], arc_length, label='Length')
    plt.scatter(curve_points[0], curve_points[1])
    plt.quiver(curve_points[0][:-1], curve_points[1][:-1], arc_xy[0], arc_xy[1], 
                scale=10, color='red', label='Velocity Vectors')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Feasible Path with Velocity Control')
    plt.legend()
    plt.show()

# Example usage
vx_limit = 0.5
vy_limit = 1.0

# Specify the points to visit
points_to_visit = [(0, 0), (1, 2), (3, 1), (5, 3), (7, 2)]

# Generate the feasible path with velocity control
generate_feasible_path(points_to_visit, vx_limit, vy_limit)
