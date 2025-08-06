#include <iostream>
#include <curl/curl.h>
#include <chrono>
#include <thread>

#include <iostream>
#include <curl/curl.h>
#include <chrono>
#include <thread>

// Funzione di callback per gestire la risposta del server
size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* out) {
    size_t totalSize = size * nmemb;
    out->append((char*)contents, totalSize);
    return totalSize;
}

// Funzione per inviare una richiesta HTTP GET
void sendHttpRequest(const std::string& url) {
    CURL* curl;
    CURLcode res;

    curl = curl_easy_init();
    if (curl) {
        std::string response;

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        } else {
            std::cout << "Request sent successfully.\n";
        }

        curl_easy_cleanup(curl);
    } else {
        std::cerr << "Failed to initialize CURL\n";
    }
}
int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <port> <interval_ns> <table_size>" << std::endl;
        return 1;
    }

    std::string port = argv[1];
    int interval_ns = std::stoi(argv[2]);
    int table_size = std::stoi(argv[3]);    // Dimensione della tabella

    // Endpoint basato sul file WAR
    std::string serverUrl = "http://localhost:" + port + "/table-generator/generate?rows=" + std::to_string(table_size);

    std::cout << "Starting request loop to " << serverUrl 
              << " with table size " << table_size << ".\n";

    // Loop infinito per inviare richieste
    while (true) {
        sendHttpRequest(serverUrl);
        std::this_thread::sleep_for(std::chrono::nanoseconds(interval_ns)); // Pausa tra le richieste
    }

    return 0;
}