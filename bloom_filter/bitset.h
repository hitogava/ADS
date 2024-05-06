#include "utils.h"
#pragma once

typedef struct {
    int8_t *content;
    size_t n_bits;
} Bitset;

void bitset_init(Bitset *bitset, size_t n) {
    bitset->n_bits = n;
    bitset->content = (int8_t *)calloc(n / 8 + 1, BYTE);
    MEM_ALLOC_GUARD(bitset->content)
}

int8_t bitset_bit_mask(Bitset *bitset, size_t bit) {
    size_t index = bit / 8 * sizeof(int8_t);
    size_t target_bit = bit - index * 8 * sizeof(int8_t);
    assert(target_bit < 8);
    int8_t mask = 0x1 << (8 - target_bit - 1);
    return mask;
}

void bitset_set(Bitset *bitset, size_t bit) {
    assert (bitset);
    if (bit >= bitset->n_bits) {
        return;
    }
    int8_t mask = bitset_bit_mask(bitset, bit);
    bitset->content[bit / 8 * sizeof(int8_t)] |= mask;
}

bool bitset_is_set(Bitset *bitset, size_t bit) {
    int8_t mask = bitset_bit_mask(bitset, bit);
    return bitset->content[bit / 8 * sizeof(int8_t)] & mask;
}

void bitset_drop(Bitset *bitset) {
    free(bitset->content);
}
