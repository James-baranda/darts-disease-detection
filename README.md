# 🌱 DARTS - Disease Detection System

https://darts-disease-detection-q6tqwq9fy7tzpsappdewemj.streamlit.app/#about-darts

**Detection Assessment and Recognition in Tarlac City Software**

A comprehensive AI-powered web application for detecting diseases in rice and sugarcane crops using deep learning and computer vision.

## 🚀 Features

- **AI-Powered Disease Detection** - Uses CNN model to classify 11 different disease types
- **Multi-Step Validation** - Black image detection, plant verification, crop-specific validation
- **Web Interface** - User-friendly Flask web application with file upload and camera capture
- **Detailed Analysis** - Provides disease information, symptoms, and management strategies
- **Real-time Processing** - Instant analysis with confidence scores

## 🎯 Supported Diseases

- Bacterial Blight
- Banded Chlorosis
- Brown Spot (Rice & Sugarcane)
- Brown Rust
- Dried Leaves
- Grassy Shoot
- Healthy Leaves
- Leaf Smut
- Tungro
- Yellow Leaf

## 🛠️ Technology Stack

- **Backend**: Flask, Python
- **AI/ML**: TensorFlow, Keras, OpenCV
- **Models**: Custom CNN, MobileNetV2
- **Frontend**: HTML, CSS, JavaScript
- **Image Processing**: PIL, NumPy

## 📋 Requirements

- Python 3.8+
- TensorFlow 2.x
- Flask
- OpenCV
- NumPy
- PIL

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/darts-disease-detection.git
   cd darts-disease-detection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the web interface**
   - Open your browser and go to `http://localhost:5000`

## 📁 Project Structure

```
darts-disease-detection/
├── app.py                 # Main Flask application
├── disease_info.py        # Disease information database
├── download_model.py      # Model download utility
├── requirements.txt       # Python dependencies
├── SYSTEM_GUIDE.md       # Detailed setup guide
├── templates/            # HTML templates
│   ├── main.html
│   ├── camera.html
│   └── result.html
├── static/               # CSS/JS assets
└── uploads/              # User uploaded images
