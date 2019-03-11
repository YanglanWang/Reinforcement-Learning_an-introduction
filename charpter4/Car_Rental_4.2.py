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

    def action_generate( self):
        # self.action = np.random.choice( [-self.state_location[1],min( 5, self.state_location[0] )], 1 )[0]
        state_location_set = []
        # state_location_tmp=np.zeros(2)
        # for location_tmp in location:
        action_tmp_set = np.arange( max( -self.state_location[1], -5 ), min( 5, self.state_location[0] ) + 1 )

        for action_tmp in action_tmp_set:
            location_after_move1 = min(self.state_location[0] - action_tmp,20)
            location_after_move2 = min(self.state_location[1] + action_tmp,20)
            state_location_set.append( [location_after_move1, location_after_move2] )
        return state_location_set,action_tmp_set

    def return_generate( self,state_tmp ):
        return_tmp_set1=np.arange(11)
            # np.random.poisson(3,1)[0]
        return_tmp_set2=np.arange(11)
        probability_return1=np.zeros(11)
        probability_return2=np.zeros(11)
        # location=np.zeros(2)
        location1=state_tmp[0]+return_tmp_set1
        location2=state_tmp[1]+return_tmp_set2
        for i in range(len(probability_return1)):
            probability_return1[i]=np.power(3,i)*np.exp(-3)/np.math.factorial(i)
            probability_return2[i]=np.power(2,i)*np.exp(-2)/np.math.factorial(i)
        probability_return1=probability_return1/sum(probability_return1)
        probability_return2=probability_return2/sum(probability_return2)

        location=generate_matrix( location1, location2 )
        probability=probability_return1.reshape(probability_return1.shape[0],-1)*probability_return2
        return location,probability
        # return location1,location2,probability_return1,probability_return2
            # np.random.poisson(2,1)[0]
        # self.state_location[0]=self.state_location[0]+return_tmp1
        # self.state_location[1]=self.state_location[1]+return_tmp2




    def request_generate( self,state_location_set,return_probability ):
        request_real_set1=np.arange(11)
            # np.random.poisson(3,1)[0]
        request_real_set2=np.arange(11)
            # np.random.poisson(4,1)[0]
        probability_request1=np.zeros(11)
        probability_request2=np.zeros(11)
        for i in range(len(probability_request1)):
            probability_request1[i]=np.power(3,i)*np.exp(-3)/np.math.factorial(i)
            probability_request2[i]=np.power(4,i)*np.exp(-4)/np.math.factorial(i)
        probability_request1=probability_request1/sum(probability_request1)
        probability_request2=probability_request2/sum(probability_request2)

        request_real_set=generate_matrix(request_real_set1,request_real_set2)
        probability_request=probability_request1.reshape(probability_request1.shape[0],-1)*probability_request2

        state_location_final=[]
        request_satisfied=[]
        probability_final=[]
        for i in range(len(state_location_set)):
            for j in range(len(state_location_set[i])):
                for a in range(len(request_real_set)):
                    for b in range(len(request_real_set[a])):
                        state_location_final_tmp=np.zeros(2)
                        probability_tmp=return_probability[i][j]*probability_request[a][b]
                        if request_real_set[a][b][0]<state_location_set[i][j][0]:
                            request_tmp1 = request_real_set[a][b][0]
                            state_location_final_tmp[0]=int(state_location_set[i][j][0]-request_real_set[a][b][0])
                        else:
                            request_tmp1 = state_location_set[i][j][0]
                            state_location_final_tmp[0]=int(0)
                        state_location_final_tmp[0]=min(state_location_final_tmp[0],19)
                        if request_real_set[a][b][1]<state_location_set[i][j][1]:
                            request_tmp2 = request_real_set[a][b][1]
                            state_location_final_tmp[1]=int(state_location_set[i][j][1]-request_real_set[a][b][1])
                        else:
                            request_tmp2 = state_location_set[i][j][1]
                            state_location_final_tmp[1]=int(0)
                        state_location_final_tmp[1]=min(state_location_final_tmp[1],19)

                        state_location_final.append(state_location_final_tmp)
                        request_satisfied.append([request_tmp1,request_tmp2])
                        probability_final.append(probability_tmp)


        return state_location_final,request_satisfied,probability_final


    def reward_calculate( self,reward_matrix,state_location_final,request_satisfied,probability_final,action_tmp):
                          # reward_matrix,a,b,state_location_set,request_tmp_set,action_tmp_set ):
        # reward_tmp_set=np.zeros(len(state_location_set))
        gama=0.9
        reward_set=[]
        for i in range(len(state_location_final)):
            reward_tmp=10*(request_satisfied[i][0]+request_satisfied[i][1])-2*np.abs(action_tmp)+reward_matrix[int(state_location_final[i][0])][int(state_location_final[i][1])]*gama
            reward_set.append(reward_tmp)
        reward_action=sum(np.array(reward_set)*np.array(probability_final))

        return reward_action

    # def reward_calculate_average( self,reward_matrix,a,b,state_location_set,request_tmp_set,action_tmp_set ):
    #     reward_tmp_set=np.zeros(len(state_location_set))
    #     gama=0.9
    #     for i in range(len(state_location_set)):
    #         reward_tmp_set[i]=10*(request_tmp_set[i][0]+request_tmp_set[i][1])-2*np.abs(action_tmp_set[i])+reward_matrix[a][b]*gama
    #     return np.average(reward_tmp_set)

