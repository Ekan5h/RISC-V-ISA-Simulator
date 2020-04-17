from stageFunctions import ProcessingUnit, State
import sys
if len(sys.argv)==2:
	f_name=sys.argv[1]
else:
	raise Exception('Inavlid Arguments')
proc=ProcessingUnit(f'{f_name}')
in_states=[State() for i in range(5)]
out_states=[]

# States
# fetch_inp=State()
# decode_inp = State()
# execute_inp = State()
# ma_inp = State()
# wb_inp = State()

print('Loaded program in Memory!')
master_PC=0
master_clock=0

while True:
	# print(f'Processing Instruction at {hex(state.PC)}')
	# IF_ID = proc.fetch(state)
	# # print(f'\tClock={state.clock} IR={hex(state.IR)} PC={hex(state.PC)}')	
	# if(state.IR==0):
	# 	break
	# ID_EX = proc.decode(IF_ID)
	# EX_MEM = proc.execute(ID_EX)
	# MEM_WB = proc.memory_access(EX_MEM)
	# state = proc.write_back(MEM_WB)
	for idx,state in enumerate(in_states):
		if idx==0:
			out_states.append(proc.fetch(state))
		if idx==1:
			out_states.append(proc.decode(state))
		if idx==2:
			out_states.append(proc.execute(state))
		if idx==3:
			out_states.append(proc.memory_access(state))
		if idx==4:
			progress=proc.write_back(state)
	if out_states[0].IR!=0:
		master_PC +=4
	master_clock +=1
	if out_states[0].IR==0 and progress=="Completed":
		break
	in_states=[State(master_PC)]
	in_states=in_states+out_states
	out_states=[]


print(f'Total number of clock cycles used up ={master_clock}')

print('Final Memory:')
print(proc.MEM)
print('Final Register:')
print(proc.RegisterFile)
