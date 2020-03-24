exe:
	python3 ./Phase\ I/ASM2MC.py ${INP}.asm
	python3 ./Phase\ II/runScript.py ${INP}.mc
