import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# --------------------------------------------------------------------------------
# 1) FUNZIONI DI PARSING E FORMATTAZIONE
# --------------------------------------------------------------------------------

def parse_number_from_line(line):
    """
    Estrae il primo numero (float) da una riga, rimuovendo i separatori di migliaia e
    convertendo le virgole in punti decimali.
    """
    import re
    line_clean = re.sub(r'(?<=\d)\.(?=\d)', '', line.strip())  # rimuove i punti "migliaia"
    line_clean = line_clean.replace(',', '.')
    match = re.search(r'(\d+(\.\d+)?)', line_clean)
    if match:
        return float(match.group(1))
    return 0

def short_number_formatter(x, pos):
    """
    Formatta i grandi numeri: es. 1500 -> 1.5K, 2.5 milioni -> 2.5M, ecc.
    """
    if x >= 1e9:
        return f"{x/1e9:.1f}G"
    elif x >= 1e6:
        return f"{x/1e6:.1f}M"
    elif x >= 1e3:
        return f"{x/1e3:.1f}K"
    else:
        return str(round(x,2))

def parse_cache_misses_and_hits(file_path):
    """
    Parsa un file di testo di perf che contiene:
      - mem_load_retired.l1_miss
      - mem_load_retired.l2_miss
      - mem_load_retired.l3_miss
      - mem_load_retired.l1_hit
      - mem_load_retired.l2_hit
      - mem_load_retired.l3_hit
    Restituisce la tupla:
      (l1_miss, l1_hit, l2_miss, l2_hit, l3_miss, l3_hit)
    Se il file non esiste, ritorna tutti 0.
    """
    if not os.path.exists(file_path):
        return (0, 0, 0, 0, 0, 0)

    l1_miss, l1_hit = 0, 0
    l2_miss, l2_hit = 0, 0
    l3_miss, l3_hit = 0, 0

    with open(file_path, 'r') as f:
        for line in f:
            if 'mem_load_retired.l1_miss' in line:
                l1_miss = parse_number_from_line(line)
            elif 'mem_load_retired.l2_miss' in line:
                l2_miss = parse_number_from_line(line)
            elif 'mem_load_retired.l3_miss' in line:
                l3_miss = parse_number_from_line(line)
            elif 'mem_load_retired.l1_hit' in line:
                l1_hit = parse_number_from_line(line)
            elif 'mem_load_retired.l2_hit' in line:
                l2_hit = parse_number_from_line(line)
            elif 'mem_load_retired.l3_hit' in line:
                l3_hit = parse_number_from_line(line)

    return (l1_miss, l1_hit, l2_miss, l2_hit, l3_miss, l3_hit)

def parse_execution_time(file_path):
    """Parsa i file che contengono il tempo medio di esecuzione (in microsecondi)."""
    if not os.path.exists(file_path):
        return 0
    avg_time = 0
    with open(file_path, 'r') as f:
        for line in f:
            if 'Average Execution Time:' in line:
                avg_time = float(line.split()[3])
    return avg_time

def parse_execution_requests(file_path):
    """Parsa i file che calcola il throughput."""
    if not os.path.exists(file_path):
        return 0
    avg_time = 0
    count=0
    with open(file_path, 'r') as f:
        for line in f:
            if 'Iter ' in line:
                count = count + 1
    return count

def parse_tlb_misses(file_path):
    """Parsa i file con TLB misses di livello L1 e L2 (dTLB)."""
    if not os.path.exists(file_path):
        return (0, 0)
    dtlb_load_stlb_hit = 0
    dtlb_store_stlb_hit = 0
    dtlb_load_walk = 0
    dtlb_store_walk = 0

    with open(file_path, 'r') as f:
        for line in f:
            if 'dTLB_load_misses.stlb_hit' in line:
                dtlb_load_stlb_hit = parse_number_from_line(line)
            elif 'dTLB_load_misses.miss_causes_a_walk' in line:
                dtlb_load_walk = parse_number_from_line(line)
            elif 'dTLB_store_misses.stlb_hit' in line:
                dtlb_store_stlb_hit = parse_number_from_line(line)
            elif 'dTLB_store_misses.miss_causes_a_walk' in line:
                dtlb_store_walk = parse_number_from_line(line)

    l2_miss = dtlb_load_walk + dtlb_store_walk
    l1_miss = dtlb_load_stlb_hit + dtlb_store_stlb_hit + l2_miss
    return (l1_miss, l2_miss)

