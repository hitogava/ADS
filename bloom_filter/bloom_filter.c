#include "bitset.h"

typedef struct {
    unsigned char ip[4];
} IP;

void ip_init(IP *ip, unsigned char b1, unsigned char b2, unsigned char b3, unsigned char b4) {
    ip->ip[0] = b1;
    ip->ip[1] = b2;
    ip->ip[2] = b3;
    ip->ip[3] = b4;
}

int hash_vector(unsigned char *input_vector, int *a_vector, size_t vectors_size, int m) {
    int hash = 0;
    for (size_t i = 0; i < vectors_size; i++) {
        hash  = (hash + input_vector[i] * a_vector[i]) % m;
    }
    assert(hash < m);
    return hash;
}

typedef struct {
    Bitset *bitset;
    size_t n_objects;
    size_t n_hashes;
    double lie_prob;
} BloomFilter;

void bfilter_init(BloomFilter *filter, size_t nbits, size_t nobj, size_t nhashes, double lie_prob) {
    filter->n_objects = nobj;
    filter->n_hashes = nhashes;
    filter->lie_prob = lie_prob;
    filter->bitset = malloc(sizeof(Bitset));
    MEM_ALLOC_GUARD(filter->bitset);
    bitset_init(filter->bitset, nbits);
}

void bfilter_drop(BloomFilter *filter) {
    bitset_drop(filter->bitset);
}

void bfilter_insert(BloomFilter *filter, IP *ip, int *hash_family, size_t vec_size) {
    for (size_t i = 0; i < filter->n_hashes; i++) {
        int hash = hash_vector(ip->ip, hash_family + i * 4, 4, filter->bitset->n_bits);
        bitset_set(filter->bitset, hash);
    }
}

bool bfilter_lookup(BloomFilter *filter, IP *ip, int *hash_family, size_t vec_size) {
    for (size_t i = 0; i < filter->n_hashes; i++) {
        int hash = hash_vector(ip->ip, hash_family + i * 4, 4, filter->bitset->n_bits);
        if (!bitset_is_set(filter->bitset, hash)) {
            return false;
        }
    }
    return true;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        puts("Wrong number of arguments");
        return 1;
    }

    srand(time(NULL));
    long S = atol(argv[1]);
    double lie_pr = atof(argv[2]);
    double ln2 = log(2);
    size_t b = (-log2(lie_pr)) / ln2;
    b += (b == 0);
    size_t k = ln2 * (float)b + 1;
    size_t n = b * S;

    int *a_vector = malloc(sizeof(int) * k * 4);
    MEM_ALLOC_GUARD(a_vector)

    for (size_t i = 0; i < k; i++)
        for (size_t j = 0; j < 4; j++)
            a_vector[i * 4 + j] = rand() % 255;


    BloomFilter *bf = malloc(sizeof(BloomFilter));
    MEM_ALLOC_GUARD(bf);
    bfilter_init(bf, n, S, k, lie_pr);

    IP ip;

    bfilter_drop(bf);
    free(bf);
    free(a_vector);
    return 0;
}
