class ProcessingUnit:
	def __init__(self, file_name):
		#Initialize the Processing Unit
		self.RegisterFile = [0 for i in range(32)]
		self.clock=0
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
		return self.signExtend(val,num_bytes*8)
			

	def write(self, address,data,num_bytes=1):
		#Address: assumed to be of type integer base10
		#INPUTS:-Data is assumed to be of type int base 10
		#Insert Memory Bounds Here
		#Assuming Byte Addressibility	
		#num_bytes=len(data)/2-1
		adr=address
		for i in range(num_bytes):
			#d_in=int(data[i*(-2)-2:i*(-2)],16)
			#adr=int(address)+i
			#MEM[adr]=d_in
			d_in=(data>>(8*i))&(0xFF)
			self.MEM[adr]=d_in
			print(f'\t\tMemory at {hex(adr)} updated to : {hex(d_in)}')
			adr=adr+1

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
		if opcode==55 or opcode==23:
			imm=(self.IR&(0xfffff000))
			return imm
		return 0
	


	def ALU(self, A, B, ALU_control):
		if ALU_control == 0:										# add
			return self.signExtend(((A + B) & (0xffffffff)), 32)
		if ALU_control == 1:										# and
			return self.signExtend(((A & B) & (0xffffffff)), 32)
		if ALU_control == 2:										# or
			return self.signExtend(((A | B) & (0xffffffff)), 32)
		if ALU_control == 3:										# sll
			B = B & 0xffffffff
			return self.signExtend(((A << B) & (0xffffffff)), 32)
		if ALU_control == 4:										# slt
			return 1 if A < B else 0
		if ALU_control == 5:										# sra
			B = B & 0xffffffff
			return self.signExtend(((A >> B) & (0xffffffff)), 32)
		if ALU_control == 6:										# srl
			B = B & 0xffffffff
			return self.signExtend(((A % 0x100000000) >> B), 32)
		if ALU_control == 7:										# sub
			return self.signExtend(((A - B) & (0xffffffff)), 32)
		if ALU_control == 8:										# xor
			return self.signExtend(((A ^ B) & (0xffffffff)), 32)
		if ALU_control == 9:										# mul
			return self.signExtend(((A * B) & (0xffffffff)), 32)
		
		if ALU_control == 10:										# div
			C = abs(A) // abs(B)
			if A*B < 0:
				C = -C
			return C
			
		if ALU_control == 11:										# rem
			Q = self.ALU(A, B, 10)
			return A - (B * Q)

		if ALU_control == 12:										# beq
			return 1 if A == B else 0
		if ALU_control == 13:										# bne
			return 1 if A != B else 0
		if ALU_control == 14:										# bge
			return 1 if A >= B else 0
		if ALU_control == 15:										# blt
			return 1 if A < B else 0
	
	def IAG(self,offset=4):
		opcode = self.IR&(0x7F)
		self.PC_temp=self.PC+4
		#jalr
		if opcode==103:
			self.PC=offset
		else:
			self.PC=self.PC+offset

	def fetch(self):
		self.IR=self.read(self.PC,4)
		self.clock=self.clock+1

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
			rs2 = self.IR&(0x1F00000)
			rs2 = rs2 >> 20
			self.RA = self.RegisterFile[rs1]
			self.RB = self.RegisterFile[rs2]
			self.RM=self.RB

	def execute(self):
		opcode = self.IR & (0x7F)
		funct3 = (self.IR >> 12) & (0x7)
		muxB_control = 0 if (opcode == 51 or opcode == 99) else 1
		immediate = self.getImmediate()
		if opcode==55:#for lui
			self.operand1=0
		elif opcode==23:#for auipc
			self.operand1=self.PC
		else:
			self.operand1 = self.RA
		self.operand2 = (muxB_control==0)*self.RB + (muxB_control==1)*immediate

		# R-type: add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem
		if opcode == 51:
			funct7 = (self.IR >> 25) & (0x7f)
			ALU_control = (funct3==0)*(funct7==0)*(0) \
				+ (funct3==7)*(funct7==0)*(1) \
				+ (funct3==6)*(funct7==0)*(2) \
				+ (funct3==1)*(funct7==0)*(3) \
				+ (funct3==2)*(funct7==0)*(4) \
				+ (funct3==5)*(funct7==32)*(5) \
				+ (funct3==5)*(funct7==0)*(6) \
				+ (funct3==0)*(funct7==32)*(7) \
				+ (funct3==4)*(funct7==0)*(8) \
				+ (funct3==0)*(funct7==1)*(9) \
				+ (funct3==4)*(funct7==1)*(10) \
				+ (funct3==6)*(funct7==1)*(11)

		# I-type: addi, andi, ori, lb, lh, lw, ld, jalr
		if opcode == 19 or opcode == 3 or opcode == 103:
			if opcode == 19:
				ALU_control = (funct3==0)*(0) + (funct3==7)*(1) + (funct3==6)*(2)
			else:
				ALU_control = 0

		# S-type: sb, sw, sd, sh
		if opcode == 35:
			ALU_control = 0

		# SB-type: beq, bne, bge, blt
		if opcode == 99:
			ALU_control = (funct3==0)*12 + (funct3==1)*13 + (funct3==5)*14 + (funct3==4)*15
		#U-Type: lui auipc
		if opcode==55 or opcode==23:
			ALU_control=0
		if opcode !=111:
			self.RZ = self.ALU(self.operand1, self.operand2, ALU_control)
		else:
			self.RZ=self.PC+4
	def memory_access(self):
		#Effective address stored in MAR in integer format
		#Data stored in MDR in Integer Format
		self.MAR=self.RZ
		self.MDR=self.RM
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
			self.IAG()
			return
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
		#elif opcode==23:
			#self.IAG()
			#self.RY=(self.PC+(self.IR&(0xFFFFF000)))&(0xFFFFFFFF)
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
			if self.RY==1:
				self.IAG(offset)
			else:
				self.IAG()

			return
		#jalr		
		elif opcode==103:
			#assuming jalr puts the offset value in RY
			#print(self.RY)
			self.IAG(self.RY)
			self.RY=self.PC_temp

		else:
			self.IAG()
		rd = self.IR&(0xF80)
		rd = rd//128
		self.RegisterFile[rd] = self.RY
		if(rd!=0):
			print(f'\t\tRegister x{rd} updated to : {hex(self.RY)}')
		self.RegisterFile[0]=0
		return





		
		
