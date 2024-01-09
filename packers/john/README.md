# John

1) hardware breakpoint at obfuscating function (hb) 
2) dump the obfuscated function from pwndgb:
'''bash
dump memory FILE START STOP

dump memory first 0x804970e (0x804970e + (0x53*4))
'''
3) patch the binary, using python (see patcher.py)
4) reopen the new patched file in ghidra. For this challenge, we have many functions to de-obfuscate. 


break *0x804970e



  iVar1 = unpack(FUN_080492a0,0x11,param_6[1]);
  iVar2 = unpack(FUN_080492e5,0x11,param_6[1]);
  iVar3 = unpack(FUN_08049329,0x17,param_6[1]);
  iVar4 = unpack(FUN_080496ab,0x18,param_6[1]);
  iVar5 = unpack(FUN_080495e4,0x31,param_6[1]);
  iVar6 = unpack(FUN_08049546,0x27,param_6[1],0);
  iVar7 = unpack(FUN_0804951f,9,param_6[1]);

flag starts as usual with flag{ and ends with }
flag's length = 33

pwndbg> dump memory first 0x080492a0 (0x080492a0 + (0x11*4))
pwndbg> dump memory second 0x080492e5 (0x080492e5 + (0x11*4))
pwndbg> dump memory third 0x08049329 (0x08049329 + (0x18*4))
pwndbg> dump memory third 0x08049329 (0x08049329 + (0x17*4))
pwndbg> dump memory fourth 0x080496ab (0x080496ab + (0x18*4))
pwndbg> dump memory fifth 0x080495e4 (0x080495e4 + (0x31*4))
pwndbg> dump memory sixth 0x08049546 (0x08049546 + (0x27*4))
pwndbg> dump memory seventh 0x0804951f (0x0804951f + (9*4))
pwndbg> dump memory check5 0x0804945e (0x0804945e + (0x30*4))
pwndbg> dump memory check4 0x08049385 (0x08049385 + (0x36*4))
