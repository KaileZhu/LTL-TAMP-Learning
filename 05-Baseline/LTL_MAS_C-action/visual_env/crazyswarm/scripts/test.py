#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

Z = 1.0

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    timeHelper.sleep(1)
    for cf in allcfs.crazyflies:
        cf.setLEDColor(1,0,1)
    allcfs.takeoff(targetHeight=0.5, duration=1.0+Z)
    timeHelper.sleep(2)

    """
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, 3])
        cf.cmdPosition(pos)

    """

    allcfs.land(targetHeight=0.02, duration=1.0+Z)
    timeHelper.sleep(1.0+Z)
