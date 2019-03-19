import numpy as np
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
from tqdm import tqdm
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.ticker as ticker



row=np.arange(1,11)
column=np.arange(1,22)
policy = np.hstack( (np.ones( (len(row), len(column)-2) ), np.zeros( (len(row), 2) )) )


def get_card():
    card=np.random.randint(1,14)
    card=min(card,10)
    return card

def calculate_value_state(initial_state,policy):
    state_set_episode=[]
    if initial_state!=None:
        dealer_self=initial_state[0]
        player_sum=initial_state[1]
        usable_ace=initial_state[2]
    else:
        dealer_self=get_card()
        player_card1 = get_card()
        player_card2 = get_card()
        player_sum=player_card1+player_card2
        ace_number=0
        if 1 in (player_card1,player_card2):
            player_sum=player_sum+10
            usable_ace=True
            if player_card1==player_card2:
                ace_number=2
            else:
                ace_number=1
        else:
            usable_ace=False

        while player_sum<12:
            player_card_addition=get_card()
            if player_card_addition==1:
                ace_number=ace_number+1
            player_sum=player_sum+player_card_addition
            if ace_number==1:
                player_sum=player_sum+10
                usable_ace = True
                if player_sum>21:
                    player_sum=player_sum-10
                    usable_ace=False

    dealer_facedown=get_card()
    dealer_sum = dealer_self + dealer_facedown
    ace_number_dealer=0
    if 1 in (dealer_facedown,dealer_self):
        dealer_sum=dealer_sum+10
        dealer_ace=True
        if dealer_self==dealer_facedown:
            ace_number_dealer=2
        else:
            ace_number_dealer=1
    else:
        dealer_ace=False

    if player_sum==21:
        if dealer_sum==21:
            rewards=0
        else:
            #dealer_sum<21
            rewards = 1
        state_set_episode.append( [dealer_self, player_sum,usable_ace] )
        return rewards, state_set_episode
    else:
        #player_sem<21
        if dealer_sum==21:
            rewards=-1
            state_set_episode.append( [dealer_self, player_sum, usable_ace] )
            return rewards, state_set_episode
        else:
            state_set_episode.append( [dealer_self, player_sum, usable_ace] )
            while True:
                location1, = np.where( dealer_self == row )
                location2, = np.where( player_sum == column )
                action = policy[location1[0]][location2[0]]
                if action==0:
                    #means stop, dealer's turn
                    while dealer_sum<17:
                        dealer_addition=get_card()
                        if dealer_addition==1:
                            ace_number_dealer=ace_number_dealer+1
                        dealer_sum=dealer_sum+dealer_addition
                        if ace_number_dealer==1:
                            dealer_sum=dealer_sum+10
                            dealer_ace=True
                            if dealer_sum>21:
                                dealer_sum=dealer_sum-10
                                dealer_ace=False
                    break
                else:
                    # means hit
                    player_card_addition = get_card()
                    player_sum = player_sum + player_card_addition
                    if player_card_addition == 1:
                        ace_number = ace_number + 1
                    if ace_number == 1:
                        player_sum = player_sum + 10
                        usable_ace = True
                        if player_sum > 21:
                            player_sum = player_sum - 10
                            usable_ace = False
                    if player_sum>21:
                        break
                    else:
                        state_set_episode.append( [dealer_self, player_sum, usable_ace] )
            if player_sum>21:
                rewards=-1
            elif player_sum==21 and dealer_sum==21:
                rewards=0
            elif player_sum==21 and dealer_sum!=21:
                rewards=1
            elif player_sum<21 and dealer_sum>21:
                rewards=1
            elif player_sum<21 and dealer_sum==21:
                rewards=-1
            else:
                if player_sum>dealer_sum:
                    rewards=1
                elif player_sum==dealer_sum:
                    rewards=0
                else:
                    rewards=-1

    return rewards,state_set_episode

