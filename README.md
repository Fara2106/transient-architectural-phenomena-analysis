# Transient Architectural Phenomena Analysis

**Analysis of Transient Architectural Phenomena in Webserver Environments**

This repository contains the complete research project analyzing the impact of context switches and interrupts on hardware performance counters (cache miss and TLB miss) through validation tests and webserver analysis in Docker environments.

## 🎓 Research Overview

This thesis research investigates transient architectural phenomena - temporary events that impact system performance due to interruptions in normal execution flow. The study focuses on how context switches and interrupts affect cache and TLB (Translation Lookaside Buffer) behavior in modern computer architectures.

### Key Findings

- **Table Server**: Resilient to disturbance (max degradation: 3.2x in L3 cache, 1.15x execution time)
  - L1 Cache: ~35M stable misses, miss rate ~1.2%
  - TLB L1: Counter-intuitive behavior (miss reduction with disturbance)
  - Access pattern: Sequential distributed, benefits from TLB pre-loading

- **Matrix Server**: Highly sensitive (degradation up to 420x in L1 cache, 5.3x execution time)
  - L1 Cache: From 1.7M to 714M misses (400x increase)
  - TLB L1: From 1.2M to 175M misses (145x increase)
  - Access pattern: Intensive localized, quickly saturates cache

## 🏗️ Project Structure

```
├── validation/                    # Validation phase tests
│   ├── cache_analysis/            # Random access array cache tests
│   │   ├── random_access_array.cc
│   │   ├── compile.sh
│   │   ├── run_perf_analysis_miss.sh
│   │   ├── run_perf_analysis_time.sh
│   │   ├── print_cache_miss.py
│   │   ├── print_output_cache_time.py
│   │   └── plots/
│   └── tlb_analysis/              # Random access array TLB tests
│       ├── random_access_array.cc
│       ├── compile.sh
│       ├── run_perf_analysis_miss.sh
│       ├── run_perf_analysis_time.sh
│       ├── print_tlb_misses.py
│       ├── print_output_tlb_time.py
│       └── plots/
│
├── webserver_analysis/           # Main webserver analysis
│   ├── table_server/             # Table generation server
│   │   ├── src/
│   │   │   ├── TableGenerator.java
│   │   │   └── WEB-INF/
│   │   ├── Dockerfile
│   │   ├── build_image.sh
│   │   ├── start_server.sh
│   │   ├── disturbator_low_frequency.sh
│   │   ├── disturbator_medium_frequency.sh
│   │   ├── disturbator_high_frequency.sh
│   │   └── plot_all.py
│   └── matrix_server/            # Matrix multiplication server
│       ├── src/
│       │   ├── MatrixMultiplier.java
│       │   └── WEB-INF/
│       ├── Dockerfile
│       ├── build_image.sh
│       ├── start_server.sh
│       ├── disturbator_low_frequency.sh
│       ├── disturbator_medium_frequency.sh
│       ├── disturbator_high_frequency.sh
│       └── plot_all.py
│
├── results/                      # Experimental results
│   ├── table_generator/          # Table server results
│   │   ├── single_core/
│   │   └── multi_core/
│   └── matrix_multiplication/    # Matrix server results
│       ├── single_core/
│       └── multi_core/
│
├── client_analysis/              # Client implementation and analysis
│   ├── cache_misses/
│   ├── execution_time/
│   └── tlb_misses/
│
├── docs/                         # Documentation and thesis
│   ├── thesis_presentation.pdf
│   ├── thesis_document.pdf
│   └── images/
│
└── scripts/                      # Automation scripts
    ├── setup.sh
    ├── run_all_tests.sh
    └── data_processing/
```

## 🛠️ System Requirements

### Hardware Specifications (Test Environment)
- **CPU**: Intel Core i9-9900K (8 physical cores, 16 logical)
- **Cache**: L1 32KB, L2 256KB, L3 16MB
- **TLB**: L1 64 pages, L2 1536 pages
- **RAM**: 32GB

### Software Environment
- **OS**: Linux kernel 5.4.0-150-generic
- **Docker**: 20.10.21
- **Java**: OpenJDK 11+ (for servlet containers)
- **Apache Tomcat**: 9.x
- **Tools**: perf, GCC, Python 3.x with matplotlib

### Performance Counter Events Monitored

**Cache Events:**
- `mem_load_retired.l1_miss` - L1 cache misses
- `mem_load_retired.l2_miss` - L2 cache misses  
- `mem_load_retired.l3_miss` - L3 cache misses

**TLB Events:**
- `dtlb_load_misses.stlb_hit` - L1 TLB load misses
- `dtlb_store_misses.stlb_hit` - L1 TLB store misses
- `dtlb_load_misses.miss_causes_a_walk` - L2 TLB load misses
- `dtlb_store_misses.miss_causes_a_walk` - L2 TLB store misses

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Fara2106/transient-architectural-phenomena-analysis.git
cd transient-architectural-phenomena-analysis
```

### 2. Setup Environment
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 3. Run Validation Tests
```bash
# Cache validation
cd validation/cache_analysis
./compile.sh
./run_perf_analysis_miss.sh
python3 print_cache_miss.py

