  
addi x29 x0,5
addi x28,x0 1
add x6 x0 x29
addi x2,x2,-4
sw x6,0(x2)
addi x2,x2,-4
sw x1,0(x2)
addi x6,x6,-1
lw x1,0(x2)
lw x6,4(x2)
addi x2 x2 8
mul x26 x26 x6
addi x26 x0 1