#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void swap(long *x, long *y) {
    long z = *x;
    *x = *y;
    *y = z;
}

void xor_swap(long *x, long *y) {
    *x = *x ^ *y;
    *y = *y ^ *x;
    *x = *x ^ *y;
}

long *lomuto_partition_branchfree(long *first, long *last) {
    assert(first <= last);
    if (last - first < 2)
        return first;
    --last;
    if (*first > *last)
        swap(first, last);
    long *pivot_pos = first;
    long pivot = *first;
    do {
        ++first;
        assert(first <= last);
    } while (*first < pivot);
    for (long *read = first + 1; read < last; ++read) {
        long x = *read;
        long smaller = -((int) (x < pivot));
        long delta = smaller & (read - first);
        first[delta] = *first;
        read[-delta] = x;
        first -= smaller;
    }
    assert(*first >= pivot);
    --first;
    *pivot_pos = *first;
    *first = pivot;
    return first;
}

long *hoare_partition(long *first, long *last) {
    assert(first <= last);
    if (last - first < 2)
        return first; // nothing interesting to do
    --last;
    if (*first > *last)
        swap(first, last);
    long *pivot_pos = first;
    long pivot = *pivot_pos;
    for (;;) {
        ++first;
        long f = *first;
        while (f < pivot)
            f = *++first;
        long l = *last;
        while (pivot < l)
            l = *--last;
        if (first >= last)
            break;
        *first = l;
        *last = f;
        --last;
    }
    --first;
    swap(first, pivot_pos);
    return first;
}

long *lomuto_partition_branchy(long *first, long *last) {
    assert(first <= last);
    if (last - first < 2)
        return first; // nothing interesting to do
    long *pivot_pos = first;
    long pivot = *first;
    ++first;
    for (long *read = first; read < last; ++read) {
        if (*read < pivot) {
            swap(read, first);
            ++first;
        }
    }
    --first;
    swap(first, pivot_pos);
    return first;
}

double sample_mean(double *x_i, size_t n) {
    double sum = 0;
    for (size_t i = 0; i < n; i++) {
        sum += x_i[i];
    }
    return (1.0 / n) * sum;
}

double geom_mean(double *x_i, size_t n) {
    double pr = 1;
    for (size_t i = 0; i < n; i++) {
        pr *= x_i[i];
    }
    return pow(pr, 1.0 / n);
}

void quickSort(long *first, long *last, void (*swap)(long *, long *)) {
    assert(first <= last);
    if (first < last) {
        long *pivot = lomuto_partition_branchfree(first, last);
        quickSort(first, pivot, swap);
        quickSort(pivot + 1, last, swap);
    }
}

int main(void) {
    clock_t t;
    size_t arr_sz = 50000000;
    void (*tswap)(long *, long *) = &swap;
    void (*xswap)(long *, long *) = &xor_swap;
#define K 1
    double bresults1[K] = {0};
    double bresults2[K] = {0};
    srand((unsigned) time(NULL));
    for (size_t i = 0; i < K; i++) {
        long *arr = (long *) malloc(sizeof(long) * arr_sz);
        long *arr1 = (long *) malloc(sizeof(long) * arr_sz);
        assert(arr);
        for (size_t i = 0; i < arr_sz; i++) {
            long r = rand() % 100000000 + 10000000;
            arr[i] = r;
            arr1[i] = r;
        }
        t = clock();
        quickSort(arr, arr + arr_sz, tswap);
        t = clock() - t;
        double time_taken = ((double) t / CLOCKS_PER_SEC);
        bresults1[i] = time_taken;

        t = clock();
        quickSort(arr1, arr1 + arr_sz, xswap);
        t = clock() - t;
        time_taken = ((double) t / CLOCKS_PER_SEC);
        bresults2[i] = time_taken;
        free(arr);
        free(arr1);
    }
    printf("%f %f\n", sample_mean(bresults1, K), geom_mean(bresults1, K));
    printf("%f %f\n", sample_mean(bresults2, K), geom_mean(bresults2, K));
    return 0;
}
