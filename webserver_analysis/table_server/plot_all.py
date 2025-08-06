import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# --------------------------------------------------------------------------------
# 1) FUNZIONI DI PARSING E FORMATTAZIONE
# --------------------------------------------------------------------------------

def parse_cache_misses(file_path):
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
    avg_time = 0
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r') as f:
        for line in f:
            if 'Average Execution Time:' in line:
                avg_time = parse_number_from_line(line)
    return avg_time

def parse_tlb_misses(file_path):
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
    if x >= 1e9:
        return f"{x/1e9:.1f}G"
    elif x >= 1e6:
        return f"{x/1e6:.1f}M"
    elif x >= 1e3:
        return f"{x/1e3:.1f}k"
    else:
        return str(round(x,2))

# --------------------------------------------------------------------------------
# 2) FUNZIONI DI CARICAMENTO DATI
# --------------------------------------------------------------------------------

def carica_dati_cache_miss(base_path_1_server, base_path_2_server, base_path_3_server, table_sizes, freqs):
    data = {}
    # 1) CASO 1 SERVER
    label_1s = '1S'
    data[label_1s] = {}
    for sz in table_sizes:
        file_name = f"misses_{sz}.txt"
        path_file = os.path.join(base_path_1_server, file_name)
        data[label_1s][sz] = parse_cache_misses(path_file)

    # 2) CASO 2 SERVER
    for freq in freqs:
        label_2s = f"2S_{freq.upper()}"
        data[label_2s] = {}
        for sz in table_sizes:
            file_name = f"misses_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_2_server, file_name)
            data[label_2s][sz] = parse_cache_misses(path_file)

    # 3) CASO 3 SERVER
    for freq in freqs:
        label_3s = f"3S_{freq.upper()}"
        data[label_3s] = {}
        for sz in table_sizes:
            file_name = f"misses_{sz}_{freq.upper()}Hz.txt"
            path_file = os.path.join(base_path_3_server, file_name)
            data[label_3s][sz] = parse_cache_misses(path_file)

    return data

def carica_dati_tempo(base_path_1_server, base_path_2_server, base_path_3_server, table_sizes, freqs):
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
    Restituisce un nuovo dict con ratio = data_cache[scenario][sz] / data_cache['1S'][sz].
    data_cache[scenario][sz] = (l1, l2, l3).
    """
    data_norm = {}
    # Copiamo la struttura
    for scenario in scenario_labels:
        data_norm[scenario] = {}
        for sz in table_sizes:
            l1, l2, l3 = data_cache[scenario][sz]
            l1_1s, l2_1s, l3_1s = data_cache["1S"][sz]
            # Evitiamo la divisione per zero
            norm_l1 = (l1 / l1_1s) if l1_1s != 0 else 0
            norm_l2 = (l2 / l2_1s) if l2_1s != 0 else 0
            norm_l3 = (l3 / l3_1s) if l3_1s != 0 else 0
            data_norm[scenario][sz] = (norm_l1, norm_l2, norm_l3)
    return data_norm

def normalizza_tempo(data_time, table_sizes, scenario_labels):
    """
    data_time[scenario][sz] = tempo medio in microsecondi.
    ratio = data_time[scenario][sz] / data_time['1S'][sz].
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
    data_tlb[scenario][sz] = (l1_miss, l2_miss).
    ratio = data_tlb[scenario][sz] / data_tlb['1S'][sz].
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
# 3) FUNZIONI DI PLOT
# --------------------------------------------------------------------------------

