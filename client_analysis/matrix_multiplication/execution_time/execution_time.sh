PORT=81  # Porta del server
OUTPUT_DIR="./perf_matrix_results_time"  # Directory di output
INTERVAL_NS=10  

# Array delle dimensioni della tabella
declare -a matrix_sizes=(
     "1" "2" "4" "8" "16" "32" "64" "128" "256" "512" "1024" "2048" "4096"
)

# Crea la directory di output se non esiste
mkdir -p $OUTPUT_DIR

echo "Starting execution time analysis on port $PORT with varying table sizes and fixed interval $INTERVAL_NS ns..."

# Ciclo per analizzare le dimensioni della tabella
for MATRIX_SIZE in "${matrix_sizes[@]}"; do
    echo "Analyzing at table size: $MATRIX_SIZE..."

    # File di output per la dimensione corrente della tabella
    OUTPUT_FILE="$OUTPUT_DIR/execution_time_matrix_${MATRIX_SIZE}.txt"
    echo "Saving result to $OUTPUT_FILE"

    # Esegui il programma con l'intervallo fisso e la dimensione della tabella corrente
    ./send_request $PORT $INTERVAL_NS $MATRIX_SIZE > "$OUTPUT_FILE"
done

echo "Analysis complete. Results saved in $OUTPUT_DIR."