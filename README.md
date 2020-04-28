# RISC-V Simualtor

### Team Details
	Paras Goyal	2018CSB1111
	Ekansh Mahendru	2018CSB1087
	Hansin Ahuja	2018CSB1094
	Sakshay Mahna	2018CSB1119
	Atul Tiwari	2018CSB1077

### Instruction Formats
	R-Type:
		ins rd rs1 rs2
	I-Type (Except jalr ):
		ins rd rs1 immed
	SB-Type:
		ins rs1 rs2 label
	S-Type:
		ins rs1 immed(rs2)
	U-Type:
		ins rs1 immed
	UJ-Type:
		jal rd label
	jalr:
		jalr rd immed(rs1)

### Note : jalr is different from I Type as we had followed the version similar to https://www.kvakil.me/venus
#### Note : We recommend cloning the source directly from https://github.com/Ekan5h/RISC-V-ISA-Simulator directly to set it up.
## Instructions to setup GUI for Phase 3 (incorporates Phase 2 as well)
1.	Extract RISCVSim.tar.gz
2.	Run the install script
3.	Run the Risc-V simulator from the shortcut.


### Note: This install script is specific to Linux. For more details please refer to requirements.txt

##  Instructions to Use CLI
1.	Navigate to the directory containing the Makefile.
2.	Run the following command for executing the Phase 2 code (without Piplining):
		make p2 INP=path/to/the/file(without the asm extension)
3.	Run the following command for executing the Phase 3 Code (with Piplining):
		make p3 INP=path/to/file (without the asm extension)

Example: <br />
	make p2 INP=test
	
Example 2: <br />
	make p3 INP=bubble

Example 3: <br />
	make p3 INP=fib
#### Note: File needs to be in same directory as the Makefile

## Contributions
As this was a team project so it is difficult to completely segregate out the work done by each us but the following would give some outline. <br />
Sakshay - I Type <br />
Atul - S Type <br />
Hansin - SB Type <br />
Paras - R UJ Type <br />
Ekansh- U and GUI <br />
### Note- It was not strictly followed, and we helped each other in both the phases.
