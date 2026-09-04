# Benchmark Specification

The benchmark uses a fixed common event taxonomy and a deterministic run protocol.

For each domain and scenario:
1. reset plant, digital twin and trust states;
2. execute a normal calibration prefix;
3. inject the event only inside the declared window;
4. calculate identical evidence channels;
5. produce diagnosis, trust and reconstruction outputs;
6. calculate cyber, reconstruction and calibration metrics.

Primary comparisons must keep the seed, steps, event window and metric implementation fixed.
