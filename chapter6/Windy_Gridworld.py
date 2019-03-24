import numpy as np
import itertools
import matplotlib.pyplot as plt
from tqdm import tqdm
import math

# a=dict()
# for i in range(4):
#     a[i]=0


wind_power=np.broadcast_to( np.transpose([[0,0,0,1,1,1,2,2,1,0]]), (10, 7) )
np.arange(10)
row=np.arange(7)
column=np.arange(10)
position= np.array([[i, j] for i, j in itertools.product(row, column )],dtype = int)


def Windy_Gridworld():
    run_set=[[] for times in range(2)]
    run_average=[[] for times in range(2)]
    action_value_optimal=[]
    action_value_optimal_set = []
    run_number=10

    for run in tqdm(range(run_number)):
        epsilon=0.1
        afa=0.5
        t_tmp=0
        episode_tmp=0
        t=[]
        episode=[]
        # t.append(t_tmp)
        # episode.append(episode_tmp)
        action_value_initial = [[dict( zip( np.arange( 4, dtype = int ), np.zeros( 4 ) ) ) for column in range( 7 )] for
                                row
                                in range( 10 )]
        action_value = np.copy( action_value_initial )

        while True:
            initial_position = np.array( [0, 3], dtype = int )
            position_t = initial_position
            action_greedy_set = []
            action_value_set = action_value[position_t[0]][position_t[1]]
            if np.random.rand() > epsilon:
                for key in action_value_set.keys():
                    if action_value_set[key] == max( action_value_set.values() ):
                        action_greedy_set.append( key )
                action = np.random.choice( action_greedy_set )
            else:
                action = np.random.choice( np.arange( 4 ) )

            # action_value_t = action_value_set[action]

            episode_tmp+=1

            if t_tmp>8000:
                break
            while True:
                action_value_set = action_value[position_t[0]][position_t[1]]
                action_value_t = action_value_set[action]

                t_tmp+=1
                episode.append( episode_tmp )
                t.append(t_tmp)
                if action==0:
                    possible_position2=int( position_t[1] + 1 + wind_power[position_t[0], position_t[1]])
                    if 0<=possible_position2<=6:
                        next_position =[position_t[0],possible_position2]
                    elif possible_position2>6:
                        next_position=[position_t[0],6]
                    else:
                        next_position = [position_t[0], 0]
                elif action==1:
                    possible_position2=int( position_t[1] - 1 + wind_power[position_t[0], position_t[1]])
                    if 0<=possible_position2<=6:
                        next_position=[position_t[0],possible_position2]
                    elif possible_position2>6:
                        next_position=[position_t[0],6]
                    else:
                        next_position=[position_t[0],0]
                elif action==2:
                    possible_position1=int(position_t[0]+1)
                    possible_position2=position_t[1]+wind_power[position_t[0],position_t[1]]
                    if possible_position1>9:
                        possible_position1=9
                    if possible_position1<0:
                        possible_position1=0
                    if possible_position2>6:
                        possible_position2=6
                    if possible_position2<0:
                        possible_position2=0
                    next_position=[possible_position1,possible_position2]
                else:
                    possible_position1=int(position_t[0]-1)
                    possible_position2=position_t[1]+wind_power[position_t[0],position_t[1]]
                    if possible_position1>9:
                        possible_position1=9
                    if possible_position1<0:
                        possible_position1=0
                    if possible_position2>6:
                        possible_position2=6
                    if possible_position2<0:
                        possible_position2=0
                    next_position=[possible_position1,possible_position2]

                # if next_position not in position:
                # if next_position[0]<0 or next_position[0]>9 or next_position[1]<0 or next_position[1]>6:
                #     break

                # if not False in (next_position == position_t):
                #     break
                # else:
                if next_position[1]==7:
                    print('fja')
                action_value_set = action_value[next_position[0]][next_position[1]]
                if np.random.rand()>epsilon:
                    action_greedy_set_next=[]
                    for key in action_value_set.keys():
                        if action_value_set[key]==max(action_value_set.values()):
                            action_greedy_set_next.append(key)
                    action_next=np.random.choice(action_greedy_set_next)
                else:
                    action_next=np.random.choice(np.arange(4))

                action_value_next=action_value_set[action_next]

                if next_position!=[7,3]:
                    reward=-1
                    test=action_value[position_t[0]][position_t[1]][action]+afa*(reward+action_value_next-action_value_t)
                    # if test==float('inf') or test==float('-inf') or math.isnan(test)==True:
                    #     print('stop')
                    action_value[position_t[0]][position_t[1]][action]+=afa*(reward+action_value_next-action_value_t)


                else:
                    reward=0
                    test=action_value[position_t[0]][position_t[1]][action]+afa*(reward+action_value_next-action_value_t)
                    # if test==float('inf') or test==float('-inf') or math.isnan(test)==True:
                    #     print('stop')
                    action_value[position_t[0]][position_t[1]][action]+=afa*(reward+action_value_next-action_value_t)
                    break

                position_t=next_position
                action=action_next
        run_set[0].append(t[0:8000])
        run_set[1].append(episode[0:8000])
        action_value_optimal_set.append(np.copy(action_value))
    run_average[0]=np.average(run_set[0],axis=0)
    run_average[1]=np.average(run_set[1],axis=0)
    # action_value_optimal=np.average(np.array(action_value_optimal_set),axis=0)
    value_average=[]
    for i in range(len(action_value)):
        row=[]
        for j in range(len(action_value[i])):
            whole_1=0
            whole_2=0
            whole_3=0
            whole_4=0
            for k in range(len(action_value_optimal_set)):
                whole_1+=action_value_optimal_set[k][i][j][0]
                whole_2+=action_value_optimal_set[k][i][j][1]
                whole_3+=action_value_optimal_set[k][i][j][2]
                whole_4+=action_value_optimal_set[k][i][j][3]
            a=dict()
            a[0]=whole_1/len(action_value_optimal_set)
            a[1]=whole_2/len(action_value_optimal_set)
            a[2]=whole_3/len(action_value_optimal_set)
            a[3]=whole_4/len(action_value_optimal_set)
            row.append(a)
        value_average.append(row)
    start_position=[0,3]
    end_position=[7,3]
    route=[]
    position_t=start_position
    while position_t!=end_position:
        route.append(position_t)
        action_greedy_set_next = []
        for key in value_average[position_t[0]][position_t[1]].keys():
            if value_average[position_t[0]][position_t[1]][key] == max( value_average[position_t[0]][position_t[1]].values() ):
                action_greedy_set_next.append( key )
        action = np.random.choice( action_greedy_set_next )
        if action == 0:
            possible_position2 = int( position_t[1] + 1 + wind_power[position_t[0], position_t[1]] )
            if 0 <= possible_position2 <= 6:
                next_position = [position_t[0], possible_position2]
            elif possible_position2 > 6:
                next_position = [position_t[0], 6]
            else:
                next_position = [position_t[0], 0]
        elif action == 1:
            possible_position2 = int( position_t[1] - 1 + wind_power[position_t[0], position_t[1]] )
            if 0 <= possible_position2 <= 6:
                next_position = [position_t[0], possible_position2]
            elif possible_position2 > 6:
                next_position = [position_t[0], 6]
            else:
                next_position = [position_t[0], 0]
        elif action == 2:
            possible_position1 = int( position_t[0] + 1 )
            possible_position2 = position_t[1] + wind_power[position_t[0], position_t[1]]
            if possible_position1 > 9:
                possible_position1 = 9
            if possible_position1 < 0:
                possible_position1 = 0
            if possible_position2 > 6:
                possible_position2 = 6
            if possible_position2 < 0:
                possible_position2 = 0
            next_position = [possible_position1, possible_position2]
        else:
            possible_position1 = int( position_t[0] - 1 )
            possible_position2 = position_t[1] + wind_power[position_t[0], position_t[1]]
            if possible_position1 > 9:
                possible_position1 = 9
            if possible_position1 < 0:
                possible_position1 = 0
            if possible_position2 > 6:
                possible_position2 = 6
            if possible_position2 < 0:
                possible_position2 = 0
            next_position = [possible_position1, possible_position2]
        position_t=next_position
    route.append( position_t )

    fig,axes=plt.subplots(1,1)
    axes.plot(run_average[0],run_average[1])
    plt.show()


    #plot the optimal route


    fig,axes=plt.subplots(1,1)
    axes.plot(np.transpose(np.array(route))[0],np.transpose(np.array(route))[1])
    plt.show()





if __name__=='__main__':
    Windy_Gridworld()