# --------------------------------------------------------------------------------
# 2) FUNZIONI DI CARICAMENTO DATI
# --------------------------------------------------------------------------------

def carica_dati_cache_miss(base_path_1_server, base_path_2_server, base_path_3_server, matrix_sizes, freqs):
    """
    Carica i dati (miss) per i 3 scenari (1S, 2S, 3S).
    Ritorna un dict:
      data_miss[scenario][matrix_size] = (l1_miss, l2_miss, l3_miss)
    e parallelamente un dict per hits:
      data_hit[scenario][matrix_size] = (l1_hit, l2_hit, l3_hit)
    """
    data_miss = {}
    data_hit = {}

    def split_miss_hit(tup):
        l1_m, l1_h, l2_m, l2_h, l3_m, l3_h = tup
        return (l1_m, l2_m, l3_m), (l1_h, l2_h, l3_h)

    # 1) CASO 1 SERVER
    label_1s = '1S'
    data_miss[label_1s] = {}
    data_hit[label_1s] = {}
    for sz in matrix_sizes:
        file_name = f"misses_{sz}.txt"
        path_file = os.path.join(base_path_1_server, file_name)
        mmh = parse_cache_misses_and_hits(path_file)
        m, h = split_miss_hit(mmh)
        data_miss[label_1s][sz] = m
        data_hit[label_1s][sz] = h

    # 2) CASO 2 SERVER
    for freq in freqs:
        label_2s = f"2S_{freq.upper()}"
        data_miss[label_2s] = {}
        data_hit[label_2s] = {}
        for sz in matrix_sizes:
            file_name = f"misses_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_2_server, file_name)
            mmh = parse_cache_misses_and_hits(path_file)
            m, h = split_miss_hit(mmh)
            data_miss[label_2s][sz] = m
            data_hit[label_2s][sz] = h

    # 3) CASO 3 SERVER
    for freq in freqs:
        label_3s = f"3S_{freq.upper()}"
        data_miss[label_3s] = {}
        data_hit[label_3s] = {}
        for sz in matrix_sizes:
            file_name = f"misses_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_3_server, file_name)
            mmh = parse_cache_misses_and_hits(path_file)
            m, h = split_miss_hit(mmh)
            data_miss[label_3s][sz] = m
            data_hit[label_3s][sz] = h

    return data_miss, data_hit

def carica_dati_tempo(base_path_1_server, base_path_2_server, base_path_3_server, matrix_sizes, freqs):
    """
    Carica i dati dei tempi di esecuzione (medio) in microsecondi per i 3 scenari (1S, 2S, 3S).
    Ritorna un dict: data[scenario][matrix_size] = avg_time_us.
    """
    data = {}
    label_1s = '1S'
    data[label_1s] = {}
    for sz in matrix_sizes:
        file_name = f"execution_time_matrix_{sz}.txt"
        path_file = os.path.join(base_path_1_server, file_name)
        data[label_1s][sz] = parse_execution_time(path_file)

    for freq in freqs:
        label_2s = f"2S_{freq.upper()}"
        data[label_2s] = {}
        for sz in matrix_sizes:
            file_name = f"execution_time_matrix_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_2_server, file_name)
            data[label_2s][sz] = parse_execution_time(path_file)

    for freq in freqs:
        label_3s = f"3S_{freq.upper()}"
        data[label_3s] = {}
        for sz in matrix_sizes:
            file_name = f"execution_time_matrix_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_3_server, file_name)
            data[label_3s][sz] = parse_execution_time(path_file)

    return data

