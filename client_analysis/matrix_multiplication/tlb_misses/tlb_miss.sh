PORT=81
OUTPUT_DIR="./perf_results_matrix_tlb_misses"
ITERATIONS=50                 # Numero di iterazioni per il comando perf
CPU_LIST=0                    # Core da stressare
INTERVAL_NS=10                              

# Crea la directory di output se non esiste
mkdir -p $OUTPUT_DIR

echo "Starting cache miss analysis on port $PORT with table size $MATRIX_SIZE..."

# Ciclo per analizzare componente tabella crescente
declare -a matrix_sizes=(
     "1" "2" "4" "8" "16" "32" "64" "128" "256" "512" "1024" "2048" "4096" "8192"
)
for MATRIX_SIZE in "${matrix_sizes[@]}" 
do  
    echo "Analyzing at table size: $MATRIX_SIZE  ($INTERVAL_NS ns per request)..."

    # Genera richieste alla frequenza specificata
    ./send_request $PORT $INTERVAL_NS $MATRIX_SIZE &  # Invia richieste al server
    REQUEST_PID=$!

    # Analisi miss
    L_OUTPUT="$OUTPUT_DIR/misses_${MATRIX_SIZE}.txt"
    perf stat -C $CPU_LIST -r $ITERATIONS -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk,context-switches -- sleep 2 > "$L_OUTPUT" 2>&1
    #perf stat -a -r $ITERATIONS -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk,context-switches -- sleep 2 > "$L_OUTPUT" 2>&1
    echo "Misses saved to $L_OUTPUT"

    # Ferma il generatore di richieste
    kill -9 $REQUEST_PID
    wait $REQUEST_PID 2>/dev/null
done

echo "Analysis complete. Results saved in $OUTPUT_DIR."