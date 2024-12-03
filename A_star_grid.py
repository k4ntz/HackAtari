# Python program for A* Search Algorithm
import heapq
from hackatari import HackAtari

# Define the Cell class


class Cell:
    def __init__(self):
        # Parent cell's row index
        self.parent_i = 0
        # Parent cell's column index
        self.parent_j = 0
        # Total cost of the cell (g + h)
        self.f = float("inf")
        # Cost from start to this cell
        self.g = float("inf")
        # Heuristic cost from this cell to destination
        self.h = 0


# Define the size of the grid
ROW = 14
COL = 18

# Check if a cell is valid (within the grid)


def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)


# Check if a cell is unblocked


def is_unblocked(grid, row, col):
    return grid[row][col] == 1


# Check if a cell is the destination


def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]


# Calculate the heuristic value of a cell (Euclidean distance to destination)


def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5


# Trace the path from source to destination


def trace_path(cell_details, dest):
    # print("The Path is ")
    path = []
    row = dest[0]
    col = dest[1]

    # Trace the path from destination to source using parent cells
    while not (
        cell_details[row][col].parent_i == row
        and cell_details[row][col].parent_j == col
    ):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path.append((row, col))
    # Reverse the path to get the path from source to destination
    path.reverse()

    # Print the path
    # for i in path:
    #     print("->", i, end=" ")
    # print()
    return path


# Implement the A* search algorithm


def a_star_search(grid, src, dest):
    # Check if the source and destination are valid
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("Source or destination is invalid")
        return

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(
        grid, dest[0], dest[1]
    ):
        print("Source or the destination is blocked")
        return

    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # For each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # ,
        #   (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the successor is valid, unblocked, and not visited
            if (
                is_valid(new_i, new_j)
                and is_unblocked(grid, new_i, new_j)
                and not closed_list[new_i][new_j]
            ):
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    print("The destination cell is found")
                    # Trace and print the path from source to destination
                    path = trace_path(cell_details, dest)
                    found_dest = True
                    return path
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    if (
                        cell_details[new_i][new_j].f == float("inf")
                        or cell_details[new_i][new_j].f > f_new
                    ):
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    # If the destination is not found after visiting all cells
    if not found_dest:
        print("Failed to find the destination cell")


# Driver Code


def main():
    # Define the grid (1 for unblocked, 0 for blocked)

    grid1 = [
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    grid2 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
        [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    ]

    env = HackAtari("MsPacman", ["maze_man"], "", "", render_mode="human")
    env.reset()
    done = False
    nstep = 1
    # src = None
    dest = None
    pos = None
    path = None
    path_i = 0
    reset = True
    while not done:
        action = 0
        # action = env.action_space.sample()
        x, y = env.objects[0].xy
        i, j = 0, 0
        if x < 80:
            i = x >> 3
        else:
            x -= 84
            i = 9 + (x >> 3) + 1
        j = int((y - 3) / 12)
        pos = [j, i]
        if path is not None:
            try:
                if path[path_i] is None:
                    action = 0
                    path_i += 1
                elif pos[0] < path[path_i][0]:
                    action = 4
                elif pos[0] > path[path_i][0]:
                    action = 1
                elif pos[1] < path[path_i][1]:
                    action = 2
                elif pos[1] > path[path_i][1]:
                    action = 3
                else:
                    path_i += 1
            except:
                # import ipdb; ipdb.set_trace()
                reset = True
                path = None
        elif reset and len(env.objects) > 1:
            op = 0
            for i in range(len(env.objects)):
                try:
                    new_dest = list(env.objects[i].grid_ij)
                    op = i
                    break
                except:
                    new_dest = None
            # new_dest = list(env.objects[1].grid_ij)
            if new_dest != dest:
                print(env.objects[op].grid_ij)
                dest = new_dest
                path = a_star_search(grid1, pos, dest)
                try:
                    path.extend([None] * 5)
                except:
                    pass
                print(pos, dest)
                print(path)
                path_i = 1
                reset = False
        # print(action, pos, path_i)
        obs, reward, terminated, truncated, _ = env.step(action)
        if terminated or truncated:
            env.reset()
        if nstep % 100 == 0:
            print(".", end="", flush=True)
        nstep += 1
        env.render()
    env.close()

    # Define the source and destination
    src = [7, 3]
    dest = [0, 0]

    # Run the A* search algorithm
    a_star_search(grid1, src, dest)


if __name__ == "__main__":
    main()
