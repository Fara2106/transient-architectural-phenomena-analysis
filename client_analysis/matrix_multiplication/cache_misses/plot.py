import os
import matplotlib.pyplot as plt

# Directory dei risultati
input_dir = "./perf_results_matrix_cache_misses"

# Liste per memorizzare i dati
table_sizes = []  # Dimensione della tabella (estratta dal nome del file)
l1_misses = []
l2_misses = []
l3_misses = []

# Lettura dei file
for file_name in sorted(os.listdir(input_dir)):
    if "misses_" in file_name:
        try:
            # Estrai la dimensione della tabella dal nome del file
            table_size = int(file_name.split("_")[-1].split(".")[0])
            
            # Leggi i valori di miss
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, 'r') as file:
                for line in file:
                    if "mem_load_retired.l1_miss" in line:
                        l1_value = float(line.split()[0].replace('.', '').replace(',','.'))
                    elif "mem_load_retired.l2_miss" in line:
                        l2_value = float(line.split()[0].replace('.', '').replace(',','.'))
                    elif "mem_load_retired.l3_miss" in line:
                        l3_value = float(line.split()[0].replace('.', '').replace(',','.'))

            # Aggiungi i dati alle liste
            table_sizes.append(table_size)
            l1_misses.append(l1_value)
            l2_misses.append(l2_value)
            l3_misses.append(l3_value)

        except Exception as e:
            print(f"Errore nel file {file_name}: {e}")

# Ordina i dati per dimensione della tabella
data = list(zip(table_sizes, l1_misses, l2_misses, l3_misses))
data.sort(key=lambda x: x[0])

table_sizes, l1_misses, l2_misses, l3_misses = zip(*data)

# Calcola i valori minimi, massimi e medi per ogni livello
l1_min, l1_max, l1_avg = min(l1_misses), max(l1_misses), sum(l1_misses) / len(l1_misses)
l2_min, l2_max, l2_avg = min(l2_misses), max(l2_misses), sum(l2_misses) / len(l2_misses)
l3_min, l3_max, l3_avg = min(l3_misses), max(l3_misses), sum(l3_misses) / len(l3_misses)

# Creazione del grafico
fig, axs = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

# Grafico L1
axs[0].plot(table_sizes, l1_misses, marker='o', linestyle='-', color='blue', label="L1 Cache Misses")
axs[0].axhline(l1_min, color='red', linestyle='--', label=f"L1 Min: {l1_min:.2f}")
axs[0].axhline(l1_max, color='green', linestyle='--', label=f"L1 Max: {l1_max:.2f}")
axs[0].axhline(l1_avg, color='purple', linestyle='--', label=f"L1 Average: {l1_avg:.2f}")
axs[0].set_title("L1 Cache Misses per Matrix Size")
axs[0].set_ylabel("Cache Misses")
axs[0].legend()
axs[0].grid(True)

# Grafico L2
axs[1].plot(table_sizes, l2_misses, marker='o', linestyle='-', color='orange', label="L2 Cache Misses")
axs[1].axhline(l2_min, color='red', linestyle='--', label=f"L2 Min: {l2_min:.2f}")
axs[1].axhline(l2_max, color='green', linestyle='--', label=f"L2 Max: {l2_max:.2f}")
axs[1].axhline(l2_avg, color='purple', linestyle='--', label=f"L2 Average: {l2_avg:.2f}")
axs[1].set_title("L2 Cache Misses per Matrix Size")
axs[1].set_ylabel("Cache Misses")
axs[1].legend()
axs[1].grid(True)

# Grafico L3
axs[2].plot(table_sizes, l3_misses, marker='o', linestyle='-', color='green', label="L3 Cache Misses")
axs[2].axhline(l3_min, color='red', linestyle='--', label=f"L3 Min: {l3_min:.2f}")
axs[2].axhline(l3_max, color='green', linestyle='--', label=f"L3 Max: {l3_max:.2f}")
axs[2].axhline(l3_avg, color='purple', linestyle='--', label=f"L3 Average: {l3_avg:.2f}")
axs[2].set_title("L3 Cache Misses per Matrix Size")
axs[2].set_xlabel("Table Size")
axs[2].set_ylabel("Cache Misses")
axs[2].legend()
axs[2].grid(True)

# Salvataggio e visualizzazione
plt.tight_layout()
plt.savefig("cache_misses_per_matrix_size.png")
plt.show()