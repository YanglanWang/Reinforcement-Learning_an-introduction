class State:
    def __init__(self,state):
        self.value=0
        self.value_star=0
        self.new_value=0
        self.new_value_star=0
        self.state=state
        self.action_star=[]
        self.up_state=self.state-4
        self.down_state=self.state+4
        self.left_state=self.state-1
        self.right_state=self.state+1
        self.up_reward = -1
        self.down_reward = -1
        self.left_reward = -1
        self.right_reward = -1
        # if self.left_state==0:
        #     self.left_reward=0
        # if self.up_state==0:
        #     self.up_reward=0
        # if self.right_state==0:
        #     self.right_reward=0
        # if self.down_state==0:
        #     self.down_reward=0

        if self.up_state<0:
            # self.up_reward=-1
            self.up_state=self.up_state+4
        # else:
        #     self.up_reward=0
        if self.down_state>15:
            # self.down_reward=-1
            self.down_state=self.down_state-4
        # else:
        #     self.down_reward=0
        if self.left_state in [3,7,11]:
            # self.left_reward=-1
            self.left_state=self.left_state+1
        # else:
        #     self.left_reward=0
        if self.right_state in [4,8,12]:
            # self.right_reward=-1
            self.right_state=self.right_state-1
        if self.state==13:
            self.down_state=16
        if self.state==16:
            self.up_state=13
            self.left_state=12
            self.right_state=14
            self.down_state=16
        # else:
        #     self.right_reward=0

        # if self.state==1:
        #     self.up_state = 21
        #     self.down_state = 21
        #     self.left_state = 21
        #     self.right_state = 21
        #     self.up_reward=10
        #     self.down_reward=10
        #     self.left_reward=10
        #     self.right_reward=10
        # if self.state==3:
        #     self.up_state = 13
        #     self.down_state = 13
        #     self.left_state = 13
        #     self.right_state = 13
        #     self.up_reward=5
        #     self.down_reward=5
        #     self.left_reward=5
        #     self.right_reward=5

        # self.down=down
        # self.left=left
        # self.right=right
        # self.state=state
        # self.reward=reward
        # self.id=id
    def update_v( self ,state_set):
        gama = 1
        self.new_value=0.25*(state_set[self.up_state].value*gama+self.up_reward+state_set[self.down_state].value*gama+self.down_reward+state_set[self.left_state].value*gama+self.left_reward+state_set[self.right_state].value*gama+self.right_reward)
    def update_v_star( self,state_set):
        gama=1
        g_set=[]
        g_set.append(state_set[self.up_state].value_star*gama+self.up_reward)

        g_set.append(state_set[self.down_state].value_star*gama+self.down_reward)
        g_set.append(state_set[self.left_state].value_star*gama+self.left_reward)
        g_set.append(state_set[self.right_state].value_star*gama+self.right_reward)
        self.action_star=[i for i,j in enumerate(g_set) if j==max(g_set)]

        self.new_value_star=max(g_set)

def Gridworld(n,size):
    state_set=[]
    for i in range(size[0]*size[1]+1):
        state_set.append( State(i ) )

    for time in range(n):
        for i in range(1,size[0]*size[1]-1):
            state_set[i].update_v(state_set)
            state_set[i].update_v_star(state_set)
        state_set[16].update_v(state_set)
        state_set[16].update_v_star(state_set)
        for i in range(1,size[0]*size[1]-1):
            state_set[i].value=state_set[i].new_value
        # for i in range(1,size[0]*size[1]-1):
            state_set[i].value_star=state_set[i].new_value_star
        state_set[16].value = state_set[i].new_value
        state_set[16].value_star = state_set[i].new_value_star

    for i in range(size[0]*size[1]+1):
        print(str(state_set[i].new_value)+' ',end='')
        if i%4==3:
            print('\n')
    for i in range(size[0]*size[1]+1):
        print(str(state_set[i].value_star)+','+str(state_set[i].action_star)+" ",end='')

        if i%4==3:
            print('\n')


if __name__=='__main__':
    Gridworld(100,[4,4])




