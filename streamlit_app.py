import streamlit as st
import numpy as np
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="DARTS - Disease Detection System",
    page_icon="🌱",
    layout="wide"
)

# Embedded disease data (minimal version)
disease_data = {
    "Healthy": {
        "Type": "Normal Condition",
        "Symptoms": ["Vibrant green color", "Normal leaf shape"],
        "Management": ["Continue current care routine", "Monitor for changes"],
        "Indicator": "green"
    },
    "Mild Disease": {
        "Type": "Early Stage",
        "Symptoms": ["Slight yellowing", "Minor spots"],
        "Management": ["Check watering", "Monitor closely"],
        "Indicator": "orange"
    },
    "Severe Disease": {
        "Type": "Advanced Stage",
        "Symptoms": ["Brown spots", "Wilting", "Yellow leaves"],
        "Management": ["Immediate treatment needed", "Consult expert"],
        "Indicator": "red"
    }
}

def analyze_image(image):
    """Simple color-based analysis"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            # Calculate average RGB values
            red = np.mean(img_array[:, :, 0])
            green = np.mean(img_array[:, :, 1])
            blue = np.mean(img_array[:, :, 2])
            
            # Simple analysis
            if green > red and green > blue and green > 100:
                return "Healthy", 0.85
            elif green > 50:
                return "Mild Disease", 0.70
            else:
                return "Severe Disease", 0.80
        else:
            return "Unknown", 0.50
    except:
        return "Error", 0.0

def main():
    st.title("🌱 DARTS - Disease Detection System")
    st.markdown("**Detection Assessment and Recognition in Tarlac City Software**")
    
    st.markdown("---")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a plant leaf image",
        type=['png', 'jpg', 'jpeg']
    )
    
    if uploaded_file is not None:
        # Display image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📤 Uploaded Image")
            st.image(uploaded_file, caption="Plant Leaf", use_column_width=True)
        
        # Analyze button
        if st.button("🔍 Analyze Plant Health", type="primary"):
            with st.spinner("Analyzing..."):
                # Load and analyze image
                image = Image.open(uploaded_file)
                result, confidence = analyze_image(image)
                
                with col2:
                    st.subheader("🔬 Analysis Results")
                    
                    # Show result
                    if result == "Healthy":
                        st.success(f"🌿 **Status: {result}**")
                        st.success(f"**Confidence: {confidence:.1%}**")
                    elif result == "Mild Disease":
                        st.warning(f"🌿 **Status: {result}**")
                        st.warning(f"**Confidence: {confidence:.1%}**")
                    else:
                        st.error(f"🌿 **Status: {result}**")
                        st.error(f"**Confidence: {confidence:.1%}**")
                    
                    # Show disease info
                    if result in disease_data:
                        info = disease_data[result]
                        st.info(f"**Type:** {info['Type']}")
                        st.info(f"**Symptoms:** {', '.join(info['Symptoms'])}")
                        st.info(f"**Management:** {', '.join(info['Management'])}")
                        
                        # Show indicator
                        indicator = info['Indicator']
                        if indicator == "green":
                            st.success("🟢 **Condition: Healthy**")
                        elif indicator == "orange":
                            st.warning("🟠 **Condition: Mild**")
                        else:
                            st.error("🔴 **Condition: Severe**")
    
    st.markdown("---")
    st.markdown("**Note:** This is a simplified demo version. For full AI-powered analysis, use the complete Flask application.")

if __name__ == "__main__":
    main()
