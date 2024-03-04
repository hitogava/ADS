#include "vector.h"
#include <stdio.h>

VECTOR(int);

int vector_int_at(vector_int *vec, size_t index) {
    int *ith = at(vec, index);
    if (!ith) {
        printf("Vector out of boundary error\n");
        exit(1);
    }
    return *ith;
}
void vector_int_print(vector_int *vec) {
    assert(vec && vec->data);
    for (size_t i = 0; i < vec->len; i++) {
        printf("%d ", vector_int_at(vec, i));
        if (i == vec->len - 1)
            printf("\n");
    }
}

int main(void) {
    vector_int *vec = halloc_vector_int();
    for (size_t i = 0; i < 100; i++) {
        vector_int_add_last(vec, i);
        printf("Length: %zu, capacity: %zu\n", vec->len, vec->cap);
    }
    for (size_t i = 0; i < 100; i++) {
        vector_int_remove_last(vec);
        printf("Length: %zu, capacity: %zu\n", vec->len, vec->cap);
    }
    free(vec->data);
    free(vec);
    return 0;
}