def plot_cache_misses(data_cache, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot con valori assoluti di L1, L2, L3 (3 subplots).
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    x = np.arange(len(table_sizes))
    bar_width = 0.1

    for i, level in enumerate(["L1", "L2", "L3"]):
        ax = axes[i]
        for s_idx, scenario in enumerate(scenario_labels):
            values = []
            for size in table_sizes:
                (l1, l2, l3) = data_cache[scenario][size]
                if level == "L1":
                    values.append(l1)
                elif level == "L2":
                    values.append(l2)
                else:
                    values.append(l3)

            x_positions = x + (s_idx - len(scenario_labels)/2)*bar_width + bar_width/2
            ax.bar(x_positions, values, bar_width, 
                   label=scenario_legend_map[scenario])

        ax.set_title(f"{level} Miss\n(Analysis for the single-core table generator)")
        ax.set_ylabel(f"{level} Miss")
        ax.grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
        ax.yaxis.set_major_formatter(FuncFormatter(short_number_formatter))
        ax.legend()

    axes[-1].set_xticks(x)
    axes[-1].set_xticklabels([str(s) for s in table_sizes], rotation=45)
    axes[-1].set_xlabel("Table size")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "cache_misses_subplots.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_cache_misses_normalized(data_cache_norm, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot con valori NORMALIZZATI (ratio rispetto a 1S) di L1, L2, L3 (3 subplots).
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    x = np.arange(len(table_sizes))
    bar_width = 0.1

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
            ax.bar(x_positions, values, bar_width, 
                   label=scenario_legend_map[scenario])

        ax.set_title(f"{level} Miss (Normalized to 1 Server)\n(single-core table generator)")
        ax.set_ylabel(f"{level} Ratio")
        ax.grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
        ax.legend()

    axes[-1].set_xticks(x)
    axes[-1].set_xticklabels([str(s) for s in table_sizes], rotation=45)
    axes[-1].set_xlabel("Table size")

    plt.tight_layout()
    out_file = os.path.join(output_dir, "cache_misses_subplots_normalized.png")
    plt.savefig(out_file, dpi=300)
    plt.show()


def plot_execution_time(data_time, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot con valori assoluti di tempo (in secondi).
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

    ax.set_title("Execution Time (seconds)\n(Analysis for the single-core table generator)")
    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in table_sizes], rotation=45)
    ax.set_ylabel("Execution time (s)")
    ax.set_xlabel("Table size")
    ax.grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
    ax.legend()

    plt.tight_layout()
    out_file = os.path.join(output_dir, "execution_time_barplot.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

def plot_execution_time_normalized(data_time_norm, table_sizes, scenario_labels, scenario_legend_map, output_dir):
    """
    Plot con valori NORMALIZZATI di tempo (rapporto con 1S).
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

    ax.set_title("Execution Time (Normalized to 1 Server)\n(single-core table generator)")
    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in table_sizes], rotation=45)
    ax.set_ylabel("Time ratio")
    ax.set_xlabel("Table size")
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

    axes[0].set_title("TLB L1 Miss\n(Analysis for the single-core table generator)")
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

    axes[1].set_title("TLB L2 Miss\n(Analysis for the single-core table generator)")
    axes[1].set_ylabel("TLB L2 Miss")
    axes[1].grid(True, which='major', axis='both', linestyle='--', alpha=0.7)
    axes[1].yaxis.set_major_formatter(FuncFormatter(short_number_formatter))

    axes[1].set_xticks(x)
    axes[1].set_xticklabels([str(s) for s in table_sizes], rotation=45)
    axes[1].set_xlabel("Table size")
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

    axes[0].set_title("TLB L1 Miss (Normalized to 1 Server)\n(single-core table generator)")
    axes[0].set_ylabel("TLB L1 Ratio")
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

    axes[1].set_title("TLB L2 Miss (Normalized to 1 Server)\n(single-core table generator)")
    axes[1].set_ylabel("TLB L2 Ratio")
    axes[1].grid(True, which='major', axis='both', linestyle='--', alpha=0.7)

    axes[1].set_xticks(x)
    axes[1].set_xticklabels([str(s) for s in table_sizes], rotation=45)
    axes[1].set_xlabel("Table size")
    axes[1].legend()

    plt.tight_layout()
    out_file = os.path.join(output_dir, "tlb_misses_subplots_normalized.png")
    plt.savefig(out_file, dpi=300)
    plt.show()

# --------------------------------------------------------------------------------
# 4) MAIN
# --------------------------------------------------------------------------------

def main():
    # Percorso dove salvare le figure
    output_dir = "/home2/faraoni/Progetti/webServer_aggiuntivi/1_tableGenerator"

    # Definisci i percorsi base
    base_path_1_server_cache = "/home2/faraoni/Progetti/webServer_aggiuntivi/1_tableGenerator/1 Active Server/Cache_misses/perf_results_table_cache_misses"
    base_path_2_server_cache = "/home2/faraoni/Progetti/webServer_aggiuntivi/1_tableGenerator/2 Active Server/Cache_misses/perf_results_table_cache_misses"
    base_path_3_server_cache = "/home2/faraoni/Progetti/webServer_aggiuntivi/1_tableGenerator/3 Active Server/Cache_misses/perf_results_table_cache_misses"

    base_path_1_server_time = "/home2/faraoni/Progetti/webServer_aggiuntivi/1_tableGenerator/1 Active Server/Execution_time/perf_table_results_time"
    base_path_2_server_time = "/home2/faraoni/Progetti/webServer_aggiuntivi/1_tableGenerator/2 Active Server/Execution_time/perf_table_results_time"
    base_path_3_server_time = "/home2/faraoni/Progetti/webServer_aggiuntivi/1_tableGenerator/3 Active Server/Execution_time/perf_table_results_time"

    base_path_1_server_tlb = "/home2/faraoni/Progetti/webServer_aggiuntivi/1_tableGenerator/1 Active Server/TLB_misses/perf_results_table_tlb_misses"
    base_path_2_server_tlb = "/home2/faraoni/Progetti/webServer_aggiuntivi/1_tableGenerator/2 Active Server/TLB_misses/perf_results_table_tlb_misses"
    base_path_3_server_tlb = "/home2/faraoni/Progetti/webServer_aggiuntivi/1_tableGenerator/3 Active Server/TLB_misses/perf_results_table_tlb_misses"

    # Dimensioni di tabella
    table_sizes = [
        10000, 50000, 100000, 200000, 300000, 400000,
        500000, 600000, 700000, 800000, 900000, 1000000
    ]

    # Frequenze di disturbo
    freqs = ["LOW", "MEDIUM", "HIGH"]

    # Carichiamo i dati
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

    # I 7 scenari (ordine con cui plottare internamente)
    scenario_labels = [
        "1S",
        "2S_LOW", "2S_MEDIUM", "2S_HIGH",
        "3S_LOW", "3S_MEDIUM", "3S_HIGH"
    ]

    # Legende
    scenario_legend_map = {
        "1S":       "1 Server (no disturbance)",
        "2S_LOW":   "2 Servers (low disturbance)",
        "2S_MEDIUM":"2 Servers (medium disturbance)",
        "2S_HIGH":  "2 Servers (high disturbance)",
        "3S_LOW":   "3 Servers (low disturbance)",
        "3S_MEDIUM":"3 Servers (medium disturbance)",
        "3S_HIGH":  "3 Servers (high disturbance)",
    }

    # -------------------------------
    # 1) PLOT VALORI ASSOLUTI
    # -------------------------------
    # Cache Misses
    plot_cache_misses(data_cache, table_sizes, scenario_labels, scenario_legend_map, output_dir)
    # Tempo
    plot_execution_time(data_time, table_sizes, scenario_labels, scenario_legend_map, output_dir)
    # TLB Misses
    plot_tlb_misses(data_tlb, table_sizes, scenario_labels, scenario_legend_map, output_dir)

    # -------------------------------
    # 2) PLOT VALORI NORMALIZZATI RISPETTO A 1S
    # -------------------------------
    data_cache_norm = normalizza_cache_miss(data_cache, table_sizes, scenario_labels)
    data_time_norm  = normalizza_tempo(data_time, table_sizes, scenario_labels)
    data_tlb_norm   = normalizza_tlb_miss(data_tlb, table_sizes, scenario_labels)

    # Cache Misses (normalized)
    plot_cache_misses_normalized(data_cache_norm, table_sizes, scenario_labels, scenario_legend_map, output_dir)
    # Tempo (normalized)
    plot_execution_time_normalized(data_time_norm, table_sizes, scenario_labels, scenario_legend_map, output_dir)
    # TLB Misses (normalized)
    plot_tlb_misses_normalized(data_tlb_norm, table_sizes, scenario_labels, scenario_legend_map, output_dir)


if __name__ == "__main__":
    main()
