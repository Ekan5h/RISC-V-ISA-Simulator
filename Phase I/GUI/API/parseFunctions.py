def parseS(st,l,labels):
    out = ""
    funct3 = ""
    imm11_5 = ""
    imm0_4 = ""
    opcode = "0100011"
    w = "010"
    h = "001"
    d = "011"
    b = "000"
    st = st.replace('(',' ')
    st = st.replace(')',' ')
    x = st.split()
    if len(x) != 4:
        raise Exception(f"Store excepts 4 arguments but got {len(x)} >>"+st)
    [operation, res2 , immediate , res1] = x
    if operation[1] == 'w':
        funct3 = w
    elif operation[1] == 'b':
        funct3 = b
    elif operation[1] == 'h':
        funct3 = h
    else:
        funct3 = d
    if res2[0] != 'x':
        raise Exception(f"{res2} is not a valid register. >>"+st)
    res2 = res2.replace('x','')
    res2 = int(res2)
    if res2 < 0 or res2 > 31:
        raise Exception("Register value out of bounds. >>"+st)
    res2 = bin(res2)[2:]
    if res1[0] != 'x':
        raise Exception(f"{res1} is not a valid register. >>"+st)
    res1 = res1.replace('x','')
    res1 = int(res1)
    if res1 < 0 or res1 > 31:
        raise Exception("Register value out of bounds. >>"+st)
    res1 = bin(res1)[2:]
    if immediate[0] == '0' and len(immediate) > 1 and immediate[1] == 'x':
        immediate = immediate[2:]
        immediate = int(immediate,16)
        if immediate > 4096 or immediate < -4096:
            raise Exception("Immediate value out of bounds. >>"+st)
        immediate = bin(immediate)[2:]
    elif immediate[0] == '-':
        immediate = immediate[1:]
        num = 0 - (int(immediate))
        if num > 4096 or num < -4096:
            raise Exception("Immediate value out of bounds. >>"+st)
        immediate = ''.join(reversed([str((num >> i) & 1) for i in range(12)]))
    else:
        immediate = int(immediate)
        if immediate > 4096 or immediate < -4096:
            raise Exception("Immediate value out of bounds. >>"+st)
        immediate = bin(immediate)[2:]
    for j in range(12 - len(immediate)):
        immediate = '0' + immediate
    for j in range(5 - len(res1)):
        res1 = '0' + res1
    for j in range(5 - len(res2)):
        res2 = '0' + res2
    imm11_5 = immediate[0:7]
    imm0_4 = immediate[7:12]
    out += imm11_5
    out += res2
    out += res1
    out += funct3
    out += imm0_4
    out += opcode  
    return out



def parseU(instruction, line_number, label_dict):
    try:
        [ins, reg, imm] = instruction.split()
    except:
        raise Exception("Incorrect instruction format >>"+instruction)
    letter = reg[0]
    try:
        reg = int(reg[1:])
    except:
        raise Exception("Incorrect register format >>"+instruction)
    if(ins == 'auipc'):
        opcode = '0010111'
    elif(ins == 'lui'):
        opcode = '0110111'
    if(letter!='x' or reg > 31 or reg < 0):
        raise Exception("Undefined Register >>" +instruction)
    if(imm[:2]=='0x'):
        try:
            imm = int(imm,0)
        except:
            raise Exception("Invalid immediate value >>" +instruction)
    else:
        try:
            imm = int(imm)
        except:
            raise Exception("Invalid immediate value >>" +instruction)
    if(imm < 0 or imm > 1048575):
        raise Exception("Immediate value out of range [0-1048575] >>" + instruction)
    imm = ''.join(reversed([str((imm >> i) & 1) for i in range(20)]))
    reg = ''.join(reversed([str((reg >> i) & 1) for i in range(5)]))
    return imm+reg+opcode

def isValidRegister(reg):
    if reg[0] != 'x':
        return False
    if reg[1:].isnumeric() == False:
        return False
    if int(reg[1:]) < 0 or int(reg[1:]) > 31:
        return False
    return True


