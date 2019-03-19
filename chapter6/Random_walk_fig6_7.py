import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def get_value_state_td(afa_td,episode):
    value_state_td=np.zeros((len(afa_td),episode,5))
    policy=np.broadcast_to([-1,1],(5,2))
    reward_tmp=np.broadcast_to([0,0],(4,2))
    reward=np.vstack((reward_tmp,[0,1]))
    lamda=1
    RMS_td=np.zeros((len(afa_td),episode))
    value_state_true=np.arange(1,6)/6

    for afa_tmp in afa_td:
        value_state_episode=np.ones(5)*0.5
        for i in tqdm( range( episode )):
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
    return RMS_td
def get_value_state_mc(afa_mc,episode):
    value_state_mc=np.zeros((len(afa_mc),episode,5))
    policy=np.broadcast_to([-1,1],(5,2))
    reward_tmp=np.broadcast_to([0,0],(4,2))
    reward=np.vstack((reward_tmp,[0,1]))
    lamda=1
    RMS_mc=np.zeros((len(afa_mc),episode))
    value_state_true=np.arange(1,6)/6

    for afa_tmp in afa_mc:
        value_state_episode=np.ones(5)*0.5
        value_state_set_episode=[[] for x in range(5)]
        for i in range(episode):
            if i!=0:
                state_sequence=[]
                s_t_index=2
                reward_whole=0
                t=0
                while True:
                    if s_t_index not in state_sequence:
                        state_sequence.append( s_t_index )
                    a=np.random.choice(policy[s_t_index])
                    s_nextt_index =  s_t_index + a
                    reward_tmp = reward[s_t_index, max( a, 0 )]
                    reward_whole=reward_whole+np.power(lamda,t)*reward_tmp
                    t=t+1
                    if s_nextt_index == 5 or s_nextt_index == -1:
                        break
                    s_t_index = s_nextt_index
                for s_t_index_episode in state_sequence:
                    value_state_set_episode[s_t_index_episode].append(reward_whole)
                    value_state_episode[s_t_index_episode]=np.average(value_state_set_episode[s_t_index_episode])

            value_state_mc[afa_mc.index(afa_tmp),i, :] = value_state_episode
    for afa_tmp in range(len(afa_mc)):
        RMS_mc[afa_tmp,:]=np.power(np.average(np.power(value_state_mc[afa_tmp,:,:]-value_state_true,2),axis = 1),0.5)

    return RMS_mc




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



if __name__=="__main__":
    figure6_7()