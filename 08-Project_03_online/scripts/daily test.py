import matplotlib.pyplot as plt
import os
import re
import time
import sys

import numpy as np
import networkx as nx
import matplotlib.patches as patches

from PIL import Image
from matplotlib import pyplot as plt
from MAS_TL_STAP import *

a = {
            "rwbs": "task001",  
            "mbbs": "mbbs001", 
            "hlptbs": "A1", 
            "XDSL": 2, 
            "mzzzsj": "2024-04-29 18:00:20", 
            "mzzwsj": "2024-04-29 18:00:35", 
            "djbhsj": 10,
            "sslbs": "fscbs007-ssl0",  
            "sslmc": "fscnm007-ssl0",
            "zcptbs": "fscbs001",
            "zckssj": "2024-04-29 17:55:03",
            "zcjssj": "2024-04-29 17:55:03",
            "zhptbs": "fscbs001"
        }
del a["zhptbs"]  # 删除
print(a)