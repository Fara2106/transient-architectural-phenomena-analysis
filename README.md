# Analysis of Transient Architectural Phenomena

This repository contains the code and tools used for the Master's thesis "Analisi dei Fenomeni Architetturali Transienti" (Analysis of Transient Architectural Phenomena) - University of Siena, Academic Year 2023-2024.

## 📋 Project Overview

This research analyzes the impact of transient architectural phenomena (caused by context switches and interrupts) on system performance through:

1. **Preliminary validation** with test programs to saturate cache and TLB
2. **Experimental analysis** on two distinct web servers:
   - HTML table generator server
   - Matrix multiplication server

### Key Findings
- **Table server**: resilient to disturbances (max degradation 3.2x in L3 cache)
- **Matrix server**: highly sensitive (degradation up to 420x in L1 cache, 5.3x in execution time)
- Significant differences between single-core and multi-core configurations

## 🏗️ Project Structure

```
project/
├── validation/                    # Validation programs
│   ├── cache_analysis/           # Cache miss analysis
│   │   ├── random_access_cache.cc
│   │   ├── compile_cache.sh
│   │   ├── run_cache_analysis.sh
│   │   ├── results/              # Results organized by array size
│   │   │   ├── cache_32KB.txt    # Results for 32KB array
│   │   │   ├── cache_256KB.txt   # Results for 256KB array
│   │   │   ├── cache_16MB.txt    # Results for 16MB array
│   │   │   ├── time_32KB.txt     # Execution times for 32KB
│   │   │   ├── time_256KB.txt    # Execution times for 256KB
│   │   │   └── time_16MB.txt     # Execution times for 16MB
│   │   ├── plot_cache.py
│   │   └── graphs/
│   │       ├── cache_miss_plot.png
│   │       └── execution_time_plot.png
│   └── tlb_analysis/             # TLB miss analysis
│       ├── random_access_tlb.cc
│       ├── compile_tlb.sh
│       ├── run_tlb_analysis.sh
│       ├── results/              # Results organized by page count
│       │   ├── tlb_64pages.txt   # Results for 64 pages
│       │   ├── tlb_1536pages.txt # Results for 1536 pages
│       │   ├── tlb_4096pages.txt # Results for 4096 pages
│       │   ├── time_64pages.txt  # Execution times for 64 pages
│       │   ├── time_1536pages.txt # Execution times for 1536 pages
│       │   └── time_4096pages.txt # Execution times for 4096 pages
│       ├── plot_tlb.py
│       └── graphs/
│           ├── tlb_miss_plot.png
│           └── execution_time_plot.png
├── webserver_analysis/           # Web server analysis
│   ├── table_server/            # Table generation server
│   │   ├── single_core/
│   │   │   ├── cache_miss/
│   │   │   │   ├── client.cc
│   │   │   │   ├── makefile
│   │   │   │   ├── benchmark_cache.sh
│   │   │   │   └── results/      # Results organized by disturbance type
│   │   │   │       ├── misses_baseline.txt     # No disturbance
│   │   │   │       ├── misses_1_LOWHZ.txt      # 1 disturbing server, low freq
│   │   │   │       ├── misses_1_MEDIUMHZ.txt   # 1 disturbing server, medium freq
│   │   │   │       ├── misses_1_HIGHHZ.txt     # 1 disturbing server, high freq
│   │   │   │       ├── misses_2_LOWHZ.txt      # 2 disturbing servers, low freq
│   │   │   │       ├── misses_2_MEDIUMHZ.txt   # 2 disturbing servers, medium freq
│   │   │   │       └── misses_2_HIGHHZ.txt     # 2 disturbing servers, high freq
│   │   │   ├── tlb_miss/
│   │   │   │   ├── client.cc
│   │   │   │   ├── makefile
│   │   │   │   ├── benchmark_tlb.sh
│   │   │   │   └── results/      # Results organized by disturbance type
│   │   │   │       ├── tlb_baseline.txt        # No disturbance
│   │   │   │       ├── tlb_1_LOWHZ.txt         # 1 disturbing server, low freq
│   │   │   │       ├── tlb_1_MEDIUMHZ.txt      # 1 disturbing server, medium freq
│   │   │   │       ├── tlb_1_HIGHHZ.txt        # 1 disturbing server, high freq
│   │   │   │       ├── tlb_2_LOWHZ.txt         # 2 disturbing servers, low freq
│   │   │   │       ├── tlb_2_MEDIUMHZ.txt      # 2 disturbing servers, medium freq
│   │   │   │       └── tlb_2_HIGHHZ.txt        # 2 disturbing servers, high freq
│   │   │   └── execution_time/
│   │   │       ├── client.cc
│   │   │       ├── makefile
│   │   │       ├── benchmark_time.sh
│   │   │       └── results/      # Execution times organized by disturbance type
│   │   │           ├── time_baseline.txt       # No disturbance
│   │   │           ├── time_1_LOWHZ.txt        # 1 disturbing server, low freq
│   │   │           ├── time_1_MEDIUMHZ.txt     # 1 disturbing server, medium freq
│   │   │           ├── time_1_HIGHHZ.txt       # 1 disturbing server, high freq
│   │   │           ├── time_2_LOWHZ.txt        # 2 disturbing servers, low freq
│   │   │           ├── time_2_MEDIUMHZ.txt     # 2 disturbing servers, medium freq
│   │   │           └── time_2_HIGHHZ.txt       # 2 disturbing servers, high freq
│   │   ├── multi_core/
│   │   │   ├── cache_miss/
│   │   │   │   └── results/      # Same structure as single_core
│   │   │   ├── tlb_miss/
│   │   │   │   └── results/
│   │   │   └── execution_time/
│   │   │       └── results/
│   │   ├── src/
│   │   │   └── TableGenerator.java
│   │   ├── WEB-INF/
│   │   │   └── classes/
│   │   ├── build_war.sh
│   │   ├── table-generator.war
│   │   ├── start_server.sh
│   │   ├── disturb_low.sh        # 1 req/s
│   │   ├── disturb_medium.sh     # 10 req/s
│   │   ├── disturb_high.sh       # 100 req/s
│   │   └── plot_table_results.py
│   └── matrix_server/           # Matrix multiplication server
│       ├── single_core/
│       │   ├── cache_miss/
│       │   │   ├── client.cc
│       │   │   ├── makefile
│       │   │   ├── benchmark_cache.sh
│       │   │   └── results/      # Results organized by disturbance type
│       │   │       ├── misses_baseline.txt     # No disturbance
│       │   │       ├── misses_1_LOWHZ.txt      # 1 disturbing server, low freq
│       │   │       ├── misses_1_MEDIUMHZ.txt   # 1 disturbing server, medium freq
│       │   │       ├── misses_1_HIGHHZ.txt     # 1 disturbing server, high freq
│       │   │       ├── misses_2_LOWHZ.txt      # 2 disturbing servers, low freq
│       │   │       ├── misses_2_MEDIUMHZ.txt   # 2 disturbing servers, medium freq
│       │   │       └── misses_2_HIGHHZ.txt     # 2 disturbing servers, high freq
│       │   ├── tlb_miss/
│       │   │   ├── client.cc
│       │   │   ├── makefile
│       │   │   ├── benchmark_tlb.sh
│       │   │   └── results/      # Results organized by disturbance type
│       │   │       ├── tlb_baseline.txt        # No disturbance
│       │   │       ├── tlb_1_LOWHZ.txt         # 1 disturbing server, low freq
│       │   │       ├── tlb_1_MEDIUMHZ.txt      # 1 disturbing server, medium freq
│       │   │       ├── tlb_1_HIGHHZ.txt        # 1 disturbing server, high freq
│       │   │       ├── tlb_2_LOWHZ.txt         # 2 disturbing servers, low freq
│       │   │       ├── tlb_2_MEDIUMHZ.txt      # 2 disturbing servers, medium freq
│       │   │       └── tlb_2_HIGHHZ.txt        # 2 disturbing servers, high freq
│       │   └── execution_time/
│       │       ├── client.cc
│       │       ├── makefile
│       │       ├── benchmark_time.sh
│       │       └── results/      # Execution times organized by disturbance type
│       │           ├── time_baseline.txt       # No disturbance
│       │           ├── time_1_LOWHZ.txt        # 1 disturbing server, low freq
│       │           ├── time_1_MEDIUMHZ.txt     # 1 disturbing server, medium freq
│       │           ├── time_1_HIGHHZ.txt       # 1 disturbing server, high freq
│       │           ├── time_2_LOWHZ.txt        # 2 disturbing servers, low freq
│       │           ├── time_2_MEDIUMHZ.txt     # 2 disturbing servers, medium freq
│       │           └── time_2_HIGHHZ.txt       # 2 disturbing servers, high freq
│       ├── multi_core/
│       │   ├── cache_miss/
│       │   │   └── results/      # Same structure as single_core
│       │   ├── tlb_miss/
│       │   │   └── results/
│       │   └── execution_time/
│       │       └── results/
│       ├── src/
│       │   └── MatrixMultiplier.java
│       ├── WEB-INF/
│       │   └── classes/
│       ├── build_war.sh
│       ├── matrix-multiplier.war
│       ├── start_server.sh
│       ├── disturb_low.sh        # 1 req/s
│       ├── disturb_medium.sh     # 5 req/s
│       ├── disturb_high.sh       # 10 req/s
│       └── plot_matrix_results.py
└── final_results/               # Consolidated results and final graphs
    ├── validation_graphs/
    │   ├── cache_validation.png
    │   └── tlb_validation.png
    ├── comparison_graphs/
    │   ├── table_vs_matrix_single.png
    │   ├── table_vs_matrix_multi.png
    │   └── single_vs_multi_comparison.png
    └── thesis_graphs/          # All graphs used in the thesis
```

