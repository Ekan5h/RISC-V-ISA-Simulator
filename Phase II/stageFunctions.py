class ProcessingUnit:
	def __init__(self, file_name):
		#Initialize the Processing Unit
		self.RegisterFile = [0 for i in range(32)]
		self.RegisterFile[2]=int('0x7FFFFFF0',0)
		self.RegisterFile[3]=int('0x10000000',0)
		self.MEM = {}
		self.MAR = 0
		self.MDR = 0
		self.RZ = 0
		self.RM = 0
		self.RY = 0
		self.PC = 0
		self.PC_temp = 0
		self.RA = 0
		self.RB = 0
		self.IR = 0
		self.operand1 = 0
		self.operand2 = 0

		self.load_program_memory(file_name)

	def load_program_memory(self, file_name):
		#Loads the program and data memory from the mc file
		try:
			f=open('./'+file_name)
			ins=f.readline().split()
			while ins[1]!='0x00000000':		
				self.MEM[int(ins[0],0)]=int(ins[1][-2:],16)
				self.MEM[int(ins[0],0)+1]=int(ins[1][-4:-2],16)
				self.MEM[int(ins[0],0)+2]=int(ins[1][-6:-4],16)
				self.MEM[int(ins[0],0)+3]=int(ins[1][-8:-6],16)
				ins=f.readline().split()
			self.MEM[int(ins[0],0)]=0
			self.MEM[int(ins[0],0)+1]=0
			self.MEM[int(ins[0],0)+2]=0
			self.MEM[int(ins[0],0)+3]=0
			for l in f:
				if l=='\n':
					continue
				else:
					l=l.split()
					self.MEM[int(l[0],0)]=int(l[1],0)
			
		except FileNotFoundError:
			print("Error opening target code!")
		
	def read(self, address,num_bytes=1):
		#address assumed to be int with base10
		#Insert Check Bounds Here
		#Value returned in Integer Format base10
		val=0
		for i in range(num_bytes):
			adr=address+i
			if adr in self.MEM.keys():
				val=val+self.MEM[adr]*(1<<(8*i))
		return val
			

	def write(self, address,data,num_bytes=1):
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
			self.MEM[adr]=d_in
	
	def IAG(self,offset=4):
		self.PC_temp=self.PC_temp+4
		self.PC=self.PC+offset

	def fetch(self):
		pass


	def decode(self):
		opcode = self.IR&(0x7F)
		#U and UJ format
		if(opcode == 23 or opcode == 55 or opcode == 111):
			pass
		#I format
		elif(opcode == 3 or opcode == 19 or opcode == 103):
			rs1 = self.IR&(0xF8000)
			rs1 = rs1 >> 15
			self.RA = self.RegisterFile[rs1]
		#R S SB format
		else:
			rs1 = self.IR&(0xF8000)
			rs1 = rs1 >> 15
			rs2 = self.IR&(0x1F0000)
			rs2 = rs2 >> 20
			self.RA = self.RegisterFile[rs1]
			self.RB = self.RegisterFile[rs2]

	def execute(self):
		pass

	def memory_access(self):
		#Effective address stored in MAR in integer format
		#Data stored in MDR in Integer Format
		opcode=self.IR&(0x7F)
		funct3=(self.IR>>12)&(0x7)
		if opcode == 3:
			if funct3>=0 and funct3<=3:
				self.MDR=self.read(self.MAR,2**(funct3))
		elif opcode== (8*4+3):
			if funct3>=0 and funct3<=3:
				self.write(self.MAR,self.MDR,2**(funct3))
		#For jal, PC_temp updates RY
		elif opcode == 111:
			self.RY = self.PC_temp
		else:	
			pass

	def write_back(self):
		#Determine whether write back is used
		opcode = self.IR&(0x7F)
		#S and SB check
		if opcode == 35 or opcode == 99:
			pass
		
		rd = self.IR&(0xF80)
		rd = rd/128

		self.RegisterFile[rd] = self.RY
		
		#Update Program Counter
		self.PC += 4

		#Update PC, if jal, jalr, beq, bne, bge, blt
		if(opcode == 111 or opcode == 23 or opcode == 99 or opcode == 103):
			self.PC += self.RY
		
		return





		
		
