import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import axes3d
class Day:
    def __init__(self,state_location):
        self.state_location=state_location
        self.reward=[0,0]
        self.request=[0,0]
        self.action=0

    def return_generate( self ):
        return_tmp1=np.random.poisson(3,1)[0]
        return_tmp2=np.random.poisson(2,1)[0]
        self.state_location[0]=self.state_location[0]+return_tmp1
        self.state_location[1]=self.state_location[1]+return_tmp2

    def action_generate( self,action_tmp_set ):
        # self.action = np.random.choice( [-self.state_location[1],min( 5, self.state_location[0] )], 1 )[0]
        state_location_set=[]
        state_location_tmp=np.zeros(2)
        for action_tmp in action_tmp_set:
            state_location_tmp[0]=self.state_location[0]-action_tmp
            state_location_tmp[1]=self.state_location[1]+action_tmp
            if state_location_tmp[0] > 20:
                state_location_tmp[0] = 20
            if state_location_tmp[1] > 20:
                state_location_tmp[1] = 20
            state_location_set.append([state_location_tmp[0],state_location_tmp[1]])
        return state_location_set


    def request_generate( self,state_location_set ):
        request_real1=np.random.poisson(3,1)[0]
        request_real2=np.random.poisson(4,1)[0]
        request_tmp_set=[]
        for state_location_tmp in state_location_set:
            if request_real1<=state_location_tmp[0]:
                # self.request[0]=request_tmp1
                request_tmp1=request_real1
                state_location_tmp[0]=state_location_tmp[0]-request_tmp1
            else:
                request_tmp1=state_location_tmp[0]
                state_location_tmp[0]=0
            if request_real2<=state_location_tmp[1]:
                # self.request[1]=request_tmp2
                request_tmp2=request_real2
                state_location_tmp[1]=state_location_tmp[1]-request_tmp2
            else:
                request_tmp2=state_location_tmp[1]
                state_location_tmp[1]=0
            request_tmp_set.append([request_tmp1,request_tmp2])
        return state_location_set,request_tmp_set

    def reward_calculate_max( self,reward_matrix,a,b,state_location_set,request_tmp_set,action_tmp_set ):
        reward_tmp_set=np.zeros(len(state_location_set))
        gama=0.9
        for i in range(len(state_location_set)):
            reward_tmp_set[i]=10*(request_tmp_set[i][0]+request_tmp_set[i][1])-2*np.abs(action_tmp_set[i])+reward_matrix[a][b]*gama
        reward_max_tmp=max(reward_tmp_set)
        action_max_set=[action_tmp_set[i] for i,j in enumerate(reward_tmp_set) if j==reward_max_tmp]
        return action_max_set,reward_max_tmp

    def reward_calculate_average( self,reward_matrix,a,b,state_location_set,request_tmp_set,action_tmp_set ):
        reward_tmp_set=np.zeros(len(state_location_set))
        gama=0.9
        for i in range(len(state_location_set)):
            reward_tmp_set[i]=10*(request_tmp_set[i][0]+request_tmp_set[i][1])-2*np.abs(action_tmp_set[i])+reward_matrix[a][b]*gama
        return np.average(reward_tmp_set)

