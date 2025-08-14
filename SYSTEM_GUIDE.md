# 🌱 Disease Detection System (DARTS)

**Detection Assessment and Recognition in Tarlac City Software**

A web-based application for detecting diseases in rice and sugarcane crops using artificial intelligence.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Required Python packages (see requirements.txt)

### Installation

1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python run_app.py
   ```

4. **Open your browser and go to:** `http://localhost:5000`

## 🎯 **HOW TO RUN THE SYSTEM**

### **Option 1: Flask Application (Full AI System)**

#### **Step 1: Navigate to the correct directory**
```bash
cd "my_flask_app - Copy"
```

#### **Step 2: Install all required packages**
```bash
pip install -r requirements.txt
```

#### **Step 3: Run the system using the startup script**
```bash
python run_app.py
```

#### **Step 4: Access the application**
- Open your browser
- Go to: `http://localhost:5000` or `http://127.0.0.1:5000`
- If localhost doesn't work, try: `http://0.0.0.0:5000`

#### **Alternative: Run Flask directly**
```bash
python app.py
```

### **Option 2: Streamlit Application (Simplified Version)**

#### **Step 1: Navigate to the correct directory**
```bash
cd "my_flask_app - Copy"
```

#### **Step 2: Install Streamlit dependencies**
```bash
pip install -r requirements_demo.txt
```

#### **Step 3: Run the Streamlit app**
```bash
streamlit run simple_app.py
```

#### **Step 4: Access the application**
- Streamlit will automatically open your browser
- Default URL: `http://localhost:8501`
- If browser doesn't open automatically, manually navigate to the URL shown in terminal

### **Option 3: Ultra-Simple Streamlit Demo**
```bash
pip install -r requirements_ultra_simple.txt
streamlit run ultra_simple_app.py
```

## 🔧 **SYSTEM FEATURES**

### ✅ **What's Fixed**

1. **Model Loading Issues**
   - Fixed model path to correctly point to `../model/Dataset_cnn.h5`
   - Added proper error handling for model loading
   - Implemented automatic model download if not found

2. **Import Errors**
   - Removed duplicate imports in `app.py`
   - Made waitress import optional (falls back to Flask development server)
   - Fixed all import dependencies

3. **Disease Mapping**
   - Cleaned up disease mapping to remove duplicates
   - Added missing "Dried Leaves" disease information
   - Ensured all diseases in mapping have corresponding info

4. **Image Validation**
   - Improved plant detection logic to be more permissive
   - Enhanced color-based validation for rice/sugarcane detection
   - Lowered confidence thresholds for better detection rates

5. **Error Handling**
   - Added comprehensive error handling throughout the application
   - Better user feedback for invalid inputs
   - Graceful fallbacks for missing components

6. **Navigation**
   - Fixed camera page navigation back to home
   - Improved user experience flow

### 🎯 **Supported Diseases**

The system can detect the following conditions:

1. **BacterialBlight** - Bacterial infection causing wilting and yellowing
2. **Banded Chlorosis** - Nutrient deficiency causing yellow bands
3. **Brownspot (Rice)** - Fungal disease with reddish-brown spots
4. **Brown Spot (Sugarcane)** - Fungal disease affecting sugarcane
5. **BrownRust** - Rust disease affecting crops
6. **Dried Leaves** - Environmental stress causing dehydration
7. **Grassy shoot** - Viral disease causing stunted growth
8. **Healthy Leaves** - No disease detected
9. **Leafsmut** - Fungal disease with black spots
10. **Tungro** - Viral disease transmitted by leafhoppers
11. **Yellow Leaf** - Fungal disease causing yellowing

### 📱 **How to Use**

1. **Upload Image**: Click "Diagnose Now!" and upload a clear image of a rice or sugarcane leaf
2. **Camera Capture**: Use the camera feature to take a photo directly
3. **Get Results**: View detailed disease information, symptoms, causes, and management strategies
4. **Indicator System**: 
   - 🟢 **Green**: Healthy - No disease detected
   - 🟠 **Orange**: Mild - Early signs detected, monitoring recommended
   - 🔴 **Red**: Severe - Critical condition requiring immediate intervention

## 🛠️ **TECHNICAL DETAILS**

### **Architecture**
- **Backend**: Flask web framework
- **AI Model**: TensorFlow/Keras CNN for disease classification
- **Image Processing**: OpenCV for image validation and preprocessing
- **Frontend**: HTML/CSS/JavaScript with responsive design

### **Model Information**
- **CNN Model**: Custom-trained model for rice/sugarcane disease classification
- **Input Size**: 224x224 pixels
- **Output**: 11 disease classes + confidence scores
- **Validation**: MobileNetV2 for plant detection