## 🔧 System Requirements

### Hardware
- Processor with performance counter support (Intel/AMD)
- Multi-core architecture recommended
- RAM: minimum 8GB recommended

### Software
- **Operating System**: Linux (tested on Ubuntu with kernel 5.4.0-150-generic)
- **Java**: JDK 1.7 or higher
- **Apache Tomcat**: servlet-compatible version
- **Docker**: 20.10.21 or higher
- **GCC**: for C++ client compilation
- **Python**: 3.x with matplotlib
- **C++ Libraries**: libcurl-dev
- **System Tools**: perf (included in Linux kernel)

### Dependencies Installation (Ubuntu/Debian)
```bash
# Update system
sudo apt update

# Install Java and build tools
sudo apt install openjdk-8-jdk gcc make

# Install libcurl for HTTP clients
sudo apt install libcurl4-openssl-dev

# Install Python and matplotlib
sudo apt install python3 python3-pip
pip3 install matplotlib

# Install Docker
sudo apt install docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER

# Install Apache Tomcat
sudo apt install tomcat9
```

## 🔐 Administrator Permissions Required

**Important**: This project requires administrator privileges to access hardware performance counters through `perf`.

### Option 1: Configure perf permissions (Recommended)
```bash
# Allow unprivileged access to perf events
echo -1 | sudo tee /proc/sys/kernel/perf_event_paranoid

# Make permanent by adding to /etc/sysctl.conf
echo "kernel.perf_event_paranoid = -1" | sudo tee -a /etc/sysctl.conf
```

