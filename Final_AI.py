import numpy as np
import copy
import random
import sys
import time


invalid = {1: 38, 4: 14, 16: 6, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100, 98: 78, 95: 75, 93: 73, 87: 24,
           64: 60, 62: 19, 56: 53, 49: 11, 48: 26}

def update(matrix, cur, dice):
    matrix[cur][cur] = 1
    if cur == 100:
        return
    if dice == 0:
        if cur + 4 < 100:
            if cur+4 in list(invalid.keys()):
                matrix[cur][invalid[cur+4]] -= 2 / 3
            else:
                matrix[cur][cur+4] -= 2 / 3
            if cur in list(invalid.keys()):
                matrix[cur][invalid[cur]] -= 1 / 3
            else:
                matrix[cur][cur] -= 1 / 3
        elif cur < 100:
            matrix[cur][100] = -2 / 3
            if cur in list(invalid.keys()):
                matrix[cur][invalid[cur]] -= 1 / 3
            else:
                matrix[cur][cur] -= 1 / 3
    elif dice == 1:
        if cur + 6 < 100:
            if cur+6 in list(invalid.keys()):
                matrix[cur][invalid[cur+6]] -= 1 / 3
            else:
                matrix[cur][cur+6] -= 1 / 3
            if cur+2 in list(invalid.keys()):
                matrix[cur][invalid[cur+2]] -= 2 / 3
            else:
                matrix[cur][cur+2] -= 2 / 3
        elif cur + 2 < 100:
            matrix[cur][100] = -1 / 3
            if cur + 2 in list(invalid.keys()):
                matrix[cur][invalid[cur + 2]] -= 2 / 3
            else:
                matrix[cur][cur + 2] -= 2 / 3
        else:
            matrix[cur][100] = -1
    elif dice == 2:
        if cur + 5 < 100:
            if cur+5 in list(invalid.keys()):
                matrix[cur][invalid[cur+5]] -= 1 / 2
            else:
                matrix[cur][cur+5] -= 1 / 2
            if cur+1 in list(invalid.keys()):
                matrix[cur][invalid[cur+1]] -= 1 / 2
            else:
                matrix[cur][cur+1] -= 1 / 2
        elif cur + 1 < 100:
            matrix[cur][100] = -1 / 2
            if cur + 1 in list(invalid.keys()):
                matrix[cur][invalid[cur + 1]] -= 1 / 2
            else:
                matrix[cur][cur + 1] -= 1 / 2
        else:
            matrix[cur][100] = -1
    elif dice == 3:
        if cur + 3 < 100:
            if cur + 3 in list(invalid.keys()):
                matrix[cur][invalid[cur + 3]] -= 1
            else:
                matrix[cur][cur + 3] -= 1
        else:
            matrix[cur][100] = -1


def expected(matrix, policy):
    for i in range(101):
        update(matrix, i, policy[i])

    b = [1 for i in range(101)]
    b[100] = 0


    a = np.asarray(matrix)
    b1 = np.asarray(b)

    try:
        x = np.linalg.solve(a, b1)
        return x
    except np.linalg.LinAlgError as err:
        if 'Singular matrix' in str(err):
            return [float('inf')]

def update_policy(policy, x, matrix_ret):
    count = 0
    for i in range(99, -1, -1):
        for j in range(4):
            matrix_new = [[0 for k in range(101)] for p in range(101)]
            policy_new = copy.deepcopy(policy)
            policy_new[i] = j
            x_new = expected(matrix_new, policy_new)[0]
            if x_new < x:
                count += 1
                matrix_ret = copy.deepcopy(matrix_new)
                policy[i] = j
                x = x_new
    return policy, x, matrix_ret, count

def main():
    policy = [2 for i in range(101)]
    policy_old = copy.deepcopy(policy)
    matrix = []

    x = float('inf')
    count = 0
    policy, x, matrix, count2 = update_policy(policy, x, matrix)
    count += count2
    while policy_old != policy:
        policy_old = copy.deepcopy(policy)
        policy, x, matrix, count2 = update_policy(policy, x, matrix)
        count += count2
    print(count)
    for i in matrix:
        print(i)
    print(policy)
    print(x)
    return x, count, policy

start_time = time.time()
main()
print(time.time() - start_time)





# matrix = [[0 for i in range(101)] for j in range(101)]
# # policy = [1 for i in range(101)]
# # policy = [2, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 0, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 2, 1, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2]
# policy = [2, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 0, 3, 3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3, 1, 2, 0, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3, 3, 2, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2]
# print(expected(matrix, policy))

# x = float("inf")
# for i in range(100):
#     x_new, count_new, policy = main()
#     if x_new < x:
#         print(x_new, x)
#         x = x_new
#         count = count_new
#         print(x, count, policy)


