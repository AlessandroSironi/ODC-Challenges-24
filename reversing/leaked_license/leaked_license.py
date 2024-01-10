"""
We can exploit this by changing memory during execution. the license number is split in 5 parts

in ghidra: 0x001012b5
after this address in the code, the variable at $rbp-0x58 is the part of the license number we want to change.

in my case the address in gdb was 0x5555555552b5 and the variable was at 0x7fffffffdaf0

b *0x5555555552b5

set *0x7fffffffdaf0=0x726cfc2d
c
set *0x7fffffffdaf0=0x26c6defe
c
set *0x7fffffffdaf0=0xdb065621
c
set *0x7fffffffdaf0=0x99f5c7d0
c
set *0x7fffffffdaf0=0xda4f4930
c

Stack configuration with GDB:

0x7ffffffdd000     0x7ffffffff000 rw-p    22000 0      [stack]

###### STACK VISUALIZATION #######

At 0x5555555552b5

pwndbg> x/20gx $rsp
0x7fffffffdab0: 0x00007fffffffdc38      0x0000000100000000
0x7fffffffdac0: 0x0000000000000000      0x0000000000000020
0x7fffffffdad0: 0x0000000000000000      0x0000000000000000
0x7fffffffdae0: 0x0000000000000000      0x00000000f3ed47e2 <-
0x7fffffffdaf0: 0x00000000f3ed47e2 <-   0x0000000000000001
0x7fffffffdb00: 0x0000000000000001      0x000055555555549d
0x7fffffffdb10: 0x0000000000000000      0x0000555555555450
0x7fffffffdb20: 0x0000000000000000      0x0000555555555080
0x7fffffffdb30: 0x00007fffffffdc30      0x0000000000000000
0x7fffffffdb40: 0x0000000000000000      0x00007ffff7ddeb25

the addresses pointed by the arrows indicate the memory that contains the part of the original license number

we only need to change one for this to work, reiterate 5 times, flaggeroni

"""

"flag{a0db6e1e-2e5b00fb-643fe729-30d2348f-48c74576}"
