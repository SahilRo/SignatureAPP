import os
from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import pytesseract
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Get the paths from environment variables
tesseract_path = os.getenv('TESSERACT_PATH')
fonts_path = os.getenv('FONTS_PATH')

# Set the Tesseract path
pytesseract.pytesseract.tesseract_cmd = tesseract_path

@app.route('/generate_signature', methods=['POST'])
def generate_signature():
    name = request.form.get('name')
    file = request.files.get('signatureImage')

    if name:
        image_path = create_signature_from_text(name)
    elif file:
        extracted_text = extract_text_from_image(file)
        if extracted_text:
            image_path = create_signature_from_text(extracted_text)
        else:
            return 'No text found in the uploaded image', 400
    else:
        return 'No input provided', 400

    return send_file(image_path, mimetype='image/png', as_attachment=True)

def create_signature_from_text(name):
    # Create an image with white background
    image = Image.new('RGB', (650, 200), 'white')
    draw = ImageDraw.Draw(image)
    # Load a font
    font_path = os.path.join(fonts_path, 'Fashioniqa.ttf')

    try:
        font = ImageFont.truetype(font_path, 150)
    except OSError:
        print("Font file not found or cannot be opened.")
        raise
    # Draw the text
    draw.text((50, 40), name, fill='black', font=font)
    # Save the image
    image_path = f'signatures/{name}.jpeg'
    os.makedirs(os.path.join('static', 'signatures'), exist_ok=True)
    image.save(os.path.join('static', image_path))
    return image_path


def extract_text_from_image(file):
    # Save the uploaded file temporarily
    temp_path = os.path.join('temp', file.filename)
    os.makedirs('temp', exist_ok=True)
    file.save(temp_path)

    # Use pytesseract to extract text
    image = Image.open(temp_path)
    extracted_text = pytesseract.image_to_string(image)
    print(extracted_text)
    # Clean up temporary file
    os.remove(temp_path)

    return extracted_text.strip()


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
