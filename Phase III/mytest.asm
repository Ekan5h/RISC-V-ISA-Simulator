addi x10,x0,6

#seed 1 in x3
#seed 2 in x4
addi x3,x0,0
addi x4,x0,1

addi x31,x0,1

jal x1,fib
beq x0,x0,bye

fib:
addi x2,x2,-4
sw x1,0(x2)
addi x2,x2,-4
sw x10,0(x2)

beq x10,x0,se1
beq x10,x31,se2
addi x10,x10,-1
jal x1,fib
addi x2,x2,-4
sw x11,0(x2)
#add x12,x0,x11
addi x10,x10,-1
jal x1,fib
addi x2,x2,-4
sw x11,0(x2)
beq x0,x0,exit1
se1:add x11,x0,x3
beq x0,x0,exit
se2:add x11,x0,x4
beq x0,x0,exit
exit1:
lw x28,0(x2)
    lw x29,4(x2)
    addi x2,x2,8
    add x11,x28,x29
exit:
lw x10,0(x2)
    lw x1,4(x2)
    addi x2,x2,8
    jalr x0 0(x1)
   
   
bye: