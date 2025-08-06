import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def format_size(pages):
    """Format page numbers for better readability"""
    if pages >= 1024:
        return f'{pages/1024:.0f}K'
    return f'{pages}'

def format_misses(value):
    """Format miss numbers with K/M suffix"""
    if value >= 1e6:
        return f'{value/1e6:.1f}M'
    elif value >= 1e3:
        return f'{value/1e3:.1f}K'
    return f'{value:.0f}'

def read_misses(file_path):
    l1_misses = 0
    l2_misses = 0
    stlb_hit_load = stlb_hit_store = l2_misses_load = l2_misses_store = 0
    
    with open(file_path, 'r') as f:
        for line in f:
            line_split = line.split()
            if len(line_split) < 3:
                continue
            if 'dTLB_load_misses.stlb_hit' in line:
                stlb_hit_load = float(line_split[0].replace('.', '').replace(',', '.'))
            elif 'dTLB_store_misses.stlb_hit'  in line:
                stlb_hit_store = float(line_split[0].replace('.', '').replace(',', '.'))
            elif 'dTLB_load_misses.miss_causes_a_walk' in line:
                l2_misses_load = float(line_split[0].replace('.', '').replace(',', '.'))
            elif 'dTLB_store_misses.miss_causes_a_walk' in line:
                l2_misses_store = float(line_split[0].replace('.', '').replace(',', '.'))
    
    stlb_hit = stlb_hit_load + stlb_hit_store
    l2_misses = l2_misses_load + l2_misses_store
    l1_misses = stlb_hit + l2_misses
    return l1_misses, l2_misses

if __name__ == '__main__':
    OUTPUT_DIR = '/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Progetti/Random access array/random_access_array_TLB/output_TLB_miss_analysis'

    # Configurazione dei file
    OUTPUT_FILES = {
        1: 'miss_1.txt', 2: 'miss_2.txt', 4: 'miss_4.txt',
        8: 'miss_8.txt', 16: 'miss_16.txt', 32: 'miss_32.txt',
        64: 'miss_64.txt', 128: 'miss_128.txt', 256: 'miss_256.txt',
        512: 'miss_512.txt', 1024: 'miss_1024.txt', 2048: 'miss_2048.txt',
        4096: 'miss_4096.txt', 8192: 'miss_8192.txt', 16384: 'miss_16384.txt',
        32768: 'miss_32768.txt', 65536: 'miss_65536.txt'
    }

    # Set font sizes
    plt.rcParams.update({
        'font.size': 14, # dimensione base font
        'axes.labelsize': 25, # dimensione font assi
        'axes.titlesize': 30, # font titolo
        'xtick.labelsize': 14, # tick asse x
        'ytick.labelsize': 14, # tick asse y
        'legend.fontsize': 22 # font legenda
    })
    plt.style.use('seaborn-v0_8-whitegrid')

    # Dati per i grafici
    L1_MISSES_TOTAL = {}
    L2_MISSES_TOTAL = {}

    # Lettura dei dati
    for size, output_file in OUTPUT_FILES.items():
        miss_l1, miss_l2 = read_misses(os.path.join(OUTPUT_DIR, output_file))
        L1_MISSES_TOTAL[size] = miss_l1
        L2_MISSES_TOTAL[size] = miss_l2

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 20))  # Aumentata la larghezza a 20

    # Format x-axis labels
    x_values = list(L1_MISSES_TOTAL.keys())
    x_ticks = [format_size(x) for x in x_values]

    # Plot L1 Misses with both TLB capacity lines
    ax1.plot(x_values, list(L1_MISSES_TOTAL.values()), 
             marker='o', color='orange', linewidth=2, 
             markersize=8, label='L1 TLB Misses')
    ax1.axvline(64, linestyle='--', color='red', 
                label='Capacità L1 TLB (64 Pagine)')
    ax1.axvline(1536, linestyle='--', color='green', 
                label='Capacità L2 TLB (1536 Pagine)')
    
    # Plot L2 Misses with both TLB capacity lines
    ax2.plot(x_values, list(L2_MISSES_TOTAL.values()), 
             marker='o', color='purple', linewidth=2, 
             markersize=8, label='L2 TLB Misses')
    ax2.axvline(64, linestyle='--', color='red', 
                label='Capacità L1 TLB (64 Pagine)')
    ax2.axvline(1536, linestyle='--', color='green', 
                label='Capacità L2 TLB (1536 Pagine)')

    # Configure both axes
    for ax, title in [(ax1, 'L1 TLB Misses'), (ax2, 'L2 TLB Misses')]:
        ax.set_xscale('log', base=2)
        ax.set_xticks(x_values)
        ax.set_xticklabels(x_ticks, rotation=0, ha='center')
        
        # Format y-axis
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
            lambda x, p: format_misses(x)))
        
        ax.set_xlabel('Dimensione Array (pagine)', labelpad=10)
        ax.set_ylabel('Numero di Misses', labelpad=10)
        # Add legend with semi-transparent white background
        ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.8)
        ax.grid(True, which='both', linestyle='--', alpha=0.7)
        ax.set_title(title, pad=20)
        
        # Add minor gridlines
        ax.grid(True, which='minor', linestyle=':', alpha=0.4)

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.3)  # Aumentato lo spazio tra i subplot

    plt.savefig('/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Progetti/Random access array/random_access_array_TLB/plots/tlb_misses.png',
                bbox_inches='tight', dpi=300)