### Option 2: Run with sudo
```bash
# Run all benchmark scripts with sudo
sudo ./benchmark_cache.sh
sudo ./benchmark_tlb.sh
```

### Security Note
The perf tool accesses low-level hardware counters. Ensure you understand the security implications before modifying system permissions.

## 🚀 Usage Guide

### 1. Validation Phase

#### Cache Miss Analysis
```bash
cd validation/cache_analysis/
./compile_cache.sh
sudo ./run_cache_analysis.sh
python3 plot_cache.py
```

#### TLB Miss Analysis
```bash
cd validation/tlb_analysis/
./compile_tlb.sh
sudo ./run_tlb_analysis.sh
python3 plot_tlb.py
```

### 2. Web Server Analysis

#### Table Server Setup
```bash
cd webserver_analysis/table_server/
./build_war.sh
./start_server.sh
```

#### Single-Core Test Execution
```bash
cd single_core/cache_miss/

# Test without disturbance
sudo ./benchmark_cache.sh

# Test with low disturbance (in separate terminals)
../../disturb_low.sh &
sudo ./benchmark_cache.sh

# Test with medium disturbance
../../disturb_medium.sh &
sudo ./benchmark_cache.sh

# Test with high disturbance
../../disturb_high.sh &
sudo ./benchmark_cache.sh
```

#### Multi-Core Test Execution
```bash
cd multi_core/cache_miss/

# Follow same pattern as single-core
# Tests will automatically utilize multiple cores
```

#### Test Configurations

**Table Server:**
- Dimensions: 10,000 - 1,000,000 rows
- Disturbance frequencies: 1, 10, 100 requests/second

**Matrix Server:**
- Dimensions: 1x1 - 4096x4096
- Disturbance frequencies: 1, 5, 10 requests/second

### 3. Results Analysis
```bash
# Generate graphs from results
python3 plot_table_results.py  # For table server analysis
python3 plot_matrix_results.py # For matrix server analysis

# Graphs are saved in respective results/ folders
```

## 📊 File Structure and Content

### Validation Results
Each validation test generates results organized by data structure size:
- **Cache analysis**: Results for different array sizes (32KB, 256KB, 16MB, etc.)
- **TLB analysis**: Results for different page counts (64, 1536, 4096 pages, etc.)

### Webserver Results  
Each webserver test generates results organized by disturbance configuration:

