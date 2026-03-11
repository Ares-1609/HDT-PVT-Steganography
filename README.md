# HDT-PVD Image Steganography System

## Overview

This project implements a secure **Image Steganography System** using the proposed **Hybrid Dynamic Tiling Pixel Value Differencing (HDT-PVD)** algorithm.

The system hides secret messages inside digital images while maintaining high image quality and minimizing the risk of statistical detection.

Unlike traditional techniques such as **LSB and PVD**, the proposed approach introduces **chaotic key-driven tiling, random pivot selection, and texture-adaptive embedding**, making the hidden data significantly harder to detect.

The application also provides a **web interface built with Flask** that allows users to embed and extract hidden messages.

---

# Features

- Hide secret messages inside images
- Extract hidden messages using the correct key
- Chaotic key-based tile generation using a logistic map
- Hybrid dynamic tiling (variable square and rectangular blocks)
- Pivot-based PVD embedding
- Texture-adaptive embedding
- Visualization of dynamic tile map
- Image quality evaluation metrics:
  - PSNR (Peak Signal-to-Noise Ratio)
  - MSE (Mean Squared Error)
  - Embedding Capacity
- Simple web interface for embedding and extraction

---

# System Architecture

## Embedding Process

Input Image + Secret Message + Secret Key  
↓  
Chaotic Logistic Map Generator  
↓  
Dynamic Tile Generation  
↓  
Random Pivot Selection  
↓  
Texture Analysis  
↓  
PVD Data Embedding  
↓  
Stego Image  

## Extraction Process

Stego Image + Secret Key  
↓  
Tile Reconstruction  
↓  
Pivot Identification  
↓  
Pixel Difference Analysis  
↓  
Bitstream Recovery  
↓  
Recovered Secret Message  

---

# Project Structure

HDT-PVD-Steganography
│
├── app.py
├── steganography.py
├── utils.py
│
├── static
│ ├── style.css
│ ├── stego.png
│ └── tile_map.png
│
├── templates
│ └── index.html
│
└── README.md


---

# Dependencies

Install the following Python libraries:

- Flask
- Pillow
- NumPy

---

# Installation

### 1. Clone the Repository

git clone https://github.com/Ares-1609/HDT-PVD-Steganography.git

cd HDT-PVD-Steganography

---

### 2. Install Required Libraries
pip install flask pillow numpy

---

# Running the Application

Run the Flask server:
python app.py


The application will start on:
http://127.0.0.1:5000


Open this link in your browser.

---

# How to Use

## Embed a Message

1. Upload a cover image.
2. Enter the secret message.
3. Enter a secret key.
4. Click **Encrypt Image**.

The system will generate:

- Stego Image
- Tile Map Visualization
- PSNR
- MSE
- Embedding Capacity

---

## Extract a Message

1. Upload the stego image.
2. Enter the same secret key used during embedding.
3. Click **Decrypt**.

The hidden message will appear on the screen.

---

# Evaluation Metrics

## Mean Squared Error (MSE)
MSE = (1 / MN) * Σ (I - Is)^2


Measures the average squared difference between the original and stego image.

Lower MSE indicates less distortion.

---

## Peak Signal to Noise Ratio (PSNR)
PSNR = 10 log10 (255² / MSE)


Measures the visual quality of the stego image.

Higher PSNR indicates better image quality.

---

## Embedding Capacity
Capacity = Embedded Bits / Total Pixels


Represents how much secret data can be hidden inside the image.

---

# Advantages of HDT-PVD

- Removes fixed embedding patterns used in traditional methods
- Uses chaotic key-driven tile generation
- Improves security against statistical steganalysis
- Maintains high image quality
- Provides adaptive embedding based on image texture

---

# Comparison with Traditional Techniques

| Method | Structure | Detectability | Security |
|------|------|------|------|
| LSB | Fixed pixels | High | Low |
| PVD | Pixel pairs | Moderate | Medium |
| RPVD | Random pairs | Moderate | Medium-High |
| **HDT-PVD** | Dynamic chaotic tiles | Very Low | High |

---

# Author

Rakshit Awadhiya  
B.Tech Computer Science Engineering

---

# License

This project is intended for **academic and research purposes**.
