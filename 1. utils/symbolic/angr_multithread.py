import angr
import claripy
import concurrent.futures

def attempt_flag(binary_path, input_len, correct_address, avoid_addresses):
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
        return solution
    return None

def main():
    binary_path = 'notsohandy'
    correct_address = 0x1422
    avoid_addresses = [0x1433, 0x13dc, 0x12a5]
    min_length = 30
    max_length = 70

    num_threads = 4

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(attempt_flag, binary_path, input_len, correct_address, avoid_addresses)
                   for input_len in range(min_length, max_length + 1)}

        for future in concurrent.futures.as_completed(futures):
            solution = future.result()
            if solution:
                print("Correct flag: ", solution)
                return  # Exit as soon as one solution is found

    print("No solution found.")

if __name__ == '__main__':
    main()
