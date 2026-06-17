import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev

# Set the linear velocity and time step
vx = 1.0
vy = 0.5
dt = 0.1

# Set the plan (list of points to visit)
# plan = np.array([(0, 0), (1, 2), (3, 1), (5, 3), (7, 2)])
plan = np.array([(0, 0), (1, 2)])

# Perform cubic spline interpolation
tck, u = splprep(plan.T, k=1, s=0, per=False)

# Evaluate the spline at more points for a smooth curve
t_eval = np.linspace(0, 1, 100)
curve_points = splev(t_eval, tck)

# Plot the original plan points and the interpolated curve
plt.plot(plan[:, 0], plan[:, 1], 'ro', label='Plan Points')
plt.plot(curve_points[0], curve_points[1], 'b-', label='Interpolated Curve')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Cubic Spline Interpolation for Robot Path')
plt.legend()
plt.show()