# TLB validation  
cd ../tlb_analysis
./compile.sh
./run_perf_analysis_miss.sh
python3 print_tlb_misses.py
```

### 4. Webserver Analysis
```bash
# Table server
cd webserver_analysis/table_server
./build_image.sh
./start_server.sh

# In another terminal - start client analysis
cd client_analysis/table_generator/cache_misses
make
./cache_miss.sh

# Matrix server
cd webserver_analysis/matrix_server
./build_image.sh
./start_server.sh
```

## 📊 Test Configurations

### Table Generator Server
- **Test sizes**: 10,000 - 1,000,000 rows
- **Disturbance server**: 10,000 rows (3MB)
- **Frequencies**: 
  - Low: 1 req/s
  - Medium: 10 req/s  
  - High: 100 req/s

### Matrix Multiplication Server
- **Test sizes**: 1 - 4096 (matrix dimensions)
- **Disturbance server**: 256x256 matrices (768KB)
- **Frequencies**:
  - Low: 1 req/s
  - Medium: 5 req/s
  - High: 10 req/s

### Container Configurations
- **Single-core**: `--cpuset-cpus="0" --cpus=1`
- **Multi-core**: Full CPU utilization

## 📈 Key Results Summary

### Performance Comparison (Maximum Load)

| Parameter | Table Server (1M rows) | Matrix Server (4096x4096) |
|-----------|-------------------------|---------------------------|
| L1 Cache Miss | 35M → 35M (~1x) | 1.7M → 714M (420x) |
| L2 Cache Miss | 11M → 11M (~1x) | 1.2M → 11.9M (~10x) |
| L3 Cache Miss | 0.14M → 0.45M (3.2x) | 4K → 0.14M (140x) |
| TLB L1 Miss | 20M → 11.7M (↓40%) | 1.2M → 170M (142x) |
| TLB L2 Miss | 1M → 0.7M (↓30%) | 0.5M → 0.44M (~1x) |
| Execution Time | 0.153s → 0.176s (1.15x) | 410s → 2162s (5.3x) |

## 🔬 Research Methodology

1. **Validation Phase**: Random access array tests to validate performance counters
2. **Baseline Establishment**: Single server performance measurement
3. **Disturbance Analysis**: Progressive load increase with 1-3 concurrent servers
4. **Architecture Comparison**: Single-core vs multi-core behavior analysis
5. **Performance Correlation**: Mapping between architectural events and performance

## 📝 Usage Examples

### Running Cache Analysis
```bash
cd validation/cache_analysis
./compile.sh

# Test different array sizes (2^15 to 2^24 bytes)
for size in {15..24}; do
    echo "Testing size: 2^$size bytes"
    perf stat -e mem_load_retired.l1_miss,mem_load_retired.l2_miss,mem_load_retired.l3_miss \
    ./random_access_array $size > output_$size.txt 2>&1
done

python3 print_cache_miss.py
```

### Webserver Load Testing
```bash
# Start table server
cd webserver_analysis/table_server
./start_server.sh

# Generate load in separate terminals
./disturbator_low_frequency.sh &
./disturbator_medium_frequency.sh &
./disturbator_high_frequency.sh &

# Monitor with perf
cd ../../client_analysis/table_generator/cache_misses
perf stat -e mem_load_retired.l1_miss,mem_load_retired.l2_miss,mem_load_retired.l3_miss \
./send_request http://localhost:8080/table-generator 100000
```

## 📊 Data Analysis

The `results/` directory contains comprehensive experimental data:
- Raw performance counter measurements
- Execution time recordings
- Statistical analysis plots
- Comparative performance charts

Use the provided Python scripts to regenerate plots:
```bash
cd results/table_generator/plots
python3 plot_cache_analysis.py
python3 plot_performance_comparison.py
```

## 🤝 Contributing

This is a research project completed for academic purposes. However, contributions and discussions are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/analysis-improvement`)
3. Commit your changes (`git commit -am 'Add new analysis method'`)
4. Push to the branch (`git push origin feature/analysis-improvement`)
5. Create a Pull Request

## 📚 Academic Citation

If you use this work in your research, please cite:

```bibtex
@mastersthesis{faraoni2024transient,
  title={Analisi dei Fenomeni Architetturali Transienti},
  author={Faraoni, Lorenzo},
  year={2024},
  school={Università di Siena},
  department={Dipartimento di Ingegneria dell'Informazione e Scienze Matematiche},
  type={Tesi di Laurea in Ingegneria Informatica e dell'Informazione},
  supervisor={Bartolini, Sandro}
}
```

## 🔗 Connect

- **Author**: Lorenzo Faraoni
- **LinkedIn**: [lorenzo-faraoni-881340262](https://www.linkedin.com/in/lorenzo-faraoni-881340262/)
- **Instagram**: [@lore_fara](https://www.instagram.com/lore_fara/)
- **University**: University of Siena, Italy

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Prof. Sandro Bartolini (Thesis Supervisor) - University of Siena
- Department of Information Engineering and Mathematical Sciences
- University of Siena Computing Infrastructure
- Research community for open-source tools and methodologies

---

*This research contributes to the understanding of transient architectural phenomena in modern computing systems, providing insights for performance optimization in server environments.*
