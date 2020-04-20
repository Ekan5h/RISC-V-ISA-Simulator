from stageFunctions import State
class HDU:
    def __init__(self):
        # self.states=[]
        # self.is_control_hazard=[False,-1] #[bool,no. of stalls]
        # self.is_data_hazard=[False,-1]
        pass
    def check_data_hazard(self,states):
        states=states[1:] #removed the fetch stage instruction
        if len(states)==1:
            return [False,-1]
        elif len(states)>=2:
            exe_state=states[1]
            decode_state=states[0]
            if exe_state.rd!=-1 and decode_state.rs1!=-1:
                if exe_state.rd==decode_state.rs1 or exe_state.rd==decode_state.rs2:
                    return [True,2]
            if len(states)>=3:
                mem_state=states[2]
                if mem_state.rd!=-1 and decode_state.rs1!=-1:
                    if mem_state.rd==decode_state.rs1 or mem_state.rd==decode_state.rs2:
                        return [True,1]
        
        return [False,-1]

        #return is_control_hazard

    def check_control_hazard(self):
        pass
        #return is_data_hazard

    # def add_new_state(self,new_state):
    #     self.states.append(new_state)
    #     if len(self.states)>=5:
    #         self.states=self.states[-5:]

    #     self.check_data_hazard()
    #     self.check_control_hazard()