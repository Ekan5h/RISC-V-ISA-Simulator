from stageFunctions import State
class HDU:
    def __init__(self):
        # self.states=[]
        # self.is_control_hazard=[False,-1] #[bool,no. of stalls]
        # self.is_data_hazard=[False,-1]
        pass

    def check_data_hazard(self,states):
        new_states = []     # updated states
        new_states = [states[0], states[1]]
        toExecute = states[2]
        toMem = states[3]
        toWB = states[4]
        isHazard = False    # is there a data hazard?
        doStall = False     # do we need to stall in case of data forwarding?

        toExecute_opcode = toExecute.IR & (0x7F)
        toMem_opcode = toMem.IR & (0x7F)
        toWB_opcode = toWB.IR & (0x7F)
        
        # M->E and M->M forwarding before E->E forwarding, because E->E forward takes  
        # precedence over the other two, and should have the capacity to overwrite

        # M->M forwarding
        if (toWB_opcode==3 or toWB_opcode==55) and toMem_opcode==35:
            if toWB.rd > 0 and toWB.rd == toMem.rs2:
                toMem.RB = toWB.RY
                isHazard = True

        # M->E forwarding
        if toWB.rd > 0:
            if toWB.rd == toExecute.rs1:
                toExecute.RA = toWB.RY
                isHazard = True

            if toWB.rd == toExecute.rs2:
                toExecute.RB = toWB.RY
                isHazard = True

        # E->E forwarding
        if toMem.rd > 0:

            # If the producer is a load instruction
            if toMem_opcode == 3 or toMem_opcode == 55:

                # If the consumer is a store instruction
                if toExecute_opcode == 35:

                    # Stall required for address calculation of store instruction
                    if toExecute.rs1 == toMem.rd:
                        isHazard = True
                        doStall = True
                    
                # If the consumer isn't a store instruction, a stall is needed
                else:
                    isHazard = True
                    doStall = True

            # If the producer isn't a load instruction, perform E->E data forwarding
            else:
                if toExecute.rs1 == toMem.rd:
                    toExecute.RA = toMem.RZ
                    isHazard = True

                if toExecute.rs2 == toMem.rd:
                    toExecute.RB = toMem.RZ
                    isHazard = True

        new_states = new_states + [toExecute, toMem, toWB]
        return [isHazard, doStall, new_states]


    def check_control_hazard(self):
        pass
        #return is_data_hazard

    # def add_new_state(self,new_state):
    #     self.states.append(new_state)
    #     if len(self.states)>=5:
    #         self.states=self.states[-5:]

    #     self.check_data_hazard()
    #     self.check_control_hazard()