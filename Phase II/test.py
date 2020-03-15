from stageFunctions import ProcessingUnit
proc=ProcessingUnit('test.mc')

while True:
	print(f'{proc.clock} IR={hex(proc.IR)}')
	proc.fetch()
	if(proc.IR==0):
		break
	proc.decode()
	proc.execute()
	proc.memory_access()
	proc.write_back()

print(proc.MEM)
print(proc.RegisterFile)
