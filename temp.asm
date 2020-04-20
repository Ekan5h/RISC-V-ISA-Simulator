jal x1 label
addi x5 x0 1
beq x0 x0 end
label:
addi x1 x1 4
jalr x0 0(x1)
end:
