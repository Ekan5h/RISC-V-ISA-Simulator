R=[0 for i in range(32)]

MEM={}
PC=0
MAR=0
MDR=0
IR=0
operand1=0
operand2=0

def load_program_memory(file_name):
	#Loads the program and data memory from the mc file
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

def read(address,num_bytes=1):
	#address assumed to be int with base10
	#Insert Check Bounds Here
	#Value returned in Integer Format base10
	val=0
	for i in range(num_bytes):
		adr=address+i
		if adr in MEM.keys():
			val=val+MEM[adr]*(1<<(8*i))
	return val
		

def write(address,data,num_bytes=1):
	
	#Address: assumed to be of type integer base10
	#INPUTS:-Data is assumed to be of type int base 10
	#Insert Memory Bounds Here
	#Assuming Byte Addressibility	
	#num_bytes=len(data)/2-1
	for i in range(num_bytes):
		#d_in=int(data[i*(-2)-2:i*(-2)],16)
		#adr=int(address)+i
		#MEM[adr]=d_in
		d_in=(data>>(8*i))&(0xFF)
		adr=adr+i
		MEM[adr]=d_in
		

#load_program_memory('test.mc')

#print(MEM)
def fetch():
	pass
def decode():
	pass
def execute():
	pass
def memory_access():
	#Effective address stored in MAR in integer format
	#Data stored in MDR in Integer Format
	opcode=IR&(0x7F)
	funct3=(IR>>12)&(0x7)
	if opcode == 3:
		if funct3>=0 and funct3<=3:
			MDR=read(MAR,2**(funct3))
	elif opcode== (8*4+3):
		if funct3>=0 and funct3<=3:
			write(MAR,MDR,2**(funct3))
	else:	
		pass
def write_back():
	pass



		
		