def carica_dati_richieste(base_path_1_server, base_path_2_server, base_path_3_server, matrix_sizes, freqs):
    """
    Carica i dati dei tempi di esecuzione (medio) in microsecondi per i 3 scenari (1S, 2S, 3S).
    Ritorna un dict: data[scenario][matrix_size] = avg_time_us.
    """
    data = {}
    label_1s = '1S'
    data[label_1s] = {}
    for sz in matrix_sizes:
        file_name = f"execution_time_matrix_{sz}.txt"
        path_file = os.path.join(base_path_1_server, file_name)
        data[label_1s][sz] = parse_execution_requests(path_file)

    for freq in freqs:
        label_2s = f"2S_{freq.upper()}"
        data[label_2s] = {}
        for sz in matrix_sizes:
            file_name = f"execution_time_matrix_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_2_server, file_name)
            data[label_2s][sz] = parse_execution_requests(path_file)

    for freq in freqs:
        label_3s = f"3S_{freq.upper()}"
        data[label_3s] = {}
        for sz in matrix_sizes:
            file_name = f"execution_time_matrix_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_3_server, file_name)
            data[label_3s][sz] = parse_execution_requests(path_file)

    return data

def carica_dati_tlb(base_path_1_server, base_path_2_server, base_path_3_server, matrix_sizes, freqs):
    """
    Carica i dati TLB misses per i 3 scenari (1S, 2S, 3S).
    Ritorna un dict: data[scenario][matrix_size] = (l1_miss, l2_miss).
    """
    data = {}
    label_1s = '1S'
    data[label_1s] = {}
    for sz in matrix_sizes:
        file_name = f"misses_{sz}.txt"
        path_file = os.path.join(base_path_1_server, file_name)
        data[label_1s][sz] = parse_tlb_misses(path_file)

    for freq in freqs:
        label_2s = f"2S_{freq.upper()}"
        data[label_2s] = {}
        for sz in matrix_sizes:
            file_name = f"tlb_misses_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_2_server, file_name)
            data[label_2s][sz] = parse_tlb_misses(path_file)

    for freq in freqs:
        label_3s = f"3S_{freq.upper()}"
        data[label_3s] = {}
        for sz in matrix_sizes:
            file_name = f"tlb_misses_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_3_server, file_name)
            data[label_3s][sz] = parse_tlb_misses(path_file)

    return data

# --------------------------------------------------------------------------------
# 2B) NORMALIZZAZIONE RISPETTO A '1S'
# --------------------------------------------------------------------------------

def normalizza_cache_miss(data_cache_miss, matrix_sizes, scenario_labels):
    """
    Ritorna un dict normalizzato rispetto al caso '1S':
    data_cache_norm[scenario][sz] = (l1_ratio, l2_ratio, l3_ratio).
    """
    data_norm = {}
    for scenario in scenario_labels:
        data_norm[scenario] = {}
        for sz in matrix_sizes:
            l1, l2, l3 = data_cache_miss[scenario][sz]
            l1_1s, l2_1s, l3_1s = data_cache_miss['1S'][sz]
            norm_l1 = (l1 / l1_1s) if l1_1s else 0
            norm_l2 = (l2 / l2_1s) if l2_1s else 0
            norm_l3 = (l3 / l3_1s) if l3_1s else 0
            data_norm[scenario][sz] = (norm_l1, norm_l2, norm_l3)
    return data_norm

def normalizza_tempo(data_time, matrix_sizes, scenario_labels):
    """
    Ritorna un dict normalizzato rispetto a '1S' (tempo medio):
    data_time_norm[scenario][sz] = time_scenario / time_1S.
    """
    data_norm = {}
    for scenario in scenario_labels:
        data_norm[scenario] = {}
        for sz in matrix_sizes:
            t = data_time[scenario][sz]
            t_1s = data_time['1S'][sz]
            data_norm[scenario][sz] = (t / t_1s) if t_1s else 0
    return data_norm

