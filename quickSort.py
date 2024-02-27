import random


def HoarePartition(nums, i, j):
    pivot = nums[random.randint(i, j)]
    while i <= j:
        if nums[i] >= pivot:
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
            j -= 1
        else:
            if nums[j] > pivot:
                j -= 1
            i += 1
    return j


def LomutosPartition(nums, i, j):
    pInd = random.randint(i, j)
    pivot = nums[pInd]
    nums[pInd], nums[i] = nums[i], nums[pInd]
    l, h, c = (i, i, i + 1)

    while c <= j:
        if nums[c] < pivot:
            tmp = nums[c]
            nums[c] = nums[h + 1]
            nums[h + 1] = nums[l]
            nums[l] = tmp
            l += 1
            h += 1
            c += 1
        elif nums[c] == pivot:
            nums[c], nums[h + 1] = nums[h + 1], nums[c]
            c += 1
            h += 1
        else:
            c += 1
    print(nums, l, h)
    return (l, h)


def quickSort(nums, l, r):
    if l >= r:
        return
    # pivot = HoarePartition(nums, l, r)
    pivot = LomutosPartition(nums, l, r)
    quickSort(nums, l, pivot[0] - 1)
    quickSort(nums, pivot[1] + 1, r)


nums = [2, 5, 3, 4, 1, 33, 2, 12]
quickSort(nums, 0, len(nums) - 1)
print(nums)
nums = [1, 1, 1, 1]
quickSort(nums, 0, len(nums) - 1)
print(nums)
nums = [3, 2, 1, 0]
quickSort(nums, 0, len(nums) - 1)
print(nums)
nums = [3, 1]
quickSort(nums, 0, len(nums) - 1)
print(nums)
