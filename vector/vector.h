#pragma once
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define begin(dyn_arr) (((dyn_arr)->len) ? (&dyn_arr->data[0]) : (NULL))

#define end(dyn_arr) (((dyn_arr)->len) ? (&(dyn_arr)->data[dyn_arr->len - 1]) : (NULL))

#define at(dyn_arr, ind) ((ind < dyn_arr->len) ? (&(dyn_arr->data[ind])) : (NULL))

void alloc_guard(void* ptr) {
    if (!ptr) {
        printf("Heap allocation error\n");
        exit(1);
    }
}

#define VECTOR(T)                                                                                  \
    typedef struct {                                                                               \
        T* data;                                                                                   \
        size_t len;                                                                                \
        size_t cap;                                                                                \
    } vector_##T;                                                                                  \
                                                                                                   \
    void init_vector_##T(vector_##T* arr) {                                                        \
        arr->data = NULL;                                                                          \
        arr->len = 0;                                                                              \
        arr->cap = 0;                                                                              \
    }                                                                                              \
    vector_##T* halloc_vector_##T(void) {                                                          \
        vector_##T* arr = malloc(sizeof(vector_##T));                                              \
        alloc_guard(arr);                                                                          \
        init_vector_##T(arr);                                                                      \
        return arr;                                                                                \
    }                                                                                              \
    void vector_##T##_ensure_capacity(vector_##T* self, size_t src_len) {                          \
        assert(self);                                                                              \
        size_t nlen = self->len + src_len;                                                         \
        size_t ncap = nlen * 2;                                                                    \
        if (nlen >= self->cap) {                                                                   \
            self->data = realloc(self->data, ncap * sizeof(T));                                    \
            alloc_guard(self->data);                                                               \
            self->cap = ncap;                                                                      \
        }                                                                                          \
        self->len = nlen;                                                                          \
    }                                                                                              \
    void vector_##T##_add_last(vector_##T* self, T value) {                                        \
        vector_##T##_ensure_capacity(self, 1);                                                     \
        self->data[self->len - 1] = value;                                                         \
    }                                                                                              \
    void vector_##T##_shrink(vector_##T* self) {                                                   \
        size_t nlen = self->len - 1;                                                               \
        size_t ncap = self->cap / 2;                                                               \
        if (nlen <= self->cap / 4) {                                                               \
            self->data = realloc(self->data, ncap * sizeof(T));                                    \
            alloc_guard(self->data);                                                               \
            self->cap = ncap;                                                                      \
        }                                                                                          \
    }                                                                                              \
    void vector_##T##_remove(vector_##T* self, size_t ind) {                                       \
        if (self->len == 0)                                                                        \
            return;                                                                                \
        vector_##T##_shrink(self);                                                                 \
        memmove(self->data + ind, self->data + ind + 1, sizeof(T) * (self->len - ind - 1));        \
        self->len--;                                                                               \
    }                                                                                              \
    void vector_##T##_remove_last(vector_##T* self) {                                              \
        assert(self);                                                                              \
        vector_##T##_remove(self, self->len - 1);                                                  \
    }
