import os
import matplotlib.pyplot as plt

# Directory con i risultati
input_dir = "./perf_results_matrix_tlb_misses"

# Liste per memorizzare i dati
matrix_sizes = []  # Dimensioni delle tabelle
l1_misses = []    # Miss L1
l2_misses = []    # Miss L2

# Lettura dei file
for file_name in sorted(os.listdir(input_dir)):
    if file_name.startswith("misses_") and file_name.endswith(".txt"):
        try:
            # Estrai la dimensione della tabella dal nome del file
            matrix_size = int(file_name.split("_")[-1].split(".")[0])

            # Leggi i valori dal file
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, 'r') as file:
                dtlb_load_stlb_hit = 0
                dtlb_store_stlb_hit = 0
                dtlb_load_walk = 0
                dtlb_store_walk = 0

                for line in file:
                    if "dTLB_load_misses.stlb_hit" in line:
                        dtlb_load_stlb_hit = float(line.split()[0].replace('.', '').replace(',', '.'))
                    elif "dTLB_store_misses.stlb_hit" in line:
                        dtlb_store_stlb_hit = float(line.split()[0].replace('.', '').replace(',', '.'))
                    elif "dTLB_load_misses.miss_causes_a_walk" in line:
                        dtlb_load_walk = float(line.split()[0].replace('.', '').replace(',', '.'))
                    elif "dTLB_store_misses.miss_causes_a_walk" in line:
                        dtlb_store_walk = float(line.split()[0].replace('.', '').replace(',', '.'))

            # Calcola le miss L1 e L2
            l2_miss = dtlb_load_walk + dtlb_store_walk
            l1_miss = dtlb_load_stlb_hit + dtlb_store_stlb_hit + l2_miss

            # Aggiungi i dati alle liste
            matrix_sizes.append(matrix_size)
            l1_misses.append(l1_miss)
            l2_misses.append(l2_miss)

        except Exception as e:
            print(f"Errore nel file {file_name}: {e}")

# Ordina i dati in base alla dimensione della tabella
data = list(zip(matrix_sizes, l1_misses, l2_misses))
data.sort(key=lambda x: x[0])

matrix_sizes, l1_misses, l2_misses = zip(*data)

# Calcola i valori massimi, minimi e medi
l1_max, l1_min, l1_avg = max(l1_misses), min(l1_misses), sum(l1_misses) / len(l1_misses)
l2_max, l2_min, l2_avg = max(l2_misses), min(l2_misses), sum(l2_misses) / len(l2_misses)

# Creazione del grafico
fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# Grafico L1
axs[0].plot(matrix_sizes, l1_misses, marker='o', linestyle='-', color='blue', label="L1 TLB Misses")
axs[0].axhline(l1_max, color='red', linestyle='--', label=f"L1 Max: {l1_max:.2f}")
axs[0].axhline(l1_min, color='green', linestyle='--', label=f"L1 Min: {l1_min:.2f}")
axs[0].axhline(l1_avg, color='purple', linestyle='--', label=f"L1 Average: {l1_avg:.2f}")
axs[0].set_title("L1 TLB Misses per Matrix Size")
axs[0].set_ylabel("TLB Misses")
axs[0].legend()
axs[0].grid(True)

# Grafico L2
axs[1].plot(matrix_sizes, l2_misses, marker='o', linestyle='-', color='orange', label="L2 TLB Misses")
axs[1].axhline(l2_max, color='red', linestyle='--', label=f"L2 Max: {l2_max:.2f}")
axs[1].axhline(l2_min, color='green', linestyle='--', label=f"L2 Min: {l2_min:.2f}")
axs[1].axhline(l2_avg, color='purple', linestyle='--', label=f"L2 Average: {l2_avg:.2f}")
axs[1].set_title("L2 TLB Misses per matrix Size")
axs[1].set_xlabel("Matrix Size (rows)")
axs[1].set_ylabel("TLB Misses")
axs[1].legend()
axs[1].grid(True)

# Salvataggio e visualizzazione
plt.tight_layout()
plt.savefig("tlb_misses_matrix_size_analysis.png")
plt.show()