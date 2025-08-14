from flask import Flask, render_template, request, send_from_directory
import os
import numpy as np
import cv2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from disease_info import disease_data  # Import disease details
try:
    from waitress import serve
    WAITRESS_AVAILABLE = True
except ImportError:
    WAITRESS_AVAILABLE = False
    print("Warning: waitress not available, using Flask development server")
from download_model import download_model_from_drive
import gdown # Added gdown for Google Drive download

app = Flask(__name__)

# Fixed disease mapping - removed duplicates and ensured consistency
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

# Ensure uploads directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Load Models with proper error handling
CNN_MODEL_PATH = "../model/Dataset_cnn.h5"

# Google Drive model URL (you'll need to upload your model and get this URL)
MODEL_DRIVE_URL = "https://drive.google.com/uc?id=YOUR_MODEL_FILE_ID"

rice_model = None
plant_model = None

try:
    print("Loading CNN model...")
    rice_model = load_model(CNN_MODEL_PATH)
    print("✅ CNN model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load CNN model: {e}")
    print("Attempting to download model...")
    try:
        download_model_from_drive()
        rice_model = load_model(CNN_MODEL_PATH)
        print("✅ CNN model downloaded and loaded successfully")
    except Exception as download_error:
        print(f"❌ Failed to download model: {download_error}")
        raise RuntimeError(f"Could not load or download the model: {download_error}")

# Load Pretrained Model for Detection
try:
    print("Loading MobileNetV2 model...")
    plant_model = MobileNetV2(weights="imagenet")
    print("✅ MobileNetV2 model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load MobileNetV2 model: {e}")
    raise RuntimeError(f"Could not load MobileNetV2 model: {e}")

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')

        # Validate if it's an image
        if not file or not allowed_file(file.filename):
            return render_template(
                'result.html',
                disease="Invalid Input",
                confidence_score=0.0,
                details={
                    "Type": "N/A",
                    "Symptoms": ["Invalid file type. Please upload a valid image."],
                    "Causes": ["N/A"],
                    "Management Strategies": ["Ensure the uploaded file is an image of rice or sugarcane disease."]
                },
                image_url=None
            )

        # Save the uploaded file
        img_path = os.path.join('uploads', file.filename)
        file.save(img_path)

        # Step 1: Check if the image is black
        if is_black_image(img_path):
            return render_template(
                'result.html',
                disease="Invalid Input",
                confidence_score=0.0,
                details={
                    "Type": "N/A",
                    "Symptoms": ["Uploaded image is too dark or black. Please upload a clear image."],
                    "Causes": ["N/A"],
                    "Management Strategies": ["Ensure the image has enough light and clear details."]
                },
                image_url=f"/uploads/{file.filename}"
            )

        # Step 2: Validate if it's a rice or sugarcane
        if not is_plant_image(img_path):
            return render_template(
                'result.html',
                disease="Invalid Input",
                confidence_score=0.0,
                details={
                    "Type": "N/A",
                    "Symptoms": ["Uploaded image does not appear to be a plant leaf."],
                    "Causes": ["N/A"],
                    "Management Strategies": ["Please upload a clear image of rice or sugarcane leaves."]
                },
                image_url=f"/uploads/{file.filename}"
            )

        # Step 3: Predict Disease
        prediction_result = predict_disease(img_path)

        if prediction_result["predicted_disease"] == "Invalid Input":
            return render_template(
                'result.html',
                disease="Invalid Input",
                confidence_score=0.0,
                details={
                    "Type": "N/A",
                    "Symptoms": ["The image does not match rice or sugarcane diseases."],
                    "Causes": ["N/A"],
                    "Management Strategies": ["Please upload a valid image of rice or sugarcane."]
                },
                image_url=f"/uploads/{file.filename}"
            )

        # Fetch disease details including the indicator
        disease_details = disease_data.get(
            prediction_result["predicted_disease"],
            {
                "Type": "Unknown",
                "Symptoms": ["No information available"],
                "Causes": ["No information available"],
                "Management Strategies": ["No information available"],
                "indicator": "green"  # Default indicator for unknown condition
            }
        )
        indicator = disease_details.get("indicator", "green")

        return render_template(
            'result.html',
            disease=prediction_result["predicted_disease"],
            confidence_score=prediction_result["confidence_score"],
            secondary_disease=prediction_result["secondary_disease"],
            secondary_confidence_score=prediction_result["secondary_confidence_score"],
            details=disease_details,
            indicator=indicator,
            image_url=f"/uploads/{file.filename}"
        )
    return render_template('main.html')

