import numpy as np
import matplotlib.pyplot as plot
e=[0,0.1,0.01]
r_whole=[]
for e_tmp in e:
    r_sample = []
    r_sample_optimal_action=[]
    r_tmp=[]
    r_optimal_action=[]
    for sample in range( 2000 ):
        s_expected_update = dict()
        r_time=[]
        mu, sigma = 0, 1  # mean and standard deviation
        s_xing = np.random.normal( mu, sigma, 10 )
        s_expected = [0] * 10
        s_xing_max=-float("inf")
        for i in range(len(s_xing)):
             if s_xing[i]>s_xing_max:
                 s_xing_max=s_xing[i]
                 optimal_index=i
        action_set=[]
        rate_for_optimal_action=[]
        for t in range( 1000 ):
            e_random=np.random.rand()
            if e_tmp < e_random:
                s_max_expected = max( s_expected )
                index_max=s_expected.index(s_max_expected)
                s_max=s_xing[index_max]
                r=np.random.normal(s_max,sigma,1)
                # optimal_index=index_max
            else:
                e_random2=np.random.randint(len(s_xing),size=1)
                index_max=e_random2[0]
                r=np.random.normal(s_xing[index_max],sigma,1)
            action_set.append(index_max)
            if index_max not in s_expected_update.keys():
                s_expected_update[index_max]= [r]
            else:
                s_expected_update[index_max].append(r)
            s_expected[index_max] = np.average( s_expected_update[index_max] )
            r_time.append(r)
        for i in range(len(action_set)):
            if action_set[i]==optimal_index:
                rate_for_optimal_action.append(1)
            else:
                rate_for_optimal_action.append(0)
        r_sample_optimal_action.append(rate_for_optimal_action)
        r_sample.append(r_time)
    # r_tmp=np.average( r_sample_optimal_action, axis = 0 )
    r_optimal_action=np.average(r_sample_optimal_action,axis = 0)
    # r_line=[]
    # for i in range( len( r_optimal_action ) ):
    #     for j in range( len( r_optimal_action[i] ) ):
    #         r_line.append( r_optimal_action[i][j] )
    # for i in range(len(r_optimal_action)):
    #     if i!=0:
    #         r_optimal_action[i]=r_optimal_action[i-1]+r_optimal_action[i]
    # for i in range(len(r_optimal_action)):
    #     r_optimal_action[i] =r_optimal_action[i]/(i+1)
    plot.plot(range(len(r_optimal_action)),r_optimal_action)
    # for i in range(len(r_sample[0])):
    #     plot.plot([i]*len(r_sample),r_sample[:][i])
plot.show()
