# Ekansh Mahendru (2018CSB1087)
# Right: Hansin
# Left: Stephen


###################################
#			  Queue				  #
#		1 -> Enqueue			  #
#		2 -> Dequeue		 	  #
#		3 -> Size				  #
#		4 -> exit				  #
###################################
# The queue is stored in the format:
#	0x10000100 -> [max_size][cur_size][queue_elements...]
# Slither function makes the queue stay in the same location when enqueued
# Dequeue function returns the popped element in x12 and decreases the cur_size of the queue
# All inputs are given through data.
# Enqueue is O(n) while dequeue is O(1)

.data
	max_size: .word 20
    str1: .asciiz "E Success"
    str2: .asciiz "D Success"
    input: .word 1 10 1 20 2 1 6 3 2 1 7 3 0
.text
    beq x0 x0 main
    size:									# x11 queue location x1 return address
    	lw x15 4(x11)
        jalr x0 0(x1)
        
	enqueue:								# x10 element, x11 queue location,x1 return address
    	lw t0 4(x11) #Current Size
        lw t1 0(x11) #Max Size
        # Check for overflow
        bne t0 t1 skip
        addi sp sp -4
        sw x1 4(sp)
        jal x1 overflow
        lw x1 4(sp)
        addi sp sp 4
        jalr x0 0(x1)
        skip:
        addi t0 t0 1
        sw t0 4(x11)
        # Function call to slither
        addi sp sp -12
        sw x10 4(sp)
        sw x11 8(sp)
        sw x1 12(sp)
        jal x1 slither
        lw x1 12(sp)
        lw x11 8(sp)
        lw x10 4(sp)
        addi sp sp 12
        
        sw x10 8(x11)
        
        #Storing success message
        lui t0 0x10000
        addi t0 t0 4
        lui t1 0x10000
        addi t1 t1 0x200
        lb t2 0(t0)
        strloop:
        	beq t2 x0 endstrloop
            sw t2 0(t1)
            addi t0 t0 1
            addi t1 t1 1
            lb t2 0(t0)
            beq x0 x0 strloop
        endstrloop:
        addi x10 x0 0
        jalr x0 0(x1)
	
    slither:
    	lw t0 0(x11) #Max Size
        addi t0 t0 -1
        addi x11 x11 8
        add t0 x11 t0
        addi t1 t0 -4
        loop:
        	beq t0 x11 fall
            lw t2 0(t1)
            sw t2 0(t0)
            addi t0 t0 -4
            addi t1 t1 -4
            beq x0 x0 loop
        fall:
        jalr x0 0(x1)
        
    dequeue:						# x11 queue location x1 return address returns in x12
    	lw t0 4(x11) #Current Size
        addi sp sp -4
        sw x1 4(sp)
        jal x1 underflow
        lw x1 4(sp)
        addi sp sp 4
        jalr x0 0(x1)
        skipd:
        addi t0 t0 -1
        sw t0 4(x11)
        #Storing success message
        lui t0 0x10000
        addi t0 t0 14
        lui t1 0x10000
        addi t1 t1 0x200
        lb t2 0(t0)
        strloop2:
        	beq t2 x0 endstrloop2
            sw t2 0(t1)
            addi t0 t0 1
            addi t1 t1 1
            lb t2 0(t0)
            beq x0 x0 strloop2
        endstrloop2:
        addi x10 x0 0
        lw t0 4(x11)
        add t0 x11 t0
        lw x12 8(t0)
        jalr x0 0(x1)
        
	overflow:
    	lw t0 4(x11) #Current Size
        lw t1 0(x11) #Max Size
        # Check for overflow
        addi x10 x0 0
        bne t0 t1 skipover
    	addi x10 x0 -2
        skipover:
        jalr x0 0(x1)
        
    underflow:
    	addi x10 x0 0
    	lw t0 4(x11) #Current Size
    	addi x10 x0 -1
        skipunder:
        jalr x0 0(x1)
    


    main:
    #Queue declaration
	lui t0 0x10000
    addi t0 t0 0x100
    lui t1 0x10000
    lw t2 0(t1)  #Max_size
    sw t2 0(t0)
    addi t0 t0 4
    sw x0 0(t0)  #Current_size
    
    #Reading the input
    lui s10 0x10000
    addi s10 s10 0x18 # Reading Start Address
    
    addi s2 x0 1
    addi s3 x0 2
    addi s4 x0 3
    addi s5 x0 -1
    addi s6 x0 -2
    
    lw s11 0(s10)
    inputloop:
        bne s11 s2 end1
            # Enqueue
            addi s10 s10 4
            lw t2 0(s10)
            add x10 x0 t2
            lui x11 0x10000
            addi x11 x11 0x100
            jal x1 enqueue
        end1:
        bne s11 s3 end2
            # Dequeue
            lui x11 0x10000
            addi x11 x11 0x100
            jal x1 dequeue
        end2:
        bne s11 s2 end3
            # Size
            lui x11 0x10000
            addi x11 x11 0x100
            jal x1 size
        end3:
        beq x10 s5 exit
        beq x10 s6 exit
        addi s10 s10 4
        lw s11 0(s10)
    exit:
