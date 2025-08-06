#include <iostream>     // Per input/output (std::cout, std::cerr)
#include <curl/curl.h>  // Libreria libcurl per le richieste HTTP
#include <chrono>
#include <thread>       // Per std::this_thread::sleep_for

// Funzione di callback: gestisce la risposta del server e la salva in una stringa
size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* out) {
    size_t totalSize = size * nmemb;  // Calcola la dimensione effettiva dei dati ricevuti
    out->append((char*)contents, totalSize); // Aggiunge i dati ricevuti alla stringa `out`
    return totalSize;  // Ritorna la dimensione dei dati elaborati
}

// Funzione per inviare una richiesta HTTP GET
float sendHttpRequest(const std::string& url) {
    CURL* curl;            // Puntatore a una sessione libcurl
    CURLcode res;          // Variabile per catturare il risultato dell'operazione CURL
    float execution_time = 0;

    curl = curl_easy_init();  // Inizializza una sessione CURL
    if (curl) {               // Controlla se l'inizializzazione è andata a buon fine
        std::string response;  // Stringa per salvare la risposta del server

        // Configura l'URL del server da cui fare la richiesta
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

        // Configura la funzione di callback per ricevere i dati della risposta
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);

        // Passa la stringa dove salvare i dati ricevuti alla funzione di callback
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        // Prendo il tempo di esecuzione...
        auto start = std::chrono::high_resolution_clock::now();

        // Esegue la richiesta HTTP
        res = curl_easy_perform(curl);

        // Fine tempo esecuzione e calcolo del tempo
        auto end = std::chrono::high_resolution_clock::now();
        execution_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

        // Controlla se la richiesta è andata a buon fine
        if (res != CURLE_OK) {
            // Stampa un messaggio di errore in caso di fallimento
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
            execution_time = 0;
        }

        // Pulisce le risorse usate dalla sessione CURL
        curl_easy_cleanup(curl);
    } else {
        // Stampa un messaggio di errore se CURL non è stato inizializzato
        std::cerr << "Failed to initialize CURL" << std::endl;
    }

    return execution_time;
}

int main(int argc, char* argv[]) {
    // Controlla che l'utente abbia inserito i parametri richiesti
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <port> <interval_ns> <matrix_size>" << std::endl;
        return 1;
    }

    std::string port = argv[1];           // Porta del server
    int interval_ns = std::stoi(argv[2]); // Intervallo tra richieste in nanosecondi
    int matrix_size = std::stoi(argv[3]);     // Dimensione della tabella
    int NUM_ITERATIONS;

    // Specifica l'URL del server
    std::string serverUrl = "http://localhost:" + port + "/matrix-multiplication/compute?dimension=" + std::to_string(matrix_size);

    if (matrix_size <= 512){
        NUM_ITERATIONS = 500;
    } else {
        NUM_ITERATIONS = 5;
    }

    float total_time = 0;  // Variabile per sommare tutti i tempi

    // Iterazioni per calcolare il tempo di esecuzione
    for (int i = 0; i < NUM_ITERATIONS; i++) {
        auto time = sendHttpRequest(serverUrl);
        if (time > 0) {
            total_time += time;  // Aggiunge il tempo di ogni richiesta al totale
            std::cout << "Iter " << i + 1 << ": Execution time: " << time << " microseconds" << std::endl;
        }

        // Pausa tra le richieste
        std::this_thread::sleep_for(std::chrono::nanoseconds(interval_ns));
    }

    // Calcola la media
    float average_time = total_time / NUM_ITERATIONS;

    std::cout << "\nAverage Execution Time: " << average_time << " microseconds\n";

    return 0;
}