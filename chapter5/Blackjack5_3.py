import numpy as np
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.ticker as ticker

def get_value(state_tmp1,state_tmp2,usable_ace,policy):
    #action=0 means stcik; action=1 means hit
    state_set_episode=[]

    dealer_showing=state_tmp1
    player_sum=state_tmp2
    dealer_facedown=np.random.choice(np.arange(1,12))
    location1, = np.where( dealer_showing == row )
    location2, = np.where( player_sum == column )
    action = policy[location1[0]][location2[0]]
    state_set_episode.append( [dealer_showing, player_sum, action] )

    if usable_ace == True:
        choice_set = np.arange( 1, 12 )
    else:
        choice_set = np.arange( 1, 11 )
    # the first time
    if action==1:
        #continue to hit
        player_action = np.random.choice( choice_set )
        player_sum = player_sum + player_action
    else:
        #choose to stick
        pass
    # the first state after first action

    while True:
        if player_sum>21:
            rewards=-1
            break
        else:
            location1, = np.where( dealer_showing == row )
            location2, = np.where( player_sum == column )
            action = policy[location1[0]][location2[0]]
            # action=policy[int(dealer_showing-1)][int(player_sum-12)]
            state_set_episode.append( [dealer_showing, player_sum, action] )
            if action == 1:
                # choose to hit
                player_action=np.random.choice(choice_set)
                player_sum=player_sum+player_action
            else:
            # choose to stick
                while dealer_facedown + dealer_showing < 17:
                    dealer_facedown = dealer_facedown + np.random.choice( choice_set )
                if dealer_facedown + dealer_showing > 21:
                    rewards = 1
                    break
                elif dealer_facedown + dealer_showing > player_sum:
                    rewards = -1
                    break
                elif dealer_facedown + dealer_showing < player_sum:
                    rewards = 1
                    break
                else:
                    rewards = 0
                    break
    return rewards,state_set_episode


row_list=[11]
row_list.extend(range(2,11))
row=np.array(row_list)
# row=np.arange(1,11)
column=np.arange(10,22)
def figure5_5(usable_ace, episodes):

    # states = ((i, j) for i, j in itertools.product(row, column ))
    # states_value = ([] for i, j in itertools.product(row, column ))
    state_value_set0=[]
    state_value_set1=[]

    action_value0=np.zeros((len(row),len(column)))
    action_value1=np.zeros((len(row),len(column)))

    for i in range(len(row)):
        row_circulate=[]
        for j in range(len(column)):
            row_circulate.append([])
        state_value_set0.append(row_circulate)
        state_value_set1.append(row_circulate)

    if usable_ace==True:
        # for i in range(len(states)):
        #     for j in range(len(states[i])):
        #         value=[]
        policy = np.hstack( (np.ones( (len(row), len(column)-2) ), np.zeros( (len(row), 2) )) )
        for k in range(episodes):
            rewards,value_set=get_value(np.random.choice(row),np.random.choice(column),usable_ace,policy)
            for i,j,l in value_set:
                location1,=np.where(i==row)
                location2,=np.where(j==column)
                if l==0:
                    state_value_set0[location1[0]][location2[0]].append(rewards)
                    action_value0[location1[0]][location2[0]] = np.average(
                        np.array( state_value_set0[location1[0]][location2[0]] ) )
                else:
                    state_value_set1[location1[0]][location2[0]].append(rewards)
                    action_value1[location1[0]][location2[0]] = np.average(
                        np.array( state_value_set1[location1[0]][location2[0]] ) )
                if max( action_value0[location1[0]][location2[0]], action_value1[location1[0]][location2[0]] ) == action_value0[location1[0]][location2[0]]:
                    policy[location1[0]][location2[0]] = 0
                else:
                    policy[location1[0]][location2[0]]=1
            policy_new=np.copy(policy)

    fig,axes=plot.subplots(1,1)
    # fig = plot.figure()
    # ax = fig.add_subplot( 111, projection = '3d' )
    axes.pcolor( np.transpose(policy) )
    xmajorLocator = MultipleLocator( 1 )
    axes.xaxis.set_major_locator( xmajorLocator )

    # row[0]=1
    # axes.set_xticks(row)
    ymajorLocator = MultipleLocator( 1 )
    axes.yaxis.set_major_locator( ymajorLocator )

    # axes.set_yticks(column)
    # axes.yaxis.set_major_locator( ticker.FixedLocator( (pos_list) ) )

    axes.yaxis.set_major_formatter( ticker.FixedFormatter( np.arange(9,22) ) )

    # row[0]=1
    # X, Y = np.meshgrid( row,column )
    # Axes3D.plot_wireframe( ax,X, Y, np.transpose(a))
    # r = [-1, 1]
    # for s, e in combinations( np.array( list( product( [1,10], [12,21], [-1,1] ) ) ), 2 ):
    #     if np.sum( np.abs( s - e ) ) == r[1] - r[0] or np.sum( np.abs( s - e ) ) == 9:
    #         ax.plot3D( *zip( s, e ), color = "b" )
    plot.show()


if __name__=="__main__":
    figure5_5(True,1000000)