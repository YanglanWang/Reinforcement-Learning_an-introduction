import numpy as np
import matplotlib.pyplot as plt
class Bandit:
    def __init__(self,epsilon,action,q_estimate,q_xing):
        self.epsilon=epsilon
        self.action_n=action
        self.action_times=np.zeros(action)
        self.q_estimate=q_estimate
        # self.q_xing=np.random.randn(action_times)
        self.q_xing=q_xing
        # self.action_optimal_index=[index_xing for index_xing,q_xing_tmp in enumerate(self.q_xing) if q_xing_tmp==max(self.q_xing)]
        self.preference=np.zeros(action)
        self.reward_reference=0
        self.reward_t=0
        self.action_t=action
        self.pi_action=np.ones(action)/action



    def action( self ):
        self.action_optimal_index=[index_xing for index_xing,q_xing_tmp in enumerate(self.q_xing) if q_xing_tmp==max(self.q_xing)]
        if np.random.rand()<self.epsilon:
            action_return=np.random.randint(len(self.action_times))
        else:
            action_return=np.random.choice([action_max_set for action_max_set,q_estimate_max in enumerate(self.q_estimate) if q_estimate_max==max(self.q_estimate)])
        self.action_times[action_return]=self.action_times[action_return]+1
        return action_return

    def action_rc(self):
        afa=0.1
        self.action_optimal_index=[index_xing for index_xing,q_xing_tmp in enumerate(self.q_xing) if q_xing_tmp==max(self.q_xing)]
        beta=0.1
        self.reward_reference=self.reward_reference+afa*(self.reward_t-self.reward_reference)
        if self.action_t!=self.action_n:
            self.preference[self.action_t]=self.preference[self.action_t]+beta*(self.reward_t-self.reward_reference)
        self.pi_action=np.exp(self.preference)/sum(np.exp(self.preference))
        action_return=np.random.choice(self.action_n,1,p=self.pi_action)[0]
        self.action_t=action_return
        return action_return

    def action_pursuit( self ):
        beta_pursuit = 0.01
        self.action_optimal_index=[index_xing for index_xing,q_xing_tmp in enumerate(self.q_xing) if q_xing_tmp==max(self.q_xing)]
        # if np.random.rand()<self.epsilon:
        #     action_return=np.random.randint(len(self.action_times))
        # else:
        action_return=np.random.choice(self.action_n,1,p=self.pi_action)[0]
        if action_return in self.action_optimal_index:
            self.pi_action[action_return]=self.pi_action[action_return]+beta_pursuit*(1-self.pi_action[action_return])
        else:
            self.pi_action[action_return]=self.pi_action[action_return]+beta_pursuit*(0-self.pi_action[action_return])
        self.pi_action=self.pi_action/np.sum(self.pi_action)
        self.action_times[action_return]=self.action_times[action_return]+1
        return action_return

    def reward( self,action_index,afa ):
        reward_return=1*np.random.randn()+self.q_xing[action_index]
        if afa==0:
            self.q_estimate[action_index]=(self.q_estimate[action_index]*(self.action_times[action_index]-1)+reward_return)/self.action_times[action_index]
        if afa==0.1:
            self.q_estimate[action_index]=self.q_estimate[action_index]+afa*(reward_return-self.q_estimate[action_index])
        #if the problem is static, q_xing doesn't change; or else, q_xing changes
        # self.q_xing=self.q_xing+1*np.random.randn(10)

        return reward_return
    def reward_rc(self,action_index):
        reward_return=1*np.random.randn()+self.q_xing[action_index]
        return reward_return




def simulate(sample,play,epsilon_tmp,afa):
    reward_set=[]
    action_set=[]
    for i in np.arange(sample):
        sample_reward=[]
        sample_action=[]
        action = 10
        q_estimate = np.zeros( action )
        q_xing=np.random.randn(action)
        bandit_tmp=Bandit(epsilon_tmp,action,q_estimate,q_xing)
        for j in np.arange(play):
            action_return=bandit_tmp.action()
            reward_return=bandit_tmp.reward(action_return,afa)
            sample_reward.append(reward_return)
            if action_return in bandit_tmp.action_optimal_index:
                sample_action.append(1)
            else:
                sample_action.append(0)
        reward_set.append(sample_reward)
        action_set.append(sample_action)
    reward_calculate=np.average(np.array(reward_set),axis=0)
    action_calculate=np.average(np.array(action_set),axis=0)
    return reward_calculate, action_calculate

def exe_2_5_simulate(sample,play,epsilon,afa):
    reward_set=[]
    action_set=[]
    for i in np.arange(sample):
        sample_reward=[]
        sample_action=[]
        action = 10
        q_estimate = np.zeros( action )
        q_xing=np.ones(action)
        bandit_tmp=Bandit(epsilon,action,q_estimate,q_xing)
        for j in np.arange(play):
            action_return=bandit_tmp.action()
            reward_return=bandit_tmp.reward(action_return,afa)
            bandit_tmp.reward_t=reward_return
            sample_reward.append(reward_return)
            if action_return in bandit_tmp.action_optimal_index:
                sample_action.append(1)
            else:
                sample_action.append(0)
        reward_set.append(sample_reward)
        action_set.append(sample_action)
    reward_calculate=np.average(np.array(reward_set),axis=0)
    # for k in np.array( reward_set )[:, 0]:
    #     f.write(str(k)+'\n')
    # f.close()
    action_calculate=np.average(np.array(action_set),axis=0)
    return reward_calculate, action_calculate

