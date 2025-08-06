import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# --------------------------------------------------------------------------------
# 1) FUNZIONI DI PARSING E FORMATTAZIONE
# --------------------------------------------------------------------------------

def parse_cache_stats(file_path):
    """
    Parsing di:
    - L1, L2, L3 miss
    - L1, L2, L3 hit

    Ritorna una tupla di 6 valori:
      (l1_miss, l2_miss, l3_miss, l1_hit, l2_hit, l3_hit)

    Se il file non esiste, restituisce tutti zeri.
    """
    l1_miss, l2_miss, l3_miss = 0, 0, 0
    l1_hit,  l2_hit,  l3_hit  = 0, 0, 0

    if not os.path.exists(file_path):
        return (0, 0, 0, 0, 0, 0)

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

    return (l1_miss, l2_miss, l3_miss, l1_hit, l2_hit, l3_hit)

def parse_execution_time(file_path):
    """Parsa i file che contengono il tempo medio di esecuzione (in microsecondi)."""
    avg_time = 0
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r') as f:
        for line in f:
            if 'Average Execution Time:' in line:
                avg_time = float(line.split()[3])
    return avg_time

def parse_tlb_misses(file_path):
    """
    Restituisce (l1_miss, l2_miss). Nessuna modifica strutturale.
    """
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

def parse_number_from_line(line):
    # Rimuove i separatori di migliaia e converte eventuali virgole in punti
    line_clean = re.sub(r'(?<=\d)\.(?=\d)', '', line.strip())
    line_clean = line_clean.replace(',', '.')
    match = re.search(r'(\d+(\.\d+)?)', line_clean)
    if match:
        return float(match.group(1))
    return 0

def short_number_formatter(x, pos):
    """Formatta l'asse y in k, M, G per valori grandi."""
    if x >= 1e9:
        return f"{x/1e9:.1f}G"
    elif x >= 1e6:
        return f"{x/1e6:.1f}M"
    elif x >= 1e3:
        return f"{x/1e3:.1f}K"
    else:
        return str(round(x, 2))

# --------------------------------------------------------------------------------
# (A) NUOVE FUNZIONI PER IL THROUGHPUT (in scala lineare)
# --------------------------------------------------------------------------------

def parse_execution_requests(file_path):
    """
    Conta quante volte compare la stringa 'Iter ' nel file => numero di richieste.
    """
    if not os.path.exists(file_path):
        return 0
    count = 0
    with open(file_path, 'r') as f:
        for line in f:
            if 'Iter ' in line:
                count += 1
    return count

def carica_dati_richieste(base_path_1_server_time, base_path_2_server_time, base_path_3_server_time,
                          table_sizes, freqs):
    """
    Carica il numero di richieste (Iter) per i vari scenari (1S, 2S, 3S).
    """
    data_requests = {}
    # 1) CASO 1 SERVER
    label_1s = '1S'
    data_requests[label_1s] = {}
    for sz in table_sizes:
        file_name = f"execution_time_table_{sz}.txt"
        path_file = os.path.join(base_path_1_server_time, file_name)
        data_requests[label_1s][sz] = parse_execution_requests(path_file)

    # 2) CASO 2 SERVER
    for freq in freqs:
        label_2s = f"2S_{freq.upper()}"
        data_requests[label_2s] = {}
        for sz in table_sizes:
            file_name = f"execution_time_table_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_2_server_time, file_name)
            data_requests[label_2s][sz] = parse_execution_requests(path_file)

    # 3) CASO 3 SERVER
    for freq in freqs:
        label_3s = f"3S_{freq.upper()}"
        data_requests[label_3s] = {}
        for sz in table_sizes:
            file_name = f"execution_time_table_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_3_server_time, file_name)
            data_requests[label_3s][sz] = parse_execution_requests(path_file)

    return data_requests

