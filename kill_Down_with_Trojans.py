import numpy as np
import scipy


def load_input_file(file_name):
    with open(file_name, 'r') as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)

# TODO:
# all H +
# all D +
# all H and D +
# protector token +?
# the other token +?

# tautology: go right or down
# subproblems: coords, protector (have or not), multiplier (have or not)

def DP(n, H, tile_types, tile_values, memo):
    
    if n == 0 or n == 1:
        return True

    # if it works for going right first, don't even bother solving the way going down
    # if I want best path, then can easily change this
    return (H + DPhelper(n, H, tile_types, tile_values, 0, 1, 0, 0, memo) >= 0) or (H + DPhelper(n, H, tile_types, tile_values, 1, 0, 0, 0, memo) >= 0)

def DPhelper(n, H, tile_types, tile_values, row, col, protector, multiplier, memo):

    # you died.
    if H < 0:
        return -np.Inf
    
    # out of bounds
    if row >= n or col >= n:
        return -np.Inf
    
    curr_type = tile_types[row][col]
    
    match curr_type:
        case 0: # damage
            net_H = -tile_values[row][col]
        case 1: # healing
            net_H = tile_values[row][col]
        case 2: # protection
            net_H = 0 # protect tiles don't have value, but just in case
            protector = 1
        case 3: # multiplier
            net_H = 0 # multiplier tiles don't have value, but just in case
            multiplier = 1

    if row == n - 1 and col == n - 1:
        if protector and curr_type == 0: # if have protection and last tile is damage tile
            return 0
        if multiplier and curr_type == 1: # if have multiplier and last tile is healing tile
            return net_H * 2
        return net_H
    if not np.isnan(memo[row][col][protector][multiplier]):
        return memo[row][col][protector][multiplier]
    
    # no tokens used on current tile
    go_right = DPhelper(n, H + net_H, tile_types, tile_values, row, col + 1, protector, multiplier, memo) + net_H
    go_down = DPhelper(n, H + net_H, tile_types, tile_values, row + 1, col, protector, multiplier, memo) + net_H

    # current tile is damage type, we have protector, and we use it
    if protector and curr_type == 0:
        protect_then_right = DPhelper(n, H, tile_types, tile_values, row, col + 1, 0, multiplier, memo)
        protect_then_down = DPhelper(n, H, tile_types, tile_values, row + 1, col, 0, multiplier, memo)

        go_right = max(go_right, protect_then_right)
        go_down = max(go_down, protect_then_down)

    # current tile is healing type, we have multiplier, and we use it
    if multiplier and curr_type == 1:
        mult_then_right = DPhelper(n, H + 2 * net_H, tile_types, tile_values, row, col + 1, protector, 0, memo) + net_H * 2
        mult_then_down = DPhelper(n, H + 2 * net_H, tile_types, tile_values, row + 1, col, protector, 0, memo) + net_H * 2

        go_right = max(go_right, mult_then_right)
        go_down = max(go_down, mult_then_down)

    memo[row][col][protector][multiplier] = max(go_right, go_down)

    return memo[row][col][protector][multiplier]


def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    memo = np.zeros((n, n, 2, 2))
    memo[:] = np.nan
    result = DP(n, H, tile_types, tile_values, memo)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)
    # print(memo)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])
