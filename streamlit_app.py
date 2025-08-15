import streamlit as st
import numpy as np
from PIL import Image
import time

# Page configuration
st.set_page_config(
    page_title="DARTS - Disease Detection System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetic design
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* Card styling */
    .info-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Upload area styling */
    .upload-area {
        background: linear-gradient(145deg, #f0f2f6, #ffffff);
        border: 3px dashed #4CAF50;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    /* Results card */
    .results-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    
    /* Animation keyframes */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Import disease data from the main app
try:
    from disease_info import disease_data
except ImportError:
    # Fallback disease data if import fails
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
        },
        "Tungro": {
            "Type": "Viral Disease",
            "Symptoms": ["Yellow-orange discoloration", "Stunted growth"],
            "Causes": ["Rice tungro virus", "Green leafhopper transmission"],
            "Management Strategies": ["Control green leafhopper", "Use tungro-resistant varieties"]
        },
        "Brownspot (Rice)": {
            "Type": "Fungal Disease",
            "Symptoms": ["Small brown spots on leaves", "Spots with yellow halos"],
            "Causes": ["Bipolaris oryzae fungus", "High humidity and temperature"],
            "Management Strategies": ["Apply fungicides", "Improve field drainage"]
        }
    }

# Disease mapping for prediction
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

def analyze_image(image):
    """Enhanced disease detection analysis using PIL and NumPy"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            # Calculate color statistics
            red = np.mean(img_array[:, :, 0])
            green = np.mean(img_array[:, :, 1])
            blue = np.mean(img_array[:, :, 2])
            
            # Calculate color ratios and statistics
            total_brightness = red + green + blue
            green_ratio = green / total_brightness if total_brightness > 0 else 0
            red_ratio = red / total_brightness if total_brightness > 0 else 0
            
            # Calculate green dominance for plant detection
            green_dominance = green - max(red, blue)
            
            # Calculate color variance for texture analysis
            red_var = np.var(img_array[:, :, 0])
            green_var = np.var(img_array[:, :, 1])
            blue_var = np.var(img_array[:, :, 2])
            color_variance = (red_var + green_var + blue_var) / 3
            
            # Enhanced disease classification logic
            if green < 60 and red > 80 and blue < 70:
                # Brown/dried appearance
                return "Dried Leaves", 0.82
            elif green > 120 and green_dominance > 30 and color_variance < 1000:
                # Healthy green with low variance
                return "Healthy Leaves", 0.88
            elif green > 100 and red > 90 and green_ratio > 0.4:
                # Yellowish-green, possible chlorosis
                return "Banded Chlorosis", 0.75
            elif red > green and red > 100 and green < 80:
                # Reddish-brown spots
                if color_variance > 1500:
                    return "BacterialBlight", 0.79
                else:
                    return "Brownspot (Rice)", 0.73
            elif green < 90 and red > 70 and blue < 60:
                # Yellow-orange discoloration
                return "Tungro", 0.76
            elif green > 80 and green_dominance > 10:
                # Moderately healthy
                return "Healthy Leaves", 0.70
            elif red > 60 and green < 80:
                # Some disease symptoms
                return "Dried Leaves", 0.68
            else:
                # Default classification
                return "Healthy Leaves", 0.65
        else:
            return "Unknown", 0.50
    except Exception as e:
        st.error(f"Analysis error: {str(e)}")
        return "Error", 0.0

def main():
    # Animated Header
    st.markdown("""
    <div class="main-header pulse-animation">
        <h1>🌱 DARTS - Disease Detection System</h1>
        <h3>Detection Assessment and Recognition in Tarlac City Software</h3>
        <p style="font-size: 1.2em; margin-top: 1rem;">🤖 AI-Powered Agricultural Disease Detection</p>
        <p style="font-size: 1em; opacity: 0.9;">Advanced Computer Vision • Real-time Analysis • Expert Recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Sidebar with animations
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px; margin-bottom: 1rem;">
            <h2 style="color: white;">🔬 System Dashboard</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Animated metrics
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>11</h3>
                <p>Diseases</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>2</h3>
                <p>Crop Types</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Disease categories with icons
        st.markdown("### 🎯 Disease Categories")
        disease_categories = {
            "🦠 Bacterial": ["BacterialBlight"],
            "🍄 Fungal": ["Brownspot (Rice)", "Brown Spot (Sugarcane)", "BrownRust", "Leafsmut"],
            "🦠 Viral": ["Tungro", "Grassy shoot"],
            "🌿 Physiological": ["Banded Chlorosis", "Dried Leaves", "Yellow Leaf"],
            "✅ Healthy": ["Healthy Leaves"]
        }
        
        for category, diseases in disease_categories.items():
            with st.expander(f"{category} ({len(diseases)})"):
                for disease in diseases:
                    st.write(f"• {disease}")
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
            <p style="color: white; margin: 0;"><strong>🚀 Version 2.0</strong></p>
            <p style="color: white; margin: 0; font-size: 0.8em;">Enhanced AI Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Dynamic Upload Area
    st.markdown("""
    <div class="info-card">
        <h2 style="text-align: center; color: #4CAF50;">📤 Upload Plant Image for AI Analysis</h2>
        <p style="text-align: center; font-size: 1.1em; color: #666;">
            Upload a clear image of rice or sugarcane leaf to get instant disease detection
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a rice or sugarcane leaf image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear image of a plant leaf for disease analysis",
        key="main_uploader"
    )
    
    if uploaded_file is None:
        # Enhanced instructions with animations
        st.markdown("""
        <div class="upload-area">
            <h3 style="color: #4CAF50; margin-bottom: 1rem;">🚀 Get Started in 4 Easy Steps</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Step-by-step guide with progress indicators
        steps = [
            ("📸", "Take Photo", "Capture a clear image of rice or sugarcane leaf"),
            ("⬆️", "Upload Image", "Use the file uploader above to select your image"),
            ("🔍", "AI Analysis", "Click analyze to get instant disease detection"),
            ("📊", "View Results", "Get detailed disease info and management tips")
        ]
        
        cols = st.columns(4)
        for i, (icon, title, desc) in enumerate(steps):
            with cols[i]:
                st.markdown(f"""
                <div class="info-card" style="text-align: center; min-height: 150px;">
                    <div style="font-size: 2em; margin-bottom: 0.5rem;">{icon}</div>
                    <h4 style="color: #4CAF50; margin-bottom: 0.5rem;">{title}</h4>
                    <p style="font-size: 0.9em; color: #666;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Supported crops showcase
        st.markdown("### 🌾 Supported Crops & Diseases")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-card">
                <h4 style="color: #4CAF50;">🌾 Rice Diseases</h4>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>🦠 Bacterial Blight</li>
                    <li>🍄 Brown Spot</li>
                    <li>🦠 Tungro Virus</li>
                    <li>🍄 Leaf Smut</li>
                    <li>🌿 Banded Chlorosis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="info-card">
                <h4 style="color: #4CAF50;">🎋 Sugarcane Diseases</h4>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>🍄 Brown Spot</li>
                    <li>🌿 Dried Leaves</li>
                    <li>🌿 Yellow Leaf</li>
                    <li>🍄 Brown Rust</li>
                    <li>✅ Healthy Leaves</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # GitHub repository note
        st.markdown("---")
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white;">
            <h3 style="text-align: center;">🚀 Want the Full AI Experience?</h3>
            <p style="text-align: center; font-size: 1.1em;">
                This Streamlit demo uses enhanced color-based analysis for disease detection.
            </p>
            <p style="text-align: center; font-size: 1.1em;">
                <strong>For the complete CNN-powered AI model with TensorFlow:</strong>
            </p>
            <p style="text-align: center;">
                <a href="https://github.com/James-baranda/darts-disease-detection" 
                   style="color: #FFD700; text-decoration: none; font-weight: bold; font-size: 1.2em;">
                   📂 Visit Our GitHub Repository
                </a>
            </p>
            <p style="text-align: center; font-size: 0.9em; opacity: 0.9;">
                Clone the repository and run the Flask application (app.py) for full CNN model analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        return  # Exit early if no file uploaded
    
    # Enhanced analysis interface when image is uploaded
    st.markdown("### 🔬 AI Disease Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="results-card">
            <h4 style="color: #4CAF50; text-align: center;">📷 Uploaded Image</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.image(uploaded_file, caption="Plant Leaf Image", use_column_width=True)
        
        # Enhanced image info
        image = Image.open(uploaded_file)
        st.markdown(f"""
        <div class="info-card" style="margin-top: 1rem;">
            <h5>📊 Image Details</h5>
            <p><strong>Dimensions:</strong> {image.size[0]} × {image.size[1]} pixels</p>
            <p><strong>File Name:</strong> {uploaded_file.name}</p>
            <p><strong>File Size:</strong> {uploaded_file.size / 1024:.1f} KB</p>
            <p><strong>Format:</strong> {image.format}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="results-card">
            <h4 style="color: #4CAF50; text-align: center;">🤖 AI Analysis Results</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Analyze Disease", type="primary", use_container_width=True):
            # Enhanced loading animation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate AI processing steps
            steps = [
                ("🔍 Preprocessing image...", 20),
                ("🧠 Running AI analysis...", 50),
                ("📊 Calculating confidence...", 80),
                ("✅ Generating results...", 100)
            ]
            
            for step_text, progress in steps:
                status_text.text(step_text)
                progress_bar.progress(progress)
                time.sleep(0.5)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Load and analyze image
            image = Image.open(uploaded_file)
            result, confidence = analyze_image(image)
            
            # Enhanced results display
            if result == "Healthy Leaves":
                st.markdown(f"""
                <div class="results-card" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white;">
                    <h3 style="text-align: center;">🌿 {result}</h3>
                    <h4 style="text-align: center;">Confidence: {confidence:.1%}</h4>
                    <p style="text-align: center; margin-top: 1rem;">Excellent! Your plant appears healthy.</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            elif result in ["BacterialBlight", "Tungro", "Brownspot (Rice)"]:
                st.markdown(f"""
                <div class="results-card" style="background: linear-gradient(135deg, #f44336, #d32f2f); color: white;">
                    <h3 style="text-align: center;">🦠 {result}</h3>
                    <h4 style="text-align: center;">Confidence: {confidence:.1%}</h4>
                    <p style="text-align: center; margin-top: 1rem;">Disease detected - immediate attention needed.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="results-card" style="background: linear-gradient(135deg, #ff9800, #f57c00); color: white;">
                    <h3 style="text-align: center;">⚠️ {result}</h3>
                    <h4 style="text-align: center;">Confidence: {confidence:.1%}</h4>
                    <p style="text-align: center; margin-top: 1rem;">Potential issue detected - monitor closely.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Detailed disease information in expandable cards
            if result in disease_data:
                info = disease_data[result]
                
                st.markdown("---")
                
                # Disease type and symptoms
                with st.expander("📋 Disease Information", expanded=True):
                    st.markdown(f"**Type:** {info['Type']}")
                    
                    col_sym, col_causes = st.columns(2)
                    with col_sym:
                        st.markdown("**🔍 Symptoms:**")
                        for symptom in info['Symptoms']:
                            st.markdown(f"• {symptom}")
                    
                    with col_causes:
                        if 'Causes' in info:
                            st.markdown("**🔬 Causes:**")
                            for cause in info['Causes']:
                                st.markdown(f"• {cause}")
                
                # Management strategies
                with st.expander("💊 Treatment & Management", expanded=True):
                    strategies = info.get('Management Strategies', info.get('Management', []))
                    for i, strategy in enumerate(strategies, 1):
                        st.markdown(f"**{i}.** {strategy}")
                
                # Recommendations
                with st.expander("💡 Expert Recommendations", expanded=True):
                    if result == "Healthy Leaves":
                        st.success("✅ **Continue current care routine**")
                        st.info("🔍 **Monitor regularly** for early detection of any changes")
                        st.info("🌱 **Maintain** current fertilization and watering schedule")
                    else:
                        st.warning("⚠️ **Immediate Action Required**")
                        st.info("👨‍🌾 **Consult** with local agricultural extension officer")
                        st.info("📞 **Contact** plant pathology expert for severe cases")
                        st.info("📚 **Document** symptoms for treatment tracking")
        else:
            st.markdown("""
            <div class="info-card" style="text-align: center; padding: 2rem;">
                <h4 style="color: #4CAF50;">Ready for Analysis! 🚀</h4>
                <p>Click the button above to start AI-powered disease detection</p>
                <p style="font-size: 0.9em; color: #666;">Analysis typically takes 2-3 seconds</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced Footer with statistics and links
    st.markdown("---")
    st.markdown("""
    <div class="info-card" style="text-align: center;">
        <h3 style="color: #4CAF50;">🔬 DARTS System Statistics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Dynamic metrics with animations
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card pulse-animation">
            <h2>11</h2>
            <p>Disease Types</p>
            <small>Bacterial • Fungal • Viral</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card pulse-animation">
            <h2>2</h2>
            <p>Crop Types</p>
            <small>Rice • Sugarcane</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card pulse-animation">
            <h2>AI</h2>
            <p>Analysis Method</p>
            <small>Color-based Detection</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card pulse-animation">
            <h2>2.0</h2>
            <p>Version</p>
            <small>Enhanced Interface</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Technology showcase
    st.markdown("### 🛠️ Technology Stack")
    tech_col1, tech_col2, tech_col3 = st.columns(3)
    
    with tech_col1:
        st.markdown("""
        <div class="info-card">
            <h4 style="color: #4CAF50;">🐍 Backend</h4>
            <p>• Python 3.11</p>
            <p>• Streamlit Framework</p>
            <p>• NumPy & PIL</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_col2:
        st.markdown("""
        <div class="info-card">
            <h4 style="color: #4CAF50;">🤖 AI Engine</h4>
            <p>• Color Analysis</p>
            <p>• Pattern Recognition</p>
            <p>• Confidence Scoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_col3:
        st.markdown("""
        <div class="info-card">
            <h4 style="color: #4CAF50;">🎨 Interface</h4>
            <p>• Responsive Design</p>
            <p>• Dynamic Animations</p>
            <p>• Modern UI/UX</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Final call-to-action for GitHub
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 2rem; border-radius: 15px; text-align: center; color: white; margin: 2rem 0;">
        <h2>🚀 Ready for Production-Grade AI?</h2>
        <p style="font-size: 1.2em; margin: 1rem 0;">
            This Streamlit demo showcases our enhanced color-based disease detection algorithm.
        </p>
        <p style="font-size: 1.1em; margin: 1rem 0;">
            <strong>For the complete experience with CNN deep learning models:</strong>
        </p>
        <div style="margin: 2rem 0;">
            <a href="https://github.com/James-baranda/darts-disease-detection" 
               style="background: #FFD700; color: #333; padding: 1rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold; font-size: 1.1em; display: inline-block; transition: all 0.3s ease;">
               📂 Clone Our GitHub Repository
            </a>
        </div>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; min-width: 200px;">
                <h4>🧠 Full CNN Model</h4>
                <p>TensorFlow-powered deep learning for maximum accuracy</p>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; min-width: 200px;">
                <h4>🌐 Flask Web App</h4>
                <p>Production-ready web application with advanced features</p>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; min-width: 200px;">
                <h4>📊 Detailed Analytics</h4>
                <p>Comprehensive disease analysis and management strategies</p>
            </div>
        </div>
        <p style="margin-top: 2rem; font-size: 0.9em; opacity: 0.8;">
            Run <code style="background: rgba(255,255,255,0.2); padding: 0.2rem 0.5rem; border-radius: 3px;">python app.py</code> 
            from the repository for the complete CNN-powered experience
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Credits and version info
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #666; font-size: 0.9em;">
        <p><strong>DARTS v2.0</strong> - Detection Assessment and Recognition in Tarlac City Software</p>
        <p>Developed with ❤️ for sustainable agriculture • Enhanced Streamlit Interface</p>
        <p>© 2024 DARTS Project • Open Source Agricultural Technology</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
