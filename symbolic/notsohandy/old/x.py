import angr
import claripy

def main():
    binary_path = 'notsohandy'
    correct_address = 0x1422  # Replace with the actual address
    avoid_addresses = [0x1433, 0x13dc, 0x12a5]  # Replace with actual addresses
    min_length = 49  # Adjust as needed
    max_length = 49  # Adjust as needed

    for input_len in range(min_length, max_length + 1):
        print(f"Trying with input length: {input_len}")

        # Create a symbolic bitvector for the input
        flag = claripy.BVS('flag', 8 * input_len)

        # Create an angr project
        project = angr.Project(binary_path, auto_load_libs=False)

        # Define the entry state with the symbolic input as an argument
        entry_state = project.factory.entry_state(args=[binary_path, flag])

        # Add constraints for the input
        for byte in flag.chop(8):
            entry_state.solver.add(byte >= ord(' '))
            entry_state.solver.add(byte <= ord('~'))

        # Create a simulation manager
        simulation = project.factory.simgr(entry_state)

        # Explore the binary
        simulation.explore(find=correct_address, avoid=avoid_addresses)

        if simulation.found:
            solution_state = simulation.found[0]
            solution = solution_state.solver.eval(flag, cast_to=bytes)
            print("Correct flag: ", solution)
            break
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()


""" import angr
import claripy

def try_with_length(binary_path, input_len, correct_address, avoid_addresses):
    # Create a symbolic bitvector for angr to try to solve
    flag = claripy.BVS('flag', 8 * input_len)

    # Create an angr project
    project = angr.Project(binary_path, auto_load_libs=False)

    # Define the entry state with the symbolic input
    entry_state = project.factory.entry_state(args=[binary_path, flag])

    # Add constraints for the input
    for byte in flag.chop(8):
        entry_state.solver.add(byte >= ord(' '))
        entry_state.solver.add(byte <= ord('~'))

    # Create a simulation manager
    simulation = project.factory.simgr(entry_state)

    # Explore the binary
    simulation.explore(find=correct_address, avoid=avoid_addresses)

    return simulation

def main():
    binary_path = 'path/to/your/binary'
    correct_address = 0xADDRESS  # Replace with the actual address
    avoid_addresses = [0xAddress1, 0xAddress2, 0xAddress3]  # Replace with actual addresses

    min_length = 20  # Adjust as needed
    max_length = 100  # Adjust as needed

    for input_len in range(min_length, max_length + 1):
        print(f"Trying with input length: {input_len}")
        simulation = try_with_length(binary_path, input_len, correct_address, avoid_addresses)

        if simulation.found:
            solution_state = simulation.found[0]
            solution = solution_state.solver.eval(flag, cast_to=bytes)
            print("Correct flag: ", solution)
            break
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()
 """