def parseSB(instruction, line_number, label_dict):
    components = instruction.split()
    if(len(components) != 4):
        err = "Error! Branch instruction expected 3 arguments, got " +  str(len(components)-1) + " instead. >>"+instruction
        raise Exception(err)
    [operation, rs1, rs2, target_label] = instruction.split()
    if isValidRegister(rs1) == False:
        raise Exception("Error! Argument 1 is not a valid register. >>" + instruction)
    if isValidRegister(rs2) == False:
        raise Exception("Error! Argument 2 is not a valid register. >>"+instruction)
    if target_label not in label_dict.keys():
        raise Exception("Error! Target label not found. >>" + instruction)
    immediate_field = label_dict[target_label] - line_number
    if immediate_field > 4095 or immediate_field < -4096:
        raise Exception("Error! Target label is too far. >>" + instruction)
    rs1 = int(rs1[1:])
    rs2 = int(rs2[1:])
    rs1 = ('0' * (5 - len(str(bin(rs1))[2:]))) + (str(bin(rs1))[2:])
    rs2 = ('0' * (5 - len(str(bin(rs2))[2:]))) + (str(bin(rs2))[2:])
    immediate_field = ''.join(reversed([str((immediate_field >> i) & 1) for i in range(13)]))
    opcode = '1100011'
    funct3 = '000'*(operation=='beq') + '001'*(operation=='bne') + '100'*(operation=='blt') + '101'*(operation=='bge')
    machine_code = immediate_field[0] + immediate_field[2:8] + rs2 + rs1 + funct3 + immediate_field[8:12] + immediate_field[1] + opcode
    return machine_code

def parseR(instruction,inst,labels={}):
    import re
    x=re.split(r'[,\s]\s*',instruction)
    if len(x)!=4:
        raise Exception(f'Expected 3 argumets.Got {len(x)-1} instead. >>' + instruction)
    [ins,rd,rs1,rs2]=x
    if not isValidRegister(rs1) or not isValidRegister(rs2) or not isValidRegister(rd):
        raise Exception('Invalid Register Operands! >>'+instruction)
    opcode='0110011'
    rs1=int(rs1[1:])
    rs2=int(rs2[1:])
    rd=int(rd[1:])
    if rs1<0 or rs1>31:
        raise Exception("Register rs1 invalid! >>" + instruction)
    if rs2<0 or rs2>31:
        raise Exception("Register rs2 invalid! >>" + instruction)
    if rd<0 or rd>31:
        raise Exception("Register rd invalid! >>"+instruction)
    funct3='000'*(ins=='sub' or ins=='add' or ins=='mul')+'111'*(ins=='and')+'001'*(ins=='sll')+'010'*(ins=='slt')+'101'*(ins=='sra'or ins=='srl')+'100'*(ins=='xor' or ins=='div')+'110'*(ins=='or' or ins=='rem')
    funct7='0000000'*(ins=='add' or ins=='and' or ins=='sll' or ins=='slt' or ins=='srl' or ins=='xor' or ins=='or')+'0100000'*(ins=='sub' or ins=='sra')+'0000010'*(ins=='div'or ins=='rem'or ins=='mul')
    rs1=f'{rs1:05b}'
    rs2=f'{rs2:05b}'
    rd=f'{rd:05b}'
    return funct7+rs2+rs1+funct3+rd+opcode

def parseUJ(instruction,inst,labels={}):
    import re
    x=re.split(r'[,\s]\s*',instruction)
    if len(x)!=3:
        raise Exception(f"Expexted 2 operands, got{len(x)-1} instead. >>" + instruction)
    [ins,rd,label]=x
    if not isValidRegister(rd):
        raise Exception("Invalid Register Operand! >>" + instruction)        
    opcode='1101111'
    if label not in labels.keys():
        raise Exception("Label Not Found! >>" + instruction)
    rd=int(rd[1:])
    if rd<0 or rd>31:
        raise Exception('Register rd invalid! >>' + instruction)
    rd=f'{rd:05b}'
    diff=labels[label]-inst
    if diff > 2**20-1 or diff <-2**20:
        raise Exception('Address Out of Range! Use jalr instead >>' + instruction)
    diff=''.join([str(diff>>i & 1) for i in range (0,21)])[::-1]
    imm=diff[0]+diff[10:20]+diff[9]+diff[1:9]
    return imm+rd+opcode

