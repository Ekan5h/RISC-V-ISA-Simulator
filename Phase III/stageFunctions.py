class State:
	def __init__(self):
		#Initialize to state at t=0
		self.reset_interRegisters()
		self.clock=0

	def update_clock(self):
		self.clock = self.clock + 1

	def reset_interRegisters(self):
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


class ProcessingUnit:
	def __init__(self, file_name):
		self.MEM = {}
		self.RegisterFile = [0 for i in range(32)]
		self.RegisterFile[2]=int('0x7FFFFFF0',0)
		self.RegisterFile[3]=int('0x10000000',0)
		self._load_program_memory(file_name)

	def _load_program_memory(self, file_name):
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
		
	def _read(self, address,num_bytes=1):
		#address assumed to be int with base10
		#Insert Check Bounds Here
		#Value returned in Integer Format base10
		val=0
		for i in range(num_bytes):
			adr=address+i
			if adr in self.MEM.keys():
				val=val+self.MEM[adr]*(1<<(8*i))
		return self._signExtend(val,num_bytes*8)
			

	def _write(self, address,data,num_bytes=1):
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

	def _signExtend(self, num, num_bits):
		sign_bit = 1 << (num_bits - 1)
		ans = (num & (sign_bit - 1)) - (num & sign_bit)
		return ans

	def _get_opcode(self, IR):
		opcode = IR & (0x7F)
		return opcode

	def _get_funct3(self, IR):
		funct3 = (IR >> 12) & (0x7)
		return funct3

	def _getImmediate(self, IR):
		opcode = self._get_opcode(IR)

		# I-type
		if opcode == 19 or opcode == 3 or opcode == 103:
			return self._signExtend(((IR >> 20) & (0xfffff)), 12)

		# S-type
		if opcode == 35:
			imm11to5 = ((IR >> 25) & (0x7f)) << 5
			imm4t0 = (IR >> 7) & (0x1f)
			return self._signExtend((imm11to5 + imm4t0), 12)

		# SB-type
		if opcode == 99:
			# imm12 = ((self.IR >> 31) & (0x1)) << 12
			# imm10to5 = ((self.IR >> 25) & (0x3f)) << 5
			# imm4to1 = ((self.IR >> 8) & (0xf)) << 1
			# imm11 = ((self.IR >> 7) & (0x1)) << 11
			# return self._signExtend((imm12 + imm10to5 + imm4to1 + imm11), 13)
			offset=0
			offset += (IR&(0x80)) << 4
			offset += (IR&(0xF00)) >> 7
			offset += (IR&(0x7E000000)) >> 20

			#Working with sign bit
			if(IR&(0x80000000) == 0x80000000):
				offset = offset ^ 0xFFF
				offset += 1
				offset = -1 * offset
			return offset

		# Add for U and UJ-type
		if opcode==55 or opcode==23:
			imm=(IR&(0xfffff000))
			return imm
		#jal
		if opcode==111:
			immed_20=str((IR&0x80000000)>>31)
			immed_19_12=bin((IR&(0x000ff000))>>12)[2:]
			immed_19_12='0'*(8-len(immed_19_12))+immed_19_12
			immed_11=str((IR&(0x00100000))>>20)
			immed_10_1=bin((IR&(0x7fe00000))>>21)[2:]
			immed_10_1='0'*(10-len(immed_10_1))+immed_10_1
			immediate=immed_20*12+immed_19_12+immed_11+immed_10_1+'0'
			offset=int(immediate,2)
			if immediate[0]=='1':
				offset^=0xFFFFFFFF
				offset+=1
				offset=-offset
			return offset
		return 0
	


	def ALU(self, A, B, ALU_control):
		if ALU_control == 0:										# add
			return self._signExtend(((A + B) & (0xffffffff)), 32)
		if ALU_control == 1:										# and
			return self._signExtend(((A & B) & (0xffffffff)), 32)
		if ALU_control == 2:										# or
			return self._signExtend(((A | B) & (0xffffffff)), 32)
		if ALU_control == 3:										# sll
			B = B & 0xffffffff
			return self._signExtend(((A << B) & (0xffffffff)), 32)
		if ALU_control == 4:										# slt
			return 1 if A < B else 0
		if ALU_control == 5:										# sra
			B = B & 0xffffffff
			return self._signExtend(((A >> B) & (0xffffffff)), 32)
		if ALU_control == 6:										# srl
			B = B & 0xffffffff
			return self._signExtend(((A % 0x100000000) >> B), 32)
		if ALU_control == 7:										# sub
			return self._signExtend(((A - B) & (0xffffffff)), 32)
		if ALU_control == 8:										# xor
			return self._signExtend(((A ^ B) & (0xffffffff)), 32)
		if ALU_control == 9:										# mul
			return self._signExtend(((A * B) & (0xffffffff)), 32)
		
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
	
	def IAG(self, state):
		opcode = self._get_opcode(state.IR)
		#self.PC_temp=self.PC+4
		#jal
		if opcode==111:
			immed=self._getImmediate(state.IR)
			state.PC=state.PC+immed
			return
		#SB
		if opcode==99:
			immed=self._getImmediate(state.IR)
			if state.RY==1:
				state.PC=state.PC+immed
			else:
				state.PC=state.PC+4
			return
		#jalr
		if opcode==103:
			state.PC=state.RY
			return
		
		state.PC=state.PC+4

		return state

	def fetch(self, state):
		state.IR=self._read(state.PC,4)
		state.clock=state.clock+1
		state.PC_temp=state.PC+4

		return state

	def decode(self, state):
		opcode = self._get_opcode(state.IR)
		#U and UJ format
		if(opcode == 23 or opcode == 55 or opcode == 111):
			pass
		#I format
		elif(opcode == 3 or opcode == 19 or opcode == 103):
			rs1 = state.IR&(0xF8000)
			rs1 = rs1 >> 15
			state.RA = self.RegisterFile[rs1]
		#R S SB format
		else:
			rs1 = state.IR&(0xF8000)
			rs1 = rs1 >> 15
			rs2 = state.IR&(0x1F00000)
			rs2 = rs2 >> 20
			state.RA = self.RegisterFile[rs1]
			state.RB = self.RegisterFile[rs2]
			state.RM=state.RB

		return state

	def execute(self, state):
		opcode = self._get_opcode(state.IR)
		funct3 = self._get_funct3(state.IR)
		muxB_control = 0 if (opcode == 51 or opcode == 99) else 1
		immediate = self._getImmediate(state.IR)
		if opcode==55:#for lui
			state.operand1=0
		elif opcode==23:#for auipc
			state.operand1=state.PC
		else:
			state.operand1 = state.RA
		
		state.operand2 = (muxB_control==0)*state.RB + (muxB_control==1)*immediate

		# R-type: add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem
		if opcode == 51:
			funct7 = (state.IR >> 25) & (0x7f)
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
			state.RZ = self.ALU(state.operand1, state.operand2, ALU_control)
		else:
			state.RZ=state.PC+4

		return state

	def memory_access(self, state):
		#Effective address stored in MAR in integer format
		#Data stored in MDR in Integer Format
		state.MAR=state.RZ
		state.MDR=state.RM
		opcode=self._get_opcode(state.IR)
		funct3=self._get_funct3(state.IR)
		if opcode == 3:
			if funct3>=0 and funct3<=3:
				state.MDR=self._read(state.MAR,2**(funct3))
				state.RY=state.MDR
		elif opcode== (8*4+3):
			if funct3>=0 and funct3<=3:
				self._write(state.MAR,state.MDR,2**(funct3))
		else:
			state.RY=state.RZ

		return state

	def write_back(self, state):
		#Determine whether write back is used
		opcode = self._get_opcode(state.IR)
		# #S Check
		# if opcode == 35:
		# 	self.IAG(state)
		# 	return
		#jal
		# if opcode==111:
		# 	#Extract the immediate field and generate the offset
		# 	immed_20=str((self.IR&0x80000000)>>31)
		# 	immed_19_12=bin((self.IR&(0x000ff000))>>12)[2:]
		# 	immed_19_12='0'*(8-len(immed_19_12))+immed_19_12
		# 	immed_11=str((self.IR&(0x00100000))>>20)
		# 	immed_10_1=bin((self.IR&(0x7fe00000))>>21)[2:]
		# 	immed_10_1='0'*(10-len(immed_10_1))+immed_10_1
		# 	immediate=immed_20*12+immed_19_12+immed_11+immed_10_1+'0'
		# 	offset=int(immediate,2)
		# 	if immediate[0]=='1':
		# 		offset^=0xFFFFFFFF
		# 		offset+=1
		# 		offset=-offset
		# 	#pass the offset to IAG 
		# 	self.IAG(offset)
			#set the self.RY to PC_temp
		#Handle AUIPC
		#elif opcode==23:
			#self.IAG(state)
			#self.RY=(self.PC+(self.IR&(0xFFFFF000)))&(0xFFFFFFFF)
		#SB		
		# elif opcode == 99 :
		# 	offset = 0
			
		# 	#Immediate Field Distribution
		# 	# Array:    [31] [30-25] [11-8] [7]
		# 	# ImmField:  12   10:5     4:1   11
		# 	# Shifts:    R19  R20      R7    L4

		# 	offset += (self.IR&(0x80)) << 4
		# 	offset += (self.IR&(0xF00)) >> 7
		# 	offset += (self.IR&(0x7E000000)) >> 20

		# 	#Working with sign bit
		# 	if(self.IR&(0x80000000) == 0x80000000):
		# 		offset = offset ^ 0xFFF
		# 		offset += 1
		# 		offset = -1 * offset
		# 	if self.RY==1:
		# 		self.IAG(offset)
		# 	else:
		# 		self.IAG(state)

		# 	return
		#jalr		
		# elif opcode==103:
		# 	#assuming jalr puts the offset value in RY
		# 	#print(self.RY)
		# 	self.IAG(self.RY)
		# 	self.RY=self.PC_temp

		# else:
		# 	self.IAG(state)
		
		self.IAG(state)
		#jal and jalr
		if opcode==103 or opcode==111:
			state.RY=state.PC_temp
		#S and SB check
		if opcode!=35 and opcode!=99:
			rd = state.IR&(0xF80)
			rd = rd//128
			self.RegisterFile[rd] = state.RY
			if(rd!=0):
				print(f'\t\tRegister x{rd} updated to : {hex(state.RY)}')
			self.RegisterFile[0]=0
		
		return state





		
		
