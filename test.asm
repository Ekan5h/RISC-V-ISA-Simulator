.data
var1: .word 15 69 77 666

.text
addi x29 x0 2
addi x30 x0 1
auipc x3 65536 
addi x3 x3 -8
addi x4 x0 0
addi x5 x0 3
auipc x11 65536 
addi x11 x11 -24
jal x1 mergesort
beq x0 x0 ff
mergesort:
addi x2 x2 -4
sw x4 0(x2)
addi x2 x2 -4
sw x5 0(x2)
addi x2 x2 -4
sw x1 0(x2)
bge x4 x5 exit
add x9 x5 x4
srl x5 x9 x30
jal x1 mergesort
addi x4 x5 1
#addi x4 x5 0
lw x5 4(x2)
jal x1 mergesort
lw x25 8(x2)
add x26 x0 x4
#addi x26 x26 1
add x27 x0 x5
addi x27 x27 1
jal x1 merge
exit:lw x1 0(x2)
lw x5 4(x2)
lw x4 8(x2)
addi x2 x2 12
jalr x0 0(x1)

merge:
    addi x2 x2 -4
    sw x1 0(x2)
    sll x25 x25 x29
    sll x26 x26 x29
    sll x27 x27 x29

    add x25 x25 x11
    add x26 x26 x11
    add x27 x27 x11
    add x22 x0 x25
    addi x21 x26 0
    mergeloop: bge x25 x21 l1
            bge x26 x27 l2
            lw x23 0(x25)
            lw x24 0(x26)
            blt x23 x24 one
            addi x2 x2 -4
            addi x26 x26 4
            sw x24 0(x2)
            jal x0 mergeloop
            one:
            addi x2 x2 -4
            addi x25 x25 4
            sw x23 0(x2)
            jal x0 mergeloop
    l1:
        bge x26 x27 mergeexit
        lw x24 0(x26)
        addi x26 x26 4
        addi x2 x2 -4
        sw x24 0(x2)
        jal x0 l1
    l2: bge x25 x21 mergeexit
        lw x23 0(x25)
        addi x25 x25 4
        addi x2 x2 -4
        sw x23 0(x2)
        jal x0 l2

    mergeexit:
    add x25 x0 x22
    addi x27 x27 -4
    in_loop:
            blt x27 x25 mergebye
            lw x17 0(x2)
            sw x17 0(x27)
            addi x2 x2 4
            addi x27 x27 -4
            jal x0 in_loop
    mergebye:
        lw x1 0(x2)
        addi x2 x2 4
        jalr x0 0(x1)
ff: