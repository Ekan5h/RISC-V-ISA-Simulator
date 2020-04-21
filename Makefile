exe:
	python3 ./Phase\ I/ASM2MC.py ${INP}.asm
	python3 ./Phase\ III/runScript.py ${INP}.mc