def plot_throughput(data_time, data_requests, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot a barre del Throughput (requests/second) in scala **lineare** su Y.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(table_sizes))
    bar_width = 0.1

    for s_idx, scenario in enumerate(scenario_labels):
        throughput_vals = []
        for size in table_sizes:
            # tempo in microsecondi
            us = data_time[scenario][size]
            seconds = us / 1e6
            num_requests = data_requests[scenario][size]
            # Se seconds=0 => throughput=0 per evitare div/0
            thr = num_requests / seconds if seconds != 0 else 0
            throughput_vals.append(thr)

        x_positions = x + (s_idx - len(scenario_labels)/2)*bar_width + bar_width/2
        ax.bar(x_positions, throughput_vals, bar_width, label=scenario_legend_map[scenario])

    ax.set_title("Throughput (richieste/secondo)\n(Multi-core generatore tabella)")
    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in table_sizes], rotation=45)
    ax.set_ylabel("Throughput (req/s)")
    # Scala Y lineare (NON log)
    ax.set_yscale('linear')
    ax.set_xlabel("Dimensione Tabella (# righe)")
    ax.grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
    ax.legend()

    plt.tight_layout()
    out_file = os.path.join(output_dir, "throughput_barplot.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

# --------------------------------------------------------------------------------
# 2) FUNZIONI DI CARICAMENTO DATI (già presenti)
# --------------------------------------------------------------------------------

def carica_dati_cache_miss(base_path_1_server, base_path_2_server, base_path_3_server, table_sizes, freqs):
    """
    Carica i 6 valori (miss e hit) per L1, L2, L3.
    """
    data = {}
    # 1) CASO 1 SERVER
    label_1s = '1S'
    data[label_1s] = {}
    for sz in table_sizes:
        file_name = f"misses_{sz}.txt"
        path_file = os.path.join(base_path_1_server, file_name)
        data[label_1s][sz] = parse_cache_stats(path_file)

    # 2) CASO 2 SERVER
    for freq in freqs:
        label_2s = f"2S_{freq.upper()}"
        data[label_2s] = {}
        for sz in table_sizes:
            file_name = f"misses_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_2_server, file_name)
            data[label_2s][sz] = parse_cache_stats(path_file)

    # 3) CASO 3 SERVER
    for freq in freqs:
        label_3s = f"3S_{freq.upper()}"
        data[label_3s] = {}
        for sz in table_sizes:
            file_name = f"misses_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_3_server, file_name)
            data[label_3s][sz] = parse_cache_stats(path_file)

    return data

def carica_dati_tempo(base_path_1_server, base_path_2_server, base_path_3_server, table_sizes, freqs):
    """
    Carica i tempi di esecuzione (in microsecondi).
    """
    data = {}
    label_1s = '1S'
    data[label_1s] = {}
    for sz in table_sizes:
        file_name = f"execution_time_table_{sz}.txt"
        path_file = os.path.join(base_path_1_server, file_name)
        data[label_1s][sz] = parse_execution_time(path_file)

    for freq in freqs:
        label_2s = f"2S_{freq.upper()}"
        data[label_2s] = {}
        for sz in table_sizes:
            file_name = f"execution_time_table_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_2_server, file_name)
            data[label_2s][sz] = parse_execution_time(path_file)

    for freq in freqs:
        label_3s = f"3S_{freq.upper()}"
        data[label_3s] = {}
        for sz in table_sizes:
            file_name = f"execution_time_table_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_3_server, file_name)
            data[label_3s][sz] = parse_execution_time(path_file)

    return data

def carica_dati_tlb(base_path_1_server, base_path_2_server, base_path_3_server, table_sizes, freqs):
    """
    Carica i TLB misses.
    """
    data = {}
    label_1s = '1S'
    data[label_1s] = {}
    for sz in table_sizes:
        file_name = f"misses_{sz}.txt"
        path_file = os.path.join(base_path_1_server, file_name)
        data[label_1s][sz] = parse_tlb_misses(path_file)

    for freq in freqs:
        label_2s = f"2S_{freq.upper()}"
        data[label_2s] = {}
        for sz in table_sizes:
            file_name = f"tlb_misses_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_2_server, file_name)
            data[label_2s][sz] = parse_tlb_misses(path_file)

    for freq in freqs:
        label_3s = f"3S_{freq.upper()}"
        data[label_3s] = {}
        for sz in table_sizes:
            file_name = f"tlb_misses_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_3_server, file_name)
            data[label_3s][sz] = parse_tlb_misses(path_file)

    return data

# --------------------------------------------------------------------------------
# 2B) NORMALIZZAZIONE RISPETTO A '1S'
# --------------------------------------------------------------------------------

def normalizza_cache_miss(data_cache, table_sizes, scenario_labels):
    """
    Consideriamo solo i miss (l1_miss, l2_miss, l3_miss) e li normalizziamo
    rispetto ai corrispondenti miss di 1S.
    """
    data_norm = {}
    for scenario in scenario_labels:
        data_norm[scenario] = {}
        for sz in table_sizes:
            l1_miss, l2_miss, l3_miss, _, _, _ = data_cache[scenario][sz]
            l1_miss_1s, l2_miss_1s, l3_miss_1s, _, _, _ = data_cache["1S"][sz]
            norm_l1 = (l1_miss / l1_miss_1s) if l1_miss_1s != 0 else 0
            norm_l2 = (l2_miss / l2_miss_1s) if l2_miss_1s != 0 else 0
            norm_l3 = (l3_miss / l3_miss_1s) if l3_miss_1s != 0 else 0
            data_norm[scenario][sz] = (norm_l1, norm_l2, norm_l3)
    return data_norm

def normalizza_tempo(data_time, table_sizes, scenario_labels):
    """
    Normalizzazione dei tempi rispetto al tempo di 1S.
    """
    data_norm = {}
    for scenario in scenario_labels:
        data_norm[scenario] = {}
        for sz in table_sizes:
            t = data_time[scenario][sz]
            t_1s = data_time["1S"][sz]
            if t_1s != 0:
                data_norm[scenario][sz] = t / t_1s
            else:
                data_norm[scenario][sz] = 0
    return data_norm

def normalizza_tlb_miss(data_tlb, table_sizes, scenario_labels):
    """
    Normalizzazione TLB (l1_miss, l2_miss) rispetto a 1S.
    """
    data_norm = {}
    for scenario in scenario_labels:
        data_norm[scenario] = {}
        for sz in table_sizes:
            l1, l2 = data_tlb[scenario][sz]
            l1_1s, l2_1s = data_tlb["1S"][sz]
            norm_l1 = (l1 / l1_1s) if l1_1s != 0 else 0
            norm_l2 = (l2 / l2_1s) if l2_1s != 0 else 0
            data_norm[scenario][sz] = (norm_l1, norm_l2)
    return data_norm

# --------------------------------------------------------------------------------
# 3) FUNZIONI DI PLOT (non modificate, salvo l'aggiunta di throughput sopra)
# --------------------------------------------------------------------------------

def _find_closest_xpos(num_rows, table_sizes, clamp_value):
    """
    Restituisce la posizione x corrispondente a 'num_rows' sulla scala discrete
    di table_sizes, interpolando. Se num_rows < table_sizes[0], torna clamp_value.
    Se num_rows > table_sizes[-1], torna len(table_sizes)-1.
    """
    if num_rows <= table_sizes[0]:
        return clamp_value
    if num_rows >= table_sizes[-1]:
        return len(table_sizes) - 1

    for i in range(len(table_sizes) - 1):
        if table_sizes[i] <= num_rows <= table_sizes[i+1]:
            x0 = i
            x1 = i + 1
            r0 = table_sizes[i]
            r1 = table_sizes[i+1]
            frac = (num_rows - r0) / (r1 - r0)
            return x0 + frac
    return len(table_sizes) - 1

def _add_cache_vertical_lines(ax, table_sizes):
    # """
    # Aggiunge linee verticali per indicare la saturazione di L1 (32KB), L2 (256KB), L3 (16MB).
    # Con offset diversi se cadono < table_sizes[0], così non si sovrappongono.
    # Inoltre, riportiamo in legenda quante righe servono per saturare ogni livello.
    # """
    # # Byte totali
    # l1_bytes = 32 * 1024        # 32 KB
    # l2_bytes = 256 * 1024       # 256 KB
    # l3_bytes = 16 * 1024 * 1024 # 16 MB

    # bytes_per_row = 300.0
    # l1_rows = l1_bytes / bytes_per_row   # ~106 righe
    # l2_rows = l2_bytes / bytes_per_row   # ~853 righe
    # l3_rows = l3_bytes / bytes_per_row   # ~53333 righe

    # # Forziamo L1, L2, L3 a clamp diversi, così se stanno <0 non si sovrappongono.
    # x_l1 = _find_closest_xpos(l1_rows, table_sizes, clamp_value=-0.2)
    # x_l2 = _find_closest_xpos(l2_rows, table_sizes, clamp_value=-0.3)
    # x_l3 = _find_closest_xpos(l3_rows, table_sizes, clamp_value=-0.4)

    # # Creiamo label con quante righe servono (arrotondate):
    # label_l1 = f"Saturazione L1 (~{int(round(l1_rows))} righe)"
    # label_l2 = f"Saturazione L2 (~{int(round(l2_rows))} righe)"
    # label_l3 = f"Saturazione L3 (~{int(round(l3_rows))} righe)"

    # ax.axvline(x=x_l1, color='red',   linestyle='--', alpha=0.9, label=label_l1)
    # ax.axvline(x=x_l2, color='orange',linestyle='--', alpha=0.9, label=label_l2)
    # ax.axvline(x=x_l3, color='green', linestyle='--', alpha=0.9, label=label_l3)

    # # Forziamo i limiti dell'asse x per vedere anche linee negative
    # ax.set_xlim(-1.0, len(table_sizes) - 1 + 0.5)
    pass

def plot_cache_misses(data_cache, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot con valori assoluti di L1, L2, L3 Miss (3 subplots).
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    x = np.arange(len(table_sizes))
    bar_width = 0.1

    # Mappa per sapere la dimensione di cache associata
    cache_sizes = {"L1": "32 KB", "L2": "256 KB", "L3": "16 MB"}

    for i, level in enumerate(["L1", "L2", "L3"]):
        ax = axes[i]
        for s_idx, scenario in enumerate(scenario_labels):
            values = []
            for size in table_sizes:
                (l1_miss, l2_miss, l3_miss, _, _, _) = data_cache[scenario][size]
                if level == "L1":
                    values.append(l1_miss)
                elif level == "L2":
                    values.append(l2_miss)
                else:
                    values.append(l3_miss)

            x_positions = x + (s_idx - len(scenario_labels)/2)*bar_width + bar_width/2
            ax.bar(x_positions, values, bar_width, label=scenario_legend_map[scenario])

        ax.set_title(f"{level} Miss\n(Multi-core generatore tabella)")

        # Aggiungiamo la dimensione di cache in legenda come entry fittizia
        ax.plot([], [], ' ', label=f"Dimensione cache: {cache_sizes[level]}")

        # Aggiungiamo linee verticali (con riga in legenda che riporta #righe)
        _add_cache_vertical_lines(ax, table_sizes)

        ax.set_ylabel(f"{level} Miss")
        ax.grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
        ax.yaxis.set_major_formatter(FuncFormatter(short_number_formatter))
        ax.legend()

    axes[-1].set_xticks(x)
    axes[-1].set_xticklabels([str(s) for s in table_sizes], rotation=45)
    axes[-1].set_xlabel("Dimensione tabella (# righe)")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "cache_misses_subplots.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_cache_miss_rate(data_cache, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot con i Miss Rate (100 * miss / (miss + hit)) di L1, L2, L3 (3 subplots).
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    x = np.arange(len(table_sizes))
    bar_width = 0.1

    cache_sizes = {"L1": "32 KB", "L2": "256 KB", "L3": "16 MB"}

    for i, level in enumerate(["L1", "L2", "L3"]):
        ax = axes[i]
        for s_idx, scenario in enumerate(scenario_labels):
            rates = []
            for size in table_sizes:
                (l1_miss, l2_miss, l3_miss, l1_hit, l2_hit, l3_hit) = data_cache[scenario][size]
                if level == "L1":
                    total = l1_miss + l1_hit
                    miss = l1_miss
                elif level == "L2":
                    total = l2_miss + l2_hit
                    miss = l2_miss
                else:
                    total = l3_miss + l3_hit
                    miss = l3_miss

                rate = (miss / total * 100) if total != 0 else 0
                rates.append(rate)

            x_positions = x + (s_idx - len(scenario_labels)/2)*bar_width + bar_width/2
            ax.bar(x_positions, rates, bar_width, label=scenario_legend_map[scenario])

        ax.set_title(f"{level} Miss Rate\n(Multi-core generatore tabella)")
        ax.plot([], [], ' ', label=f"Dimensione cache: {cache_sizes[level]}")

        # Anche qui aggiungiamo linee verticali con #righe in legenda
        _add_cache_vertical_lines(ax, table_sizes)

        ax.set_ylabel("Miss Rate (%)")
        ax.grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
        ax.legend()

    axes[-1].set_xticks(x)
    axes[-1].set_xticklabels([str(s) for s in table_sizes], rotation=45)
    axes[-1].set_xlabel("Dimensione tabella (# righe)")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "cache_miss_rate_subplots.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_cache_misses_normalized(data_cache_norm, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot dei miss normalizzati (ratio rispetto a 1S) per L1, L2, L3 (3 subplots).
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    x = np.arange(len(table_sizes))
    bar_width = 0.1

    cache_sizes = {"L1": "32 KB", "L2": "256 KB", "L3": "16 MB"}

    for i, level in enumerate(["L1", "L2", "L3"]):
        ax = axes[i]
        for s_idx, scenario in enumerate(scenario_labels):
            values = []
            for size in table_sizes:
                (l1, l2, l3) = data_cache_norm[scenario][size]
                if level == "L1":
                    values.append(l1)
                elif level == "L2":
                    values.append(l2)
                else:
                    values.append(l3)

            x_positions = x + (s_idx - len(scenario_labels)/2)*bar_width + bar_width/2
            ax.bar(x_positions, values, bar_width, label=scenario_legend_map[scenario])

        ax.set_title(f"{level} Miss (Normalizzato ad 1 Server)\n(Multi-core generatore tabella)")
        ax.plot([], [], ' ', label=f"Dimensione cache: {cache_sizes[level]}")

        _add_cache_vertical_lines(ax, table_sizes)
        ax.set_ylabel(f"{level} Normalizzato")
        ax.grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
        ax.legend()

    axes[-1].set_xticks(x)
    axes[-1].set_xticklabels([str(s) for s in table_sizes], rotation=45)
    axes[-1].set_xlabel("Dimensione tabella (# righe)")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "cache_misses_subplots_normalized.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_execution_time(data_time, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot dei tempi di esecuzione (valori assoluti).
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(table_sizes))
    bar_width = 0.1

    for s_idx, scenario in enumerate(scenario_labels):
        times_sec = []
        for size in table_sizes:
            avg_t_us = data_time[scenario][size]
            avg_t_s = avg_t_us / 1e6
            times_sec.append(avg_t_s)

        x_positions = x + (s_idx - len(scenario_labels)/2)*bar_width + bar_width/2
        ax.bar(x_positions, times_sec, bar_width, label=scenario_legend_map[scenario])

    ax.set_title("Tempo di Elaborazione Richieste (secondi)\n(Multi-core generatore tabella)")
    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in table_sizes], rotation=45)
    ax.set_ylabel("Tempo Elaborazione (s)")
    ax.set_xlabel("Dimensione tabella (# righe)")
    ax.grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
    ax.legend()

    plt.tight_layout()
    out_file = os.path.join(output_dir, "execution_time_barplot.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_execution_time_normalized(data_time_norm, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot dei tempi di esecuzione (valori normalizzati a 1S).
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(table_sizes))
    bar_width = 0.1

    for s_idx, scenario in enumerate(scenario_labels):
        ratios = []
        for size in table_sizes:
            ratio = data_time_norm[scenario][size]
            ratios.append(ratio)

        x_positions = x + (s_idx - len(scenario_labels)/2)*bar_width + bar_width/2
        ax.bar(x_positions, ratios, bar_width, label=scenario_legend_map[scenario])

    ax.set_title("Tempo di Elaborazione Richieste (Normalizzato ad 1 Server)\n(Multi-core generatore tabella)")
    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in table_sizes], rotation=45)
    ax.set_ylabel("Tempo Normalizzato")
    ax.set_xlabel("Dimensione tabella (# righe)")
    ax.grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
    ax.legend()

    plt.tight_layout()
    out_file = os.path.join(output_dir, "execution_time_barplot_normalized.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_execution_time_normalized(data_time_norm, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot dei tempi di esecuzione (valori normalizzati a 1S).
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(table_sizes))
    bar_width = 0.1

    for s_idx, scenario in enumerate(scenario_labels):
        ratios = []
        for size in table_sizes:
            ratio = data_time_norm[scenario][size]
            ratios.append(ratio)

        x_positions = x + (s_idx - len(scenario_labels)/2)*bar_width + bar_width/2
        ax.bar(x_positions, ratios, bar_width, label=scenario_legend_map[scenario])

    ax.set_title("Tempo di Elaborazione Richieste (Normalizzato ad 1 server)\n(Multi-core generatore tabella)")
    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in table_sizes], rotation=45)
    ax.set_ylabel("Tempo Normalizzato")
    ax.set_xlabel("Dimensione tabella (# righe)")
    ax.grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
    ax.legend()

    plt.tight_layout()
    out_file = os.path.join(output_dir, "execution_time_barplot_normalized.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_tlb_misses(data_tlb, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot con valori assoluti di TLB L1 e L2.
    """
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    x = np.arange(len(table_sizes))
    bar_width = 0.1

    # TLB L1
    for s_idx, scenario in enumerate(scenario_labels):
        l1_vals = []
        for size in table_sizes:
            (tlb_l1, _) = data_tlb[scenario][size]
            l1_vals.append(tlb_l1)

        x_positions = x + (s_idx - len(scenario_labels)/2)*bar_width + bar_width/2
        axes[0].bar(x_positions, l1_vals, bar_width, label=scenario_legend_map[scenario])

    axes[0].set_title("TLB L1 Miss\n(Multi-core generatore tabella)")
    axes[0].set_ylabel("TLB L1 Miss")
    axes[0].grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
    axes[0].yaxis.set_major_formatter(FuncFormatter(short_number_formatter))
    axes[0].legend()

    # TLB L2
    for s_idx, scenario in enumerate(scenario_labels):
        l2_vals = []
        for size in table_sizes:
            (_, tlb_l2) = data_tlb[scenario][size]
            l2_vals.append(tlb_l2)

        x_positions = x + (s_idx - len(scenario_labels)/2)*bar_width + bar_width/2
        axes[1].bar(x_positions, l2_vals, bar_width, label=scenario_legend_map[scenario])

    axes[1].set_title("TLB L2 Miss\n(Multi-core generatore tabella)")
    axes[1].set_ylabel("TLB L2 Miss")
    axes[1].grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
    axes[1].yaxis.set_major_formatter(FuncFormatter(short_number_formatter))

    axes[1].set_xticks(x)
    axes[1].set_xticklabels([str(s) for s in table_sizes], rotation=45)
    axes[1].set_xlabel("Dimensione tabella (# righe)")
    axes[1].legend()

    plt.tight_layout()
    out_file = os.path.join(output_dir, "tlb_misses_subplots.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_tlb_misses_normalized(data_tlb_norm, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot con valori NORMALIZZATI di TLB L1 e L2.
    """
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    x = np.arange(len(table_sizes))
    bar_width = 0.1

    # TLB L1
    for s_idx, scenario in enumerate(scenario_labels):
        l1_vals = []
        for size in table_sizes:
            (tlb_l1, _) = data_tlb_norm[scenario][size]
            l1_vals.append(tlb_l1)

        x_positions = x + (s_idx - len(scenario_labels)/2)*bar_width + bar_width/2
        axes[0].bar(x_positions, l1_vals, bar_width, label=scenario_legend_map[scenario])

    axes[0].set_title("TLB L1 Miss (Normalizzato ad 1 Server)\n(Multi-core generatore tabella)")
    axes[0].set_ylabel("TLB L1 Normalizzato")
    axes[0].grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
    axes[0].legend()

    # TLB L2
    for s_idx, scenario in enumerate(scenario_labels):
        l2_vals = []
        for size in table_sizes:
            (_, tlb_l2) = data_tlb_norm[scenario][size]
            l2_vals.append(tlb_l2)

        x_positions = x + (s_idx - len(scenario_labels)/2)*bar_width + bar_width/2
        axes[1].bar(x_positions, l2_vals, bar_width, label=scenario_legend_map[scenario])

    axes[1].set_title("TLB L2 Miss (Normalizzato ad 1 Server)\n(Multi-core generatore tabella)")
    axes[1].set_ylabel("TLB L2 Normalizzato")
    axes[1].grid(True, which='major', axis='both', linestyle='--', alpha=0.7)

    axes[1].set_xticks(x)
    axes[1].set_xticklabels([str(s) for s in table_sizes], rotation=45)
    axes[1].set_xlabel("Dimensione tabella (# righe)")
    axes[1].legend()

    plt.tight_layout()
    out_file = os.path.join(output_dir, "tlb_misses_subplots_normalized.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

# --------------------------------------------------------------------------------
# 4) MAIN (CASO MULTI-CORE) - con THROUGHPUT aggiunto in scala lineare
# --------------------------------------------------------------------------------

def main():
    """
    Questo main è per il caso MULTI-CORE, con AGGIUNTA DEL THROUGHPUT (lineare).
    """
    # Percorso dove salvare le figure
    output_dir = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Table Generator/Multi Core/Plots"

    # Definisci i percorsi base (Multi-Core)
    base_path_1_server_cache = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Table Generator/Multi Core/1 Active Server/perf_results_table_cache_misses"
    base_path_2_server_cache = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Table Generator/Multi Core/2 Active Server/perf_results_table_cache_misses"
    base_path_3_server_cache = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Table Generator/Multi Core/3 Active Server/perf_results_table_cache_misses"

    base_path_1_server_time = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Table Generator/Multi Core/1 Active Server/perf_table_results_time"
    base_path_2_server_time = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Table Generator/Multi Core/2 Active Server/perf_table_results_time"
    base_path_3_server_time = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Table Generator/Multi Core/3 Active Server/perf_table_results_time"

    base_path_1_server_tlb = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Table Generator/Multi Core/1 Active Server/perf_results_table_tlb_misses"
    base_path_2_server_tlb = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Table Generator/Multi Core/2 Active Server/perf_results_table_tlb_misses"
    base_path_3_server_tlb = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Table Generator/Multi Core/3 Active Server/perf_results_table_tlb_misses"

    # Dimensioni di tabella (numero di righe)
    table_sizes = [
        10000, 50000, 100000, 200000, 300000, 400000,
        500000, 600000, 700000, 800000, 900000, 1000000
    ]

    # Frequenze di disturbo (LOW, MEDIUM, HIGH)
    freqs = ["LOW", "MEDIUM", "HIGH"]

    # Carichiamo i dati di Cache e Tempo
    data_cache = carica_dati_cache_miss(
        base_path_1_server_cache,
        base_path_2_server_cache,
        base_path_3_server_cache,
        table_sizes,
        freqs
    )
    data_time = carica_dati_tempo(
        base_path_1_server_time,
        base_path_2_server_time,
        base_path_3_server_time,
        table_sizes,
        freqs
    )
    data_tlb = carica_dati_tlb(
        base_path_1_server_tlb,
        base_path_2_server_tlb,
        base_path_3_server_tlb,
        table_sizes,
        freqs
    )

    # Carichiamo i dati delle richieste (Iter) - NOVITÀ
    data_requests = carica_dati_richieste(
        base_path_1_server_time,
        base_path_2_server_time,
        base_path_3_server_time,
        table_sizes,
        freqs
    )

    # I 7 scenari (ordine con cui plottare):
    scenario_labels = [
        "1S",
        "2S_LOW", "2S_MEDIUM", "2S_HIGH",
        "3S_LOW", "3S_MEDIUM", "3S_HIGH"
    ]

    # Mappa per le legende
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
    # 1) PLOT VALORI ASSOLUTI
    # -------------------------------
    # a) Miss (assoluti)
    plot_cache_misses(data_cache, table_sizes, scenario_labels, scenario_legend_map, output_dir)
    # b) Miss Rate
    plot_cache_miss_rate(data_cache, table_sizes, scenario_labels, scenario_legend_map, output_dir)
    # c) Tempo di esecuzione (assoluto)
    plot_execution_time(data_time, table_sizes, scenario_labels, scenario_legend_map, output_dir)
    # d) TLB Misses (assoluti)
    plot_tlb_misses(data_tlb, table_sizes, scenario_labels, scenario_legend_map, output_dir)
    # e) Throughput (NUOVO, in scala lineare)
    plot_throughput(data_time, data_requests, table_sizes, scenario_labels, scenario_legend_map, output_dir)

    # -------------------------------
    # 2) PLOT VALORI NORMALIZZATI RISPETTO A 1S
    # -------------------------------
    data_cache_norm = normalizza_cache_miss(data_cache, table_sizes, scenario_labels)
    data_time_norm  = normalizza_tempo(data_time, table_sizes, scenario_labels)
    data_tlb_norm   = normalizza_tlb_miss(data_tlb, table_sizes, scenario_labels)

    # f) Miss (normalizzati)
    plot_cache_misses_normalized(data_cache_norm, table_sizes, scenario_labels, scenario_legend_map, output_dir)
    # g) Tempo (normalizzato)
    plot_execution_time_normalized(data_time_norm, table_sizes, scenario_labels, scenario_legend_map, output_dir)
    # h) TLB Misses (normalizzati)
    plot_tlb_misses_normalized(data_tlb_norm, table_sizes, scenario_labels, scenario_legend_map, output_dir)


if __name__ == "__main__":
    main()