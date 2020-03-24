from stageFunctions import ProcessingUnit
f_name=input('Enter the file name for Machine Code : ')
proc=ProcessingUnit(f'{f_name}.mc')
print('Loaded program in Memory!')
while True:
	print(f'Processing Instruction at {hex(proc.PC)}')
	proc.fetch()
	print(f'\tClock={proc.clock} IR={hex(proc.IR)} PC={hex(proc.PC)}')	
	if(proc.IR==0):
		break
	proc.decode()
	proc.execute()
	proc.memory_access()
	proc.write_back()
print(f'Total number of clock cycles used up ={proc.clock}')

print('Final Memory:')
print(proc.MEM)
print('Final Register:')
print(proc.RegisterFile)
