p3:
	python3 ./Phase\ I/ASM2MC.py ${INP}.asm
	python3 ./Phase\ III/runScript.py ${INP}.mc
p2:
	python3 ./Phase\ I/ASM2MC.py ${INP}.asm
	python3 ./Phase\ II/runScript.py ${INP}.mc