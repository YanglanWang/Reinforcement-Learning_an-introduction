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

    def action_generate( self,action):
        # state_location=[self.state_location[0]-action[0],self.state_location[1]+action[0]]
        state_location=self.state_location-action*np.array([1,-1])
        # else:
        #     action_set_deal=np.array(action_set)
        #     state_location=self.state_location-action_set_deal.reshape(action_set.shape[0],-1)*np.ones((1,2))
        return state_location

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
    action_matrix=np.ones((states,states))
    action_matrix_new=np.zeros((states,states))

    action_whole=[]
    # Day_matrix=np.array((states,states),dtype = Day)
    Day_matrix=[]
    for i in range(states):
        day_matrix_row = []
        for j in range(states):
            day_matrix_row.append(Day([i,j]))
        Day_matrix.append(day_matrix_row)

    while False in (action_matrix==action_matrix_new):

        # action_matrix = action_matrix_new
        for i in range(len(action_matrix_new)):
            for j in range(len(action_matrix_new[i])):
                action_matrix[i][j]=action_matrix_new[i][j]


        #policy evaluation
        deta=float("inf")
        while deta>deta_value:
            for i in range(states):
                for j in range(states):
                    reward_each_state=[]
                    state_location = Day_matrix[i][j].action_generate( action_matrix[i][j] )
                    # for state_tmp in range(len(state_location_set)):
                    location,return_probability=Day_matrix[i][j].return_generate(state_location)

                    # action_tmp_set = np.arange( max( -location2, -5 ),min( 5, location1 ) + 1 )
                    # state_location_set = Day_matrix[i][j].action_generate( location,action_tmp_set )

                    state_location_final,request_satisfied,probability_final = Day_matrix[i][j].request_generate( location,return_probability )

                    reward_each_action=Day_matrix[i][j].reward_calculate(reward_matrix,state_location_final,request_satisfied,probability_final,action_matrix[i][j])


                    # reward_matrix_new[i][j]=reward_each_action
                    reward_matrix[i][j]=reward_each_action

                    # action_matrix_new[i][j]=action_each_state_max[0]
                    if i==j==0:
                        deta=0
                    deta=max(np.abs(reward_each_action-reward_matrix[i][j]),deta)
            # reward_matrix = reward_matrix_new

            # for i in range(len(reward_matrix_new)):
            #     for j in range(len(reward_matrix_new[i])):
            #         reward_matrix[i][j]=reward_matrix_new[i][j]

        #policy improvement
        for i in range( states ):
            for j in range( states ):
                reward_each_state = []
                action_set = np.arange( max( -j, -5 ), min( 5, i ) + 1 )
                for action in action_set:

                    state_location = Day_matrix[i][j].action_generate(action)
                    # for state_tmp in range(len(state_location_set)):
                    location, return_probability = Day_matrix[i][j].return_generate( state_location )

                    # action_tmp_set = np.arange( max( -location2, -5 ),min( 5, location1 ) + 1 )
                    # state_location_set = Day_matrix[i][j].action_generate( location,action_tmp_set )

                    state_location_final, request_satisfied, probability_final = Day_matrix[i][j].request_generate(
                        location, return_probability )

                    reward_each_action = Day_matrix[i][j].reward_calculate( reward_matrix, state_location_final,
                                                                            request_satisfied, probability_final,
                                                                            action_matrix[i][j] )
                    reward_each_state.append( reward_each_action )
                    # reward_matrix_new[i][j]=reward_each_state_max

                reward_each_state_max = max( reward_each_state )
                action_each_state_max = [action_set[i] for i, j in enumerate( reward_each_state ) if
                                         j == reward_each_state_max]
                # reward_matrix_new[i][j] = reward_each_action
                action_matrix_new[i][j] = action_each_state_max[0]

        # if action_matrix!=action_matrix_new:
        action_whole.append(action_matrix_new)



    for i in range(len(action_whole)):
        fig, ax = plt.subplots( 1, 1 )
        ax.pcolor( action_whole[i] )
        plt.show()


    return reward_matrix,action_matrix
    # return reward_matrix_new

def generate_matrix(a,b):
    c=[]
    for i in a:
        c_row=[]
        for j in b:
            c_row.append([i,j])
        c.append(c_row)
    return c




if __name__=="__main__":
    # reward_matrix_new=Car_Rental_average(50,20)
    reward_matrix_new,action_matrix=Car_Rental_greedy(0.0001,20)






