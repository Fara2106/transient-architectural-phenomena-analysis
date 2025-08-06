import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def format_size(pages):
    """Format page numbers for better readability"""
    if pages >= 1024:
        return f'{pages/1024:.0f}K'
    return f'{pages}'

def read_execution_time(file_path):
    time_value = 0
    with open(file_path, 'r') as f:
        for line in f:
            line_split = line.split()
            if len(line_split) < 3:
                continue
            if 'seconds' in line:
                time_value = float(line_split[0].replace(',', '.'))
    return time_value

if __name__ == '__main__':
    OUTPUT_DIR = '/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Progetti/Random access array/random_access_array_TLB/output_time_TLB'

    OUTPUT_FILES = {
        1: 'time_1.txt', 2: 'time_2.txt', 4: 'time_4.txt',
        8: 'time_8.txt', 16: 'time_16.txt', 32: 'time_32.txt',
        64: 'time_64.txt', 128: 'time_128.txt', 256: 'time_256.txt',
        512: 'time_512.txt', 1024: 'time_1024.txt', 2048: 'time_2048.txt',
        4096: 'time_4096.txt', 8192: 'time_8192.txt', 16384: 'time_16384.txt',
        32768: 'time_32768.txt', 65536: 'time_65536.txt',
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

    EXECUTION_TIMES = {}

    # Leggiamo i file e estraiamo i tempi di esecuzione
    for size, output_file in OUTPUT_FILES.items():
        file_path = os.path.join(OUTPUT_DIR, output_file)
        time_value = read_execution_time(file_path)
        EXECUTION_TIMES[size] = time_value

    # Create figure
    fig, ax = plt.subplots(figsize=(16, 10))

    # Get x values and format labels
    x_values = list(EXECUTION_TIMES.keys())
    x_ticks = [format_size(x) for x in x_values]

    # Plot execution times and TLB capacity lines
    ax.plot(x_values, list(EXECUTION_TIMES.values()), 
            marker='o', color='orange', linewidth=2, 
            markersize=8, label='Tempo Esecuzione')
    ax.axvline(64, linestyle='--', color='red', 
               label='Capacità L1 TLB (64 Pagine)')
    ax.axvline(1536, linestyle='--', color='green', 
               label='Capacità L2 TLB (1536 Pagine)')

    # Configure x axis
    ax.set_xscale('log', base=2)
    ax.set_xticks(x_values)
    ax.set_xticklabels(x_ticks, rotation=0, ha='center')

    # Add minor gridlines
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    ax.grid(True, which='minor', linestyle=':', alpha=0.4)

    # Labels and title
    ax.set_xlabel('Dimensione Array (pagine)', labelpad=10)
    ax.set_ylabel('Tempo Esecuzione (secondi)', labelpad=10)
    ax.set_title('Tempo di Esecuzione per Dimensione Array (TLB)', pad=20)

    # Legend with frame
    ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.8)

    # Layout
    plt.tight_layout()
    plt.savefig('/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Progetti/Random access array/random_access_array_TLB/plots/tlb_execution_time.png',
                bbox_inches='tight', dpi=300)