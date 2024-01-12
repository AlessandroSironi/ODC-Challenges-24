import angr
import claripy
from pwn import *

strlen = 45

prog = angr.Project('./odcware')

find = [0x00101a9b] 
avoid = [0x00101ab4] 

input_flag = claripy.BVS('flag', 8 * strlen)

state = prog.factory.entry_state(args=['./odcware', 'checker', input_flag], add_options={angr.options.LAZY_SOLVES})

#allowed_char = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

for byte in input_flag.chop(8):
	state.add_constraints(byte >= 0x20)
	state.add_constraints(byte <= 0x7f)

state.add_constraints(input_flag.chop(8)[0] == ord('f'))
state.add_constraints(input_flag.chop(8)[1] == ord('l'))
state.add_constraints(input_flag.chop(8)[2] == ord('a'))
state.add_constraints(input_flag.chop(8)[3] == ord('g'))
state.add_constraints(input_flag.chop(8)[4] == ord('{'))
state.add_constraints(input_flag.chop(8)[strlen-1] == ord('}'))

simgr = prog.factory.simulation_manager(state)
simgr.explore(find=find, avoid=avoid)

if simgr.found:
	s = simgr.found[0].solver

	flag = s.eval(input_flag)
	flag = bytes.fromhex(hex(flag)).decode('utf-8')

	print(flag)
else:
	print('unsat')