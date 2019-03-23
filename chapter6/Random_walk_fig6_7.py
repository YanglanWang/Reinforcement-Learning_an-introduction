import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm



def get_value_state_td(afa_td,episode):
    value_state_td=np.zeros((len(afa_td),episode,5))
    policy=np.broadcast_to([-1,1],(5,2))
    reward_tmp=np.broadcast_to([0,0],(4,2))
    reward=np.vstack((reward_tmp,[0,1]))
    lamda=1
    value_state_true=np.arange(1,6)/6
    RMS_td_100run_set=[]
    RMS_td_100run=np.zeros((len(afa_td),episode))
    for run in range(100):
        RMS_td = np.zeros( (len( afa_td ), episode) )
        for afa_tmp in afa_td:
            value_state_episode=np.ones(5)*0.5
            # for i in tqdm( range( episode )):
            for i in  range( episode ) :
                if i != 0:
                    s_t_index = 2
                    while True:
                        s_t_value = value_state_episode[s_t_index]
                        a = np.random.choice( policy[s_t_index] )
                        s_nextt_index =  s_t_index + a
                        reward_tmp = reward[s_t_index, max( a, 0 )]
                        if s_nextt_index == 5 or s_nextt_index == -1:
                            s_nextt_value = 0
                            value_state_episode[s_t_index] = s_t_value + afa_tmp * (reward_tmp + lamda * s_nextt_value - s_t_value)
                            break
                        else:
                            s_nextt_value = value_state_episode[s_nextt_index]
                            value_state_episode[s_t_index] = s_t_value + afa_tmp * (reward_tmp + lamda * s_nextt_value - s_t_value)
                            s_t_index = s_nextt_index

                    value_state_td[afa_td.index(afa_tmp),i, :] = value_state_episode

        for afa_tmp in range(len(afa_td)):
            RMS_td[afa_tmp,:]=np.power(np.average(np.power(value_state_td[afa_tmp,:,:]-value_state_true,2),axis = 1),0.5)
        RMS_td_100run_set.append( RMS_td )
    for i in range( len( RMS_td_100run_set[0] ) ):
        RMS_td_100run[i, :] = np.average(np.array(RMS_td_100run_set)[:, i, :],axis=0)
    return RMS_td_100run

def get_value_state_mc(afa_mc,episode):
    value_state_mc=np.zeros((len(afa_mc),episode,5))
    policy=np.broadcast_to([-1,1],(5,2))
    reward_tmp=np.broadcast_to([0,0],(4,2))
    reward=np.vstack((reward_tmp,[0,1]))
    lamda=1
    value_state_true=np.arange(1,6)/6
    RMS_mc_100run_set=[]
    RMS_mc_100run=np.zeros((len(afa_mc),episode))

    for run in range(100):
        RMS_mc = np.zeros( (len( afa_mc ), episode) )
        for afa_tmp in afa_mc:
            value_state_episode=np.ones(5)*0.5
            # value_state_set_episode=[[] for x in range(5)]
            for i in range(episode):
                if i!=0:
                    state_sequence=[]
                    s_t_index=2
                    reward_whole=0
                    t=0
                    while True:
                        # if s_t_index not in state_sequence:
                        state_sequence.append( s_t_index )
                        s_t_value = value_state_episode[s_t_index]
                        a=np.random.choice(policy[s_t_index])
                        s_nextt_index =  s_t_index + a
                        reward_tmp = reward[s_t_index, max( a, 0 )]
                        reward_whole=reward_whole+np.power(lamda,t)*reward_tmp
                        t=t+1
                        if s_nextt_index == 5 or s_nextt_index == -1:
                            break
                        s_t_index = s_nextt_index
                    for s_t_index_episode in state_sequence:
                        value_state_episode[s_t_index_episode]=value_state_episode[s_t_index_episode]+afa_tmp*(reward_whole-value_state_episode[s_t_index_episode])
                        # value_state_set_episode[s_t_index_episode].append(reward_whole)
                        # value_state_episode[s_t_index_episode]=np.average(value_state_set_episode[s_t_index_episode])

                value_state_mc[afa_mc.index(afa_tmp),i, :] = value_state_episode
        for afa_tmp in range(len(afa_mc)):
            RMS_mc[afa_tmp,:]=np.power(np.average(np.power(value_state_mc[afa_tmp,:,:]-value_state_true,2),axis = 1),0.5)
        RMS_mc_100run_set.append(RMS_mc)
    for i in range(len(RMS_mc_100run_set[0])):
        RMS_mc_100run[i,:]=np.average( np.array( RMS_mc_100run_set )[:, i, :], axis = 0 )

    return RMS_mc_100run

