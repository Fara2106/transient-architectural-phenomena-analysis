import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# --------------------------------------------------------------------------------
# 1) FUNZIONI DI PARSING E FORMATTAZIONE
# --------------------------------------------------------------------------------

def parse_cache_misses(file_path):
    """Parsa i file con le tre tipologie di cache misses (L1, L2, L3)."""
    l1_miss, l2_miss, l3_miss = 0, 0, 0
    if not os.path.exists(file_path):
        return (0, 0, 0)
    with open(file_path, 'r') as f:
        for line in f:
            if 'mem_load_retired.l1_miss' in line:
                l1_miss = parse_number_from_line(line)
            elif 'mem_load_retired.l2_miss' in line:
                l2_miss = parse_number_from_line(line)
            elif 'mem_load_retired.l3_miss' in line:
                l3_miss = parse_number_from_line(line)
    return (l1_miss, l2_miss, l3_miss)

def parse_execution_time(file_path):
    """Parsa i file che contengono il tempo medio di esecuzione (in microsecondi)."""
    avg_time = 0
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r') as f:
        for line in f:
            if 'Average Execution Time:' in line:
                avg_time = parse_number_from_line(line)
    return avg_time

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

    # Nel codice di esempio, si sommavano i "walk" (L2) e si definiva L1 come somma di stlb_hit + walk
    l2_miss = dtlb_load_walk + dtlb_store_walk
    l1_miss = dtlb_load_stlb_hit + dtlb_store_stlb_hit + l2_miss
    return (l1_miss, l2_miss)

def parse_number_from_line(line):
    """
    Estrae il primo numero (float) da una riga, rimuovendo i separatori di migliaia e
    convertendo le virgole in punti decimali.
    """
    line_clean = re.sub(r'(?<=\d)\.(?=\d)', '', line.strip())  # rimuove i punti "migliaia"
    line_clean = line_clean.replace(',', '.')
    match = re.search(r'(\d+(\.\d+)?)', line_clean)
    if match:
        return float(match.group(1))
    return 0

def short_number_formatter(x, pos):
    """
    Formatta i grandi numeri: es. 1500 -> 1.5k, 2.5 milioni -> 2.5M, ecc.
    """
    if x >= 1e9:
        return f"{x/1e9:.1f}G"
    elif x >= 1e6:
        return f"{x/1e6:.1f}M"
    elif x >= 1e3:
        return f"{x/1e3:.1f}K"
    else:
        return str(round(x,2))

# --------------------------------------------------------------------------------
# 2) FUNZIONI DI CARICAMENTO DATI
# --------------------------------------------------------------------------------

def carica_dati_cache_miss(base_path_1_server, base_path_2_server, base_path_3_server, matrix_sizes, freqs):
    """
    Carica i dati delle cache misses per i 3 scenari (1S, 2S, 3S).
    Ritorna un dict: data[scenario][matrix_size] = (l1_miss, l2_miss, l3_miss).
    """
    data = {}

    # 1) CASO 1 SERVER
    label_1s = '1S'
    data[label_1s] = {}
    for sz in matrix_sizes:
        file_name = f"misses_{sz}.txt"
        path_file = os.path.join(base_path_1_server, file_name)
        data[label_1s][sz] = parse_cache_misses(path_file)

    # 2) CASO 2 SERVER
    for freq in freqs:
        label_2s = f"2S_{freq.upper()}"
        data[label_2s] = {}
        for sz in matrix_sizes:
            file_name = f"misses_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_2_server, file_name)
            data[label_2s][sz] = parse_cache_misses(path_file)

    # 3) CASO 3 SERVER
    for freq in freqs:
        label_3s = f"3S_{freq.upper()}"
        data[label_3s] = {}
        for sz in matrix_sizes:
            file_name = f"misses_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_3_server, file_name)
            data[label_3s][sz] = parse_cache_misses(path_file)

    return data

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

def normalizza_cache_miss(data_cache, matrix_sizes, scenario_labels):
    """
    Ritorna un dict normalizzato rispetto al caso '1S':
    data_cache_norm[scenario][sz] = (l1_ratio, l2_ratio, l3_ratio).
    """
    data_norm = {}
    for scenario in scenario_labels:
        data_norm[scenario] = {}
        for sz in matrix_sizes:
            l1, l2, l3 = data_cache[scenario][sz]
            l1_1s, l2_1s, l3_1s = data_cache['1S'][sz]
            norm_l1 = (l1 / l1_1s) if l1_1s else 0
            norm_l2 = (l2 / l2_1s) if l2_1s else 0
            norm_l3 = (l3 / l3_1s) if l3_1s else 0
            data_norm[scenario][sz] = (norm_l1, norm_l2, norm_l3)
    return data_norm

