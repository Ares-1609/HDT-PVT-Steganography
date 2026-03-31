# HDT-PVD Image Steganography System

## Overview

This project implements a highly secure, stealth-focused **Image Steganography System** using the proposed **Hybrid Dynamic Tiling Pixel Value Differencing (HDT-PVD)** algorithm.

Designed for real-world secure covert communication, this system prioritizes extreme statistical invisibility over raw payload bloat. It abandons the rigid, static grids and predictable ranges of traditional methods (like LSB and standard PVD). Instead, the proposed approach introduces **chaotic key-driven tiling, dynamic median variance thresholding, and randomized pivot selection**, making the hidden data mathematically indistinguishable from the natural cover image to modern steganalysis tools.

The application also provides a **web interface built with Flask** that allows users to easily embed, extract, and analyze hidden messages.

---

## Features

*   **Extreme Stealth PVD:** Defeats targeted Pixel Difference Histogram (PDH) attacks by naturally eliminating traditional PVD "step effects."
*   **Cryptographic Unpredictability:** Utilizes a SHA-256 seeded chaotic logistic map to generate dynamically shifting tile sizes on the fly.
*   **The 50% Shield (Median Variance):** Automatically calculates the global median of all local tile variances, strictly hiding data only in the most chaotic top 50% of the image to protect vulnerable smooth regions.
*   **Perfect Statistical Evasion:** Analytically proven to achieve 0.0000 Chi-Square p-values and perfectly balanced RS Steganalysis scores ($R_M \approx R_{-M}$).
*   **Web-Based Interface:** Simple Flask UI for seamless embedding, extraction, and visualization.
*   **Real-Time Analytics:** Calculates and displays:
    *   Tile Map Visualization
    *   PSNR (Peak Signal-to-Noise Ratio)
    *   MSE (Mean Squared Error)
    *   Embedding Capacity

---

## System Architecture

### Embedding Process

Input Image + Secret Message + Secret Key  
↓  
Chaotic Logistic Map Generator  
↓  
Dynamic Tile Generation  
↓  
Local Variance Calculation & Global Median Evaluation  
↓  
Random Pivot Selection  
↓  
PVD Data Embedding (Strictly in $\sigma^2_{tile} > \sigma^2_{median}$)  
↓  
Stego Image  

### Extraction Process

Stego Image + Secret Key  
↓  
Tile Reconstruction via Logistic Map  
↓  
Global Median Variance Recalculation  
↓  
Pivot Identification  
↓  
Pixel Difference Analysis  
↓  
Bitstream Recovery  
↓  
Recovered Secret Message  

---

## Project Structure

```text
HDT-PVD-Steganography
│
├── datasets
│   ├── baboon.png
│   ├── boat.png
│   ├── jet.png
│   ├── lena.png
│   └── peppers.png
│
├── results
│
├── static
│   ├── input.png
│   ├── stego_input.png
│   └── style.css
│
├── templates
│   └── index.html
│
├── uploads
│
├── app.py
├── batch_test.py
├── pdh_analysis.py
├── plot_graphs.py
├── README.md
├── resistance_analysis.py
├── steganography.py
└── utils.py
```

---

## Dependencies

Install the following Python libraries:

*   Flask
*   Pillow
*   NumPy
*   SciPy (Required for statistical resistance analysis)
*   Matplotlib (Required for PDH and Histogram generation)

---

## Installation

### 1. Clone the Repository

```bash
git clone [https://github.com/Ares-1609/HDT-PVD-Steganography.git](https://github.com/Ares-1609/HDT-PVD-Steganography.git)
cd HDT-PVD-Steganography
```

### 2. Install Required Libraries

```bash
pip install flask pillow numpy scipy matplotlib
```

---

## Running the Application

Run the Flask server:

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`. Open this link in your browser.

---

## How to Use

### Embed a Message

1.  Upload a cover image.
2.  Enter the secret message.
3.  Enter a secret key.
4.  Click **Encrypt Image**.

The system will generate:
*   The Stego Image (Output stored in the `static` folder)
*   Tile Map Visualization
*   PSNR and MSE metrics
*   Embedding Capacity calculations

### Extract a Message

1.  Upload the stego image.
2.  Enter the exact secret key used during embedding.
3.  Click **Decrypt**.

The hidden message will securely render on the screen.

---

## Evaluation Metrics

### Local Variance ($\sigma^2$)
Measures the spread of pixel intensities within a dynamically generated tile to assess texture complexity.

$$\sigma^2 = \frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2$$

### Mean Squared Error (MSE)
Measures the average squared difference between the original and stego image. Lower MSE indicates less distortion.

$$MSE = \frac{1}{MN} \sum_{i=1}^{M} \sum_{j=1}^{N} (I(i,j) - I_s(i,j))^2$$

### Peak Signal to Noise Ratio (PSNR)
Measures the visual quality of the stego image. Higher PSNR indicates better image quality (typically > 38 dB is considered imperceptible).

$$PSNR = 10 \cdot \log_{10} \left( \frac{255^2}{MSE} \right)$$

### Embedding Capacity
Represents the maximum secure payload the image can hold, measured in Bits Per Pixel (BPP).

---

## Advantages of HDT-PVD

*   **Self-Scaling Adaptivity:** Replaces hardcoded thresholds with a dynamic median variance, automatically adapting to the unique lighting and contrast of any cover image.
*   **Elimination of Structural Signatures:** Shifting tile boundaries and dynamic range assignments prevent the formation of predictable pixel block grids.
*   **Security Over Bloat:** Mathematically restricts capacity to highly textured zones, trading raw storage for cryptographic invisibility.
*   **Robustness to Analysis:** Visually and mathematically passes standard visual inspection, LSB-targeted Chi-Square attacks, RS Steganalysis, and PVD-targeted difference histogram tests.

---

## Academic Comparison with State-of-the-Art

| Metric | Proposed HDT-PVD | EPIS (Ismail et al., 2026) | Adaptive PVD (Pradhan et al., 2017) |
| :--- | :--- | :--- | :--- |
| **Primary Objective** | Maximum Stealth & Chaos | Maximum Payload Capacity | Balanced Edge Embedding |
| **Adaptivity Method** | Dynamic Median Variance | Canny & Sobel Edge Fusion | Static 2x3 & 3x2 Block Correlation |
| **Embedding Logic** | Variable Tiling PVD | MSB & LSB Substitution | Directional Block PVD |
| **Average PSNR** | **~45 to 52 dB** | 42.27 dB | 50.93 dB |
| **Embedding Capacity** | ~0.11 BPP | 2.97 BPP | 1.83 BPP |
| **PDH Attack** | **Passed** (Smooth Curve) | Not Tested | Passed (Smooth Curve) |
| **Chi-Square p-value** | **0.0000** (Perfect Pass) | 0.1240 (Pass) | Not Tested |
| **RS Detection Rate** | **Passed** ($R_M \approx R_{-M}$) | 32.7% Detection Rate | Passed ($R_M \approx R_{-M}$) |

---

## Authors

*   **Rakshit Awadhiya**
*   **Hardik Chanana**
*   **Aryan Verma**

*B.Tech Computer Science Engineering*

---

## License

This project is intended for **academic and research purposes**.
