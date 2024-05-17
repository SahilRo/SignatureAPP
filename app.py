from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/generate_signature', methods=['POST'])
def generate_signature():
    name = request.form.get('name')
    file = request.files.get('signatureImage')

    if name:
        image_path = create_signature_from_text(name)
    elif file:
        image_path = process_signature_image(file)
    else:
        return 'No input provided', 400

    return send_file(image_path, mimetype='image/png', as_attachment=True)

def create_signature_from_text(name):
    # Create an image with white background
    image = Image.new('RGB', (650, 200), 'white')
    draw = ImageDraw.Draw(image)
    # Load a font
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'Fashioniqa.ttf')

    try:
        font = ImageFont.truetype(font_path, 150)
    except OSError:
        print("Font file not found or cannot be opened.")
        raise
    # Draw the text
    draw.text((50, 40), name, fill='black', font=font)
    # Save the image
    image_path = f'signatures/{name}.jpeg'
    os.makedirs(r"C:\Users\Sahil\Downloads\signatures", exist_ok=True)
    image.save(image_path)
    return image_path

def process_signature_image(file):
    # Save the uploaded file
    image_path = os.path.join(r"C:\Users\Sahil\Downloads", file.filename)
    os.makedirs(r"C:\Users\Sahil\Downloads", exist_ok=True)
    image = Image.open(image_path)
    resized_image = image.resize((700, 200))
    resized_image.save(image_path)
    # Here you could add additional processing if needed
    return image_path

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')