def reinforcement_comparison_simulate(sample,play):
    reward_set=[]
    action_set=[]
    afa=0.1
    for i in np.arange(sample):
        sample_reward=[]
        sample_action=[]
        action = 10
        q_estimate = np.zeros( action )
        q_xing=np.random.randn(action)
        bandit_tmp=Bandit(None,action,q_estimate,q_xing)
        #epsilon in bandit_tmp will not be used

        for j in np.arange(play):
            action_return=bandit_tmp.action_rc()
            reward_return=bandit_tmp.reward_rc(action_return)
            bandit_tmp.reward_t=reward_return
            sample_reward.append(reward_return)
            if action_return in bandit_tmp.action_optimal_index:
                sample_action.append(1)
            else:
                sample_action.append(0)
        reward_set.append(sample_reward)
        action_set.append(sample_action)
    reward_calculate=np.average(np.array(reward_set),axis=0)
    action_calculate=np.average(np.array(action_set),axis=0)
    return reward_calculate, action_calculate

def pursuit_simulate(sample,play):
    reward_set=[]
    action_set=[]
    for i in np.arange(sample):
        sample_reward=[]
        sample_action=[]
        action = 10
        q_estimate = np.zeros( action )
        q_xing=np.random.randn(action)
        bandit_tmp=Bandit(None,action,q_estimate,q_xing)
        for j in np.arange(play):
            action_return=bandit_tmp.action_pursuit()
            reward_return=bandit_tmp.reward(action_return,0)
            bandit_tmp.reward_t=reward_return
            sample_reward.append(reward_return)
            if action_return in bandit_tmp.action_optimal_index:
                sample_action.append(1)
            else:
                sample_action.append(0)
        reward_set.append(sample_reward)
        action_set.append(sample_action)
    reward_calculate=np.average(np.array(reward_set),axis=0)
    action_calculate=np.average(np.array(action_set),axis=0)
    return reward_calculate, action_calculate

def figure_2_1(sample,play):
    epsilon=[0,0.01,0.1]
    total_data=np.zeros([len(epsilon),2,play])
    afa=0
    for epsilon_tmp in epsilon:
        # bandit_tmp=Bandit(epsilon_tmp,action_times,q_estimate)
        reward_calculate,action_calculate=simulate(sample,play,epsilon_tmp,afa)
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
def exe_2_5(sample,play):
    epsilon=0.1
    total_data=np.zeros([2,2,play])
    #afa=0 denotes afa=1/k
    afa_set=[0,0.1]
    for afa in afa_set:
        reward_calculate,action_calculate=exe_2_5_simulate(sample,play,epsilon,afa)
        total_data[afa_set.index(afa),0,:]=reward_calculate
        total_data[afa_set.index(afa),1,:]=action_calculate
    fig,axes=plt.subplots(2,1,sharex = True)
    for i in range(total_data.shape[1]):
        for j in range(total_data.shape[0]):
            axes[i].plot(total_data[j][i][1:],label=str(afa_set[j]))
        axes[i].legend()
        axes[i].set_xlabel('Plays')
        if i==0:
            axes[i].set_ylabel('Average rewards')
        else:
            axes[i].set_ylabel('Rate of optimal action')

    plt.show()

def old_figure_2_6(sample,play):
    #[a,b]:a=eplison;b=afa
    case_set=['pursuit','reinforcement comparison',[0.1,0.1]]
    total_data=np.zeros([len(case_set),2,play])
    for case in case_set:
        if case_set.index(case)==0:
            reward_calculate, action_calculate = pursuit_simulate( sample, play)
        elif case_set.index(case)==1:
            reward_calculate, action_calculate = reinforcement_comparison_simulate( sample, play)
        else:
            reward_calculate, action_calculate = simulate( sample, play, case[0],case[1])

        total_data[case_set.index( case ), 0, :] = reward_calculate
        total_data[case_set.index( case ), 1, :] = action_calculate

    fig, axes = plt.subplots( 2, 1, sharex = True )
    for i in range(total_data.shape[1]):
        for j in range(total_data.shape[0]):
            if j==0 or j==1:
                label_tmp=case_set[j]
            else:
                label_tmp='epsilon='+str(case_set[j][0])+', afa='+str(case_set[j][1])
            axes[i].plot(total_data[j][i],label=label_tmp)
        axes[i].legend()
        axes[i].set_xlabel('Plays')
        if i==0:
            axes[i].set_ylabel('Average rewards')
        else:
            axes[i].set_ylabel('Rate of optimal action')

    plt.show()
if __name__=='__main__':
    # figure_2_1(2000,1000)
    # exe_2_5(2000,5000)
    old_figure_2_6(2000,1000)