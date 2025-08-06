#include <iostream>

int main(int argc, char* argv[])
{
    if (argc < 2) {
        std::cerr << "Inserire numero di pagine da allocare\n";
        return 1;
    }

    uint64_t  n_pages = (std::atoi(argv[1]));
    int N_ITER = 100'000'000;

    std::cout << "Pages number: " << n_pages << " pages\n";

    const uint64_t DIM_PAGE = 4096; //ogni pagina è 4096 byte = 4 KB
    const uint64_t SIZE = DIM_PAGE * n_pages;

    char* array = new char[SIZE]; 
    for (int i = 0; i < SIZE; i++){
        array[i] = 0;
    }
    
    srand(time(NULL));
    for (int n = 0; n < N_ITER; n++) {
        int idx = (rand() % SIZE >> 12) << 12; //indirizzo di pagina
        array[idx] += idx;
    }

    delete[] array;

    return 0;
}