def normalizza_tlb_miss(data_tlb, matrix_sizes, scenario_labels):
    """
    Ritorna un dict normalizzato rispetto a '1S':
    data_tlb_norm[scenario][sz] = (l1_ratio, l2_ratio).
    """
    data_norm = {}
    for scenario in scenario_labels:
        data_norm[scenario] = {}
        for sz in matrix_sizes:
            l1, l2 = data_tlb[scenario][sz]
            l1_1s, l2_1s = data_tlb['1S'][sz]
            norm_l1 = (l1 / l1_1s) if l1_1s else 0
            norm_l2 = (l2 / l2_1s) if l2_1s else 0
            data_norm[scenario][sz] = (norm_l1, norm_l2)
    return data_norm

# --------------------------------------------------------------------------------
# 3) FUNZIONI PER PLOT DELLE CACHE
# --------------------------------------------------------------------------------

def add_fixed_cache_capacity_lines(ax):
    """
    Aggiunge linee verticali fisse alle posizioni di saturazione cache:
      - L1 saturata a x=52.26
      - L2 saturata a x=147.8
      - L3 saturata a x=1182.41
    """
    lines = [
        (52.26,  "L1=32KB"),
        (147.8,  "L2=256KB"),
        (1182.41,"L3=16MB")
    ]
    for xval, label in lines:
        ax.axvline(xval, color='red', linestyle='--', alpha=0.7)
        ax.text(
            xval, 
            0.95 * ax.get_ylim()[1], 
            label,
            rotation=90, color='red', ha='right', va='top', fontsize=8
        )

def plot_cache_misses(data_cache_miss, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot in verticale (3 subplots) di L1, L2, L3 su scala log2 (asse X),
    per la multi-core matrix multiplication.
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 14), sharex=True)
    levels = ["L1", "L2", "L3"]

    for i, level in enumerate(levels):
        ax = axes[i]
        for s_idx, scenario in enumerate(scenario_labels):
            vals = []
            for sz in matrix_sizes:
                (l1, l2, l3) = data_cache_miss[scenario][sz]
                if level == "L1":
                    vals.append(l1)
                elif level == "L2":
                    vals.append(l2)
                else:
                    vals.append(l3)
            x = np.array(matrix_sizes, dtype=float)
            bar_offset = 0.07
            bar_width  = 0.06
            x_positions = x * (1 + bar_offset * (s_idx - (len(scenario_labels) - 1)/2))
            ax.bar(x_positions, vals, width=bar_width * x, 
                   label=scenario_legend_map[scenario] if i == 0 else "")

        ax.set_title(f"Cache {level} Misses\n(Multi-core moltiplicazione matrici)")
        ax.set_ylabel(f"{level} Misses")
        ax.set_xscale('log', base=2)
        ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)
        ax.yaxis.set_major_formatter(FuncFormatter(short_number_formatter))

        add_fixed_cache_capacity_lines(ax)

        if i == 0:
            ax.legend()

    axes[-1].set_xticks(matrix_sizes)
    axes[-1].set_xticklabels([str(s) for s in matrix_sizes], rotation=45)
    axes[-1].set_xlabel("Dimensione matrice (NxN, scala log2)")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "cache_misses_subplots.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_cache_misses_normalized(data_cache_miss_norm, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot in verticale (3 subplots) di L1, L2, L3 normalizzati a 1S,
    per la multi-core matrix multiplication.
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 14), sharex=True)
    levels = ["L1", "L2", "L3"]

    for i, level in enumerate(levels):
        ax = axes[i]
        for s_idx, scenario in enumerate(scenario_labels):
            vals = []
            for sz in matrix_sizes:
                (l1, l2, l3) = data_cache_miss_norm[scenario][sz]
                if level == "L1":
                    vals.append(l1)
                elif level == "L2":
                    vals.append(l2)
                else:
                    vals.append(l3)
            x = np.array(matrix_sizes, dtype=float)
            bar_offset = 0.07
            bar_width  = 0.06
            x_positions = x * (1 + bar_offset * (s_idx - (len(scenario_labels) - 1)/2))
            ax.bar(x_positions, vals, width=bar_width * x, 
                   label=scenario_legend_map[scenario] if i == 0 else "")

        ax.set_title(f"Cache {level} Misses (Normalizzato ad 1 server)\n(Multi-core moltiplicazione matrici)")
        ax.set_ylabel(f"{level} Normalizzato")
        ax.set_xscale('log', base=2)
        ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)

        add_fixed_cache_capacity_lines(ax)

        if i == 0:
            ax.legend()

    axes[-1].set_xticks(matrix_sizes)
    axes[-1].set_xticklabels([str(s) for s in matrix_sizes], rotation=45)
    axes[-1].set_xlabel("Dimensione matrice (NxN, scala log2)")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "cache_misses_subplots_normalized.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

