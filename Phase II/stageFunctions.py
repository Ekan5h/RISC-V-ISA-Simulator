R=[0 for i in range(32)]

MEM={}

IR=''
operand1=0
operand2=0

def load_program_memory(file_name):
	try:
		f=open('./'+file_name)
		ins=f.readline().split()
		while ins[1]!='0x00000000':		
			MEM[int(ins[0],0)]=int(ins[1][-2:],16)
			MEM[int(ins[0],0)+1]=int(ins[1][-4:-2],16)
			MEM[int(ins[0],0)+2]=int(ins[1][-6:-4],16)
			MEM[int(ins[0],0)+3]=int(ins[1][-8:-6],16)
			ins=f.readline().split()
		MEM[int(ins[0],0)]=0
		MEM[int(ins[0],0)+1]=0
		MEM[int(ins[0],0)+2]=0
		MEM[int(ins[0],0)+3]=0
	except FileNotFoundError:
		print("Error opening target code!")

load_program_memory('test.mc')

print(MEM)

def read(address):
	#Insert Check Bounds Here
	if address in MEM.keys():
		return MEM[address]
	else:
		return 0
		

def write(address,data):
	#Insert Memory Bounds Here
	#Assuming Byte Addressibility	
	MEM[address]=data