def calculate_action_state( initial_state_action, policy_action ):
    state_action_set = []
    #reward, action_state_set, action_state_set=[ i, j, k, l]
    if initial_state_action != None:
        dealer_self = initial_state_action[0]
        player_sum = initial_state_action[1]
        usable_ace = initial_state_action[2]
        action=initial_state_action[3]
    else:
        dealer_self = get_card()
        player_card1 = get_card()
        player_card2 = get_card()
        player_sum = player_card1 + player_card2
        ace_number = 0
        if 1 in (player_card1, player_card2):
            if player_card1 == player_card2:
                ace_number = 2
                player_sum = player_sum + 20
                usable_ace = True
                if player_sum > 21:
                    player_sum = player_sum - 10
                    ace_number = ace_number-1
                    if player_sum > 21:
                        player_sum = player_sum - 10
                        ace_number = ace_number - 1
                        usable_ace = False
            else:
                ace_number = 1
                player_sum = player_sum + 10
                usable_ace = True
                if player_sum > 21:
                    player_sum = player_sum - 10
                    ace_number = ace_number-1
                    usable_ace=False
        else:
            usable_ace = False

        while player_sum < 12:
            player_card_addition = get_card()
            player_sum = player_sum + player_card_addition
            if player_card_addition == 1:
                player_sum=player_sum+10
                ace_number = ace_number + 1
                if ace_number==1:
                    usable_ace=True
                if player_sum > 21:
                    player_sum = player_sum - 10
                    ace_number=ace_number-1
                    if ace_number == 0:
                        usable_ace = False

    # the player_sum is [13,21]

        action=np.random.choice([0,1])

    dealer_facedown = get_card()
    dealer_sum = dealer_self + dealer_facedown
    ace_number_dealer = 0
    if 1 in (dealer_facedown, dealer_self):
        if dealer_self == dealer_facedown:
            ace_number_dealer = 2
            dealer_sum = dealer_sum + 20
            dealer_ace = True
            if dealer_sum>21:
                dealer_sum=dealer_sum-10
                ace_number_dealer=ace_number_dealer-1
                if dealer_sum>21:
                    dealer_sum = dealer_sum - 10
                    ace_number_dealer = ace_number_dealer - 1
                    dealer_ace=False
        else:
            ace_number_dealer = 1
            dealer_sum=dealer_sum+10
            dealer_ace=True
            if dealer_sum>21:
                dealer_sum=dealer_sum-10
                ace_number_dealer=ace_number_dealer-1
                dealer_ace=False
    else:
        dealer_ace = False

    while True:
        state_action_set.append([dealer_self,player_sum,usable_ace,action])
        if action == 0:
        # means stop, dealer's turn
            while dealer_sum < 17:
                dealer_addition = get_card()
                dealer_sum = dealer_sum + dealer_addition
                if dealer_addition == 1:
                    ace_number_dealer = ace_number_dealer + 1
                    dealer_sum = dealer_sum + 10
                    if ace_number_dealer==1:
                        dealer_ace = True
                while dealer_sum > 21 and ace_number_dealer>0:
                    dealer_sum = dealer_sum - 10
                    ace_number_dealer=ace_number_dealer-1
                if ace_number_dealer==0:
                    dealer_ace = False
            break
            #dealer_sum is [18,27]
        else:
        # means hit
            player_card_addition = get_card()
            player_sum = player_sum + player_card_addition
            if player_card_addition == 1:
                ace_number = ace_number + 1
                player_sum = player_sum + 10
                if ace_number == 1:
                    usable_ace = True
            while player_sum > 21 and usable_ace>0:
                    player_sum = player_sum - 10
                    usable_ace=usable_ace-1
            if ace_number==0:
                usable_ace = False
            if player_sum > 21:
                break
            else:
                location1, = np.where( dealer_self == row )
                location2, = np.where( player_sum == column )
                if usable_ace==True:
                    type=int(0)
                else:
                    type=int(1)
                action = policy_action[type][location1[0]][location2[0]]
                # state_action_set.append( [dealer_self, player_sum, usable_ace,action] )

    if player_sum>21:
        rewards=-1
    elif player_sum==21 and dealer_sum == 21:
        rewards = 0
    elif player_sum==21 and dealer_sum!=21:
        rewards = 1
    elif player_sum < 21 and dealer_sum > 21:
        rewards = 1
    elif player_sum < 21 and dealer_sum == 21:
        rewards = -1
    else:
        if player_sum > dealer_sum:
            rewards = 1
        elif player_sum == dealer_sum:
            rewards = 0
        else:
            rewards = -1

    return rewards, state_action_set


def figure5_2():
    usable_ace=[True,False]
    episodes=[10000,500000]
    state_value_whole=np.zeros((4,len( row ), len( column )))
    # states = ((i, j) for i, j in itertools.product(row, column ))
    # states_value = ([] for i, j in itertools.product(row, column ))
    for episodes_tmp in range(len(episodes)):
        state_value_set_usable = []
        state_value_set_unusable = []
        state_value_usable = np.zeros( (len( row ), len( column )) )
        state_value_unusable = np.zeros( (len( row ), len( column )) )

        for i in range( len( row ) ):
            row_circulate = []
            for j in range( len( column ) ):
                row_circulate.append( [] )
            state_value_set_unusable.append( row_circulate )
            state_value_set_usable.append( row_circulate )
        for episode in tqdm(range(episodes[episodes_tmp])):

            initial_state=None
            reward,value_state_set=calculate_value_state(initial_state,policy)
            for i,j,k in value_state_set:
                location1,=np.where(i==row)
                location2,=np.where(j==column)
                if k==True:
                    state_value_set_usable[location1[0]][location2[0]].append(reward)
                    state_value_usable[location1[0]][location2[0]]=np.average(state_value_set_usable[location1[0]][location2[0]])
                else:
                    state_value_set_unusable[location1[0]][location2[0]].append(reward)
                    state_value_unusable[location1[0]][location2[0]]=np.average(state_value_set_unusable[location1[0]][location2[0]])
        state_value_whole[(episodes_tmp*2),:,:]=state_value_usable
        state_value_whole[int(episodes_tmp*2+1),:,:]=state_value_unusable

    fig = plot.figure()
    for i in range(np.shape(state_value_whole)[0]):
        ax = fig.add_subplot( 2,2,int(i+1), projection = '3d' )
        X, Y = np.meshgrid( range(1,11),range(12,22) )
        Axes3D.plot_wireframe( ax,X, Y, np.transpose(state_value_whole[i,:,11:]))
        r = [-1, 1]
        for s, e in combinations( np.array( list( product( [1,10], [12,21], [-1,1] ) ) ), 2 ):
            if np.sum( np.abs( s - e ) ) == r[1] - r[0] or np.sum( np.abs( s - e ) ) == 9:
                ax.plot3D( *zip( s, e ), color = "b" )
    plot.show()
    plot.savefig('figure5_2.png')