def normalizza_tempo(data_time, matrix_sizes, scenario_labels):
    """
    Ritorna un dict normalizzato rispetto a '1S' (tempo medio):
    data_time_norm[scenario][sz] = ratio = time_scenario / time_1S.
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
# 3) FUNZIONI DI PLOT
# --------------------------------------------------------------------------------

def _make_grouped_bars(ax, data_dict, matrix_sizes, scenario_labels, scenario_legend_map, y_label,
                       title, is_ratio=False, levels=None):
    """
    Funzione interna che crea un plot a barre raggruppate su asse X in scala log base 2.
    levels: se None => è un caso 'tempo' (valore singolo). Se no => iteriamo su es. [L1, L2, L3].
    is_ratio: se True => label dell'asse Y con 'ratio', se False => label con valore assoluto.
    """
    x = np.array(matrix_sizes, dtype=float)
    # offset di spostamento percentuale su scala log
    bar_offset = 0.07  # puoi cambiare se vuoi aumentare/diminuire la separazione
    bar_width = 0.06   # "larghezza" nominale
    n_scenarios = len(scenario_labels)

    if levels is None:
        # Caso di un singolo valore per scenario (es. tempo)
        for s_idx, scenario in enumerate(scenario_labels):
            values = []
            for sz in matrix_sizes:
                values.append(data_dict[scenario][sz])  # es. tempo
            # Offset: x * (1 +/- bar_offset) su scala log => un piccolo shift
            x_positions = x * (1 + bar_offset * (s_idx - (n_scenarios - 1)/2))
            ax.bar(x_positions, values, width=bar_width * x, label=scenario_legend_map[scenario])
    else:
        # Caso di più "livelli" (es. L1, L2, L3 => 3 subplots)
        for level_idx, level_name in enumerate(levels):
            for s_idx, scenario in enumerate(scenario_labels):
                # Ricaviamo la tripla (l1, l2, l3) e scegliamo l'elemento giusto
                vals = []
                for sz in matrix_sizes:
                    triple = data_dict[scenario][sz]
                    vals.append(triple[level_idx])
                x_positions = x * (1 + bar_offset * (s_idx - (n_scenarios - 1)/2))
                ax.bar(x_positions, vals, width=bar_width * x, label=scenario_legend_map[scenario] 
                       if level_idx == 0 else "")  # per non duplicare la leggenda su ogni level
            ax.set_title(title)
            ax.set_ylabel(y_label)
        # Gestiamo la leggenda solo una volta
        ax.legend()

    # Impostazioni di layout
    ax.set_xscale('log', base=2)  
    ax.set_xlabel("Matrix size (log2 scale)")
    ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)
    # Tick e label
    ax.set_xticks(matrix_sizes)
    ax.set_xticklabels([str(s) for s in matrix_sizes], rotation=45)
    if not is_ratio:
        ax.yaxis.set_major_formatter(FuncFormatter(short_number_formatter))


def plot_cache_misses(data_cache, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot in verticale (3 subplots) di L1, L2, L3 su scala log2 (asse X).
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 14), sharex=True)
    levels = ["L1", "L2", "L3"]

    for i, level in enumerate(levels):
        ax = axes[i]
        # Prepara i dati "finti" per la funzione _make_grouped_bars
        # Passeremo un levels=[0] (o 1, o 2) di volta in volta. Un piccolo "trick".
        # Oppure ricicliamo la funzione con level_idx fissi.
        for s_idx, scenario in enumerate(scenario_labels):
            vals = []
            for sz in matrix_sizes:
                (l1, l2, l3) = data_cache[scenario][sz]
                if level == "L1":
                    vals.append(l1)
                elif level == "L2":
                    vals.append(l2)
                else:
                    vals.append(l3)
            # offset in log
            x = np.array(matrix_sizes, dtype=float)
            bar_offset = 0.07
            bar_width  = 0.06
            x_positions = x * (1 + bar_offset * (s_idx - (len(scenario_labels) - 1)/2))
            ax.bar(x_positions, vals, width=bar_width * x, 
                   label=scenario_legend_map[scenario] if i == 0 else "")

        ax.set_title(f"{level} Misses")
        ax.set_ylabel(f"{level} Misses")
        ax.set_xscale('log', base=2)
        ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)
        ax.yaxis.set_major_formatter(FuncFormatter(short_number_formatter))

        if i == 0:
            ax.legend()

    # Tick finali solo nell'ultimo subplot
    axes[-1].set_xticks(matrix_sizes)
    axes[-1].set_xticklabels([str(s) for s in matrix_sizes], rotation=45)
    axes[-1].set_xlabel("Matrix size (log2 scale)")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "cache_misses_subplots.png")
    plt.savefig(out_file, dpi=300)
    plt.show()


def plot_cache_misses_normalized(data_cache_norm, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Come sopra ma normalizzati a '1S'.
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 14), sharex=True)
    levels = ["L1", "L2", "L3"]

    for i, level in enumerate(levels):
        ax = axes[i]
        for s_idx, scenario in enumerate(scenario_labels):
            vals = []
            for sz in matrix_sizes:
                (l1, l2, l3) = data_cache_norm[scenario][sz]
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

        ax.set_title(f"{level} Misses (Normalized to 1S)")
        ax.set_ylabel(f"{level} Ratio")
        ax.set_xscale('log', base=2)
        ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)

        if i == 0:
            ax.legend()

    axes[-1].set_xticks(matrix_sizes)
    axes[-1].set_xticklabels([str(s) for s in matrix_sizes], rotation=45)
    axes[-1].set_xlabel("Matrix size (log2 scale)")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "cache_misses_subplots_normalized.png")
    plt.savefig(out_file, dpi=300)
    plt.show()


def plot_execution_time(data_time, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot a barre in un unico subplot con i tempi (in secondi) su asse Y e asse X log2.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.array(matrix_sizes, dtype=float)
    bar_offset = 0.07
    bar_width  = 0.06

    for s_idx, scenario in enumerate(scenario_labels):
        times_sec = []
        for sz in matrix_sizes:
            us = data_time[scenario][sz]     # microsecondi
            times_sec.append(us / 1e6)      # converto in secondi
        x_positions = x * (1 + bar_offset * (s_idx - (len(scenario_labels) - 1)/2))
        ax.bar(x_positions, times_sec, width=bar_width * x, 
               label=scenario_legend_map[scenario])

    ax.set_title("Execution Time (seconds)")
    ax.set_ylabel("Execution time (s)")
    ax.set_xscale('log', base=2)
    ax.set_xlabel("Matrix size (log2 scale)")
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
    Plot a barre in un unico subplot con i tempi normalizzati a '1S'.
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

    ax.set_title("Execution Time (Normalized to 1S)")
    ax.set_ylabel("Time ratio")
    ax.set_xscale('log', base=2)
    ax.set_xlabel("Matrix size (log2 scale)")
    ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)
    ax.legend()

    ax.set_xticks(matrix_sizes)
    ax.set_xticklabels([str(s) for s in matrix_sizes], rotation=45)

    plt.tight_layout()
    out_file = os.path.join(output_dir, "execution_time_barplot_normalized.png")
    plt.savefig(out_file, dpi=300)
    plt.show()


def plot_tlb_misses(data_tlb, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot in verticale (2 subplots): TLB L1 e TLB L2 su scala log2 (asse X).
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

        ax.set_title(level_name)
        ax.set_ylabel(level_name)
        ax.set_xscale('log', base=2)
        ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)
        ax.yaxis.set_major_formatter(FuncFormatter(short_number_formatter))

        if i == 0:
            ax.legend()

    axes[-1].set_xticks(matrix_sizes)
    axes[-1].set_xticklabels([str(s) for s in matrix_sizes], rotation=45)
    axes[-1].set_xlabel("Matrix size (log2 scale)")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "tlb_misses_subplots.png")
    plt.savefig(out_file, dpi=300)
    plt.show()


def plot_tlb_misses_normalized(data_tlb_norm, matrix_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot in verticale (2 subplots) con valori normalizzati a '1S': TLB L1, TLB L2.
    """
    fig, axes = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    levels = ["TLB L1 Misses (Normalized)", "TLB L2 Misses (Normalized)"]

    for i, level_name in enumerate(levels):
        ax = axes[i]
        for s_idx, scenario in enumerate(scenario_labels):
            vals = []
            for sz in matrix_sizes:
                (l1_miss_ratio, l2_miss_ratio) = data_tlb_norm[scenario][sz]
                if i == 0:
                    vals.append(l1_miss_ratio)
                else:
                    vals.append(l2_miss_ratio)

            x = np.array(matrix_sizes, dtype=float)
            bar_offset = 0.07
            bar_width  = 0.06
            x_positions = x * (1 + bar_offset * (s_idx - (len(scenario_labels) - 1)/2))
            ax.bar(x_positions, vals, width=bar_width * x,
                   label=scenario_legend_map[scenario] if i == 0 else "")

        ax.set_title(level_name)
        ax.set_ylabel("Ratio")
        ax.set_xscale('log', base=2)
        ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.7)

        if i == 0:
            ax.legend()

    axes[-1].set_xticks(matrix_sizes)
    axes[-1].set_xticklabels([str(s) for s in matrix_sizes], rotation=45)
    axes[-1].set_xlabel("Matrix size (log2 scale)")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "tlb_misses_subplots_normalized.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

