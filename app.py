from flask import Flask, request, send_file, render_template
import rasterio
import numpy as np
import os

app = Flask(__name__)

# নিশ্চিত করো uploads এবং outputs ফোল্ডার আছে
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')  # upload form দেখাবে

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['raster']   # HTML form এ name="raster"
    input_path = os.path.join("uploads", file.filename)
    file.save(input_path)

    # Raster পড়া
    with rasterio.open(input_path) as src:
        data = src.read(1)  # প্রথম band
        min_val, max_val = data.min(), data.max()
        normalized = (data - min_val) / (max_val - min_val)

        profile = src.profile
        output_path = os.path.join("outputs", "normalized_" + file.filename)

        # Normalized raster সেভ করা
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(normalized, 1)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
