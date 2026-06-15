import streamlit as st
import requests
from PIL import Image

st.set_page_config(
    page_title="PhytoGuard Diagnostic Terminal",
    page_icon="🌿",
    layout="wide"
)

# Target the updated endpoint path directly
API_TARGET_URL = "http://localhost:8000/api/v2/evaluate-sample"

st.title("🌿 PhytoGuard: AI Crop Health Hub")
st.caption("Enterprise-grade analytical engine powered by distributed multimodal vision matrices.")
st.markdown("---")

# Establish a two-column spatial grid layout
interaction_col, visual_col = st.columns([2, 3])

with interaction_col:
    st.subheader("Matrix Transmission Channel")
    target_specimen = st.file_uploader(
        label="Inject botanical specimen graphic into scanner core",
        type=["jpg", "jpeg", "png", "webp"]
    )
    
    if target_specimen:
        pil_representation = Image.open(target_specimen)
        st.image(pil_representation, caption="Active File Input Buffer", use_container_width=True)

with visual_col:
    st.subheader("Diagnostic Stream Output")
    
    if target_specimen:
        trigger_scan = st.button("Initialize Deep Diagnostic Scan", type="primary")
        
        if trigger_scan:
            with st.spinner("Decoding image pixel vectors and parsing via cloud vision models..."):
                try:
                    # Construct multi-part streaming payload
                    binary_payload = target_specimen.getvalue()
                    multipart_form_data = {
                        "uploaded_file": (target_specimen.name, binary_payload, target_specimen.type)
                    }
                    
                    api_transaction = requests.post(API_TARGET_URL, files=multipart_form_data)
                    
                    if api_transaction.status_code == 200:
                        mapped_response = api_transaction.json()
                        
                        # Render completely unique graphical configurations
                        if mapped_response.get("is_infected"):
                            st.error(f"🚨 Anomalous Activity Located: **{mapped_response.get('pathology_title')}**")
                        else:
                            st.success("✨ Diagnostic Scan Concluded: Structure exhibits pristine cell health profiles.")
                            
                        # Format numeric blocks into modular layouts
                        metric_left, metric_right = st.columns(2)
                        metric_left.metric("Pathogen Vector Type", str(mapped_response.get("pathogen_group")).upper())
                        metric_right.metric("System Confidence Rating", f"{mapped_response.get('metric_confidence')}%")
                        
                        # Structural change: Deploy clean, isolated data tabs
                        tab_anomalies, tab_catalysts, tab_remediations = st.tabs(
                            ["Identified Symptoms", "Environmental Catalysts", "Targeted Countermeasures"]
                        )
                        
                        with tab_anomalies:
                            for anomaly in mapped_response.get("observed_anomalies", []):
                                st.write(f"🔍 {anomaly}")
                                
                        with tab_catalysts:
                            for catalyst in mapped_response.get("catalyst_factors", []):
                                st.write(f"⚠️ {catalyst}")
                                
                        with tab_remediations:
                            for remedy in mapped_response.get("curative_actions", []):
                                st.info(remedy)
                                
                    else:
                        st.critical(f"Server Core Fault: {api_transaction.status_code} - {api_transaction.text}")
                        
                except Exception as fatal_exception:
                    st.exception(fatal_exception)
    else:
        st.info("System currently idle. Please feed a crop cell sample vector into the console controller.")