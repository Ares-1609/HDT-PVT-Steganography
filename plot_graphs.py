import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_metrics():
    # Load the data generated from Step 2
    csv_path = 'results/performance_table.csv'
    if not os.path.exists(csv_path):
        print(f"Could not find {csv_path}. Make sure Step 2 ran successfully.")
        return

    df = pd.read_csv(csv_path)

    # 1. Plot PSNR vs Payload Size
    plt.figure(figsize=(10, 6))
    for img in df['Image Name'].unique():
        subset = df[df['Image Name'] == img]
        plt.plot(subset['Payload (Bytes)'], subset['PSNR (dB)'], marker='o', label=img)
        
    plt.title('Payload Size vs PSNR Performance')
    plt.xlabel('Payload Size (Bytes)')
    plt.ylabel('PSNR (dB)')
    plt.legend(title="Test Images")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('results/graph_psnr.png', dpi=300)
    plt.close()

    # 2. Plot MSE vs Payload Size
    plt.figure(figsize=(10, 6))
    for img in df['Image Name'].unique():
        subset = df[df['Image Name'] == img]
        plt.plot(subset['Payload (Bytes)'], subset['MSE'], marker='s', linestyle='--', label=img)
        
    plt.title('Payload Size vs Mean Squared Error (MSE)')
    plt.xlabel('Payload Size (Bytes)')
    plt.ylabel('MSE')
    plt.legend(title="Test Images")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('results/graph_mse.png', dpi=300)
    plt.close()

    print("Graphs successfully generated: 'graph_psnr.png' and 'graph_mse.png' in the results folder.")

if __name__ == "__main__":
    plot_metrics()