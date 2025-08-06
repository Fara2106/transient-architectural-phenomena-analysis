#include <iostream>

int main(int argc, char* argv[])
{
    if (argc < 2) {
        std::cerr << "Inserire dimensione array\n";
        return 1;
    }

    uint64_t  SIZE = 1 << (std::atoi(argv[1]));
    int N_ITER = 100'000'000;

    std::cout << "Size: " << SIZE << " bytes\n";

    char* array = new char[SIZE];

    for (int i = 0; i < SIZE; i++){
        array[i] = 0;
    }
    
    srand(time(NULL));
    for (int n = 0; n < N_ITER; n++) {
        int idx = rand() % SIZE;
        array[idx] += idx;
    }

    delete[] array;

    return 0;
}
