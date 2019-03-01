import numpy as np
import matplotlib.pyplot as plt
class Bandit:
    def __init__(self,epsilon,action,q_estimate,q_xing):
        self.epsilon=epsilon
        self.action_times=np.zeros(action)
        self.q_estimate=q_estimate
        # self.q_xing=np.random.randn(action_times)
        self.q_xing=q_xing
        self.action_optimal_index=[index_xing for index_xing,q_xing_tmp in enumerate(self.q_xing) if q_xing_tmp==max(self.q_xing)]



    def action( self ):
        if np.random.rand()<self.epsilon:
            action_return=np.random.randint(len(self.action_times))
        else:
            action_return=np.random.choice([action_max_set for action_max_set,q_estimate_max in enumerate(self.q_estimate) if q_estimate_max==max(self.q_estimate)])
        self.action_times[action_return]=self.action_times[action_return]+1
        return action_return

    def reward( self,action_index ):
        reward_return=1*np.random.randn()+self.q_xing[action_index]
        self.q_estimate[action_index]=(self.q_estimate[action_index]*(self.action_times[action_index]-1)+reward_return)/self.action_times[action_index]
        return reward_return

def simulate(sample,play,epsilon_tmp):
    reward_set=[]
    action_set=[]
    ll=0
    for i in np.arange(sample):
        np.random.seed( ll )
        ll=ll+1

        sample_reward=[]
        sample_action=[]
        action = 10
        q_estimate = np.zeros( action )
        q_xing=np.random.randn(action)
        bandit_tmp=Bandit(epsilon_tmp,action,q_estimate,q_xing)
        for j in np.arange(play):
            np.random.seed( ll )
            ll = ll + 1
            action_return=bandit_tmp.action()
            reward_return=bandit_tmp.reward(action_return)
            sample_reward.append(reward_return)
            if action_return in bandit_tmp.action_optimal_index:
                sample_action.append(1)
            else:
                sample_action.append(0)
        reward_set.append(sample_reward)
        action_set.append(sample_action)
    # reward_calculate=np.average(np.array(reward_set),axis=0)
    # action_calculate=np.average(np.array(action_set),axis=0)

    #for EXE2.3
    reward_calculate=np.cumsum(np.average(np.array(reward_set),axis=0))
    action_calculate=np.cumsum(np.average(np.array(action_set),axis=0))
    action_calculate=action_calculate/np.arange(1,np.size(action_calculate)+1)
    return reward_calculate, action_calculate




def figure_2_1(sample,play):
    epsilon=[0,0.01,0.1]
    total_data=np.zeros([len(epsilon),2,play])
    for epsilon_tmp in epsilon:
        # bandit_tmp=Bandit(epsilon_tmp,action_times,q_estimate)
        reward_calculate,action_calculate=simulate(sample,play,epsilon_tmp)
        total_data[epsilon.index(epsilon_tmp),0,:]=reward_calculate
        total_data[epsilon.index(epsilon_tmp),1,:]=action_calculate

    fig,axes=plt.subplots(2,1,sharex = True)
    for i in range(total_data.shape[1]):
        for j in range(total_data.shape[0]):
            axes[i].plot(total_data[j][i],label=str(epsilon[j]))
        axes[i].legend()
        axes[i].set_xlabel('Plays')
        if i==0:
            axes[i].set_ylabel('Average rewards')
        else:
            axes[i].set_ylabel('Rate of optimal action')

    plt.show()

if __name__=='__main__':
    figure_2_1(2000,1000)