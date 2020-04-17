from stageFunctions import State
class HDU:
    def __init__(self):
        self.states=[]
        self.is_control_hazard=[False,-1] #[bool,state_no.]
        self.is_data_hazard=[False,-1]
        
    def check_data_hazard(self):
        pass
        #return is_control_hazard

    def check_control_hazard(self):
        pass
        #return is_data_hazard

    def add_new_state(self,new_state):
        self.states.append(new_state)
        if len(self.states)>=5:
            self.states=self.states[1:]

        self.check_data_hazard()
        self.check_control_hazard()