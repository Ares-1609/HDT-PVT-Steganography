# HDT-PVD Image Steganography System

## Overview

This project implements a highly secure, stealth-focused **Image Steganography System** using the proposed **Hybrid Dynamic Tiling Pixel Value Differencing (HDT-PVD)** algorithm.

Designed for real-world secure covert communication, this system prioritizes **statistical invisibility** over raw payload capacity. Unlike conventional techniques such as **Least Significant Bit (LSB)** and traditional **Pixel Value Differencing (PVD)**, the proposed method introduces:

- Chaotic key-driven dynamic tiling
- Dynamic median variance thresholding
- Randomized pivot selection

These mechanisms make hidden information significantly more resistant to modern statistical steganalysis while maintaining excellent visual quality.

The framework supports both:

- **8-bit Grayscale Images**
- **24-bit RGB Color Images**

and can securely embed payloads of up to **6000 bytes** in RGB images while preserving statistical parity across individual color channels.

A **Flask-based web application** is also included for embedding, extraction, and real-time performance analysis.

---

# Features

- 🔒 **Extreme-Stealth PVD**
  - Eliminates the characteristic "step effect" found in conventional PVD methods, improving resistance against Pixel Difference Histogram (PDH) attacks.

- 🔑 **Chaotic Key Generation**
  - Uses a SHA-256 seeded Logistic Map to generate unpredictable dynamic tiles.

- 📊 **Median Variance Segregation (50% Shield)**
  - Computes the global median variance and embeds data only inside highly textured regions.

- 🌈 **RGB Color Extension**
  - Supports secure embedding independently across R, G, and B channels.

- 📈 **Statistical Resistance**
  - Resistant against:
    - Pixel Difference Histogram (PDH)
    - Chi-Square Analysis
    - RS Steganalysis

- 🌐 **Flask Web Interface**
  - Embed and extract messages through an intuitive browser interface.

- 📉 **Automatic Evaluation**
  - Computes:
    - PSNR
    - MSE
    - Embedding Capacity
    - Tile Mapping
    - Statistical Analysis

---

# System Architecture

## Embedding Process

```text
Input Image (Grayscale / RGB)
            +
      Secret Message
            +
        Secret Key
            │
            ▼
 SHA-256 Seed Generation
            │
            ▼
 Chaotic Logistic Map
            │
            ▼
 Dynamic Tile Generation
            │
            ▼
 Local Variance Computation
            │
            ▼
 Global Median Threshold
            │
            ▼
 Random Pivot Selection
            │
            ▼
 PVD Data Embedding
(Only in σ²tile > σ²median)
            │
            ▼
        Stego Image
```

## Extraction Process

```text
Stego Image
     +
 Secret Key
      │
      ▼
SHA-256 Seed Generation
      │
      ▼
Logistic Map Synchronization
      │
      ▼
Tile Reconstruction
      │
      ▼
Variance Recalculation
      │
      ▼
Pivot Identification
      │
      ▼
Pixel Difference Analysis
      │
      ▼
Recovered Bitstream
      │
      ▼
Recovered Secret Message
```

---

# Project Structure

```text
HDT-PVD-Steganography
│
├── datasets/
│   ├── baboon.png
│   ├── baboon_color.png
│   ├── boat.png
│   ├── boat_color.png
│   ├── jet.png
│   ├── jet_color.png
│   ├── lena.png
│   ├── lena_color.png
│   ├── peppers.png
│   └── peppers_color.png
│
├── results/                      # Grayscale experiment outputs
├── color-results/                # RGB experiment outputs
│
├── static/
│   ├── input.png
│   ├── stego_input.png
│   └── style.css
│
├── templates/
│   └── index.html
│
├── app.py
├── batch_test.py
├── batch_test_color.py
├── resistance_analysis.py
├── resistance_analysis_color.py
├── plot_graphs.py
├── plot_graphs_color.py
├── steganography.py
├── utils.py
├── README.md
└── requirements.txt
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Ares-1609/HDT-PVD-Steganography.git

cd HDT-PVD-Steganography
```

---

## 2. Install Dependencies

```bash
pip install flask pillow numpy scipy matplotlib opencv-python
```

