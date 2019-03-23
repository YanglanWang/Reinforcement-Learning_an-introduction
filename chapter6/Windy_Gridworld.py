import numpy as np
import itertools
import matplotlib.pyplot as plt

a=dict()

for i in range(4):
    a[i]=0
action_value=[[a for column in range(10)] for row in range(7)]
wind_power=np.broadcast_to( [0,0,0,1,1,1,2,2,1,0], (7, 10) )
np.arange(10)
row=np.arange(7)
column=np.arange(10)
position= np.array([[i, j] for i, j in itertools.product(row, column )],dtype = int)


def Windy_Gridworld():
    epsilon=0.1
    afa=0.1
    t_tmp=0
    episode_tmp=0
    t=[]
    episode=[]
    t.append(t_tmp)
    episode.append(episode_tmp)

    while True:
        initial_position = np.array( [0, 3], dtype = int )
        position_t = initial_position
        episode_tmp+=1

        if t_tmp>8000:
            break
        while True:
            t_tmp+=1
            episode.append( episode_tmp )
            t.append(t_tmp)
            action_greedy_set = []
            action_value_set = action_value[position_t[0]][position_t[1]]
            if np.random.rand()<epsilon:

                for key in action_value_set.keys():
                    if action_value_set[key]==max(action_value_set.values()):
                        action_greedy_set.append(key)
                action=np.random.choice(action_greedy_set)
            else:
                action=np.random.choice(np.arange(4))

            action_value_t=action_value_set[action]

            if action==0:
                next_position=position_t+np.array([0,action+wind_power[position_t[0],position_t[1]]],dtype=int)
            elif action==1:
                next_position=position_t+np.array([0,wind_power[position_t[0],position_t[1]]-action],dtype=int)
            elif action==2:
                next_position=position_t+np.array([action,wind_power[position_t[0],position_t[1]]],dtype=int)
            else:
                next_position=position_t+np.array([-action,wind_power[position_t[0],position_t[1]]],dtype=int)

            # if next_position not in position:
            if next_position[0]<0 or next_position[0]>9 or next_position[1]<0 or next_position[1]>6:
                break
            else:

                action_value_set = action_value[next_position[0]][next_position[1]]
                if np.random.rand()<epsilon:
                    action_greedy_set_next=[]
                    for key in action_value_set.keys():
                        if action_value_set[key]==max(action_value_set.values()):
                            action_greedy_set_next.append(key)
                    action_next=np.random.choice(action_greedy_set_next)
                else:
                    action_next=np.random.choice(np.arange(4))

                action_value_next=action_value_set[action_next]
                if not False in (next_position==position_t):
                    break
                if not False in (next_position==[7,3]):
                    reward=0
                    action_value[position_t[0]][position_t[1]][action]+=afa*(reward+action_value_next-action_value_t)
                    break
                else:
                    reward=-1
                    action_value[position_t[0]][position_t[1]][action]+=afa*(reward+action_value_next-action_value_t)



                position_t=next_position

    fig,axes=plt.subplots(1,1)
    axes.plot(t,episode)
    plt.show()





if __name__=='__main__':
    Windy_Gridworld()