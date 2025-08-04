
OUTPUT_DIR="./output_time_analysis"
mkdir -p ${OUTPUT_DIR} # Crea cartella "output_time_analysis" se non esiste
PERF_OPTIONS="-e duration_time -r 20"
#-r 20 sono le ripetizioni
#$ prende il valore della varabile
#"> /dev/null direziona ad un file null"

perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_1.txt ./random_access_array 1 > /dev/null 
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_2.txt ./random_access_array 2 > /dev/null 
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_3.txt ./random_access_array 3 > /dev/null 
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_4.txt ./random_access_array 4 > /dev/null 
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_5.txt ./random_access_array 5 > /dev/null 
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_6.txt ./random_access_array 6 > /dev/null 
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_7.txt ./random_access_array 7 > /dev/null 
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_8.txt ./random_access_array 8 > /dev/null 
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_9.txt ./random_access_array 9 > /dev/null 
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_10.txt ./random_access_array 10 > /dev/null 
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_11.txt ./random_access_array 11 > /dev/null 
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_12.txt ./random_access_array 12 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_13.txt ./random_access_array 13 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_14.txt ./random_access_array 14 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_15.txt ./random_access_array 15 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_16.txt ./random_access_array 16 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_17.txt ./random_access_array 17 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_18.txt ./random_access_array 18 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_19.txt ./random_access_array 19 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_20.txt ./random_access_array 20 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_21.txt ./random_access_array 21 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_22.txt ./random_access_array 22 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_23.txt ./random_access_array 23 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_24.txt ./random_access_array 24 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_25.txt ./random_access_array 25 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_26.txt ./random_access_array 26 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_27.txt ./random_access_array 27 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_28.txt ./random_access_array 28 > /dev/null
perf stat $PERF_OPTIONS --output ${OUTPUT_DIR}/output_29.txt ./random_access_array 29 > /dev/null

