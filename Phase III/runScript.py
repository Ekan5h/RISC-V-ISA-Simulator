from stageFunctions import ProcessingUnit, State
from hazard import HDU
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
stalling_enabled=True
hdu=HDU()
while True:
	# print(f'Processing Instruction at {hex(state.PC)}')
	# IF_ID = proc.fetch(state)
	# # print(f'\tClock={state.clock} IR={hex(state.IR)} PC={hex(state.PC)}')	
	# if(state.IR==0):
	# 	break
	# ID_EX = proc.decode(IF_ID)
	# EX_MEM = proc.execute(ID_EX)
	# MEM_WB = proc.memory_access(EX_MEM)
	# state = proc.write_back(MEM_WB)_

	data_hazard=hdu.check_data_hazard(in_states)
	backup_states=in_states
	print(f'Cycle={master_clock} Hazard={data_hazard} PC={master_PC}')
	# if data_hazard[0]==True :
		# out_states=out_states[1:] #removed the output of fetch state
		# in_states.append(out_states[0]) 
		# in_states.append(State())# inserted a buuble for execute state
		# in_states=in_states+out_states[1:]
	in_states=[(idx,val) for idx,val in enumerate(in_states)]
	reversed_states=in_states[::-1]
	for idx,state in reversed_states:
		if idx==0:
			out_states.append(proc.fetch(state))
		if idx==1:
			temphazard,newpc,tempstate = proc.decode(state)
			out_states.append(tempstate)
			if temphazard and newpc:
				master_PC = newpc
				out_states[0].IR = 0
				out_states[0].rs1 = 0
				out_states[0].rs2 = 0
				out_states[0].rd = 0;
		if idx==2:
			out_states.append(proc.execute(state))
		if idx==3:
			out_states.append(proc.memory_access(state))
		if idx==4:
			progress=proc.write_back(state)
	out_states=out_states[::-1]
	if stalling_enabled:
		if out_states[0].IR!=0 and (data_hazard[0]==False):
			master_PC +=4
	else:
		if out_states[0].IR!=0:
			master_PC+=4
	if data_hazard[0]==True and stalling_enabled:
		out_states=[backup_states[1],State(0)]+out_states[2:]
	master_clock +=1
	if out_states[0].IR==0 and out_states[1].IR==0 and out_states[2].IR==0 and out_states[3].IR==0 and progress=="Completed":
		break

	in_states=[State(master_PC)]
	in_states=in_states+out_states
	out_states=[]


print(f'Total number of clock cycles used up ={master_clock}')

print('Final Memory:')
print(proc.MEM)
print('Final Register:')
print(proc.RegisterFile)
