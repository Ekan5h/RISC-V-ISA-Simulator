def parse(buffer):
    import sys
    import re
    from parseFunctions import parseS, parseI, parseR, parseSB, parseU, parseUJ
    buffer = re.sub(r'#.*\n', '\n', buffer)
    buffer = re.sub(r'#[^\n]+', '', buffer)
    buffer = re.sub(r':', ':\n', buffer)
    buffer = re.sub(r'\n\s+', '\n', buffer)
    buffer = re.sub(r'^\s+', '', buffer)
    buffer = re.sub(r'\s+$', '', buffer)
    if(len(buffer)==0):
        raise Exception("No code to process!")
    lines = [x.strip() for x in buffer.split("\n")]
    dataindices = [[i,1] for i, x in enumerate(lines) if x == ".data"]
    textindices = [[i,2] for i, x in enumerate(lines) if x == ".text"]
    directives = dataindices + textindices
    directives = sorted(directives, key = lambda x:x[0])
    text = []
    data = []
    labels = {}
    j=0
    cur = 2
    for i in range(len(lines)):
        if(j<len(directives) and i==directives[j][0]):
            cur = directives[j][1]
            j+=1
        elif(cur==2 and len(lines[i])>0):
            text.append(lines[i])
        elif(len(lines[i])>0):
            data.append(lines[i])
    OriginalCode = text
    temp = []
    for i in OriginalCode:
        if not re.match(r'[^\s,]+:', i):
            temp.append(i)
    OriginalCode = temp
    text = "\n".join(text)
    text = text.lower()
    text = re.sub(r',', ' ', text)
    text = re.sub(r'  ', ' ', text)
    text = re.sub(r'(?<=[ (])ra(?=[ )\n])', 'x1', text)
    text = re.sub(r'(?<=[ (])sp(?=[ )\n])', 'x2', text)
    text = re.sub(r'(?<=[ (])gp(?=[ )\n])', 'x3', text)
    text = re.sub(r'(?<=[ (])tp(?=[ )\n])', 'x4', text)
    text = re.sub(r'(?<=[ (])t0(?=[ )\n])', 'x5', text)
    text = re.sub(r'(?<=[ (])t1(?=[ )\n])', 'x6', text)
    text = re.sub(r'(?<=[ (])t2(?=[ )\n])', 'x7', text)
    text = re.sub(r'(?<=[ (])s0(?=[ )\n])', 'x8', text)
    text = re.sub(r'(?<=[ (])s1(?=[ )\n])', 'x9', text)
    text = re.sub(r'(?<=[ (])a0(?=[ )\n])', 'x10', text)
    text = re.sub(r'(?<=[ (])a1(?=[ )\n])', 'x11', text)
    text = re.sub(r'(?<=[ (])a2(?=[ )\n])', 'x12', text)
    text = re.sub(r'(?<=[ (])a3(?=[ )\n])', 'x13', text)
    text = re.sub(r'(?<=[ (])a4(?=[ )\n])', 'x14', text)
    text = re.sub(r'(?<=[ (])a5(?=[ )\n])', 'x15', text)
    text = re.sub(r'(?<=[ (])a6(?=[ )\n])', 'x16', text)
    text = re.sub(r'(?<=[ (])a7(?=[ )\n])', 'x17', text)
    text = re.sub(r'(?<=[ (])s2(?=[ )\n])', 'x18', text)
    text = re.sub(r'(?<=[ (])s3(?=[ )\n])', 'x19', text)
    text = re.sub(r'(?<=[ (])s4(?=[ )\n])', 'x20', text)
    text = re.sub(r'(?<=[ (])s5(?=[ )\n])', 'x21', text)
    text = re.sub(r'(?<=[ (])s6(?=[ )\n])', 'x22', text)
    text = re.sub(r'(?<=[ (])s7(?=[ )\n])', 'x23', text)
    text = re.sub(r'(?<=[ (])s8(?=[ )\n])', 'x24', text)
    text = re.sub(r'(?<=[ (])s9(?=[ )\n])', 'x25', text)
    text = re.sub(r'(?<=[ (])s10(?=[ )\n])', 'x26', text)
    text = re.sub(r'(?<=[ (])s11(?=[ )\n])', 'x27', text)
    text = re.sub(r'(?<=[ (])t3(?=[ )\n])', 'x28', text)
    text = re.sub(r'(?<=[ (])t4(?=[ )\n])', 'x29', text)
    text = re.sub(r'(?<=[ (])t5(?=[ )\n])', 'x30', text)
    text = re.sub(r'(?<=[ (])t6(?=[ )\n])', 'x31', text)
    text = text.split("\n")
    dataLocation = {}
    dataOut = {}
    mem = int("0x10000000",0)
    j = 0
    while(j<len(data)):
        if(re.match(r'[^\s,]+:', data[j])):
            label = data[j][:-1]
            dataLocation[label] = mem
            j+=1
        if(re.match(r'(\.byte|\.half|\.word|\.dword|\.asciiz)', data[j])):
            dataLocation[label] = mem
            datatype = data[j].split()[0]
            for val in re.split(r'[, ]', data[j])[1:]:
                if(re.match(r"0x", val)):
                    val = int(val,0)
                elif(datatype != ".asciiz"):
                    val = int(val)
                if(datatype == '.byte'):
                    dataOut[mem] = val
                    val = val>>8
                    if(val!=0):
                        raise Exception("Value out of range: "+data[j])
                    mem+=1
                elif(datatype == '.half'):
                    dataOut[mem] = val & 255
                    val = val >> 8
                    dataOut[mem+1] = val & 255
                    val = val>>8
                    if(val!=0):
                        raise Exception("Value out of range: "+data[j])
                    mem+=2
                elif(datatype == '.word'):
                    dataOut[mem] = val & 255
                    val = val >> 8
                    dataOut[mem+1] = val & 255
                    val = val >> 8
                    dataOut[mem+2] = val & 255
                    val = val >> 8
                    dataOut[mem+3] = val & 255
                    val = val>>8
                    if(val!=0):
                        raise Exception("Value out of range: "+data[j])
                    mem+=4
                elif(datatype == '.dword'):
                    dataOut[mem] = val & 255
                    val = val >> 8
                    dataOut[mem+1] = val & 255
                    val = val >> 8
                    dataOut[mem+2] = val & 255
                    val = val >> 8
                    dataOut[mem+3] = val & 255
                    val = val >> 8
                    dataOut[mem+4] = val & 255
                    val = val >> 8
                    dataOut[mem+5] = val & 255
                    val = val >> 8
                    dataOut[mem+6] = val & 255
                    val = val >> 8
                    dataOut[mem+7] = val & 255
                    val = val>>8
                    if(val!=0):
                        raise Exception("Value out of range: "+data[j])
                    mem+=8
                elif(datatype == '.asciiz'):
                    string = re.findall('"([^"]*)"', data[j])
                    if(len(string)!=1):
                        raise Exception(".asciiz requires single string: " + data[j])
                    for c in string[0]:
                        dataOut[mem] = ord(c)
                        mem += 1
                    dataOut[mem] = 0
                    mem += 1
                    break
        else:
            raise Exception("Unsupported directiive " + data[j])
        j+=1
    R = ['add', 'and', 'or', 'sll', 'slt', 'sra', 'srl', 'sub', 'xor', 'mul', 'div', 'rem']
    I = ['addi', 'andi', 'ori', 'lb', 'ld', 'lh', 'lw', 'jalr']
    S = ['sb', 'sw', 'sd', 'sh']
    SB = ['beq', 'bne', 'bge', 'blt']
    U = ['auipc', 'lui']
    UJ = ['jal']
    inNo = 0
    for line in text:
        if(re.match(r'[^\s,]+:', line)):
            labels[line[:-1]] = 4*inNo
            continue
        inNo+=1
    inNo = 0
    textOut = {}
    mem = 0
    BasicCode = []
    for line in text:
        if(re.match(r'[^\s,]+:', line)):
            continue
        BasicCode.append(line)
        ins = line.split()[0]
        if(ins in R):
            textOut[mem] = hex(int(parseR(line,mem,labels),2))
        elif(ins in I):
            if(ins != 'lw' or (ins =='lw' and re.match(r'.+\(x\d+\)', line))):
                textOut[mem] = hex(int(parseI(line,mem,labels),2))
            else:
                try:
                    ins, register, label = line.split()
                except:
                    raise Exception("Invalid statement >>" + line)
                if(label not in dataLocation.keys()):
                    raise Exception("Could not find label >>" + line)
                BasicCode = BasicCode[:-1]
                BasicCode.append("lui "+register+" "+hex(dataLocation[label])[:-3])
                textOut[mem] = hex(int(parseU("lui "+register+" "+hex(dataLocation[label])[:-3], mem, labels),2))
                mem += 4
                # if(int("0x"+hex(dataLocation[label])[7:],0)!=0):
                #     OriginalCode = OriginalCode[:len(BasicCode)]+[OriginalCode[len(BasicCode)-1], OriginalCode[len(BasicCode)-1]]+OriginalCode[len(BasicCode):]
                #     BasicCode.append("addi "+register+" "+register+" 0x"+hex(dataLocation[label])[7:])
                #     textOut[mem] = hex(int(parseI("addi "+register+" "+register+" 0x"+hex(dataLocation[label])[7:], mem, labels),2))
                #     mem += 4
                # else:
                OriginalCode = OriginalCode[:len(BasicCode)]+[OriginalCode[len(BasicCode)-1]]+OriginalCode[len(BasicCode):]
                BasicCode.append("lw "+register+" "+str(int("0x"+hex(dataLocation[label])[7:],0))+"("+register+")")
                textOut[mem] = hex(int(parseI("lw "+register+" 0("+register+")", mem, labels),2))
        elif(ins in S):
            textOut[mem] = hex(int(parseS(line,mem,labels),2))
        elif(ins in SB):
            textOut[mem] = hex(int(parseSB(line,mem,labels),2))
        elif(ins in U):
            textOut[mem] = hex(int(parseU(line,mem,labels),2))
        elif(ins in UJ):
            textOut[mem] = hex(int(parseUJ(line,mem,labels),2))
        else:
            raise Exception("Invalid Instruction "+line)
        mem += 4
    textOut[mem] = '0x00000000'
    MachineCode = []
    for k in textOut:
        MachineCode.append("0x"+'0'*(10-len(hex(int(textOut[k],0))))+hex(int(textOut[k],0))[2:]) 
    return OriginalCode, BasicCode, MachineCode[:-1], dataOut