def parseI(instruction, line_number, table):
    import re
    
    #I based instructions
    I = ["addi", "andi", "ori", "lb", "ld", "lh", "lw" , "jalr"]
    
    #Get the string based values by splitting
    immediate = ''
    try:
        [operation, rd, rs, immediate] = instruction.split()
    except:
        [operation, rd, rs] = instruction.split()
    
    #Check error code for operation
    if(operation not in I):
        raise Exception("The entered instruction is not a valid operation")
        return None
        
    #Regular Expression based checking
    regex = re.compile("x\d+")
    register = regex.search(rd)
    #Checking for rd
    if(register == None or len(register.group()) != len(rd)):
        raise Exception("Enter a valid destination register")
        
    #Checking for rs
    if(operation in I[3:]):
        regex = re.compile("(\d+\(x\d+\))|(0x(\d+|[A-Fa-f]+)\(x\d+\))")
        register = regex.search(rs)
        if(register == None or len(register.group()) != len(rs)):
            raise Exception("Enter a valid source register and its offset")
        
        fill_imm = True
        rs = ''
        for i in register.group():
            if(i == '('):
                fill_imm = False
                continue
            if(i == ')'):
                continue
            if(fill_imm):
                immediate = immediate + i
            else:
                rs = rs + i
    #Checking for rd
    else:
        regex = re.compile("x\d+")
        register = regex.search(rs)
        if(register == None or len(register.group()) != len(rs)):
            raise Exception("Enter a valid destination register")
            
            
    #Get the integer based value of registers
    rs = int(rs[1:])
    rd = int(rd[1:])
    
    #Exception Handling
    if(rs < 0 or rs > 32 or rd < 0 or rd > 32):
        raise Exception("Invalid register value!!! They should be between 1 to 32")
        
    #Encoding to binary
    rs = str(bin(rs))
    rs = rs[2:]
    rs = '0' * (5 - len(rs)) + rs
    
    rd = str(bin(rd))
    rd = rd[2:]
    rd = '0' * (5-len(rd)) + rd
    
    #Encoding and checking for immediate
    try:
        int(immediate, 0)
    except:
        raise Exception('Enter a valid immediate field')
        
    if(immediate[0:2] == '0x'):
        #To get the correct size of immediate field
        #Sizes smaller than 8 expanded to 8 and larger than 8 are also clipped to 8
        if(len(immediate[2:]) <= 8):
            immediate = '0x' + '0'*(8 - len(immediate[2:])) + immediate[2:]
        else:
            immediate = '0x' + immediate[len(immediate)-8:len(immediate)]
        
        immediate = int(immediate, 0)
        
        if(immediate == 4096):
            immediate = -2048
        else:
            immediate = -(immediate & 0x80000000) | (immediate & 0x7fffffff)
            
    elif(immediate[0:3] == '-0x'):
        if(len(immediate[3:]) <= 8):
            immediate = '0x' + '0' * (8 - len(immediate[3:])) + immediate[3:]
        else:
            immediate = '0x' + immediate[len(immediate)-8: len(immediate)]
            
        immediate = int(immediate, 0)
        
        if(immediate == 4096):
            immediate = -2048
        else:
            immediate = (immediate & 0x80000000) | -(immediate & 0x7fffffff)
            
    else:
        immediate = int(immediate, 0)
        
    if(immediate > 2047 or immediate < -2048):
        raise Exception('Immediate value should be in the range [-2048, 2047]')
        
    if(immediate < 0):
        immediate = -1 * immediate
        immediate = 4096 - immediate
        
    immediate = str(bin(immediate))
    immediate = immediate[2:]
    immediate = '0' * (12 - len(immediate)) + immediate
        
    opcode = ''
    funct3 = ''
    
    if(operation == 'addi'):
        opcode = '0010011'
        funct3 = '000'
    elif(operation == 'andi'):
        opcode = '0010011'
        funct3 = '111'
    elif(operation == 'ori'):
        opcode = '0010011'
        funct3 = '110'
    elif(operation == 'lb'):
        opcode = '0000011'
        funct3 = '000'
    elif(operation == 'lh'):
        opcode = '0000011'
        funct3 = '001'
    elif(operation == 'lw'):
        opcode = '0000011'
        funct3 = '010'
    elif(operation == 'ld'):
        opcode = '0000011'
        funct3 = '011'
    elif(operation == 'jalr'):
        opcode = '1100111'
        funct3 = '000'
        
    #Collect the final binary code
    final_binary = immediate + rs + funct3 + rd + opcode
    return final_binary
