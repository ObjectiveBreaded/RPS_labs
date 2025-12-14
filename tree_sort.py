def tree_sort(arr):
    if len(arr) <= 1:
        return arr

    root = arr[0]

    left = []
    for x in arr[1:]:
        if x < root:
            left.append(x)

    right = []
    for x in arr[1:]:
        if x >= root:
            right.append(x)

    return tree_sort(left) + [root] + tree_sort(right)