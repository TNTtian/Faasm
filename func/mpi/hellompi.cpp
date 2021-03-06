#include <mpi.h>
#include <stdio.h>
#include <faasm/faasm.h>

FAASM_MAIN_FUNC() {
    int res = MPI_Init(NULL, NULL);
    if(res != MPI_SUCCESS) {
        printf("Failed on MPI init\n");
        return 1;
    }

    int rank;
    int world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // Check how big the world is
    if (world_size < 2) {
        printf("World size must be greater than 1\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    int number;
    if (rank == 0) {
        number = -1;
        MPI_Send(&number, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
    }
//    else if (world_rank == 1) {
//        MPI_Recv(&number, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
//        printf("Process 1 received number %d from process 0\n", number);
//    }

    MPI_Finalize();

    return 0;
} 