#include "faasm/faasm.h"
#include <stdlib.h>
#include <stdio.h>

void _do_bad_malloc(void) {
    int *x = (int *) malloc(10 * sizeof(int));
    x[10] = 0;        // problem 1: heap block overrun

    printf("x[5] = %i\n", x[5]);
}                    // problem 2: memory leak -- x not freed


FAASM_MAIN_FUNC() {
    _do_bad_malloc();
    return 0;
}
