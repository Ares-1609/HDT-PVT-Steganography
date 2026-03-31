from flask import Flask, render_template, request
from steganography import embed_data, extract_data
from utils import psnr, mse, embedding_capacity, draw_tiles

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/embed', methods=['POST'])
def embed():

    image = request.files['image']
    message = request.form['message']
    key = request.form['key']

    input_path = "static/input.png"
    image.save(input_path)

    stego_path, tiles = embed_data(input_path, message, key)

    psnr_val   = psnr(input_path, stego_path)
    mse_val    = mse(input_path, stego_path)
    capacity   = embedding_capacity(len(message) * 8, input_path)
    tile_map   = draw_tiles(input_path, tiles)

    return render_template(
        "index.html",
        stego=stego_path,
        original=input_path,
        psnr=round(psnr_val, 4),
        mse=round(mse_val, 4),
        capacity=round(capacity, 6),
        tilemap=tile_map
    )


@app.route('/extract', methods=['POST'])
def extract():

    image = request.files['image']
    key = request.form['key']

    path = "static/stego_input.png"
    image.save(path)

    message = extract_data(path, key)

    return render_template(
        "index.html",
        message=message if message else "⚠️ No message found. Check the key or image."
    )


if __name__ == "__main__":
    app.run(debug=True)