def Car_Rental_greedy(times,states):
    reward_matrix=np.zeros((states,states))
    reward_matrix_new=np.zeros((states,states))
    action_matrix=[]
    # Day_matrix=np.array((states,states),dtype = Day)
    Day_matrix=[]
    for i in range(states):
        day_matrix_row = []
        for j in range(states):
            day_matrix_row.append(Day([i,j]))
        Day_matrix.append(day_matrix_row)

    for k in range(times):
        action_matrix_eachtime = []
        for i in range(states):
            action_matrix_row=[]
            for j in range(states):
                deta = float( "inf" )
                while deta > 1:
                    Day_matrix[i][j].return_generate()
                    action_tmp_set = np.arange( max( -Day_matrix[i][j].state_location[1], -5 ),
                                            min( 5, Day_matrix[i][j].state_location[0] ) + 1 )
                    state_location_set = Day_matrix[i][j].action_generate( action_tmp_set )
                    state_location_set, request_tmp_set = Day_matrix[i][j].request_generate( state_location_set )

                    #calculate max reward and action
                    action_max_set,reward_max_tmp=Day_matrix[i][j].reward_calculate_max(reward_matrix,i,j,state_location_set, request_tmp_set, action_tmp_set)
                    #calculate average reward
                    # reward_average=Day_matrix[i][j].reward_calculate_average(reward_matrix,i,j,state_location_set, request_tmp_set, action_tmp_set)
                    deta=np.abs(reward_max_tmp-reward_matrix_new[i][j])
                    reward_matrix_new[i][j]=reward_max_tmp
                action_matrix_row.append(action_max_set[0])
                # reward_matrix_new[i][j]=reward_average
                # print(action_max_set,end=', ')
            # print('\n')
            action_matrix_eachtime.append(action_matrix_row)
        action_matrix.append(action_matrix_eachtime)
        # print('\n')
        # print('\n')
        reward_matrix=reward_matrix_new
    fig, ax = plt.subplots( 1, 1 )
    ax.pcolor( action_matrix[0] )
    plt.show()

    fig, ax = plt.subplots( 1, 1 )
    ax.pcolor( action_matrix[1] )
    plt.show()

    fig, ax = plt.subplots( 1, 1 )
    ax.pcolor( action_matrix[2] )
    plt.show()

    fig, ax = plt.subplots( 1, 1 )
    ax.pcolor( action_matrix[3] )
    plt.show()

    fig, ax = plt.subplots( 1, 1 )
    ax.pcolor( action_matrix[4] )
    plt.show()

    return reward_matrix_new,action_matrix
    # return reward_matrix_new

def Car_Rental_average(times,states):
    reward_matrix=np.zeros((states,states))
    reward_matrix_new=np.zeros((states,states))
    action_matrix=[]
    # Day_matrix=np.array((states,states),dtype = Day)
    Day_matrix=[]
    for i in range(states):
        day_matrix_row = []
        for j in range(states):
            day_matrix_row.append(Day([i,j]))
        Day_matrix.append(day_matrix_row)

    for k in range(times):
        for i in range(states):
            action_matrix_row=[]
            for j in range(states):
                Day_matrix[i][j].return_generate()
                action_tmp_set=np.arange(max(-Day_matrix[i][j].state_location[1],-5), min( 5, Day_matrix[i][j].state_location[0] )+1)
                state_location_set=Day_matrix[i][j].action_generate(action_tmp_set)
                state_location_set,request_tmp_set=Day_matrix[i][j].request_generate( state_location_set )
                #calculate max reward and action
                # action_max_set,reward_max_tmp=Day_matrix[i][j].reward_calculate_max(reward_matrix,i,j,state_location_set, request_tmp_set, action_tmp_set)
                # calculate average reward
                reward_average=Day_matrix[i][j].reward_calculate_average(reward_matrix,i,j,state_location_set, request_tmp_set, action_tmp_set)

                reward_matrix_new[i][j]=reward_average
                # print(reward_average,end=', ')
            # print('\n')
        # print('\n')
        # print('\n')
        reward_matrix=reward_matrix_new
    fig=plt.figure()
    ax=fig.add_subplot(111,projection='3d')
    xvalues = np.arange(21)
    yvalues = np.arange(21)
    xx, yy = np.meshgrid( xvalues, yvalues )
    # X, Y, Z = axes3d.get_test_data( 0.05 )
    ax.plot_surface(X=xx,Y=yy,Z=reward_matrix_new)
    plt.show()
    return reward_matrix_new


if __name__=="__main__":
    # reward_matrix_new=Car_Rental_average(50,20)
    reward_matrix_new,action_matrix=Car_Rental_greedy(5,20)






