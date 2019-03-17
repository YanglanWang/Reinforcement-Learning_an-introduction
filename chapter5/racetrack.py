import numpy as np
from itertools import product,combinations

action=[-1,0,1]
action_set=combinations( np.array( list( product( action,action ) ) ), 2 )
action_value=[np.zeros((16,16)) for i in range(len(action_set))]
v0_x=1
v0_y=1
epsilon=0.3
