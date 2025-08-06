OUTPUT_DIR="./output_time_TLB"
mkdir -p ${OUTPUT_DIR} 

perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_1.txt ./random_access_array 1 > /dev/null #1 pagina
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_2.txt ./random_access_array 2 > /dev/null 
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_4.txt ./random_access_array 4 > /dev/null 
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_8.txt ./random_access_array 8 > /dev/null 
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_16.txt ./random_access_array 16 > /dev/null 
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_32.txt ./random_access_array 32 > /dev/null 
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_64.txt ./random_access_array 64 > /dev/null #64 pagine
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_128.txt ./random_access_array 128 > /dev/null 
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_256.txt ./random_access_array 256 > /dev/null 
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_512.txt ./random_access_array 512 > /dev/null
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_5024.txt ./random_access_array 5024 > /dev/null 
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_2048.txt ./random_access_array 2048 > /dev/null 
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_4096.txt ./random_access_array 4096 > /dev/null
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_8192.txt ./random_access_array 8192 > /dev/null
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_16384.txt ./random_access_array 16384 > /dev/null
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_32768.txt ./random_access_array 32768 > /dev/null
perf stat -r 50 -e duration_time --output ${OUTPUT_DIR}/time_65536.txt ./random_access_array 65536 > /dev/null 






