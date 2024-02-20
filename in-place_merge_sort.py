import math
import random


def insertion_sort(arr, start, end, step, reverse=False):
    if end - start < 1:
        return
    if reverse:
        comp = lambda x, y: x > y
    else:
        comp = lambda x, y: x < y
    for j in range(start + step, end + 1, step):
        i = j
        while i > start and comp(arr[i], arr[i - step]):
            arr[i], arr[i - step] = arr[i - step], arr[i]
            i -= step


def shell_sort(arr, start, end, reverse=False):
    n = end - start + 1
    if n == 0:
        return
    k_p = [2 ** k - 1 for k in range(math.floor(math.log(n, 2)), 0, -1)]
    for k in range(len(k_p)):
        insertion_sort(arr, start, end, k_p[k], reverse)

def buff_merge(nums, left, mid_start, mid_end, right, buff):
    i, j = 0, 0
    # print(f"Left: {nums[left: mid_start]}")
    # print(f"Right: {nums[mid_end: right]}")
    # print(f"Buffer: {nums[buff:]}")
    # print(f"Nums before: {nums}")
    while left + i < mid_start and mid_end + j < right:
        if nums[left + i] <= nums[mid_end + j]:
            nums[buff], nums[left + i] = nums[left + i], nums[buff]
            i += 1
        else:
            nums[buff], nums[mid_end + j] = nums[mid_end + j], nums[buff]
            j += 1
        buff += 1
    while left + i < mid_start:
        nums[buff], nums[left + i] = nums[left + i], nums[buff]
        i += 1
        buff += 1
    while mid_end + j < right:
        nums[buff], nums[mid_end + j] = nums[mid_end + j], nums[buff]
        j += 1
        buff += 1
    # print(f"Nums after: {nums}\n")


def buff_msort(nums, l, r, buff):
    if r - l > 1:
        # m = (l + r) // 2
        m = l + (r - l) // 2
        inplace_msort(nums, l, m)
        inplace_msort(nums, m, r)
        buff_merge(nums, l, m, m, r, buff)
    elif l <= r:
        nums[l], nums[buff] = nums[buff], nums[l]


def inplace_msort(nums, l, r):
    if r - l > 1:
        # m = (l + r) // 2
        m = l + (r - l) // 2
        buff = l + r - m        # buff = m + (l + r) % 2
        buff_msort(nums, l, m, buff)
        while buff - l > 2:
            t = buff
            buff = l + (t - l + 1) // 2
            # buff = l + (t - l) // 2
            buff_msort(nums, buff, t, l)
            buff_merge(nums, l, l + t - buff, t, r, buff)
        insertion_sort(nums, l, r - 1, 1)

    # print(f"Sorting {nums[]}")



# nums = [13, 99, 51, 28, 91, 30, 34, 111, 56, 22, 37, 12, 1, 5, 15, 60]
nums = [13, 99, 51, 28, 91, 30, 34, 111, 1, 5]
# nums = [5, 1, 6, 3, 9]
# nums = [5, 1, 6, 3]
inplace_msort(nums, 0, len(nums))
print(nums)
