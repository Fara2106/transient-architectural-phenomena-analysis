import os
import matplotlib.pyplot as plt
import numpy as np

# Directory con i file di testo
input_dir = "./perf_table_results_time"

# Liste per le dimensioni delle tabelle e i tempi medi di esecuzione
table_sizes = []
average_execution_times = []

# Lettura dei file di testo
for file_name in sorted(os.listdir(input_dir)):
    if "execution_time_table_" in file_name:  # Filtra i file che contengono "execution_time_table_"
        try:
            # Estrai la dimensione della tabella dal nome del file
            table_size = int(file_name.split("_")[-1].split(".")[0])  # Conversione in intero
            table_sizes.append(table_size)
            
            # Leggi i valori di tempo dal file
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, 'r') as file:
                times = []
                for line in file:
                    if "Execution time:" in line:
                        time = float(line.split(":")[2].strip().split()[0])  # Conversione in float
                        times.append(time)
            
            # Calcola il tempo medio per il file corrente
            if times:
                average_execution_times.append(np.mean(times))
        
        except Exception as e:
            print(f"Errore nel file {file_name}: {e}")

# Ordina i dati in base alla dimensione della tabella per sicurezza
sorted_data = sorted(zip(table_sizes, average_execution_times), key=lambda x: x[0])
table_sizes, average_execution_times = zip(*sorted_data)

# Calcolo dei valori minimi, massimi e medi
min_time = np.min(average_execution_times)
max_time = np.max(average_execution_times)
avg_time = np.mean(average_execution_times)

# Creazione del grafico
plt.figure(figsize=(10, 6))
plt.plot(table_sizes, average_execution_times, marker='o', linestyle='-', label="Average Execution Time")

# Linee tratteggiate per min, max e average
plt.axhline(min_time, color='red', linestyle='--', label=f"Min Time: {min_time:.2f} µs")
plt.axhline(max_time, color='green', linestyle='--', label=f"Max Time: {max_time:.2f} µs")
plt.axhline(avg_time, color='purple', linestyle='--', label=f"Average Time: {avg_time:.2f} µs")

# Personalizzazione degli assi
plt.xlabel("Table Size")
plt.ylabel("Execution Time (microseconds)")
plt.title("Average Execution Time per Table Size (1 Server Active Table Generator)")
plt.legend()
plt.grid(True)

# Salvataggio e visualizzazione del grafico
plt.tight_layout()
plt.savefig("execution_time_per_table_size.png")
plt.show()