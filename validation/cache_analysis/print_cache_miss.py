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

def format_misses(value):
    if value >= 1e6:
        return f'{value/1e6:.1f}M'
    elif value >= 1e3:
        return f'{value/1e3:.1f}K'
    return f'{value:.0f}'

def read_misses(output_dir, output_files, event_type):
    results = {}
    for size, output_file in output_files.items():
        file_path = os.path.join(output_dir, output_file)
        with open(file_path, 'r') as f:
            for line in f:
                line_split = line.split()
                if len(line_split) < 3:
                    continue
                if line_split[1] == event_type:
                    misses = float(line_split[0].replace('.', ''))
                    results[size] = misses
    return results

if __name__ == '__main__':
    OUTPUT_DIR = '/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Progetti/Random access array/random_access_array_cache/output_cache_miss_analysis'
    
    L1_FILES = {
        '1': 'L1_misses_1.txt', '2': 'L1_misses_2.txt', '3': 'L1_misses_3.txt', 
        '4': 'L1_misses_4.txt', '5': 'L1_misses_5.txt', '6': 'L1_misses_6.txt',
        '7': 'L1_misses_7.txt', '8': 'L1_misses_8.txt', '9': 'L1_misses_9.txt', 
        '10': 'L1_misses_10.txt', '11': 'L1_misses_11.txt', '12': 'L1_misses_12.txt',
        '13': 'L1_misses_13.txt', '14': 'L1_misses_14.txt', '15': 'L1_misses_15.txt',
        '16': 'L1_misses_16.txt', '17': 'L1_misses_17.txt', '18': 'L1_misses_18.txt',
        '19': 'L1_misses_19.txt', '20': 'L1_misses_20.txt', '21': 'L1_misses_21.txt',
        '22': 'L1_misses_22.txt', '23': 'L1_misses_23.txt', '24': 'L1_misses_24.txt',
        '25': 'L1_misses_25.txt', '26': 'L1_misses_26.txt', '27': 'L1_misses_27.txt'
    }

    L2_FILES = {
        '1': 'L2_misses_1.txt', '2': 'L2_misses_2.txt', '3': 'L2_misses_3.txt',
        '4': 'L2_misses_4.txt', '5': 'L2_misses_5.txt', '6': 'L2_misses_6.txt',
        '7': 'L2_misses_7.txt', '8': 'L2_misses_8.txt', '9': 'L2_misses_9.txt',
        '10': 'L2_misses_10.txt', '11': 'L2_misses_11.txt', '12': 'L2_misses_12.txt',
        '13': 'L2_misses_13.txt', '14': 'L2_misses_14.txt', '15': 'L2_misses_15.txt',
        '16': 'L2_misses_16.txt', '17': 'L2_misses_17.txt', '18': 'L2_misses_18.txt',
        '19': 'L2_misses_19.txt', '20': 'L2_misses_20.txt', '21': 'L2_misses_21.txt',
        '22': 'L2_misses_22.txt', '23': 'L2_misses_23.txt', '24': 'L2_misses_24.txt',
        '25': 'L2_misses_25.txt', '26': 'L2_misses_26.txt', '27': 'L2_misses_27.txt'
    }

    L3_FILES = {
        '1': 'L3_misses_1.txt', '2': 'L3_misses_2.txt', '3': 'L3_misses_3.txt',
        '4': 'L3_misses_4.txt', '5': 'L3_misses_5.txt', '6': 'L3_misses_6.txt',
        '7': 'L3_misses_7.txt', '8': 'L3_misses_8.txt', '9': 'L3_misses_9.txt',
        '10': 'L3_misses_10.txt', '11': 'L3_misses_11.txt', '12': 'L3_misses_12.txt',
        '13': 'L3_misses_13.txt', '14': 'L3_misses_14.txt', '15': 'L3_misses_15.txt',
        '16': 'L3_misses_16.txt', '17': 'L3_misses_17.txt', '18': 'L3_misses_18.txt',
        '19': 'L3_misses_19.txt', '20': 'L3_misses_20.txt', '21': 'L3_misses_21.txt',
        '22': 'L3_misses_22.txt', '23': 'L3_misses_23.txt', '24': 'L3_misses_24.txt',
        '25': 'L3_misses_25.txt', '26': 'L3_misses_26.txt', '27': 'L3_misses_27.txt'
    }

    L1_RESULTS = read_misses(OUTPUT_DIR, L1_FILES, 'mem_load_retired.l1_miss')
    L2_RESULTS = read_misses(OUTPUT_DIR, L2_FILES, 'mem_load_retired.l2_miss')
    L3_RESULTS = read_misses(OUTPUT_DIR, L3_FILES, 'mem_load_retired.l3_miss')

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

    fig, axs = plt.subplots(3, 1, figsize=(16,24), sharey=True)  # Aumentata la larghezza a 20

    for i, (results, title) in enumerate([(L1_RESULTS, 'L1 Cache Misses'),
                                        (L2_RESULTS, 'L2 Cache Misses'),
                                        (L3_RESULTS, 'L3 Cache Misses')]):
        # Convert x-values to sizes
        x_values = list(results.keys())
        y_values = list(results.values())
        
        # Create x-ticks with proper formatting
        x_ticks = [format_size(x) for x in x_values]
        
        # Convert cache sizes to array indices
        cache_lines = {
            'L1': (list(range(len(x_values)))[x_values.index('15')], 'red', 'L1 Cache (32 KB)'),
            'L2': (list(range(len(x_values)))[x_values.index('18')], 'green', 'L2 Cache (256 KB)'),
            'L3': (list(range(len(x_values)))[x_values.index('24')], 'blue', 'L3 Cache (16 MB)')
        }
        
        # Add vertical lines for cache capacities
        for position, color, label in cache_lines.values():
            axs[i].axvline(position, linestyle='--', color=color, label=label)
        
        # Plot misses
        axs[i].plot(range(len(x_values)), y_values, marker='o', color='orange', 
                   linewidth=2, markersize=8, label=f'{title.split()[0]} Misses')
        
        # Set x-axis ticks and labels
        axs[i].set_xticks(range(len(x_values)))
        axs[i].set_xticklabels(x_ticks, rotation=0, ha='center')  # Modificato rotation=0 e ha='center'
        
        # Format y-axis ticks
        axs[i].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
            lambda x, p: format_misses(x)))
        
        # Set titles and labels
        axs[i].set_title(title, pad=20)
        axs[i].set_xlabel('Dimensione Array (B)', labelpad=10)
        axs[i].set_ylabel('Numero di Misses', labelpad=10)
        
        # Add legend with semi-transparent background
        axs[i].legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.8)
        
        # Add grid
        axs[i].grid(True)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Add extra space at the bottom for the labels
    plt.subplots_adjust(bottom=0.1, hspace=0.4)

    plt.savefig('/Users/lorenzofaraoni/Desktop/Tesi/Laboratorio/Progetti/Random access array/random_access_array_cache/plots/cache_miss_levels.png', 
                bbox_inches='tight', dpi=300)