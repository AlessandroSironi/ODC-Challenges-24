import angr
import claripy
from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./prodkey")
    gdb.attach(r, """
    # b 
    c
    """)
    input("wait")
else:
    r = remote("bin.training.offdef.it", 2021)

r.recvuntil("Please Enter a product key to continue:")
TARGET = 0x400deb

chars = [claripy.BVS(f"c_{i}", size=8) for i in range(32)]
flag = claripy.Concat(*chars + [claripy.BVV(b'\n')])

# Create angr project
proj = angr.Project("./prodkey")
initial_state = proj.factory.entry_state()

# Constrain input to be printable

for char in chars:
    initial_state.solver.add(char >= 0x20)
    initial_state.solver.add(char <= 0x7e)

# Create simulation manager initialized with the starting state
simgr = proj.factory.simulation_manager(initial_state)
simgr.explore(find=TARGET)

if simgr.found:
    sol = simgr.found[0].posix.dumps(0)
    #print(simgr.found[0].solver.eval(flag))
    print(sol)
    
    r.sendline(sol)
    r.interactive()
else:
    print("Not found")