def is_black_image(img_path, dark_threshold=15, black_ratio=0.98):
    """Checks if the image is mostly black or too dark."""
    try:
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Load in grayscale
        if img is None:
            return True  # Unreadable image is considered black

        mean_intensity = np.mean(img)  # Compute average brightness

        # Count pixels below the dark threshold
        dark_pixels = np.sum(img < dark_threshold)
        total_pixels = img.size
        dark_ratio = dark_pixels / total_pixels  # Percentage of dark pixels

        # Consider image black if more than 98% of pixels are below the dark threshold
        return dark_ratio > black_ratio
    except Exception as e:
        print(f"Error checking black image: {e}")
        return True  # Fail-safe: Assume black if error occurs

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

def invalid_input_response(message):
    """Returns a response for invalid input."""
    return render_template(
        'result.html',
        disease="Invalid Input",
        confidence_score=0.0,
        details={
            "Type": "N/A",
            "Symptoms": [message],
            "Causes": ["N/A"],
            "Management Strategies": ["Please upload a valid rice or sugarcane image."]
        },
        image_url=None
    )

def is_plant_image(img_path):
    """Checks if an image is a plant using MobileNetV2."""
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        predictions = plant_model.predict(img_array, verbose=0)
        top_prediction = np.argmax(predictions)

        # ImageNet categories for plants (broad range)
        # Categories 0-999 include many plant-related classes
        # We'll be more permissive to avoid false negatives
        plant_categories = list(range(0, 1000))  # Accept most ImageNet categories
        
        # Additional check: if the image has significant green content, consider it a plant
        img_cv = cv2.imread(img_path)
        if img_cv is not None:
            img_hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
            lower_green = np.array([25, 30, 10])
            upper_green = np.array([100, 255, 255])
            mask = cv2.inRange(img_hsv, lower_green, upper_green)
            green_percentage = (cv2.countNonZero(mask) / mask.size) * 100
            
            # If more than 20% is green, consider it a plant
            if green_percentage > 20:
                return True

        return top_prediction in plant_categories
    except Exception as e:
        print(f"Error during plant validation: {e}")
        return False

def is_rice_or_sugarcane(img_path):
    """Verifies if the leaf is rice or sugarcane using improved color analysis."""
    try:
        img = cv2.imread(img_path)
        if img is None:
            return False
            
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define an expanded green color range for plant leaves
        lower_green = np.array([25, 30, 10])  # Allow for more shades
        upper_green = np.array([100, 255, 255])  # Include slightly yellow-green shades

        mask = cv2.inRange(img_hsv, lower_green, upper_green)
        green_percentage = (cv2.countNonZero(mask) / mask.size) * 100

        # More permissive threshold for plant detection
        return green_percentage > 15  # Lowered threshold to be more inclusive
    except Exception as e:
        print(f"Error during rice/sugarcane validation: {e}")
        return False

def predict_disease(img_path):
    """Runs CNN model to classify disease and validates confidence levels."""
    try:
        # Preprocess the image
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict disease using the model
        predictions = rice_model.predict(img_array, verbose=0)[0]

        # Sort predictions and get the top two indices
        top_two_indices = predictions.argsort()[-2:][::-1]
        primary_index = top_two_indices[0]
        secondary_index = top_two_indices[1]

        # Get confidence scores for top two predictions
        primary_confidence = float(predictions[primary_index])
        secondary_confidence = float(predictions[secondary_index])

        # Validate prediction: If confidence is too low, return "Invalid Input"
        if primary_confidence < 0.30 or primary_index not in disease_mapping:  # Lowered threshold
            return {
                "predicted_disease": "Invalid Input",
                "confidence_score": 0.0,
                "secondary_disease": None,
                "secondary_confidence_score": 0.0
            }

        return {
            "predicted_disease": disease_mapping[primary_index],
            "confidence_score": primary_confidence,
            "secondary_disease": disease_mapping.get(secondary_index, "Unknown"),
            "secondary_confidence_score": secondary_confidence
        }
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {
            "predicted_disease": "Invalid Input",
            "confidence_score": 0.0,
            "secondary_disease": None,
            "secondary_confidence_score": 0.0
        }

def allowed_file(filename):
    """Checks if the uploaded file is an allowed image type."""
    allowed_extensions = {"png", "jpg", "jpeg"}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def home():
    return "Flask Server is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
