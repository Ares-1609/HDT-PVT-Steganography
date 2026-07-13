import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from PIL import Image

def plot_color_histogram(cover_path, stego_path, output_path, img_name):
    """Plots and compares histograms for R, G, and B channels individually."""
    cover = np.array(Image.open(cover_path).convert("RGB"))
    stego = np.array(Image.open(stego_path).convert("RGB"))
    
    channels = ['Red', 'Green', 'Blue']
    colors = ['r', 'g', 'b']
    
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    
    for i, (channel_name, color) in enumerate(zip(channels, colors)):
        cover_channel = cover[:, :, i].ravel()
        stego_channel = stego[:, :, i].ravel()
        
        axes[i].hist(cover_channel, bins=256, range=(0, 256), alpha=0.4, color='gray', label='Cover Image')
        axes[i].hist(stego_channel, bins=256, range=(0, 256), alpha=0.6, histtype='step', color=color, linewidth=1.5, label=f'Stego {channel_name}')
        
        axes[i].set_title(f'{channel_name} Channel Histogram Preservation - {img_name}')
        axes[i].set_ylabel('Frequency')
        axes[i].legend()
        axes[i].grid(True, linestyle='--', alpha=0.5)
        
    plt.xlabel('Pixel Intensity')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def chi_square_test_color(stego_path):
    """Performs the Chi-Square Attack analysis on each color channel separately."""
    stego = np.array(Image.open(stego_path).convert("RGB"))
    channels = ['Red', 'Green', 'Blue']
    p_values = {}
    
    for i, ch_name in enumerate(channels):
        channel_data = stego[:, :, i].ravel()
        freq, _ = np.histogram(channel_data, bins=256, range=(0, 256))
        
        observed = []
        expected = []
        
        # Check Pairs of Values (PoVs): (2k, 2k+1)
        for k in range(128):
            y2k = freq[2 * k]
            y2k_1 = freq[2 * k + 1]
            mean_val = (y2k + y2k_1) / 2.0
            
            if mean_val > 0:
                observed.extend([y2k, y2k_1])
                expected.extend([mean_val, mean_val])
                
        if len(observed) > 0:
            _, p_val = chisquare(observed, f_exp=expected)
            p_values[ch_name] = p_val
        else:
            p_values[ch_name] = 1.0
            
    return p_values


def rs_steganalysis_color(image_path):
    """Calculates RS Steganalysis percentages (Rm, Sm, Rm-1, Sm-1) for each color plane."""
    # Use int32 to prevent overflow when calculating pixel differences
    img = np.array(Image.open(image_path).convert("RGB"), dtype=np.int32)
    H, W, C = img.shape
    
    # Ensure dimensions are even for 2x2 blocks
    H_crop = H - (H % 2)
    W_crop = W - (W % 2)
    
    results = {}
    channels = ['Red', 'Green', 'Blue']
    
    for c in range(C):
        ch_data = img[:H_crop, :W_crop, c]
        
        # Vectorized block extraction (fast slicing into 2x2 blocks)
        blocks = ch_data.reshape(H_crop//2, 2, W_crop//2, 2).swapaxes(1, 2).reshape(-1, 4)
        
        # Continuity function: sum of absolute differences around the 2x2 block
        def f(b):
            return np.abs(b[:,0]-b[:,1]) + np.abs(b[:,1]-b[:,3]) + np.abs(b[:,3]-b[:,2]) + np.abs(b[:,2]-b[:,0])
        
        # Mask functions
        def F1(x):
            return x ^ 1
            
        def Fm1(x):
            res = np.where(x % 2 == 0, x - 1, x + 1)
            return np.clip(res, 0, 255)
            
        # Apply M mask (invert LSB for pixels 2 and 3)
        b_M = blocks.copy()
        b_M[:,1] = F1(b_M[:,1])
        b_M[:,2] = F1(b_M[:,2])
        
        # Apply -M mask (shift LSB for pixels 2 and 3)
        b_m1 = blocks.copy()
        b_m1[:,1] = Fm1(b_m1[:,1])
        b_m1[:,2] = Fm1(b_m1[:,2])
        
        # Calculate scores
        f_orig = f(blocks)
        f_M = f(b_M)
        f_m1 = f(b_m1)
        
        # Calculate percentages properly using np.mean on booleans
        R_m = np.mean(f_M > f_orig) * 100
        S_m = np.mean(f_M < f_orig) * 100
        R_m1 = np.mean(f_m1 > f_orig) * 100
        S_m1 = np.mean(f_m1 < f_orig) * 100
        
        results[channels[c]] = (R_m, S_m, R_m1, S_m1)
        
    return results


if __name__ == "__main__":
    # Pointing strictly to your new color dataset
    images = ['baboon_color.png', 'jet_color.png', 'peppers_color.png']
    
    # Testing your new massive color payload
    payload_to_test = 6000 
    
    # Make sure we are pulling from the right output folder
    output_dir = 'color-results'
    os.makedirs(output_dir, exist_ok=True)
    print(f"Running Color-Space Resistance Analysis (Payload: {payload_to_test}B)...\n")
    
    for img_name in images:
        cover_image = f'datasets/{img_name}'
        stego_image = f'{output_dir}/stego_{payload_to_test}B_{img_name}'
        
        if not os.path.exists(stego_image) or not os.path.exists(cover_image):
            print(f"Skipping {img_name} due to missing files in {output_dir}.")
            continue
            
        print(f"--- Color Analysis for {img_name} ---")
        
        # 1. Triple Channel Histogram Comparison
        hist_output = f'{output_dir}/color_hist_comparison_{img_name}'
        plot_color_histogram(cover_image, stego_image, hist_output, img_name)
        print(f"  [✓] Histogram breakdown saved to {hist_output}")
        
        # 2. Channel-by-Channel Chi-Square Attack Test
        p_vals = chi_square_test_color(stego_image)
        print("  [✓] Chi-Square p-values:")
        for ch, p in p_vals.items():
            print(f"      - {ch} Channel: p = {p:.4f} (Target close to 0.0000 for high randomness/stealth)")
            
        # 3. Channel-by-Channel RS Steganalysis
        rs_results = rs_steganalysis_color(stego_image)
        print("  [✓] RS Steganalysis Percentages:")
        for ch, (Rm, Sm, Rm1, Sm1) in rs_results.items():
            print(f"      - {ch} Channel: Rm={Rm:.2f}%, Sm={Sm:.2f}%, Rm-1={Rm1:.2f}%, Sm-1={Sm1:.2f}%")
        print("-" * 40)