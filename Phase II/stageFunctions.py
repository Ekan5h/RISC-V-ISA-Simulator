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
		

	def signExtend(self, num, num_bits):
		sign_bit = 1 << (num_bits - 1)
		ans = (num & (sign_bit - 1)) - (num & sign_bit)
		return ans

	def getImmediate(self):
		opcode = self.IR & (0x7F)

		# I-type
		if opcode == 19 or opcode == 3 or opcode == 103:
			return self.signExtend(((self.IR >> 20) & (0xfffff)), 12)

		# S-type
		if opcode == 35:
			imm11to5 = ((self.IR >> 25) & (0x7f)) << 5
			imm4t0 = (self.IR >> 7) & (0x1f)
			return self.signExtend((imm11to5 + imm4t0), 12)

		# SB-type
		if opcode == 99:
			imm12 = ((self.IR >> 31) & (0x1)) << 12
			imm10to5 = ((self.IR >> 25) & (0x3f)) << 5
			imm4to1 = ((self.IR >> 8) & (0xf)) << 1
			imm11 = ((self.IR >> 7) & (0x1)) << 11
			return self.signExtend((imm12 + imm10to5 + imm4to1 + imm11), 13)

		# Add for U and UJ-type
		return 0
	
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

	def ALU(self, A, B, ALU_control):
		if ALU_control == 0:										# add
			return self.signExtend(((A + B) & (0xffffffff)), 32)
		if ALU_control == 1:										# and
			return self.signExtend(((A & B) & (0xffffffff)), 32)
		if ALU_control == 2:										# or
			return self.signExtend(((A | B) & (0xffffffff)), 32)
		if ALU_control == 3:										# sll
			return self.signExtend(((A << B) & (0xffffffff)), 32)
		if ALU_control == 4:										# slt
			return 1 if A < B else 0
		if ALU_control == 5:										# sra
			return self.signExtend(((A >> B) & (0xffffffff)), 32)
		if ALU_control == 6:										# srl
			return self.signExtend(((A % 0x100000000) >> B), 32)
		if ALU_control == 7:										# sub
			return self.signExtend(((A - B) & (0xffffffff)), 32)
		if ALU_control == 8:										# xor
			return self.signExtend(((A ^ B) & (0xffffffff)), 32)
		if ALU_control == 9:										# mul
			return self.signExtend(((A * B) & (0xffffffff)), 32)
		if ALU_control == 10:										# div
			return 0
		# 	return self.signExtend(((A ^ B) & (0xffffffff)), 32)
		if ALU_control == 11:										# rem
			return 0
		# 	return self.signExtend(((A ^ B) & (0xffffffff)), 32)
		if ALU_control == 12:										# beq
			return 1 if A == B else 0
		if ALU_control == 13:										# bne
			return 1 if A != B else 0
		if ALU_control == 14:										# bge
			return 1 if A >= B else 0
		if ALU_control == 15:										# blt
			return 1 if A < B else 0
	
	def IAG(self,offset=4):
		self.PC_temp=self.PC_temp+4
		self.PC=self.PC+offset

	def fetch(self):
		self.IR=self.read(self.PC,4)

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
				self.RY=self.MDR
		elif opcode== (8*4+3):
			if funct3>=0 and funct3<=3:
				self.write(self.MAR,self.MDR,2**(funct3))
		else:
			self.RY=self.RZ

	def write_back(self):
		#Determine whether write back is used
		opcode = self.IR&(0x7F)
		#S Check
		if opcode == 35:
			pass
		#jal
		elif opcode==111:
			#Extract the immediate field and generate the offset
			immed_20=str((self.IR&0x80000000)>>31)
			immed_19_12=bin((self.IR&(0x000ff000))>>12)[2:]
			immed_19_12='0'*(8-len(immed_19_12))+immed_19_12
			immed_11=str((self.IR&(0x00100000))>>20)
			immed_10_1=bin((self.IR&(0x7fe00000))>>21)[2:]
			immed_10_1='0'*(10-len(immed_10_1))+immed_10_1
			immediate=immed_20*12+immed_19_12+immed_11+immed_10_1+'0'
			offset=int(immediate,2)
			if immediate[0]=='1':
				offset^=0xFFFFFFFF
				offset+=1
				offset=-offset
			#pass the offset to IAG 
			self.IAG(offset)
			#set the self.RY to PC_temp
			self.RY=self.PC_temp
		#Handle AUIPC
		elif opcode==23:
			self.IAG()
			self.RY=self.PC+(self.IR&(0xFFFFF000))
		#SB		
		elif opcode == 99 :
			offset = 0
			
			#Immediate Field Distribution
			# Array:    [31] [30-25] [11-8] [7]
			# ImmField:  12   10:5     4:1   11
			# Shifts:    R19  R20      R7    L4

			offset += (self.IR&(0x80)) << 4
			offset += (self.IR&(0xF00)) >> 7
			offset += (self.IR&(0x7E000000)) >> 20

			#Working with sign bit
			if(self.IR&(0x80000000) == 0x80000000):
				offset = offset ^ 0xFFF
				offset += 1
				offset = -1 * offset

			self.IAG(offset)
		#jalr		
		elif opcode==103:
			#assuming jalr puts the offset value in RY
			self.IAG(self.RY)
			self.RY=self.PC_temp
		else:
			self.IAG()
		rd = self.IR&(0xF80)
		rd = rd/128
		self.RegisterFile[rd] = self.RY
		return





		
		
