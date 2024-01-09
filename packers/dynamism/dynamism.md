# Dynamism

1) Patch the _INIT1 that, with ptrace, checks wheter the process is being debugged with NOPs.
2) gdb break to get the address info. bin.training.offdef.it is already in clear, but the port is needed. Port is found to be 4010 (not a necessary info)
3) 0x7ffff7fe48e0 -> main address obtained by gdb. 
4) Downloaded code execution @ offset 0x1574 -> b *(0x7ffff7fe48e0 + 0x1574)
5) Check match is found @ 0x7ffff7fce240 (exploration in gdb) up to 

```bash
dump binary memory check_code 0x7ffff7fce240 0x7ffff7fce3e7
```