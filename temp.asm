addi x0 x0 1
addi x0 x0 1
jal x1 label
beq x0 x0 end
label:
addi x0 x0 1
addi x0 x0 1
jalr x0 0(x1)
end:

