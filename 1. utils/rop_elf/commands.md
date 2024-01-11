# Patch ELF

```bash
patchelf --set-interpreter ./ld-2.23.so --replace-needed libc.so.6 ./libc-2.23.so ./binary
```

# Ropper

```bash
ropper -f file
```

# One_Gadget 
```bash
one_gadget file
```
NB: one_gadget has to be used on the library.

# Check security
```bash
checksec (--file) filename
```
Arch, RELRO, Stack, NX, PIE

## Explanation
Sure, let's break down these concepts, which are commonly related to binary executable formats and their security features:

1. **Arch (Architecture)**
   - This refers to the computer architecture for which a binary is compiled. The architecture defines important aspects like the instruction set, memory organization, and how data types are represented. Common architectures include x86 (32-bit), x86_64 (64-bit, also known as AMD64), ARM, and MIPS. Each architecture has its unique characteristics and requires binaries to be specifically compiled for it.

2. **RELRO (Relocation Read-Only)**
   - RELRO stands for "Relocation Read-Only" and is a security feature that makes certain parts of the binary read-only before the main program starts. It comes in two levels:
     - Partial RELRO: This makes the Global Offset Table (GOT) read-only, preventing overwriting of function pointers.
     - Full RELRO: This additionally rearranges the binary so that the GOT comes before the BSS and data segments, and makes the entire GOT read-only. This helps protect against certain types of attacks that modify memory, like GOT overwriting or return-to-plt (procedure linkage table) attacks.

3. **Stack Canaries**
   - A stack canary is a security feature used to prevent stack buffer overflow attacks. A unique value (the canary) is placed on the stack just before the return address. Before the function returns, the canary value is checked. If it has been altered (which could happen if a buffer overflow overwrites stack memory), the program aborts, preventing the attacker from hijacking the control flow of the program.

4. **NX (Non-eXecutable bit)**
   - NX stands for "Non-eXecutable" and is a feature that marks certain regions of memory (like the stack and heap) as non-executable. This means that even if an attacker manages to inject malicious code into these regions, the processor will not execute this code. This significantly mitigates the risk of buffer overflow attacks where the attacker tries to run their code by overflowing buffers.

5. **PIE (Position Independent Executable)**
   - PIE stands for "Position Independent Executable." It means that the executable can be loaded at any address in memory, not just a fixed address. This is important for security features like ASLR (Address Space Layout Randomization), where the base address of the executable, libraries, stack, and heap are randomly positioned in memory when a program starts. PIE binaries are essential for effective ASLR, making it harder for attackers to predict the location of specific code and data in memory.

Each of these features contributes to the overall security posture of a binary, making it more resilient against common types of attacks, particularly those that involve exploiting memory corruption vulnerabilities.