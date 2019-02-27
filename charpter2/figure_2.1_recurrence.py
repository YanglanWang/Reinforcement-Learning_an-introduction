import numpy as np
import matplotlib.pyplot as plot
e=[0,0.1,0.01]
r_whole=[]
for e_tmp in e:
    r_sample = []
    r_tmp=[]
    ll = 0
    for sample in range( 2000 ):
        np.random.seed( ll )
        ll=ll+1
        s_expected_update = dict()
        r_time=[]
        mu, sigma = 0, 1  # mean and standard deviation
        s_xing = np.random.normal( mu, sigma, 10 )
        s_expected = [0] * 10
        for t in range( 1000 ):
            np.random.seed( ll )
            ll = ll + 1
            e_random=np.random.rand()
            if e_tmp < e_random:
                s_max_expected = max( s_expected )
                index_max=np.random.choice([index_max_set for index_max_set, s_max_expected_set in enumerate(s_expected) if s_max_expected_set==s_max_expected])
                s_max=s_xing[index_max]
                r=np.random.normal(s_max,sigma,1)
            else:
                e_random2=np.random.randint(len(s_xing),size=1)
                index_max=e_random2[0]
                r=np.random.normal(s_xing[index_max],sigma,1)
            if index_max not in s_expected_update.keys():
                s_expected_update[index_max]= [r]
            else:
                s_expected_update[index_max].append(r)
            s_expected[index_max] = np.average( s_expected_update[index_max] )
            r_time.append(r)
        r_sample.append(r_time)
    # for k in np.array(r_sample)[:,0,0]:
    #     f.write(str(k)+'\n')
    # f.close()
    r_tmp=np.average( r_sample, axis = 0 )
    r_line=[]
    for i in range(len(r_tmp)):
        for j in range(len(r_tmp[i])):
            r_line.append(r_tmp[i][j])
    # r_whole.append(r_line)
# r_after=np.average(r_whole,axis = 1)
# for i in range(len(r_whole)):
#     one_line=r_whole[i]
#     for i in range(len(r_line)):
#         if i!=0:
#             r_line[i]=r_line[i-1]+r_line[i]
#     for i in range(len(r_line)):
#         r_line[i] =r_line[i]/(i+1)
    plot.plot(range(len(r_line)),r_line)
plot.show()
