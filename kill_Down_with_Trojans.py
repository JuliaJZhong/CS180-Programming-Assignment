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

# idea: store the min amount of health needed to get from a spot to the end alive
# TODO protector, multiplier, both

def DP(n, H, tile_types, tile_values, memo):

    if n == 0 or n == 1:
        return True

    # if going right first works, then don't even need to go down
    return helper(n, H, tile_types, tile_values, 0, 1, 0, 0, memo) <= H or helper(n, H, tile_types, tile_values, 1, 0, 0, 0, memo) <= H


def helper(n, H, tile_types, tile_values, row, col, protector, multiplier, memo):

    if row >= n or col >= n:
        return np.Inf
    
    if not np.isnan(memo[row][col][protector][multiplier]):
        return memo[row][col][protector][multiplier]
    
    curr_type = tile_types[row][col]

    match curr_type:
        case 0: # damage
            curr_value = -tile_values[row][col]
        case 1: # healing
            curr_value = tile_values[row][col]
        case 2: # protector
            curr_value = 0
            protector = 1
        case 3: # multiplier
            curr_value = 0
            multiplier = 1

    if row == n - 1 and col == n - 1:
        if protector and curr_type == 0:
            curr_value = 0
        elif multiplier and curr_type == 1: # this is actually unnecessary. if last tile is healing, then memo stores 0 hp needed in that spot
            curr_value = curr_value * 2
        memo[row][col][protector][multiplier] = max(-curr_value, 0)
        return memo[row][col][protector][multiplier]
    
    # don't use any token on current tile, regardless of whether you have or not
    right = helper(n, H, tile_types, tile_values, row, col + 1, protector, multiplier, memo) - curr_value
    down = helper(n, H, tile_types, tile_values, row + 1, col, protector, multiplier, memo) - curr_value

    # current tile is damage, have protector token and use it
    if protector and curr_type == 0:
        protect_then_right = helper(n, H, tile_types, tile_values, row, col + 1, 0, multiplier, memo)
        protect_then_down = helper(n, H, tile_types, tile_values, row + 1, col, 0, multiplier, memo)

        right = min(right, protect_then_right)
        down = min(down, protect_then_down)

    # current tile is healing, have multiplier token and use it
    if multiplier and curr_type == 1:
        mult_then_right = helper(n, H, tile_types, tile_values, row, col + 1, protector, 0, memo) - curr_value * 2
        mult_then_down = helper(n, H, tile_types, tile_values, row + 1, col, protector, 0, memo) - curr_value * 2

        right = min(right, mult_then_right)
        down = min(down, mult_then_down)

    memo[row][col][protector][multiplier] = max(min(right, down), 0) # min hp needed from this point onward (cannot go below 0)

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