# --------------------------------------------------------------------------------
# 3B) FUNZIONI DI PLOT PER IL MISS RATE (in percentuale)
# --------------------------------------------------------------------------------

def calcola_missrate(data_miss, data_hit, matrix_sizes, scenario_labels):
    """
    Calcola il miss rate (in %) per L1, L2, L3:
       miss_rate = 100.0 * (misses / (misses + hits))
    Ritorna data_mr[scenario][size] = (mr_l1, mr_l2, mr_l3).
    """
    data_mr = {}
    for scenario in scenario_labels:
        data_mr[scenario] = {}
        for sz in matrix_sizes:
            (l1_m, l2_m, l3_m) = data_miss[scenario][sz]
            (l1_h, l2_h, l3_h) = data_hit[scenario][sz]

            mr_l1 = 100.0 * l1_m / (l1_m + l1_h) if (l1_m + l1_h) != 0 else 0
            mr_l2 = 100.0 * l2_m / (l2_m + l2_h) if (l2_m + l2_h) != 0 else 0
            mr_l3 = 100.0 * l3_m / (l3_m + l3_h) if (l3_m + l3_h) != 0 else 0

            data_mr[scenario][sz] = (mr_l1, mr_l2, mr_l3)
    return data_mr

def plot_cache_missrate(data_missrate, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot del miss rate in verticale (3 subplots) di L1, L2, L3 (in %)
    per la multi-core matrix multiplication, con scala X in log2.
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 14), sharex=True)
    levels = ["L1", "L2", "L3"]

    for i, level in enumerate(levels):
        ax = axes[i]
        for s_idx, scenario in enumerate(scenario_labels):
            vals = []
            for sz in matrix_sizes:
                (mr_l1, mr_l2, mr_l3) = data_missrate[scenario][sz]
                if level == "L1":
                    vals.append(mr_l1)
                elif level == "L2":
                    vals.append(mr_l2)
                else:
                    vals.append(mr_l3)

            x = np.array(matrix_sizes, dtype=float)
            bar_offset = 0.07
            bar_width  = 0.06
            x_positions = x * (1 + bar_offset * (s_idx - (len(scenario_labels) - 1)/2))
            ax.bar(x_positions, vals, width=bar_width * x, 
                   label=scenario_legend_map[scenario] if i == 0 else "")

        ax.set_title(f"Cache {level} Miss Rate\n(Multi-core)")
        ax.set_ylabel(f"{level} Miss Rate (%)")
        ax.set_xscale('log', base=2)
        ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)

        add_fixed_cache_capacity_lines(ax)

        if i == 0:
            ax.legend()

    axes[-1].set_xticks(matrix_sizes)
    axes[-1].set_xticklabels([str(s) for s in matrix_sizes], rotation=45)
    axes[-1].set_xlabel("Dimensione matrice (NxN, scala log2)")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "cache_missrate_subplots.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

