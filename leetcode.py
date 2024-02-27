import random, math


def insertion_sort(arr, start, end, step, reverse=False):
    n = end - start + 1
    if reverse:
        comp = lambda x, y: x > y
    else:
        comp = lambda x, y: x < y
    # for j in range(start + step, n // step, step):
    for j in range(start + step, end + 1, step):
        i = j
        while i > start and comp(arr[i], arr[i - step]):
            arr[i], arr[i - step] = arr[i - step], arr[i]
            i -= step


def shell_sort(arr, start, end, reverse=False):
    n = end - start + 1
    if n == 0:
        return
    k_p = [2**k - 1 for k in range(math.floor(math.log(n, 2)), 0, -1)]
    for k in range(len(k_p)):
        insertion_sort(arr, start, end, k_p[k], reverse)


def wiggleSort(nums: list[int]) -> None:
    n = len(nums)
    arr = nums.copy()
    shell_sort(arr, 0, n - 1)
    pivot = n // 2
    print(arr)
    for i in range(pivot):
        nums[2 * i] = arr[pivot - i - 1]
    print(nums)
    j = 1
    for i in range(n - 1, pivot - 1, -1):
        nums[j] = arr[i]
        j += 2
    print(nums)
    input()


def merge_and_count_split_inversions(nums, left, mid, right):
    i, j, k = 0, 0, 0
    res = [0] * (right - left)
    while left + i < mid and mid + j < right:
        if nums[left + i] <= nums[mid + j]:
            res[i + j] = nums[left + i]
            i += 1
        else:
            res[i + j] = nums[mid + j]
            k += mid - left - i
            j += 1
    while left + i < mid:
        res[i + j] = nums[left + i]
        i += 1
    while mid + j < right:
        res[i + j] = nums[mid + j]
        j += 1
    for i in range(len(res)):
        nums[left + i] = res[i]
    return k


def count_inversions(nums, left, right):
    if right - left <= 1:
        return 0
    mid = (left + right) // 2
    l = count_inversions(nums, left, mid)
    r = count_inversions(nums, mid, right)
    split = merge_and_count_split_inversions(nums, left, mid, right)
    return l + r + split


def count_local_inversions(nums):
    count = 0
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            count += 1
    return count


def isIdealPermutation(nums: list[int]) -> bool:
    mx = -math.inf
    if nums[0] not in [0, 1] and nums[1] not in [0, 1]:
        return False
    for i in range(len(nums) - 2):
        mx = max(mx, nums[i])
        if mx > nums[i + 2]:
            return False
    return True


def sortColors(nums):
    l = 0
    r = len(nums) - 1
    m = 0
    while m <= r:
        if nums[m] == 0:
            nums[l], nums[m] = nums[m], nums[l]
            m += 1
            l += 1
        elif nums[m] == 2:
            nums[m], nums[r] = nums[r], nums[m]
            r -= 1
        else:
            m += 1
    print(nums)


sortColors([2, 0, 2, 1, 1, 0])
sortColors([0, 2, 2, 2, 0, 2, 1, 1])
sortColors([1, 0, 2])
sortColors([1, 2, 0])
sortColors([2, 1, 2])
