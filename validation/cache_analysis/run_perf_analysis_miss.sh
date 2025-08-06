OUTPUT_DIR="./output_cache_miss_analysis"
mkdir -p ${OUTPUT_DIR} # Crea cartella "output_cache_miss_analysis" se non esiste

# L1 miss (fino a 32 KB)
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_1.txt ./random_access_array 1 > /dev/null #1 byte
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_2.txt ./random_access_array 2 > /dev/null #2 byte ...
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_3.txt ./random_access_array 3 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_4.txt ./random_access_array 4 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_5.txt ./random_access_array 5 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_6.txt ./random_access_array 6 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_7.txt ./random_access_array 7 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_8.txt ./random_access_array 8 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_9.txt ./random_access_array 9 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_10.txt ./random_access_array 10 > /dev/null #1 KB ...
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_11.txt ./random_access_array 11 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_12.txt ./random_access_array 12 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_13.txt ./random_access_array 13 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_14.txt ./random_access_array 14 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_15.txt ./random_access_array 15 > /dev/null #32 KB
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_16.txt ./random_access_array 16 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_17.txt ./random_access_array 17 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_18.txt ./random_access_array 18 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_19.txt ./random_access_array 19 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_20.txt ./random_access_array 20 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_21.txt ./random_access_array 21 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_22.txt ./random_access_array 22 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_23.txt ./random_access_array 23 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_24.txt ./random_access_array 24 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_25.txt ./random_access_array 25 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_26.txt ./random_access_array 26 > /dev/null 
perf stat -r 10 -e mem_load_retired.l1_miss --output ${OUTPUT_DIR}/L1_misses_27.txt ./random_access_array 27 > /dev/null #128 MB


# L2 miss (da 32 KB a 256 KB)
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_1.txt ./random_access_array 1 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_2.txt ./random_access_array 2 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_3.txt ./random_access_array 3 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_4.txt ./random_access_array 4 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_5.txt ./random_access_array 5 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_6.txt ./random_access_array 6 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_7.txt ./random_access_array 7 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_8.txt ./random_access_array 8 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_9.txt ./random_access_array 9 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_10.txt ./random_access_array 10 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_11.txt ./random_access_array 11 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_12.txt ./random_access_array 12 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_13.txt ./random_access_array 13 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_14.txt ./random_access_array 14 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_15.txt ./random_access_array 15 > /dev/null #32 KB
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_16.txt ./random_access_array 16 > /dev/null #64 KB
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_17.txt ./random_access_array 17 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_18.txt ./random_access_array 18 > /dev/null #256 KB
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_19.txt ./random_access_array 19 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_20.txt ./random_access_array 20 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_21.txt ./random_access_array 21 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_22.txt ./random_access_array 22 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_23.txt ./random_access_array 23 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_24.txt ./random_access_array 24 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_25.txt ./random_access_array 25 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_26.txt ./random_access_array 26 > /dev/null 
perf stat -r 10 -e mem_load_retired.l2_miss --output ${OUTPUT_DIR}/L2_misses_27.txt ./random_access_array 27 > /dev/null 


#L3 miss (da 256 KB a 16 MB)
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_1.txt ./random_access_array 1 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_2.txt ./random_access_array 2 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_3.txt ./random_access_array 3 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_4.txt ./random_access_array 4 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_5.txt ./random_access_array 5 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_6.txt ./random_access_array 6 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_7.txt ./random_access_array 7 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_8.txt ./random_access_array 8 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_9.txt ./random_access_array 9 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_10.txt ./random_access_array 10 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_11.txt ./random_access_array 11 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_12.txt ./random_access_array 12 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_13.txt ./random_access_array 13 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_14.txt ./random_access_array 14 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_15.txt ./random_access_array 15 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_16.txt ./random_access_array 16 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_17.txt ./random_access_array 17 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_18.txt ./random_access_array 18 > /dev/null #256KB
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_19.txt ./random_access_array 19 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_20.txt ./random_access_array 20 > /dev/null #1MB
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_21.txt ./random_access_array 21 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_22.txt ./random_access_array 22 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_23.txt ./random_access_array 23 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_24.txt ./random_access_array 24 > /dev/null #16 MB
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_25.txt ./random_access_array 25 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_26.txt ./random_access_array 26 > /dev/null
perf stat -r 10 -e mem_load_retired.l3_miss --output ${OUTPUT_DIR}/L3_misses_27.txt ./random_access_array 27 > /dev/null


