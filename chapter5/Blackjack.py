import numpy as np
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D

def get_value(state_tmp1,state_tmp2,usable_ace):
    state_set_episode=[]
    state_set_episode.append( [state_tmp1,state_tmp2] )

    dealer_showing=state_tmp1
    player_sum=state_tmp2
    dealer_facedown=np.random.choice(np.arange(1,12))

    if player_sum==21 and dealer_showing+dealer_facedown==21:
        rewards=0
    if player_sum==21 and dealer_showing+dealer_facedown<21:
        rewards=1
    if player_sum==21 and dealer_showing+dealer_facedown>21:
        rewards=-1
    else:
        if usable_ace == True:
            choice_set = np.arange( 1, 12 )
        else:
            choice_set = np.arange( 1, 11 )
        while True:

            player_action=np.random.choice(choice_set)
            player_sum=player_sum+player_action
            state_set_episode.append( [dealer_showing, player_sum] )
            if player_sum>21:
                rewards=-1
            elif np.random.rand()>0.5:
                #player choose stop
                while dealer_facedown+dealer_showing<17:
                    dealer_facedown=dealer_facedown+np.random.choice(np.arange(1,12))
                if dealer_facedown+dealer_showing>player_sum:
                    rewards=-1
                elif dealer_facedown+dealer_showing<player_sum:
                    rewards=1
                else:
                    rewards=0
    return rewards,state_set_episode



row_list=[11]
row_list.extend(range(2,11))
row=np.array(row_list)
column=np.arange(12,22)
def figure5_2(usable_ace, episodes):

    # states = ((i, j) for i, j in itertools.product(row, column ))
    # states_value = ([] for i, j in itertools.product(row, column ))
    state_value_set=[]
    state_value=np.zeros((len(row),len(column)))
    for i in range(len(row)):
        row_circulate=[]
        for j in range(len(column)):
            row_circulate.append([])
        state_value_set.append(row_circulate)

    if usable_ace==True:
        # for i in range(len(states)):
        #     for j in range(len(states[i])):
        #         value=[]
        for k in range(episodes):
            rewards,value_set=get_value(np.random.choice(row),np.random.choice(column),usable_ace)
            for i,j in value_set:
                location1,=np.where(i==row)
                location2,=np.where(j==column)
                state_value_set[location1][location2].append(rewards)
        for i in range(len(state_value)):
            for j in range(len(state_value[i])):
                state_value[i][j]=np.average(np.array(state_value_set[i][j]))

    Axes3D.plot_wireframe( row, column, state_value)



if __name__=="__main__":
    figure5_2(True,10000)