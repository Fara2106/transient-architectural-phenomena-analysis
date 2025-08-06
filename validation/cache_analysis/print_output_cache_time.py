import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def format_size(exp):
    size = 2 ** int(exp)
    if size >= 1024 * 1024:
        return f'{size / (1024 * 1024):.0f}M'
    elif size >= 1024:
        return f'{size / 1024:.0f}K'
    else:
        return f'{size}'

def read_time_from_file(file_path):
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
    OUTPUT_DIR = '/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Progetti/Random access array/random_access_array_cache/output_time_analysis'

    OUTPUT_FILES = {
        '1': 'output_1.txt', '2': 'output_2.txt', '3': 'output_3.txt',
        '4': 'output_4.txt', '5': 'output_5.txt', '6': 'output_6.txt',
        '7': 'output_7.txt', '8': 'output_8.txt', '9': 'output_9.txt',
        '10': 'output_10.txt', '11': 'output_11.txt', '12': 'output_12.txt',
        '13': 'output_13.txt', '14': 'output_14.txt', '15': 'output_15.txt',
        '16': 'output_16.txt', '17': 'output_17.txt', '18': 'output_18.txt',
        '19': 'output_19.txt', '20': 'output_20.txt', '21': 'output_21.txt',
        '22': 'output_22.txt', '23': 'output_23.txt', '24': 'output_24.txt',
        '25': 'output_25.txt', '26': 'output_26.txt', '27': 'output_27.txt',
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

    RESULTS = {}
    # Leggiamo i file e estraiamo i tempi di esecuzione
    for size, output_file in OUTPUT_FILES.items():
        file_path = os.path.join(OUTPUT_DIR, output_file)
        time_value = read_time_from_file(file_path)
        RESULTS[size] = time_value

    fig, ax = plt.subplots(figsize=(16, 10)) 

    # Create x-axis labels
    x_values = list(RESULTS.keys())
    x_ticks = [format_size(x) for x in x_values]

    # Set x-ticks and labels for all values
    ax.set_xticks(range(len(x_values)))
    ax.set_xticklabels(x_ticks, rotation=0, ha='center') 

    # Convert cache sizes to array indices
    cache_lines = {
        'L1': (list(range(len(x_values)))[x_values.index('14')], 'red', 'L1 Cache (32 KB)'),
        'L2': (list(range(len(x_values)))[x_values.index('17')], 'green', 'L2 Cache (256 KB)'),
        'L3': (list(range(len(x_values)))[x_values.index('23')], 'blue', 'L3 Cache (16 MB)')
    }
    
    # Add vertical lines for cache capacities
    for position, color, label in cache_lines.values():
        ax.axvline(position, linestyle='--', color=color, label=label)

    # Plot execution times
    ax.plot(range(len(x_values)), list(RESULTS.values()), 
            marker='o', color='orange', linewidth=2, 
            markersize=8, label='Tempo di Esecuzione')

    # Labels and title
    ax.set_xlabel('Dimensione Array (B)', labelpad=10)
    ax.set_ylabel('Tempo di Esecuzione (secondi)', labelpad=10)
    ax.set_title('Tempo di Esecuzione per Dimensione Array (cache)', pad=20)

    # Legend with semi-transparent background
    ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.8)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Add extra space at the bottom for the labels
    plt.subplots_adjust(bottom=0.15)

    plt.savefig('/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Progetti/Random access array/random_access_array_cache/plots/cache_execution_time.png', 
                bbox_inches='tight', dpi=300)