def figure5_5(episodes):

    state_value_star=np.zeros((2,len( row ), len( column )))
    action_value_set_usable = []
    action_value_set_unusable = []
    for i in range( len( row ) ):
        row_circulate_usable = []
        row_circulate_unusable = []
        for j in range( len( column ) ):
            different_action_usable=[]
            different_action_unusable=[]
            for k in range(2):
                different_action_usable.append([])
                different_action_unusable.append([])
            row_circulate_usable.append( different_action_usable )
            row_circulate_unusable.append(different_action_unusable)
        action_value_set_unusable.append( row_circulate_usable )
        action_value_set_usable.append( row_circulate_unusable )

    action_value_usable=[]
    for i in range(len(row)):
        action_value_usable_row=[]
        for j in range(len(column)):
            action_value_usable_row.append(np.zeros(2))
        action_value_usable.append(action_value_usable_row)
        # 0--the first one means stick, 1--hit

    action_value_unusable = []
    for i in range(len(row)):
        action_value_unusable_row=[]
        for j in range(len(column)):
            action_value_unusable_row.append(np.zeros(2))
        action_value_unusable.append(action_value_unusable_row)
        # 0--the first one means stick, 1--hit


    policy_action=np.ones((2,len( row ), len( column )))
    #policy_action[0,:,:] means usable policy
    #policy_action[1,:,:] means unusable policy
    policy_action[:,:,-2:]=0



    for episode in tqdm( range( episodes ) ):

        initial_state_action = None
        reward, action_state_set = calculate_action_state( initial_state_action, policy_action )
        # reward, action_state_set, action_state_set=[ i, j, k, l]
        # i=dealer_self,
        # j=player_sum
        # k=usable_ace
        # l=action
        for i, j, k,l in action_state_set:
            location1, = np.where( i == row )
            location2, = np.where( j == column )
            m=location1[0]
            n=location2[0]
            if k == True:
                action_value_set_usable[m][n][int(l)].append( reward )
                action_value_usable[m][n][int(l)] = np.average(action_value_set_usable[m][n][int(l)] )
                policy_action[0][m][n]=np.random.choice([a for a,b in enumerate(action_value_usable[m][n][:]) if b==max(action_value_usable[m][n][:])])
                state_value_star[0][m][n] =np.random.choice([b for a,b in enumerate(action_value_usable[m][n][:]) if b==max(action_value_usable[m][n][:])])
            else:
                action_value_set_unusable[m][n][int(l)].append( reward )
                action_value_unusable[m][n][int(l)] = np.average(
                    action_value_set_unusable[m][n][int(l)] )
                policy_action[1][m][n]=np.random.choice([a for a,b in enumerate(action_value_unusable[m][n][:]) if b==max(action_value_unusable[m][n][:])])
                state_value_star[1][m][n] =np.random.choice([b for a,b in enumerate(action_value_unusable[m][n][:]) if b==max(action_value_unusable[m][n][:])])



    fig = plot.figure()
    for i in range(np.shape(policy_action)[0]):
        ax = fig.add_subplot( 2,2,int(i*2+1))
        ax.pcolor( np.transpose(policy_action[i,:,11:] ))
        xmajorLocator = MultipleLocator( 1 )
        ax.xaxis.set_major_locator( xmajorLocator )
        ymajorLocator = MultipleLocator( 1 )
        ax.yaxis.set_major_locator( ymajorLocator )
        ax.yaxis.set_major_formatter( ticker.FixedFormatter( np.arange( 10, 22 ) ) )

    for i in range(np.shape(state_value_star)[0]):
        ax = fig.add_subplot( 2,2,int((i+1)*2), projection = '3d' )
        X, Y = np.meshgrid( range(1,11),range(12,22) )
        Axes3D.plot_wireframe( ax,X, Y, np.transpose(state_value_star[i,:,11:]))
        r = [-1, 1]
        for s, e in combinations( np.array( list( product( [1,10], [12,21], [-1,1] ) ) ), 2 ):
            if np.sum( np.abs( s - e ) ) == r[1] - r[0] or np.sum( np.abs( s - e ) ) == 9:
                ax.plot3D( *zip( s, e ), color = "b" )
    plot.savefig('figure5_5.png')
    plot.show()

if __name__=="__main__":
    figure5_2()
    # figure5_5(500000)