def get_value_state_td_batch(afa_td,episode):
    value_state_td=np.zeros((episode,5))
    policy=np.broadcast_to([-1,1],(5,2))
    reward_tmp=np.broadcast_to([0,0],(4,2))
    reward=np.vstack((reward_tmp,[0,1]))
    lamda=1
    value_state_true=np.arange(1,6)/6

    RMS_td_100run_set=[]
    RMS_td = []

    for run in tqdm(range(100)):
        # for afa_tmp in afa_td:
        value_state_episode=np.ones(5)*0.5
        # for i in tqdm( range( episode )):
        state_sequence=[]
        reward_sequence=[]
        for i in  range( episode ) :
            state_sequence_episode = []
            reward_sequence_episode=[]
            # if i != 0:

            s_t_index = 2
            state_sequence_episode.append(s_t_index)
            while True:
                # s_t_value = value_state_episode[s_t_index]
                a = np.random.choice( policy[s_t_index] )
                s_nextt_index =  s_t_index + a
                reward_tmp = reward[s_t_index, max( a, 0 )]
                reward_sequence_episode.append(reward_tmp)
                state_sequence_episode.append( s_nextt_index )
                if s_nextt_index == 5 or s_nextt_index == -1:
                    # s_nextt_value = 0
                    reward_tmp = reward[s_t_index, max( a, 0 )]
                    # reward_sequence_episode.append( reward_tmp )
                    # value_state_episode[s_t_index] = s_t_value + afa_td * (reward_tmp + lamda * s_nextt_value - s_t_value)
                    break
                else:
                    # s_nextt_value = value_state_episode[s_nextt_index]
                    # value_state_episode[s_t_index] = s_t_value + afa_td * (reward_tmp + lamda * s_nextt_value - s_t_value)
                    s_t_index = s_nextt_index


            # state_sequence_episode=[3,2,1,0]
            # reward_sequence_episode= [0, 0, 0]
            state_sequence.append(state_sequence_episode)
            reward_sequence.append(reward_sequence_episode)

            value_state_oneepisode_update=np.zeros(5)
            for j in range(len(state_sequence_episode)-1):
                s_t_index=state_sequence_episode[j]
                s_t_value=value_state_episode[s_t_index]
                reward_tmp=reward_sequence_episode[j]
                s_nextt_index = state_sequence_episode[j + 1]
                if s_nextt_index==-1 or s_nextt_index==5:
                    s_nextt_value = 0
                    value_state_oneepisode_update[s_t_index]+=reward_tmp + lamda * s_nextt_value - s_t_value
                    # value_state_episode[s_t_index] = s_t_value + afa_td * (reward_tmp + lamda * s_nextt_value - s_t_value)
                else:
                    s_nextt_value = value_state_episode[s_nextt_index]
                    value_state_oneepisode_update[s_t_index]+=reward_tmp + lamda * s_nextt_value - s_t_value
                    # value_state_episode[s_t_index] = s_t_value + afa_td * (reward_tmp + lamda * s_nextt_value - s_t_value)
            value_state_episode+=afa_td*value_state_oneepisode_update
            # value_state_td[i,j, :] = value_state_episode

            while True:
                value_state_episode_update=np.zeros(5)
                for j in range(len(state_sequence)):
                    for k in range(len(state_sequence[j])-1):
                        s_t_index=state_sequence[j][k]
                        s_t_value = value_state_episode[s_t_index]
                        # reward_tmp = reward[s_t_index, max( (s_nextt_index-s_t_index), 0 )]
                        reward_tmp=reward_sequence[j][k]
                        s_nextt_index = state_sequence[j][k + 1]
                        if s_nextt_index==-1 or s_nextt_index==5:
                            s_nextt_value = 0
                            value_state_episode_update[s_t_index]+=reward_tmp + lamda * s_nextt_value - s_t_value
                            # value_state_episode[s_t_index] = s_t_value + afa_td * (reward_tmp + lamda * s_nextt_value - s_t_value)
                        else:
                            s_nextt_value = value_state_episode[s_nextt_index]
                            value_state_episode_update[s_t_index]+=reward_tmp + lamda * s_nextt_value - s_t_value
                            # value_state_episode[s_t_index] = s_t_value + afa_td * (reward_tmp + lamda * s_nextt_value - s_t_value)
                    # value_state_td[i,j, :] = value_state_episode
                # if abs(sum(value_state_episode_update))<1e-3/afa_td:
                if sum( abs( value_state_episode_update ) ) < 1e-3 / afa_td:

                    # value_state_td[i, :] = value_state_episode
                    break
                value_state_episode+=afa_td*value_state_episode_update

            value_state_td[i, :] = value_state_episode


        RMS_td = np.power( np.average( np.power( value_state_td - value_state_true, 2 ),axis=1 ), 0.5 )

        RMS_td_100run_set.append(RMS_td)

    RMS_td_100run = np.average(np.array(RMS_td_100run_set),axis=0)
    return RMS_td_100run

