# Controlla se sono stati forniti almeno porta come argomento
if [ $# -lt 1 ]; then
    echo "Usage: $0 <port>"
    exit 1
fi

PORT_DISTURBATOR=$1  # Porta del server disturbatore
MATRIX_SIZE=256        # Dimensione della matrice
INTERVAL_NS=200000000    # Intervallo tra le richieste in nanosecondi (5 richieste/secondo)

# Calcola l'intervallo in secondi (nanosecondi -> secondi)
INTERVAL_SEC=$(echo "scale=9; $INTERVAL_NS / 1000000000" | bc)

# Loop infinito per inviare richieste
echo "Sending requests to port $PORT_DISTURBATOR with table size $MATRIX_SIZE at 100,000 requests per second (interval $INTERVAL_NS ns)..."
while true; do
curl -s "http://localhost:$PORT_DISTURBATOR/matrix-multiplication/compute?dimension=$MATRIX_SIZE" > /dev/null &    sleep $INTERVAL_SEC
done