# --------------------------------------------------------------------------------
# 4) FUNZIONI DI PLOT TLB E TEMPO (Multi-core)
# --------------------------------------------------------------------------------

def plot_execution_time(data_time, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot a barre con i tempi (in secondi) su asse Y, scala X log2,
    per la multi-core matrix multiplication.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.array(matrix_sizes, dtype=float)
    bar_offset = 0.07
    bar_width  = 0.06

    for s_idx, scenario in enumerate(scenario_labels):
        times_sec = []
        for sz in matrix_sizes:
            us = data_time[scenario][sz]  # microsecondi
            times_sec.append(us / 1e6)    # converto in secondi
        x_positions = x * (1 + bar_offset * (s_idx - (len(scenario_labels) - 1)/2))
        ax.bar(x_positions, times_sec, width=bar_width * x, 
               label=scenario_legend_map[scenario])

    ax.set_title("Tempo di Elaborazione Richieste (secondi)\n(Multi-core moltiplicazione matrici)")
    ax.set_ylabel("Tempo elaborazione (s)\n(scala log)")
    ax.set_xscale('log', base=2)
    ax.set_yscale('log')
    ax.set_xlabel("Dimensione matrice (NxN, scala log2)")
    ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)
    ax.legend()

    ax.set_xticks(matrix_sizes)
    ax.set_xticklabels([str(s) for s in matrix_sizes], rotation=45)

    plt.tight_layout()
    out_file = os.path.join(output_dir, "execution_time_barplot.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_execution_time_normalized(data_time_norm, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot a barre con i tempi normalizzati a '1S',
    per la multi-core matrix multiplication.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.array(matrix_sizes, dtype=float)
    bar_offset = 0.07
    bar_width  = 0.06

    for s_idx, scenario in enumerate(scenario_labels):
        ratios = []
        for sz in matrix_sizes:
            ratios.append(data_time_norm[scenario][sz])
        x_positions = x * (1 + bar_offset * (s_idx - (len(scenario_labels) - 1)/2))
        ax.bar(x_positions, ratios, width=bar_width * x, label=scenario_legend_map[scenario])

    ax.set_title("Tempo Elaborazione Richieste (Normalizzato ad 1 Server)\n(Multi-core moltiplicazione matrici)")
    ax.set_ylabel("Tempo Normalizzato")
    ax.set_xscale('log', base=2)
    ax.set_xlabel("Dimensione matrice (NxN, scala log2)")
    ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)
    ax.legend()

    ax.set_xticks(matrix_sizes)
    ax.set_xticklabels([str(s) for s in matrix_sizes], rotation=45)

    plt.tight_layout()
    out_file = os.path.join(output_dir, "execution_time_barplot_normalized.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_throughput(data_time, data_requests, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot a barre con il throughput su asse Y, scala X log2,
    per la multi-core matrix multiplication.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.array(matrix_sizes, dtype=float)
    bar_offset = 0.07
    bar_width  = 0.06

    for s_idx, scenario in enumerate(scenario_labels):
        throughput = []
        for sz in matrix_sizes:
            us = data_time[scenario][sz]  # microsecondi
            seconds = us / 1e6
            requests = data_requests[scenario][sz]
            throughput.append(requests / seconds)    # converto in secondi
        x_positions = x * (1 + bar_offset * (s_idx - (len(scenario_labels) - 1)/2))
        ax.bar(x_positions, throughput, width=bar_width * x, 
               label=scenario_legend_map[scenario])

    ax.set_title("Throughput (richieste/secondo)\n(Multi-core moltiplicazione matrici)")
    ax.set_ylabel("Throughput\n(scala log)")
    ax.set_xscale('log', base=2)
    ax.set_yscale('log')
    ax.set_xlabel("Dimensione matrice (NxN, scala log2)")
    ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)
    ax.legend()

    ax.set_xticks(matrix_sizes)
    ax.set_xticklabels([str(s) for s in matrix_sizes], rotation=45)

    plt.tight_layout()
    out_file = os.path.join(output_dir, "throughput_barplot.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_tlb_misses(data_tlb, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot in verticale (2 subplots): TLB L1 e TLB L2 su scala log2 (asse X),
    per la multi-core matrix multiplication.
    """
    fig, axes = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    levels = ["TLB L1 Misses", "TLB L2 Misses"]

    for i, level_name in enumerate(levels):
        ax = axes[i]
        for s_idx, scenario in enumerate(scenario_labels):
            vals = []
            for sz in matrix_sizes:
                (l1_miss, l2_miss) = data_tlb[scenario][sz]
                if i == 0:
                    vals.append(l1_miss)
                else:
                    vals.append(l2_miss)

            x = np.array(matrix_sizes, dtype=float)
            bar_offset = 0.07
            bar_width  = 0.06
            x_positions = x * (1 + bar_offset * (s_idx - (len(scenario_labels) - 1)/2))
            ax.bar(x_positions, vals, width=bar_width * x,
                   label=scenario_legend_map[scenario] if i == 0 else "")

        ax.set_title(level_name + "\n(Multi-core moltiplicazione matrici)")
        ax.set_ylabel(level_name)
        ax.set_xscale('log', base=2)
        ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)
        ax.yaxis.set_major_formatter(FuncFormatter(short_number_formatter))

        if i == 0:
            ax.legend()

    axes[-1].set_xticks(matrix_sizes)
    axes[-1].set_xticklabels([str(s) for s in matrix_sizes], rotation=45)
    axes[-1].set_xlabel("Dimensione matrice (NxN, scala log2)")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "tlb_misses_subplots.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_tlb_misses_normalized(data_tlb_norm, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot in verticale (2 subplots) con valori normalizzati a '1S': TLB L1, TLB L2,
    per la multi-core matrix multiplication.
    """
    fig, axes = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    levels = [
        "TLB L1 Misses (Normalizzato)\n(Multi-core moltiplicazione matrici)",
        "TLB L2 Misses (Normalizzato)\n(Multi-core moltiplicazione matrici)"
    ]

    for i, level_name in enumerate(levels):
        ax = axes[i]
        for s_idx, scenario in enumerate(scenario_labels):
            vals = []
            for sz in matrix_sizes:
                (l1_ratio, l2_ratio) = data_tlb_norm[scenario][sz]
                if i == 0:
                    vals.append(l1_ratio)
                else:
                    vals.append(l2_ratio)

            x = np.array(matrix_sizes, dtype=float)
            bar_offset = 0.07
            bar_width  = 0.06
            x_positions = x * (1 + bar_offset * (s_idx - (len(scenario_labels) - 1)/2))
            ax.bar(x_positions, vals, width=bar_width * x,
                   label=scenario_legend_map[scenario] if i == 0 else "")

        ax.set_title(level_name)
        ax.set_ylabel("Normalizzato")
        ax.set_xscale('log', base=2)
        ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)

        if i == 0:
            ax.legend()

    axes[-1].set_xticks(matrix_sizes)
    axes[-1].set_xticklabels([str(s) for s in matrix_sizes], rotation=45)
    axes[-1].set_xlabel("Dimensione matrice (NxN, scala log2)")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "tlb_misses_subplots_normalized.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

