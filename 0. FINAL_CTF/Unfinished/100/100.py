""" from z3 import *
from pwn import *

def convert(input_string):
    # Define the character set
    char_set = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # Initialize the values array to store the converted input
    values = []

    # Process each character in the input string
    for char in input_string:
        if len(values) > 29:  # Limit to process only up to 30 characters
            break

        # Find the index of the character in the char_set
        for i, set_char in enumerate(char_set):
            if char == set_char:
                values.append(i)
                break
    
    return values

def check():

    return 

flag_len = 30
flag = [BitVec(f'{i}', 8) for i in range(flag_len)]

solver = Solver()
s.add(flag == convert(check()))
#p = process("./challenge")

if solver.check() == sat:
    model = solver.model()
    input_string = ""

    for i in range(30):
        input_string += chr(model[flag[i]].as_long())
    
    print(input_string)
    p.sendline(input_string)
    print(p.recvall())
 """

import angr
import claripy
from pwn import *

strlen = 30

prog = angr.Project('./challenge', auto_load_libs=False)

find = [0x101290] # Print flag
avoid = [0x1012a1] # Print "Next Time :D"

input_flag = claripy.BVS('flag', 8 * strlen)
#state = prog.factory.entry_state(stdin=input_flag)
state = prog.factory.entry_state(args=['./challenge', input_flag], add_options={angr.options.LAZY_SOLVES})

# Adding constraints for the input to find:
for byte in input_flag.chop(8):
    # Constraint for '0' to '9'
    constraint_0_9 = (byte >= 0x30) & (byte <= 0x39)
    # Constraint for 'a' to 'z'
    constraint_a_z = (byte >= 0x61) & (byte <= 0x7A)
    # Constraint for 'A' to 'Z'
    constraint_A_Z = (byte >= 0x41) & (byte <= 0x5A)

    #state.solver.add(constraint_0_9)
    #state.solver.add(constraint_a_z)
    #state.solver.add(constraint_A_Z)
	

    # Combine constraints with logical OR
    state.add_constraints(constraint_0_9 | constraint_a_z | constraint_A_Z)

simgr = prog.factory.simulation_manager(state)
simgr.explore(find=find, avoid=avoid)

if simgr.found:
	s = simgr.found[0].solver
	print(s.eval(input_flag, cast_to=bytes))
	#flag = s.eval(input_flag)
	#flag = bytes.fromhex(hex(flag)[2:]).decode('utf-8')
	#print(flag)
else:
	print('Solution not found.')