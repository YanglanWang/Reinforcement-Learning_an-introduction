import numpy as np
import matplotlib.pyplot as plt
def Gambler(n):
    p=0.4
    states=np.zeros(n+1)
    # states_new=np.zeros(n+1)
    action_greedy=np.zeros(n+1)
    deta=float("inf")
    deta_value=1e-20
    whole_test=[]
    while deta>deta_value:
        deta=0
        for state_tmp in range(1,len(states)-1):
            action=np.arange(1,min(state_tmp,100-state_tmp)+1)
            action_reward=[]
            for action_tmp in action:
                if state_tmp+action_tmp<100:
                    if state_tmp-action_tmp>0:
                        v_action_tmp=p*states[state_tmp+action_tmp]+(1-p)*states[state_tmp-action_tmp]
                    else:
                        v_action_tmp = p * states[state_tmp  + action_tmp] + (1 - p) * states[0]
                else:
                    if state_tmp-action_tmp>0:
                        v_action_tmp=p*(states[100]+1)+(1-p)*states[state_tmp-action_tmp]
                    else:
                        v_action_tmp = p * (states[100]+1) + (1 - p) * states[0]

                action_reward.append(v_action_tmp)
            state_action_max_set=[action[i] for i,j in enumerate(action_reward) if j==max(action_reward)]
            action_greedy[state_tmp]=state_action_max_set[0]
            deta=max(deta,abs(states[state_tmp]-max(action_reward)))
            states[state_tmp]=max(action_reward)
            # states_new[state_tmp]=max(action_reward)
    # states=states_new
        whole_test.append(list(states))

    for state_tmp in range( 1, len( states ) - 1 ):
        action = np.arange( 1, min( state_tmp, 100 - state_tmp ) + 1 )
        action_reward = []
        for action_tmp in action:
            if state_tmp + action_tmp < 100:
                if state_tmp + 1 - action_tmp > 0:
                    v_action_tmp = p * states[state_tmp + action_tmp] + (1 - p) * states[state_tmp - action_tmp]
                else:
                    v_action_tmp = p * states[state_tmp + action_tmp] + (1 - p) * states[0]
            else:
                if state_tmp - action_tmp > 0:
                    v_action_tmp = p * (states[100] + 1) + (1 - p) * states[state_tmp - action_tmp]
                else:
                    v_action_tmp = p * (states[100] + 1) + (1 - p) * states[0]

            action_reward.append( v_action_tmp )
        state_action_max_set = [action[i] for i, j in enumerate( np.round(action_reward,5) ) if j == max( np.round(action_reward,5) )]
        action_greedy[state_tmp] = state_action_max_set[0]

    return whole_test,action_greedy

if __name__=='__main__':
    whole_test,action_greedy=Gambler(100)
    fig,(axes1,axes2)=plt.subplots(2,1)
    # for i in range(len(whole_test)):
    axes1.plot(whole_test[-1][1:len(whole_test[-1])-1])
    axes2.plot(action_greedy[1:100])
    plt.show()