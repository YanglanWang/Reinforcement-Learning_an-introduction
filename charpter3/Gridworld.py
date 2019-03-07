class State:
    def __init__(self,state):
        self.value=0
        self.state=state
        self.action_star=[]
        self.up_state=self.state-5
        self.down_state=self.state+5
        self.left_state=self.state-1
        self.right_state=self.state+1
        if self.up_state<0:
            self.up_reward=-1
            self.up_state=self.up_state+5
        else:
            self.up_reward=0
        if self.down_state>24:
            self.down_reward=-1
            self.down_state=self.down_state-5
        else:
            self.down_reward=0
        if self.left_state in [-1,4,9,14,19]:
            self.left_reward=-1
            self.left_state=self.left_state+1
        else:
            self.left_reward=0
        if self.right_state in [5,10,15,20,25]:
            self.right_reward=-1
            self.right_state=self.right_state-1
        else:
            self.right_reward=0

        if self.state==1:
            self.up_state = 21
            self.down_state = 21
            self.left_state = 21
            self.right_state = 21
            self.up_reward=10
            self.down_reward=10
            self.left_reward=10
            self.right_reward=10
        if self.state==3:
            self.up_state = 13
            self.down_state = 13
            self.left_state = 13
            self.right_state = 13
            self.up_reward=5
            self.down_reward=5
            self.left_reward=5
            self.right_reward=5

        # self.down=down
        # self.left=left
        # self.right=right
        # self.state=state
        # self.reward=reward
        # self.id=id
    def update_v( self ,state_set):
        gama = 0.9
        value_tmp=0
        self.value=0.25*(state_set[self.up_state].value*gama+self.up_reward+state_set[self.down_state].value*gama+self.down_reward+state_set[self.left_state].value*gama+self.left_reward+state_set[self.right_state].value*gama+self.right_reward)
        # for k in range(len(self.surrounding)):
        #     if self.id==1 and self.surrounding[k].id==21:
        #         value_tmp = value_tmp + 0.25 * (self.surrounding[k].value * gama + self.surrounding[k].reward)
        #     else:
        #         value_tmp=value_tmp+0.25*(self.surrounding[k].value*gama+self.surrounding[k].reward)
        # if k == 1:
        #     self.value=value_tmp+0.25*(-2+2*self.value*gama)
        # elif k==2:
        #     self.value=value_tmp+0.25*(-1+self.value*gama)
        # else:
        #     self.value=value_tmp


def Gridworld(n,size):
    state_set=[]
    for i in range(size[0]*size[1]):
        state_set.append( State(i ) )

    for time in range(n):
        for i in range(size[0]*size[1]):
            state_set[i].update_v(state_set)

    for i in range(size[0]*size[1]):
        print(str(state_set[i].value)+' ',end='')
        if i%5==4:
            print('\n')


if __name__=='__main__':
    Gridworld(100,[5,5])




