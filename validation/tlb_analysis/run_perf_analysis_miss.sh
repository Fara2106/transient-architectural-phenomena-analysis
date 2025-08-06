OUTPUT_DIR="./output_TLB_miss_analysis"
mkdir -p ${OUTPUT_DIR}  # Crea la cartella se non esiste

# Monitoraggio delle miss per le operazioni di "load"
    # dTLB_load_misses.stlb_hit: Miss al primo livello (DTLB) per le load che viene risolta dal secondo livello (STLB). QUINDI SONO SOLO LE MISS IN L1 che fanno hit in
    # L2.
    # dTLB_load_misses.miss_causes_a_walk: Miss a tutti i livelli (DTLB + STLB) per le load, che causa un page walk. MISS SIA IN L1 (una parte) CHE L2, quindi
    # corrisponde al numero di miss in L2.
    # Quindi per trovare le miss in L1 = dTLB_load_misses.miss_causes_a_walk + dTLB_load_misses.stlb_hit.
# Monitoraggio delle miss per le operazioni di "store"
    # dTLB_store_misses.stlb_hit: Miss al primo livello (DTLB) per le store che viene risolta dal secondo livello (STLB). QUINDI SONO SOLO LE MISS IN L1 che fanno hit in
    # L2.
    # dTLB_store_misses.miss_causes_a_walk: Miss a tutti i livelli (DTLB + STLB) per le store, che causa un page walk. MISS SIA IN L1 (una parte) CHE L2, quindi
    # corrisponde al numero di miss in L2.
    # Quindi per trovare le miss in L1 = dTLB_store_misses.miss_causes_a_walk + dTLB_store_misses.stlb_hit.

perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_1.txt ./random_access_array 1 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_2.txt ./random_access_array 2 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_4.txt ./random_access_array 4 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_8.txt ./random_access_array 8 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_16.txt ./random_access_array 16 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_32.txt ./random_access_array 32 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_64.txt ./random_access_array 64 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_128.txt ./random_access_array 128 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_256.txt ./random_access_array 256 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_512.txt ./random_access_array 512 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_1024.txt ./random_access_array 1024 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_2048.txt ./random_access_array 2048 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_4096.txt ./random_access_array 4096 > /dev/null 
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_8192.txt ./random_access_array 8192 > /dev/null
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_16384.txt ./random_access_array 16384 > /dev/null
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_32768.txt ./random_access_array 32768 > /dev/null
perf stat -r 10 -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk --output ${OUTPUT_DIR}/miss_65536.txt ./random_access_array 65536 > /dev/null


