# RISC-V Simualtor

### Team Details
	Paras Goyal	2018CSB1111
	Ekansh Mahendru	2018CSB1087
	Hansin Ahuja	2018CSB1094
	Sakshay Mahna	2018CSB1119
	Atul Tiwari	2018CSB1077

## Instructions to setup GUI 
1.	Extract RISCVSim.tar.gz
2.	Run the install script
3.	Run the Risc-V simulator from the shortcut.
	
### Note: This install script is specific to Linux. For more details please refer to requirements.txt

##  Instructions to Use CLI
1.	Navigate to the Phase I directory and put the asm file in this directory.
2.	Run the command
		python3 ASM2MC.py file_name.asm out_name.mc
	It will generate the mc file according to the Given Specifications.
3.	Copy the mc file to Phase II Directory.
4.	Navigate to Phase II and run the following command:
		python3 runScript out_name.mc
	This will execute the Machine Code

Example:
	cd Phase\ I <br />
	python3 ASM2MC.py test.asm out.mc <br />
	cp out.mc ../Phase\ II/out.mc <br />
	cd ../Phase\ II <br />
	python3 runScript.py out.mc <br />


## Contributions
As this was a team project so it is difficult to completely segregate out the work done by each us but the following would give some outline.
Sakshay - I Type <br />
Atul - S Type <br />
Hansin - SB Type <br />
Paras - R UJ Type <br />
Ekansh- U and GUI <br />
### Note- It was not strictly followed, and we helped each other in both the phases.
