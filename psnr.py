import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_combined_psnr():
    csv_path = 'results/performance_table.csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path)

    plt.figure(figsize=(10, 6))
    
    # Plot each image's line
    markers = ['o', 's', '^', 'D', 'v']
    images = df['Image Name'].unique()
    
    for i, img in enumerate(images):
        subset = df[df['Image Name'] == img]
        plt.plot(subset['Payload (Bytes)'], subset['PSNR (dB)'], 
                 marker=markers[i % len(markers)], label=img, linewidth=2)
        
    # Add the 38 dB Imperceptibility Threshold line
    plt.axhline(y=38, color='red', linestyle='--', linewidth=2, label='Imperceptibility Threshold (38 dB)')

    plt.title('Payload Size vs PSNR Performance (All Test Images)')
    plt.xlabel('Payload Size (Bytes)')
    plt.ylabel('PSNR (dB)')
    plt.legend(title="Legend", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    output_path = 'results/graph_combined_psnr.png'
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"Graph successfully saved to {output_path}")

if __name__ == "__main__":
    plot_combined_psnr()