def get_value_state_mc_batch(afa_mc,episode):
    value_state_mc=np.zeros((episode,5))
    policy=np.broadcast_to([-1,1],(5,2))
    reward_tmp=np.broadcast_to([0,0],(4,2))
    reward=np.vstack((reward_tmp,[0,1]))
    lamda=1
    value_state_true=np.arange(1,6)/6
    RMS_mc_100run_set=[]
    RMS_mc=[]

    for run in tqdm(range(100)):
        # for afa_tmp in afa_mc:
        value_state_episode=np.ones(5)*0.5
        state_sequence=[]
        reward_sequence=[]
        for i in range(episode):
            state_sequence_episode = []
            reward_sequence_episode=[]
            # if i!=0:

            s_t_index=2
            state_sequence_episode.append(s_t_index)
            reward_whole=0
            t=0
            while True:
                # if s_t_index not in state_sequence:
                # s_t_value = value_state_episode[s_t_index]
                # a=np.random.choice(policy[s_t_index])
                if np.random.binomial( 1, 0.5 )==0:
                    a=-1
                else:
                    a=1
                s_nextt_index =  s_t_index + a

                state_sequence_episode.append( s_nextt_index )
                reward_tmp = reward[s_t_index, max( a, 0 )]
                reward_whole=reward_whole+np.power(lamda,t)*reward_tmp
                t=t+1
                if s_nextt_index == 5 or s_nextt_index == -1:
                    # state_sequence_episode.append( reward_whole )
                    reward_sequence_episode=[reward_whole] * (len( state_sequence_episode ) - 1)
                    break
                else:
                    s_t_index = s_nextt_index

            # state_sequence_episode = [3, 4, 3, 4, 5, 4, 5, 6]
            # state_sequence_episode = [2, 3, 2, 3, 4, 3, 4, 5]
            # reward_sequence_episode = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

            state_sequence.append(state_sequence_episode)
            reward_sequence.append(reward_sequence_episode)

            value_state_oneepisode_update=np.zeros(5)

        # value_state_mc[i, :] = value_state_episode

            for j in range(len(state_sequence_episode)-1):
                s_t_index = state_sequence_episode[j]
                s_t_value = value_state_episode[s_t_index]
                s_nextt_index = state_sequence_episode[j + 1]
                reward_tmp = reward_sequence_episode[j]
                if s_nextt_index == 5 or s_nextt_index == -1:
                    s_nextt_value = 0
                    value_state_oneepisode_update[s_t_index] += reward_tmp  - s_t_value
                    # value_state_episode[s_t_index] = s_t_value + afa_td * (reward_tmp + lamda * s_nextt_value - s_t_value)
                else:
                    s_nextt_value = value_state_episode[s_nextt_index]
                    value_state_oneepisode_update[s_t_index] += reward_tmp  - s_t_value
                    # value_state_episode[s_t_index] = s_t_value + afa_td * (reward_tmp + lamda * s_nextt_value - s_t_value)
            value_state_episode += afa_mc * value_state_oneepisode_update

            while True:
                value_state_episode_update=np.zeros(5)
                for j in range(len(state_sequence)):
                    for k in range(len(state_sequence[j])-1):
                        s_t_index=state_sequence[j][k]
                        s_t_value = value_state_episode[s_t_index]
                        s_nextt_index=state_sequence[j][k+1]
                        reward_whole = reward_sequence[j][k]
                        if s_nextt_index == 5 or s_nextt_index == -1:
                            s_nextt_value = 0
                            value_state_episode_update[s_t_index] +=  (reward_whole  - s_t_value)
                        else:
                            s_nextt_value = value_state_episode[s_nextt_index]
                            value_state_episode_update[s_t_index] +=  (reward_whole - s_t_value)
                if sum(abs(value_state_episode_update))<1e-3/afa_mc:
                    break
                value_state_episode+=afa_mc*value_state_episode_update
            value_state_mc[i,:] = value_state_episode

        RMS_mc = np.power( np.average( np.power( value_state_mc - value_state_true, 2 ), axis = 1 ), 0.5 )

        RMS_mc_100run_set.append( RMS_mc )

    RMS_td_100run = np.average( np.array( RMS_mc_100run_set ), axis = 0 )
    return RMS_td_100run





def figure6_7():
    episode = 100
    lamda = 1
    afa_td = [0.05,0.1,0.15]
    afa_mc=[0.01,0.02,0.03,0.04]
    RMS_td=get_value_state_td(afa_td,episode)
    RMS_mc=get_value_state_mc(afa_mc,episode)


    fig,ax=plt.subplots(1,1)
    for i in range(len(RMS_td)):
        ax.plot(RMS_td[i],label='TD'+str(afa_td[i]))
    # for i in range(len(RMS_mc)):
    #     ax.plot(RMS_mc[i],label='MC'+str(afa_mc[i]))
    plt.legend()
    plt.savefig('Randomwalk_6_7.png')
    plt.show()

def figure6_8():
    episode = 100
    lamda = 1
    afa_td = 0.001
    afa_mc=0.001
    # times=7
    RMS_td=get_value_state_td_batch(afa_td,episode)
    RMS_mc=get_value_state_mc_batch(afa_mc,episode)

    fig,ax=plt.subplots(1,1)
    ax.plot(RMS_td,label='TD')
    ax.plot(RMS_mc,label='MC')
    plt.legend()
    plt.savefig('Randomwalk_6_8.png')
    plt.show()

if __name__=="__main__":
    # figure6_7()
    figure6_8()