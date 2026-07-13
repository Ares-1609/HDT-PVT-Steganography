import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_color_metrics():
    # 1. Point to the new color results directory
    csv_path = 'color-results/performance_table_color.csv'
    output_dir = 'color-results'
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Run batch_test_color.py first.")
        return

    df = pd.read_csv(csv_path)
    images = df['Image Name'].unique()
    markers = ['o', 's', '^', 'D', 'v']

    # --- GRAPH 1: PSNR vs Payload ---
    plt.figure(figsize=(10, 6))
    for i, img in enumerate(images):
        subset = df[df['Image Name'] == img]
        plt.plot(subset['Payload (Bytes)'], subset['PSNR (dB)'], 
                 marker=markers[i % len(markers)], label=img, linewidth=2)
        
    plt.title('Color Images: Payload Size vs PSNR')
    plt.xlabel('Payload Size (Bytes)')
    plt.ylabel('PSNR (dB)')
    plt.axhline(y=38, color='red', linestyle='--', linewidth=2, label='Imperceptibility Threshold (38 dB)')
    plt.legend(title="Test Images", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/graph_psnr_color.png', dpi=300)
    plt.close()

    # --- GRAPH 2: MSE vs Payload ---
    plt.figure(figsize=(10, 6))
    for i, img in enumerate(images):
        subset = df[df['Image Name'] == img]
        plt.plot(subset['Payload (Bytes)'], subset['MSE'], 
                 marker=markers[i % len(markers)], linestyle='--', label=img, linewidth=2)
        
    plt.title('Color Images: Payload Size vs MSE')
    plt.xlabel('Payload Size (Bytes)')
    plt.ylabel('Mean Squared Error (MSE)')
    plt.legend(title="Test Images", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/graph_mse_color.png', dpi=300)
    plt.close()

    print(f"✅ Performance graphs successfully saved to '{output_dir}'")

if __name__ == "__main__":
    plot_color_metrics()