# --------------------------------------------------------------------------------
# 4) MAIN
# --------------------------------------------------------------------------------

def main():
    # Output directory dove salvare i plot (modificalo a tuo piacimento)
    output_dir = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Single Core"

    # Base path per i 3 scenari: 1 server, 2 server, 3 server - Cache Miss
    base_path_1_server_cache = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Single Core/1 Active Server/perf_results_matrix_cache_misses"
    base_path_2_server_cache = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Single Core/2 Active Server/perf_results_matrix_cache_misses"
    base_path_3_server_cache = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Single Core/3 Active Server/perf_results_matrix_cache_misses"

    # Base path per i 3 scenari - Execution Time
    base_path_1_server_time = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Single Core/1 Active Server/perf_matrix_results_time"
    base_path_2_server_time = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Single Core/2 Active Server/perf_matrix_results_time"
    base_path_3_server_time = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Single Core/3 Active Server/perf_matrix_results_time"

    # Base path per i 3 scenari - TLB Miss
    base_path_1_server_tlb = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Single Core/1 Active Server/perf_results_matrix_tlb_misses"
    base_path_2_server_tlb = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Single Core/2 Active Server/perf_results_matrix_tlb_misses"
    base_path_3_server_tlb = "/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Analysis Matrix Multiplication/Single Core/3 Active Server/perf_results_matrix_tlb_misses"

    # Dimensioni matrici (potenze di 2, da 1 a 4096)
    matrix_sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

    # Frequenze di disturbo
    freqs = ["LOW", "MEDIUM", "HIGH"]

    # Carichiamo i dati
    data_cache = carica_dati_cache_miss(
        base_path_1_server_cache,
        base_path_2_server_cache,
        base_path_3_server_cache,
        matrix_sizes,
        freqs
    )
    data_time = carica_dati_tempo(
        base_path_1_server_time,
        base_path_2_server_time,
        base_path_3_server_time,
        matrix_sizes,
        freqs
    )
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
        "1S":       "1 Server (no disturbance)",
        "2S_LOW":   "2 Servers (low)",
        "2S_MEDIUM":"2 Servers (medium)",
        "2S_HIGH":  "2 Servers (high)",
        "3S_LOW":   "3 Servers (low)",
        "3S_MEDIUM":"3 Servers (medium)",
        "3S_HIGH":  "3 Servers (high)",
    }

    # -------------------------------
    # 1) PLOT VALORI ASSOLUTI
    # -------------------------------
    # Cache Misses
    plot_cache_misses(data_cache, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)
    # Tempo
    plot_execution_time(data_time, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)
    # TLB Misses
    plot_tlb_misses(data_tlb, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)

    # -------------------------------
    # 2) PLOT VALORI NORMALIZZATI (rispetto a 1S)
    # -------------------------------
    data_cache_norm = normalizza_cache_miss(data_cache, matrix_sizes, scenario_labels)
    data_time_norm  = normalizza_tempo(data_time, matrix_sizes, scenario_labels)
    data_tlb_norm   = normalizza_tlb_miss(data_tlb, matrix_sizes, scenario_labels)

    # Cache Misses normalizzate
    plot_cache_misses_normalized(data_cache_norm, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)
    # Tempo normalizzato
    plot_execution_time_normalized(data_time_norm, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)
    # TLB Misses normalizzate
    plot_tlb_misses_normalized(data_tlb_norm, matrix_sizes, scenario_labels, scenario_legend_map, output_dir)


if __name__ == "__main__":
    main()
