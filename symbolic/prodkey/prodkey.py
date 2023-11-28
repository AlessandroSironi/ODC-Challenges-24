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


# Code from GitHub
""" import binascii
import claripy
import angr

find_address = 0x00400e58
avoid_address = 0x00400e73

#creating the project
proj = angr.Project('prodkey')

#I need 30 bytes since the constraints, saw on the Ghidra code, need at least 29 chars
chars = [claripy.BVS('c%d' % i, 8) for i in range(30)]
input_str = claripy.Concat(*chars + [claripy.BVV(b'\n')])


#defining the initial state, passing the input_str as content
st = proj.factory.full_init_state(
    args=['./prodkey'],
    #add_options={angr.options.LAZY_SOLVES},
    stdin=angr.simos.simos.SimFileStream(name='stdin', content=input_str, has_end=False),
)

#characters needs to be printable!!!!!!!
for c in chars:
    st.solver.add(c >= 0x20, c<=0x7e)

#defining and initializing the simulation manager
simgr = proj.factory.simulation_manager(st)
simgr.explore(find=find_address, avoid=avoid_address)


try:
    print(simgr.found[0].posix.dumps(0))

    p = simgr.found[0]
    sol = p.solver.eval(input_str, cast_to=bytes)
    print(b"Solution found: " + sol)

except Exception as e:
    print('unsat', e)


#solution retrieved with angr:
#M4@@9-8  7@-@@@9 -6@BB2-@@ 88 """