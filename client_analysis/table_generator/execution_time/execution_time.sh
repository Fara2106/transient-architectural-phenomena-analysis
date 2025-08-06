# # Controlla se è stata fornita almeno la porta come argomento
# if [ $# -lt 1 ]; then
#     echo "Usage: $0 <port>"
#     exit 1
# fi

PORT=81  # Porta del server
OUTPUT_DIR="./perf_table_results_time"  # Directory di output
INTERVAL_NS=10              #Richiesta fissa               

# Array delle dimensioni della tabella
declare -a table_sizes=(
      "10000" "50000" "100000" "200000" "300000" "400000" "500000" "600000" "700000" "800000" "900000"
      "1000000"
)

# Crea la directory di output se non esiste
mkdir -p $OUTPUT_DIR

echo "Starting execution time analysis on port $PORT with varying table sizes and fixed interval $INTERVAL_NS ns..."

# Ciclo per analizzare le dimensioni della tabella
for TABLE_SIZE in "${table_sizes[@]}"; do
    echo "Analyzing at table size: $TABLE_SIZE..."

    # File di output per la dimensione corrente della tabella
    OUTPUT_FILE="$OUTPUT_DIR/execution_time_table_${TABLE_SIZE}.txt"
    echo "Saving result to $OUTPUT_FILE"

    # Esegui il programma con l'intervallo fisso e la dimensione della tabella corrente
    ./send_request $PORT $INTERVAL_NS $TABLE_SIZE > "$OUTPUT_FILE"
done

echo "Analysis complete. Results saved in $OUTPUT_DIR."