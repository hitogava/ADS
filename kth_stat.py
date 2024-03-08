import random


def partition(nums, i, j):
    pivot = nums[random.randint(i, j)]
    t = i
    while t <= j:
        if nums[t] < pivot:
            nums[t], nums[i] = nums[i], nums[t]
            t += 1
            i += 1
        elif nums[t] > pivot:
            nums[t], nums[j] = nums[j], nums[t]
            j -= 1
        else:
            t += 1
    return j


def kth(nums, l, r, k):
    if l == r:
        return nums[l]
    p = partition(nums, l, r)
    if p + 1 == k:
        return nums[p]
    elif p + 1 > k:
        return kth(nums, l, p - 1, k)
    else:
        return kth(nums, p + 1, r, k)


def naiveMin(stations):
    results = []
    for i in range(len(stations)):
        sm = 0
        for j in range(len(stations)):
            sm += abs(stations[i] - stations[j])
        results.append((stations[i], sm))
    return min(results, key=lambda x: x[1])[0]


station_ys = [7, 9, 2, 1, 6, 4, 3]
n = len(station_ys)
print(kth(station_ys, 0, n - 1, n // 2 + 1))
print(naiveMin(station_ys))

station_ys = [12, 8, 5, 1]
n = len(station_ys)
print(kth(station_ys, 0, n - 1, n // 2))
print(naiveMin(station_ys))