Or install from:

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# Evaluation Metrics

## Local Variance (σ²)

Measures the spread of pixel intensities within a dynamically generated tile to estimate local texture complexity. Higher variance indicates more textured regions that are better suited for data embedding.

**Formula**

**σ² = (1/N) × Σ<sub>i=1</sub><sup>N</sup>(xᵢ − μ)²**

where:

- **N** = Number of pixels in a tile
- **xi** = Pixel intensity
- **μ** = Mean intensity of the tile

---

## Mean Squared Error (MSE)

Measures the average squared difference between the original image and the stego image across all RGB channels.

**Formula**

**MSE = (1 / 3MN) × Σ<sub>c∈{R,G,B}</sub> Σ<sub>i=1</sub><sup>M</sup> Σ<sub>j=1</sub><sup>N</sup>(I(i,j,c) − Iₛ(i,j,c))²**

where:

- **M × N** = Image dimensions
- **I(i,j,c)** = Original pixel value
- **Is(i,j,c)** = Stego pixel value
- **c ∈ {R, G, B}**

Lower MSE indicates less distortion.

---

## Peak Signal-to-Noise Ratio (PSNR)

Measures the visual quality of the stego image. Higher PSNR values indicate better imperceptibility.

**Formula**

**PSNR = 10 log₁₀ (255² / MSE)**

where:

- Maximum pixel value = **255**
- **PSNR > 38 dB** is generally considered visually imperceptible for steganography.

---

## Embedding Capacity (Bits Per Pixel)

Represents the amount of secret information embedded per pixel.

**Formula**

**Capacity (BPP) = Embedded Bits / Total Pixels**

Higher capacity allows more secret data but may increase detectability.

---

## Chi-Square Analysis

Evaluates whether the statistical distribution of pixel values has been significantly altered after embedding.

- Lower statistical deviation indicates stronger resistance against Chi-Square steganalysis.
- The proposed HDT-PVD maintains near-natural pixel distributions across all channels.

---

## RS Steganalysis

RS analysis partitions pixels into regular and singular groups to detect hidden data.

A secure steganographic algorithm satisfies:

```text
RM ≈ R−M
SM ≈ S−M
```

where:

- **RM** = Regular groups after positive flipping
- **R−M** = Regular groups after negative flipping
- **SM** = Singular groups after positive flipping
- **S−M** = Singular groups after negative flipping

The proposed HDT-PVD maintains balanced RS statistics, making it resistant to RS-based detection.

# Experimental Results

| Image Type | Payload | PSNR | Capacity |
|------------|---------|------|----------|
| Grayscale | Variable | ~42 dB | ~0.11 BPP |
| RGB | 6000 Bytes | ~38 dB | High Capacity |

The proposed framework maintains:

- Excellent visual quality
- Balanced RGB channel statistics
- Resistance against common steganalysis attacks

---

# Comparison with Existing Methods

| Metric | Proposed HDT-PVD | EPIS (Ismail et al., 2026) | Adaptive PVD (Pradhan et al., 2017) |
|---------|-----------------|----------------------------|-------------------------------------|
| Primary Goal | Maximum Stealth | Maximum Payload | Balanced Embedding |
| Adaptivity | Dynamic Median Variance | Canny + Sobel | Static Block Correlation |
| Embedding Logic | Dynamic Tiling PVD | MSB + LSB | Directional PVD |
| Average PSNR | ~42 dB (Gray)<br>~38 dB (RGB) | 42.27 dB | 50.93 dB |
| Capacity | ~0.11 BPP | 2.97 BPP | 1.83 BPP |
| PDH Resistance | ✅ Passed | Not Tested | ✅ Passed |
| Chi-Square | Strong Resistance | 0.1240 | Not Tested |
| RS Analysis | Passed | 32.7% Detection | Passed |

---

# Technologies Used

- Python
- Flask
- NumPy
- Pillow
- OpenCV
- SciPy
- Matplotlib

---

# Authors

- **Rakshit Awadhiya**
- **Hardik Chanana**
- **Aryan Verma**

B.Tech Computer Science Engineering

---

# License

This project is intended **solely for academic and research purposes**.