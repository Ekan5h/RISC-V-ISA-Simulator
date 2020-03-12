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
		for l in f:
			if l=='\n':
				continue
			else:
				l=l.split()
				MEM[int(l[0],0)]=int(l[1],0)
		
	except FileNotFoundError:
		print("Error opening target code!")

load_program_memory('test.mc')

print(MEM)
def fetch():
	pass
def decode():
	pass
def execute():
	pass
def memory_access():
	pass
def write_back():
	pass


def read(address,num_bytes=1):
	#Insert Check Bounds Here
	val=0
	for i in range(num_bytes):
		adr=int(address)+i
		if adr in MEM.keys():
			val=val+MEM[adr]
	return val
		

def write(address,data):
	#Address: Hex value of 32 bits
	#INPUTS:-Data is assumed to be of length , atleast 4 and begin with 0x
	#Insert Memory Bounds Here
	#Assuming Byte Addressibility	
	num_bytes=len(data)/2-1
	for i in range(num_bytes):
		d_in=int(data[i*(-2)-2:i*(-2)],16)
		adr=int(address)+i
		MEM[adr]=d_in

		
		
