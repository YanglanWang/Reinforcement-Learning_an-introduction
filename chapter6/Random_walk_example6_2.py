import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def figure6_6():
    value_state=np.zeros((5,5))
    value_state_episode=np.ones(5)*0.5
    policy=np.broadcast_to([-1,1],(5,2))
    reward_tmp=np.broadcast_to([0,0],(4,2))
    reward=np.vstack((reward_tmp,[0,1]))
    episodes=[0,1,10,100,100000]
    lamda=1
    afa=0.1
    for i in tqdm(range(episodes[-1]+1)):
        if i!=0:
            s_t_index=2
            while True:
                s_t_value = value_state_episode[s_t_index]
                a = np.random.choice( policy[s_t_index] )
                s_nextt_index=int(s_t_index+a)
                reward_tmp = reward[s_t_index, max( a, 0 )]
                if s_nextt_index==5 or s_nextt_index==-1:
                    s_nextt_value=0
                    value_state_episode[s_t_index]=s_t_value+afa*(reward_tmp+lamda*s_nextt_value-s_t_value)
                    break
                else:
                    s_nextt_value=value_state_episode[s_nextt_index]
                    value_state_episode[s_t_index]=s_t_value+afa*(reward_tmp+lamda*s_nextt_value-s_t_value)
                s_t_index=s_nextt_index

        if i in episodes:
            value_state[episodes.index(i),:]=value_state_episode
    fig,ax=plt.subplots(1,1)
    for i in range(len(value_state)):
        ax.plot(value_state[i],label=str(episodes[i]))
    plt.legend()
    # plt.savefig('Randomwalk_6_6.png')
    plt.show()



if __name__=="__main__":
    figure6_6()