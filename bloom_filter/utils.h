#include <stdint.h>
#include <inttypes.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>

#pragma once

#define BYTE (sizeof(char))

#define MEM_ALLOC_GUARD(ptr) \
    if (!(ptr)) { \
        puts("Memory allocation error"); \
        exit (1); } \

