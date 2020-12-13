"""

"""

from math import ceil

from ortools.linear_solver import pywraplp


def read_file():
    with open("./input.txt", mode="r") as file_pointer:
        lines = file_pointer.read().split("\n")
        earliest_departure = int(lines[0])
        bus_schedule = tuple(
            int(val) if val != "x" else None for val in lines[1].split(",")
        )
        return earliest_departure, bus_schedule


def solve_part_one(earliest_departure, bus_schedule):
    bus_schedule = tuple(val for val in bus_schedule if val)
    waiting_times = tuple(
        (
            bus * ceil(earliest_departure / bus) % earliest_departure
            for bus in bus_schedule
        )
    )
    return min(waiting_times) * bus_schedule[waiting_times.index(min(waiting_times))]


def solve_part_two(bus_schedule):
    constraints = tuple((val, i) for i, val in enumerate(bus_schedule) if val)
    solver = pywraplp.Solver.CreateSolver("SCIP")

    infinity = solver.infinity()
    t = solver.IntVar(100_000_000_000_000, infinity, "t")
    # t = solver.IntVar(0.0, infinity, "t")
    variables = tuple(
        solver.IntVar(0.0, infinity, f"x{i}") for i in range(len(constraints))
    )
    print("Number of variables =", solver.NumVariables())

    for var, (multiplier, offset) in zip(variables, constraints):
        solver.Add(t == multiplier * var - offset)
    # solver.Add(t >= 1)
    print("Number of constraints =", solver.NumConstraints())

    solver.Minimize(t)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("Objective value =", solver.Objective().Value())
        print("t =", t.solution_value())
        for var in variables:
            print(f"{var.name()} = {var.solution_value()}")
    else:
        print("The problem does not have an optimal solution.")

    print("\nAdvanced usage:")
    print("Problem solved in %f milliseconds" % solver.wall_time())
    print("Problem solved in %d iterations" % solver.iterations())
    print("Problem solved in %d branch-and-bound nodes" % solver.nodes())

    return t.solution_value()


if __name__ == "__main__":
    earliest_departure, bus_schedule = read_file()
    solution_1 = solve_part_one(earliest_departure, bus_schedule)
    # assert solution_1 == 2382
    print(f"The solution to part 1 is '{solution_1}'.")
    solution_2 = solve_part_two(bus_schedule)
    print(f"The solution to part 2 is '{solution_2}'.")