# --------------------------------------------------------------------------------
# 5) MAIN
# --------------------------------------------------------------------------------

def main():
    # Output directory dove salvare i plot
    output_dir = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Multi Core/Plots"

    # Base path per i 3 scenari (1 server, 2 server, 3 server) - Cache Miss
    base_path_1_server_cache = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Multi Core/1 Active Server/perf_results_matrix_cache_misses"
    base_path_2_server_cache = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Multi Core/2 Active Server/perf_results_matrix_cache_misses"
    base_path_3_server_cache = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Multi Core/3 Active Server/perf_results_matrix_cache_misses"

    # Base path per i 3 scenari - Execution Time
    base_path_1_server_time = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Multi Core/1 Active Server/perf_matrix_results_time"
    base_path_2_server_time = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Multi Core/2 Active Server/perf_matrix_results_time"
    base_path_3_server_time = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Multi Core/3 Active Server/perf_matrix_results_time"

    # Base path per i 3 scenari - TLB Miss
    base_path_1_server_tlb = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Multi Core/1 Active Server/perf_results_matrix_tlb_misses"
    base_path_2_server_tlb = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Multi Core/2 Active Server/perf_results_matrix_tlb_misses"
    base_path_3_server_tlb = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Multi Core/3 Active Server/perf_results_matrix_tlb_misses"

    # Dimensioni matrici (potenze di 2, da 1 a 4096)
    matrix_sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

    # Frequenze di “disturbo”
    freqs = ["LOW", "MEDIUM", "HIGH"]

    # Carichiamo i dati di cache (miss + hit)
    data_cache_miss, data_cache_hit = carica_dati_cache_miss(
        base_path_1_server_cache,
        base_path_2_server_cache,
        base_path_3_server_cache,
        matrix_sizes,
        freqs
    )
    # Carichiamo i tempi
    data_time = carica_dati_tempo(
        base_path_1_server_time,
        base_path_2_server_time,
        base_path_3_server_time,
        matrix_sizes,
        freqs
    )

    # Carica i dati per il throuhput
    data_request = carica_dati_richieste(
        base_path_1_server_time,
        base_path_2_server_time,
        base_path_3_server_time,
        matrix_sizes,
        freqs
    )

    # Carichiamo i TLB
    data_tlb = carica_dati_tlb(
        base_path_1_server_tlb,
        base_path_2_server_tlb,
        base_path_3_server_tlb,
        matrix_sizes,
        freqs
    )

    # Scenari e legend
    scenario_labels = [
        "1S",
        "2S_LOW", "2S_MEDIUM", "2S_HIGH",
        "3S_LOW", "3S_MEDIUM", "3S_HIGH"
    ]
    scenario_legend_map = {
        "1S":       "1 Server (no disturbo)",
        "2S_LOW":   "2 Servers (basso disturbo)",
        "2S_MEDIUM":"2 Servers (medio disturbo)",
        "2S_HIGH":  "2 Servers (alto disturbo)",
        "3S_LOW":   "3 Servers (basso disturbo)",
        "3S_MEDIUM":"3 Servers (medio disturbo)",
        "3S_HIGH":  "3 Servers (alto disturbo)",
    }

    # -------------------------------
    # 1) PLOT VALORI ASSOLUTI (Cache, Tempo, TLB)
    # -------------------------------
    plot_cache_misses(data_cache_miss, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)
    plot_execution_time(data_time, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)
    plot_tlb_misses(data_tlb, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)
    plot_throughput(data_time, data_request, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)

    # -------------------------------
    # 2) PLOT VALORI NORMALIZZATI (Cache, Tempo, TLB)
    # -------------------------------
    data_cache_miss_norm = normalizza_cache_miss(data_cache_miss, matrix_sizes, scenario_labels)
    data_time_norm = normalizza_tempo(data_time, matrix_sizes, scenario_labels)
    data_tlb_norm = normalizza_tlb_miss(data_tlb, matrix_sizes, scenario_labels)

    plot_cache_misses_normalized(data_cache_miss_norm, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)
    plot_execution_time_normalized(data_time_norm, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)
    plot_tlb_misses_normalized(data_tlb_norm, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)

    # -------------------------------
    # 3) PLOT MISS RATE (Cache) - IN PERCENTUALE
    # -------------------------------
    data_missrate = calcola_missrate(data_cache_miss, data_cache_hit, matrix_sizes, scenario_labels)
    plot_cache_missrate(data_missrate, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)


if __name__ == "__main__":
    main()