### **File Structure**
```
my_flask_app - Copy/
├── app.py                 # Main Flask application
├── simple_app.py          # Streamlit version (deployment-ready)
├── ultra_simple_app.py    # Ultra-simple Streamlit demo
├── disease_info.py        # Disease information database
├── download_model.py      # Model download utility
├── run_app.py            # Startup script
├── test_system.py        # System testing script
├── requirements.txt      # Python dependencies (Flask)
├── requirements_demo.txt # Streamlit dependencies
├── requirements_ultra_simple.txt # Minimal dependencies
├── templates/            # HTML templates
│   ├── main.html         # Home page
│   ├── camera.html       # Camera interface
│   └── result.html       # Results page
├── static/               # Static assets
│   └── assets/           # Images and CSS
└── uploads/              # Uploaded images storage
```

## 🧪 **TESTING**

### **Test the Flask System**
```bash
cd "my_flask_app - Copy"
python test_system.py
```

### **Test the Streamlit System**
```bash
cd "my_flask_app - Copy"
python quick_test.py
```

### **What Tests Check**
- ✅ All required imports
- ✅ Model loading
- ✅ Disease information
- ✅ Image processing capabilities
- ✅ Application startup

## 🚨 **TROUBLESHOOTING**

### **Common Issues & Solutions**

#### **1. "can't open file 'run_app.py'"**
**Problem**: Wrong directory
**Solution**: 
```bash
cd "C:\Users\IFBC G\Documents\Disease detector\my_flask_app - Copy"
```

#### **2. "localhost refused to connect"**
**Problem**: App not running or wrong URL
**Solutions**:
- Check if the app is running in terminal
- Try: `http://127.0.0.1:5000` instead of `localhost`
- Try: `http://0.0.0.0:5000`
- Check firewall/antivirus settings

#### **3. "ModuleNotFoundError: No module named 'cv2'"**
**Problem**: OpenCV not installed
**Solution**: 
```bash
pip install opencv-python
```

#### **4. "streamlit : The term 'streamlit' is not recognized"**
**Problem**: Streamlit not installed
**Solution**: 
```bash
pip install streamlit
```

#### **5. "Model not found"**
**Problem**: AI model file missing
**Solution**: 
- The system will automatically download the model
- Ensure internet connection for first run
- Check if `../model/Dataset_cnn.h5` exists

### **Performance Tips**

- Use images with good lighting
- Ensure the leaf is clearly visible
- Avoid images with multiple leaves or complex backgrounds
- For best results, use images taken in natural daylight

## 🌐 **DEPLOYMENT OPTIONS**

### **Free Deployment Platforms**

#### **1. Streamlit Cloud (Recommended for Demo)**
- Upload `simple_app.py` and `requirements_demo.txt`
- Automatic deployment
- No large file issues

#### **2. Render**
- Use `render.yaml` configuration
- Free tier available
- Automatic deployment from GitHub

#### **3. Railway**
- Use `railway.json` configuration
- Free tier available
- Easy deployment

#### **4. Heroku**
- Free tier available
- Use `Procfile` for configuration

### **Deployment Steps**
1. **Push to GitHub** (use Git LFS for large files)
2. **Connect to deployment platform**
3. **Deploy automatically**

## 📞 **SUPPORT**

If you encounter any issues:

1. **Run the test script**: `python test_system.py`
2. **Check console output** for error messages
3. **Ensure all dependencies** are installed
4. **Verify file locations** and directory structure
5. **Check Python version** (3.8+ required)

## 🔄 **UPDATES**

### **Recent Fixes (Latest Update)**
- ✅ Fixed model path issues
- ✅ Improved error handling
- ✅ Enhanced image validation
- ✅ Added missing disease information
- ✅ Created comprehensive testing suite
- ✅ Added startup script for easy deployment
- ✅ Created Streamlit versions for easy deployment
- ✅ Fixed OpenCV and TensorFlow dependency issues
- ✅ Added fallback modes for deployment compatibility

### **System Versions Available**
1. **`app.py`** - Full Flask application with AI models
2. **`simple_app.py`** - Streamlit version with full functionality
3. **`ultra_simple_app.py`** - Minimal Streamlit demo
4. **`run_app.py`** - Startup script for Flask app

---

**Note**: This system is designed for educational and research purposes. For commercial agricultural use, please consult with agricultural experts and validate results with traditional diagnostic methods.

**For immediate deployment**: Use `simple_app.py` - it's deployment-ready and works without external dependencies!
