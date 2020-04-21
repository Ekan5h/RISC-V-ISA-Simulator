from stageFunctions import State
class HDU:
    def __init__(self):
        # self.states=[]
        # self.is_control_hazard=[False,-1] #[bool,no. of stalls]
        # self.is_data_hazard=[False,-1]
        pass

    def check_data_hazard(self,states):
        new_states = []     # updated states
        new_states = [states[0]]
        toDecode = states[1]
        toExecute = states[2]
        toMem = states[3]
        toWB = states[4]
        isHazard = False    # is there a data hazard?
        doStall = False     # do we need to stall in case of data forwarding?
        stallWhere = 3      # stall at the decode stage or execute stage?
                            # 1 = at execute, 2 = at decode, 3 = don't stall
                            # Sorted according to priority

        toDecode_opcode = toDecode.IR & (0x7F)
        toExecute_opcode = toExecute.IR & (0x7F)
        toMem_opcode = toMem.IR & (0x7F)
        toWB_opcode = toWB.IR & (0x7F)
        
        # M->E and M->M forwarding before E->E forwarding, because E->E forward takes  
        # precedence over the other two, and should have the capacity to overwrite

        # M->M forwarding
        # if (toWB_opcode==3 or toWB_opcode==55) and toMem_opcode==35:
        if (toWB_opcode==3) and toMem_opcode==35:
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
            # if toMem_opcode == 3 or toMem_opcode == 55:
            if toMem_opcode == 3:

                # If the consumer is a store instruction
                if toExecute_opcode == 35:

                    # Stall required for address calculation of store instruction
                    if toExecute.rs1 == toMem.rd:
                        isHazard = True
                        doStall = True
                        stallWhere = min(stallWhere, 1)
                    
                # If the consumer isn't a store instruction, a stall is needed
                else:
                    isHazard = True
                    doStall = True
                    stallWhere = min(stallWhere, 1)

            # If the producer isn't a load instruction, perform E->E data forwarding
            else:
                if toExecute.rs1 == toMem.rd:
                    toExecute.RA = toMem.RZ
                    isHazard = True

                if toExecute.rs2 == toMem.rd:
                    toExecute.RB = toMem.RZ
                    isHazard = True

        # Control hazard forwarding
        # Again, we go in reverse order to allow recent instructions to overwrite
        if toDecode_opcode == 99 or toDecode_opcode == 103:

            # M->D forwarding
            if toWB.rd > 0:
                if toWB.rd == toDecode.rs1:
                    toDecode.rs1branch = toWB.RY
                    isHazard = True
                if toWB.rd == toDecode.rs2:
                    toDecode.rs2branch = toWB.RY
                    isHazard = True

            # E->D fowarding
            if toMem.rd > 0:

                # If producer is a load instruction, result won't be available for another cycle
                if toMem_opcode == 3:
                    isHazard = True
                    doStall = True
                    stallWhere = min(stallWhere, 2)

                else:
                    if toMem.rd == toDecode.rs1:
                        toDecode.rs1branch = toMem.RZ
                        # print("HEyO", toDecode.rs1branch)
                        isHazard = True
                    if toMem.rd == toDecode.rs2:
                        toDecode.rs2branch = toMem.RZ
                        isHazard = True

            # If branch depends upon the preceding instruction, stall required
            if toExecute.rd > 0 and (toExecute.rd == toDecode.rs1 or toExecute.rd == toDecode.rs2):
                isHazard = True
                doStall = True
                stallWhere = min(stallWhere, 2)
            

        new_states = new_states + [toDecode, toExecute, toMem, toWB]
        return [isHazard, doStall, new_states, stallWhere]

    def check_data_hazard_stalling(self,states):
        states=states[1:] #removed the fetch stage instruction
        if len(states)==1:
            return [False,-1]
        elif len(states)>=2:
            exe_state=states[1]
            decode_state=states[0]
            if exe_state.rd!=-1 and decode_state.rs1!=-1:
                if exe_state.rd==decode_state.rs1 :
                    if exe_state.rd!=0:
                        return [True,2]
                if exe_state.rd==decode_state.rs2:
                    if exe_state.rd!=0:
                        return [True,2]
            if len(states)>=3:
                mem_state=states[2]
                if mem_state.rd!=-1 and decode_state.rs1!=-1:
                    if mem_state.rd==decode_state.rs1 :
                        if mem_state.rd!=0:
                            return [True,1]
                    if mem_state.rd==decode_state.rs2:
                        if mem_state.rd!=0:
                            return [True,1]
        
        return [False,-1]



    def check_control_hazard(self):
        pass
        #return is_data_hazard

    # def add_new_state(self,new_state):
    #     self.states.append(new_state)
    #     if len(self.states)>=5:
    #         self.states=self.states[-5:]

    #     self.check_data_hazard()
    #     self.check_control_hazard()