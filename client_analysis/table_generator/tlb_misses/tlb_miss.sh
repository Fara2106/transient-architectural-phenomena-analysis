# # Controlla se è stata fornita la porta come argomento
# if [ $# -lt 1 ]; then
#     echo "Usage: $0 <port>"
#     exit 1
# fi

PORT=81
OUTPUT_DIR="./perf_results_table_tlb_misses"
ITERATIONS=50                 # Numero di iterazioni per il comando perf
CPU_LIST=0                    # Core da stressare
INTERVAL_NS=10              #Richiesta fissa (100 req/s)                

# Crea la directory di output se non esiste
mkdir -p $OUTPUT_DIR

echo "Starting cache miss analysis on port $PORT with table size $TABLE_SIZE..."

# Ciclo per analizzare componente tabella crescente
declare -a table_sizes=(
      "10000" "50000" "100000" "200000" "300000" "400000" "500000" "600000" "700000" "800000" "900000"
      "1000000"
)
for TABLE_SIZE in "${table_sizes[@]}" 
do  
    echo "Analyzing at table size: $TABLE_SIZE  ($INTERVAL_NS ns per request)..."

    # Genera richieste alla frequenza specificata
    ./send_request $PORT $INTERVAL_NS $TABLE_SIZE &  # Invia richieste al server
    REQUEST_PID=$!

    # Analisi miss
    L_OUTPUT="$OUTPUT_DIR/misses_${TABLE_SIZE}.txt"
    perf stat -C $CPU_LIST -r $ITERATIONS -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk,context-switches -- sleep 2 > "$L_OUTPUT" 2>&1
    #perf stat -a -r $ITERATIONS -e dTLB_load_misses.stlb_hit,dTLB_load_misses.miss_causes_a_walk,dTLB_store_misses.stlb_hit,dTLB_store_misses.miss_causes_a_walk,context-switches -- sleep 2 > "$L_OUTPUT" 2>&1
    echo "Misses saved to $L_OUTPUT"

    # Ferma il generatore di richieste
    kill -9 $REQUEST_PID
    wait $REQUEST_PID 2>/dev/null
done

echo "Analysis complete. Results saved in $OUTPUT_DIR."