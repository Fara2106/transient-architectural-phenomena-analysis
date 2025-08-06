# Controlla se sono stati forniti almeno porta come argomento
if [ $# -lt 1 ]; then
    echo "Usage: $0 <port>"
    exit 1
fi

PORT_DISTURBATOR=$1  # Porta del server disturbatore
TABLE_SIZE=1000        # Dimensione della tabella (3MB)
INTERVAL_NS=10000000    # Intervallo tra le richieste in nanosecondi (100 richieste/secondo)

# Calcola l'intervallo in secondi (nanosecondi -> secondi)
INTERVAL_SEC=$(echo "scale=9; $INTERVAL_NS / 1000000000" | bc)

# Loop infinito per inviare richieste
echo "Sending requests to port $PORT_DISTURBATOR with table size $TABLE_SIZE at 100,000 requests per second (interval $INTERVAL_NS ns)..."
while true; do
    curl -s "http://localhost:$PORT_DISTURBATOR/table-generator/generate?rows=$TABLE_SIZE" > /dev/null &   sleep $INTERVAL_SEC
done