def Car_Rental_greedy(deta_value,states):
    reward_matrix=np.zeros((states,states))
    reward_matrix_new=np.ones((states,states))
    action_matrix=np.zeros((states,states))
    action_matrix_new=np.ones((states,states))
    action_whole=[]
    # Day_matrix=np.array((states,states),dtype = Day)
    Day_matrix=[]
    for i in range(states):
        day_matrix_row = []
        for j in range(states):
            day_matrix_row.append(Day([i,j]))
        Day_matrix.append(day_matrix_row)

    while False in (action_matrix==action_matrix_new):
        #policy evaluation
        action_matrix = action_matrix_new
        deta=float("inf")
        while deta>deta_value:
            for i in range(states):
                for j in range(states):
                    reward_each_state=[]
                    state_location_set,action_set = Day_matrix[i][j].action_generate(  )
                    for state_tmp in range(len(state_location_set)):
                    #under different actions
                        location,return_probability=Day_matrix[i][j].return_generate(state_location_set[state_tmp])

                    # action_tmp_set = np.arange( max( -location2, -5 ),min( 5, location1 ) + 1 )
                    # state_location_set = Day_matrix[i][j].action_generate( location,action_tmp_set )

                        state_location_final,request_satisfied,probability_final = Day_matrix[i][j].request_generate( location,return_probability )

                        reward_each_action=Day_matrix[i][j].reward_calculate(reward_matrix,state_location_final,request_satisfied,probability_final,action_set[state_tmp])
                        reward_each_state.append(reward_each_action)
                    #calculate max reward and action
                    reward_each_state_max=max(reward_each_state)
                    action_each_state_max=[action_set[i] for i,j in enumerate(reward_each_state) if j==reward_each_state_max]

                    #calculate average reward
                    # reward_each_state_average=np.average(reward_each_state)

                    reward_matrix_new[i][j]=reward_each_state_max
                    action_matrix_new[i][j]=action_each_state_max[0]
                    if i==j==0:
                        deta=0
                    deta=max(np.abs(reward_each_state_max-reward_matrix[i][j]),deta)
            reward_matrix = reward_matrix_new
        #policy improvement
        # if action_matrix!=action_matrix_new:
        action_whole.append(action_matrix)



    for i in range(len(action_whole)):
        fig, ax = plt.subplots( 1, 1 )
        ax.pcolor( action_whole[i] )
        plt.show()


    return reward_matrix_new,action_matrix
    # return reward_matrix_new

def generate_matrix(a,b):
    c=[]
    for i in a:
        c_row=[]
        for j in b:
            c_row.append([i,j])
        c.append(c_row)
    return c

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
    reward_matrix_new,action_matrix=Car_Rental_greedy(0.0001,20)






