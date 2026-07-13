import cv2
import os
from steganography import embed_data, extract_data

def embed_data_color(input_path, message, key):
    """
    Splits a color image into B, G, R channels, embeds a portion of the 
    message into each using the core HDT-PVD logic, and merges them back.
    """
    # 1. Read color image (OpenCV reads as BGR)
    color_img = cv2.imread(input_path)
    if color_img is None:
        raise ValueError(f"Could not read {input_path}. Ensure it is a valid color image.")
    
    B, G, R = cv2.split(color_img)
    
    # 2. Split the secret message into 3 roughly equal parts
    part_len = len(message) // 3
    msg_b = message[:part_len]
    msg_g = message[part_len:2*part_len]
    msg_r = message[2*part_len:]
    
    # 3. Save channels as temporary grayscale images
    cv2.imwrite('temp_B.png', B)
    cv2.imwrite('temp_G.png', G)
    cv2.imwrite('temp_R.png', R)
    
    # 4. Route each channel through your existing HDT-PVD embedder
    # Note: embed_data saves to 'static/stego.png' by default. We rename it 
    # immediately so the next channel doesn't overwrite it.
    stego_b_path, tiles_b = embed_data('temp_B.png', msg_b, key)
    os.rename(stego_b_path, 'stego_temp_B.png')
    
    stego_g_path, _ = embed_data('temp_G.png', msg_g, key)
    os.rename(stego_g_path, 'stego_temp_G.png')
    
    stego_r_path, _ = embed_data('temp_R.png', msg_r, key)
    os.rename(stego_r_path, 'stego_temp_R.png')
    
    # 5. Read the modified stego channels back into memory
    stego_B = cv2.imread('stego_temp_B.png', cv2.IMREAD_GRAYSCALE)
    stego_G = cv2.imread('stego_temp_G.png', cv2.IMREAD_GRAYSCALE)
    stego_R = cv2.imread('stego_temp_R.png', cv2.IMREAD_GRAYSCALE)
    
    # 6. Merge the modified channels back into a single color image
    stego_color = cv2.merge([stego_B, stego_G, stego_R])
    final_output_path = 'static/stego_color.png'
    cv2.imwrite(final_output_path, stego_color)
    
    # 7. Clean up the temporary workspace files
    temp_files = ['temp_B.png', 'temp_G.png', 'temp_R.png', 
                  'stego_temp_B.png', 'stego_temp_G.png', 'stego_temp_R.png']
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
            
    # We return tiles_b just so the web UI has something to draw, 
    # though technically all 3 channels have their own tile maps!
    return final_output_path, tiles_b


def extract_data_color(stego_path, key):
    """
    Splits the color stego image, extracts the message parts from 
    the B, G, and R channels, and reconstructs the full message.
    """
    color_img = cv2.imread(stego_path)
    if color_img is None:
        return "Error: Could not read color stego image."
        
    B, G, R = cv2.split(color_img)
    
    cv2.imwrite('temp_B.png', B)
    cv2.imwrite('temp_G.png', G)
    cv2.imwrite('temp_R.png', R)
    
    # Extract the payload from each channel using existing logic
    msg_b = extract_data('temp_B.png', key)
    msg_g = extract_data('temp_G.png', key)
    msg_r = extract_data('temp_R.png', key)
    
    # Clean up
    for f in ['temp_B.png', 'temp_G.png', 'temp_R.png']:
        if os.path.exists(f):
            os.remove(f)
            
    # Stitch the message back together
    full_message = str(msg_b) + str(msg_g) + str(msg_r)
    return full_message