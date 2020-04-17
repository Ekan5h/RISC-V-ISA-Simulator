from stageFunctions import ProcessingUnit, State
import sys
if len(sys.argv)==2:
	f_name=sys.argv[1]
else:
	raise Exception('Inavlid Arguments')
proc=ProcessingUnit(f'{f_name}')
in_states=[]
out_states=[]

# States
state = State()
IF_ID = State()
ID_EX = State()
EX_MEM = State()
MEM_WB = State()

print('Loaded program in Memory!')
while True:
	print(f'Processing Instruction at {hex(state.PC)}')
	IF_ID = proc.fetch(state)
	print(f'\tClock={state.clock} IR={hex(state.IR)} PC={hex(state.PC)}')	
	if(state.IR==0):
		break
	ID_EX = proc.decode(IF_ID)
	EX_MEM = proc.execute(ID_EX)
	MEM_WB = proc.memory_access(EX_MEM)
	state = proc.write_back(MEM_WB)
	
print(f'Total number of clock cycles used up ={state.clock}')

print('Final Memory:')
print(proc.MEM)
print('Final Register:')
print(proc.RegisterFile)