**File naming convention:**
- `baseline`: Test server only (no disturbance)
- `1_LOWHZ`: Test server + 1 disturbing server at low frequency  
- `1_MEDIUMHZ`: Test server + 1 disturbing server at medium frequency
- `1_HIGHHZ`: Test server + 1 disturbing server at high frequency
- `2_LOWHZ`: Test server + 2 disturbing servers at low frequency
- `2_MEDIUMHZ`: Test server + 2 disturbing servers at medium frequency  
- `2_HIGHHZ`: Test server + 2 disturbing servers at high frequency

## 📊 Monitored Metrics

### Hardware Performance Counters (perf)
- **Cache Miss**: L1, L2, L3 levels
- **TLB Miss**: L1, L2 levels
- **Execution time**
- **Throughput** (requests/second)

### Perf Events Used
```bash
# Cache events
mem_load_retired.l1_miss
mem_load_retired.l2_miss
mem_load_retired.l3_miss

# TLB events
dtlb_load_misses.stlb_hit
dtlb_store_misses.stlb_hit
dtlb_load_misses.miss_causes_a_walk
dtlb_store_misses.miss_causes_a_walk
```

## 🔬 Methodology

### Hardware Configuration Tested
- **CPU**: Intel Core i9-9900K (8 physical cores, 16 logical)
- **L1 Cache**: 32 KB
- **L2 Cache**: 256 KB  
- **L3 Cache**: 16 MB
- **L1 TLB**: 64 pages
- **L2 TLB**: 1536 pages

### Test Scenarios
1. **Baseline**: test server only (no disturbance)
2. **Low disturbance**: test server + 1 disturbing server
3. **Medium disturbance**: test server + 2 disturbing servers
4. **High disturbance**: test server + 2 disturbing servers (at maximum frequency)

## 📈 Expected Results

### Table Generation Server
- Stable cache misses (~35M L1, ~11M L2)
- Decreasing TLB misses with disturbance
- Contained performance degradation (1.15x)

### Matrix Multiplication Server
- Dramatically increasing cache misses (420x L1)
- Significantly increasing TLB misses (142x L1)
- Marked performance degradation (5.3x)

## ⚠️ Important Notes

### System Configuration for Consistent Results
```bash
# Disable CPU frequency scaling
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Disable CPU idle states (optional, for maximum consistency)
sudo cpupower idle-set -D 0
```

### Best Practices
- Close unnecessary applications during tests
- Run multiple iterations to validate results
- Monitor system temperature to avoid thermal throttling
- Ensure adequate cooling during intensive tests

### Hardware Adaptation
Cache and TLB parameters are configurable in test files to adapt to different hardware architectures. Modify the following in validation programs:
- Cache sizes (L1: 32KB, L2: 256KB, L3: 16MB)
- TLB capacities (L1: 64 pages, L2: 1536 pages)

## 🐛 Troubleshooting

### Common Issues

**Permission denied with perf:**
```bash
# Check current perf_event_paranoid setting
cat /proc/sys/kernel/perf_event_paranoid
# If > -1, follow permission setup above
```

**Docker permission issues:**
```bash
# Add user to docker group and restart
sudo usermod -aG docker $USER
# Log out and log back in
```

**Tomcat not starting:**
```bash
# Check if port 8080 is available
sudo netstat -tlnp | grep 8080
# Kill conflicting processes if necessary
```

**Inconsistent results:**
- Ensure system is not under thermal stress
- Disable background services and applications
- Run tests multiple times and average results

## 📚 References

- Full thesis: "Analisi dei Fenomeni Architetturali Transienti"
- University of Siena - Department of Information Engineering and Mathematical Sciences
- Supervisor: Prof. Sandro Bartolini
- Academic Year: 2023-2024

## 🎯 Research Impact

This research contributes to understanding transient architectural phenomena in modern computing systems, with applications in:
- **Performance optimization** of web servers
- **Resource allocation** in virtualized environments
- **System design** for high-throughput applications
- **Benchmarking methodology** for architectural analysis

## 👨‍💻 Author

**Lorenzo Faraoni**  
Master's in Computer and Information Engineering  
University of Siena  

📧 Email: lorefara97@gmail.com  
🔗 LinkedIn: https://www.linkedin.com/in/lorenzo-faraoni-881340262/

## 📄 License

This project is available for academic and research purposes. Please cite the original thesis when using this work.

## 🙏 Acknowledgments

Special thanks to Prof. Sandro Bartolini for supervision and guidance throughout this research project.

---

*For questions or clarifications about the code, please refer to the thesis documentation or contact the author.*
