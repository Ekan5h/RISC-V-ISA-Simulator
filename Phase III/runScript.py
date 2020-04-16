from stageFunctions import ProcessingUnit, State
import sys
if len(sys.argv)==2:
	f_name=sys.argv[1]
else:
	raise Exception('Inavlid Arguments')
proc=ProcessingUnit(f'{f_name}')
state = State()
print('Loaded program in Memory!')
while True:
	print(f'Processing Instruction at {hex(state.PC)}')
	state = proc.fetch(state)
	print(f'\tClock={state.clock} IR={hex(state.IR)} PC={hex(state.PC)}')	
	if(state.IR==0):
		break
	state = proc.decode(state)
	state = proc.execute(state)
	state = proc.memory_access(state)
	state = proc.write_back(state)
print(f'Total number of clock cycles used up ={state.clock}')

print('Final Memory:')
print(proc.MEM)
print('Final Register:')
print(proc.RegisterFile)
