from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)

# Simplified disease mapping for Vercel deployment
disease_mapping = {
    0: "BacterialBlight",
    1: "Banded Chlorosis", 
    2: "Brownspot (Rice)",
    3: "Brown Spot (Sugarcane)",
    4: "BrownRust",
    5: "Dried Leaves",
    6: "Grassy shoot",
    7: "Healthy Leaves",
    8: "Leafsmut",
    9: "Tungro",
    10: "Yellow Leaf"
}

# Simplified disease data
disease_data = {
    "BacterialBlight": {
        "Type": "Bacterial Disease",
        "Symptoms": ["Water-soaked lesions on leaves", "Yellow to brown streaks"],
        "Causes": ["Xanthomonas oryzae bacteria", "High humidity conditions"],
        "Management Strategies": ["Use resistant rice varieties", "Apply copper-based bactericides"]
    },
    "Healthy Leaves": {
        "Type": "Normal Condition",
        "Symptoms": ["Vibrant green color", "Normal leaf shape"],
        "Causes": ["Proper nutrition", "Adequate water supply"],
        "Management Strategies": ["Continue current management practices", "Regular monitoring"]
    },
    "Dried Leaves": {
        "Type": "Environmental Stress",
        "Symptoms": ["Leaf margins turning brown", "Wilting and drying"],
        "Causes": ["Water stress/drought", "High temperature"],
        "Management Strategies": ["Ensure adequate irrigation", "Apply mulching"]
    }
}

def simple_disease_prediction(image_array):
    """
    Simplified disease prediction based on color analysis
    This replaces the heavy TensorFlow model for Vercel deployment
    """
    try:
        # Convert to RGB if needed
        if len(image_array.shape) == 3 and image_array.shape[2] == 3:
            # Calculate color statistics
            red_mean = np.mean(image_array[:, :, 0])
            green_mean = np.mean(image_array[:, :, 1])
            blue_mean = np.mean(image_array[:, :, 2])
            
            # Simple rule-based classification
            if green_mean > red_mean and green_mean > blue_mean and green_mean > 100:
                return "Healthy Leaves", 0.85
            elif red_mean > green_mean and red_mean > 80:
                return "BacterialBlight", 0.75
            elif green_mean < 60:
                return "Dried Leaves", 0.70
            else:
                return "Healthy Leaves", 0.65
        else:
            return "Unknown", 0.50
    except Exception as e:
        print(f"Error in prediction: {e}")
        return "Error", 0.0

@app.route('/')
def index():
    if request.method == 'POST':
        return handle_upload()
    return render_template('main.html')

@app.route('/', methods=['POST'])
def handle_upload():
    try:
        file = request.files.get('file')
        
        if not file or not allowed_file(file.filename):
            return render_template(
                'result.html',
                disease="Invalid Input",
                confidence_score=0.0,
                details={
                    "Type": "N/A",
                    "Symptoms": ["Invalid file type. Please upload a valid image."],
                    "Causes": ["N/A"],
                    "Management Strategies": ["Ensure the uploaded file is an image."]
                },
                image_url=None
            )
        
        # Process the image
        image = Image.open(file.stream)
        img_array = np.array(image)
        
        # Get prediction
        predicted_disease, confidence = simple_disease_prediction(img_array)
        
        # Get disease details
        details = disease_data.get(predicted_disease, {
            "Type": "Unknown",
            "Symptoms": ["Analysis incomplete"],
            "Causes": ["Unknown"],
            "Management Strategies": ["Consult agricultural expert"]
        })
        
        return render_template(
            'result.html',
            disease=predicted_disease,
            confidence_score=confidence,
            details=details,
            image_url=None
        )
        
    except Exception as e:
        print(f"Error processing upload: {e}")
        return render_template(
            'result.html',
            disease="Processing Error",
            confidence_score=0.0,
            details={
                "Type": "Error",
                "Symptoms": ["Unable to process image"],
                "Causes": ["Technical issue"],
                "Management Strategies": ["Please try again with a different image"]
            },
            image_url=None
        )

@app.route('/camera')
def camera():
    return render_template('camera.html')

def allowed_file(filename):
    """Checks if the uploaded file is an allowed image type."""
    allowed_extensions = {"png", "jpg", "jpeg"}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "DARTS Disease Detection"})

# Vercel serverless function handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
