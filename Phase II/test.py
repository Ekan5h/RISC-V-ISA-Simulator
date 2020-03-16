from stageFunctions import ProcessingUnit
proc=ProcessingUnit('test.mc')
print(proc.MEM)
while True:

	proc.fetch()
	print(f'{proc.clock} IR={hex(proc.IR)} PC={hex(proc.PC)}')	
	if(proc.IR==0):
		break
	proc.decode()
	proc.execute()
	proc.memory_access()
	proc.write_back()
	
	print(f'{proc.RegisterFile} PC={proc.PC}')

print(proc.MEM)
print(proc.RegisterFile)
