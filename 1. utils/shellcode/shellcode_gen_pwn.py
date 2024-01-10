from pwn import *

# Set architecture and OS
context.arch = 'amd64'  # or 'i386', 'arm', etc. depending on your target
context.os = 'linux'

# Define the filename to open
filename = "flag"

# Craft the shellcode
shellcode = shellcraft.open(filename, 0)  # 0 for read-only
shellcode += shellcraft.read('rax', 'rsp', 1024)  # Read up to 1024 bytes from file descriptor into stack
shellcode += shellcraft.write(1, 'rsp', 'rax')  # Write from stack to STDOUT

print(shellcode)

# Assemble the shellcode into bytes
machine_code = asm(shellcode)

# Output the shellcode
print(f"Shellcode: {machine_code.hex()}")
