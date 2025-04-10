from dotenv import load_dotenv
load_dotenv()  # Load environment variables
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import time

# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Function to get Gemini response
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Function to prepare image for Gemini
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Custom CSS for improved aesthetics
def apply_custom_css():
    st.markdown("""
    <style>
        /* Overall theme */
        .stApp {
            background-color: #111111;
            color: #E0E0E0;
        }
        
        /* Header styling */
        .title-container {
            text-align: center;
            margin-bottom: 10px;
            padding-bottom: 0;
        }
        
        .logo-emoji {
            font-size: 3.5rem;
            margin-bottom: -10px;
            display: inline-block;
            padding: 5px;  /* Added padding to prevent cutting off */
        }
        
        .logo-text {
            font-size: 3.5rem;
            font-weight: 700;
            color: #FFFFFF;
            font-family: 'Helvetica Neue', sans-serif;
            margin-top: 0;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 1.1rem;
            color: #AAAAAA;
            text-align: center;
            margin-bottom: 30px;
            font-family: 'Helvetica Neue', sans-serif;
        }
        
        /* Section headers */
        .section-header {
            font-size: 1.8rem;
            font-weight: 600;
            color: #FFFFFF;
            margin-bottom: 15px;
            font-family: 'Helvetica Neue', sans-serif;
        }
        
        /* Upload container */
        .upload-container {
            background-color: #222222;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #333333;
            margin-bottom: 20px;
        }
        
        /* Remove the default border around file uploader */
        .st-emotion-cache-1vs2kde, .stFileUploader, div[data-testid="stFileUploader"] {
            border: none !important;
            padding-top: 0 !important;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #111111 !important; /* Black button */
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            border: 1px solid #333333 !important;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #222222 !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        /* Results area */
        .results-container {
            background-color: #222222;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #333333;
            margin-bottom: 20px;
        }
        
        /* Contact section */
        .contact-container {
            background-color: #1E1E1E;
            border-radius: 8px;
            padding: 15px;
            margin-top: 0;
            border: 1px solid #333333;
        }
        
        .contact-header {
            font-size: 1.3rem;
            font-weight: 600;
            color: #FFFFFF;
            margin-bottom: 10px;
        }
        
        .contact-link {
            color: #4CAF50;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .contact-link:hover {
            color: #3e8e41;
            text-decoration: underline;
        }
        
        /* Footer */
        .footer {
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid #333333;
            font-size: 0.8rem;
            color: #888888;
            text-align: center;
        }
        
        /* Remove whitespace and padding */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        
        /* Fix file uploader */
        .css-1db87p5 {
            background-color: #222222 !important;
        }
        
        .stFileUploader label {
            color: #CCCCCC !important;
        }
        
        /* Social media icons */
        .social-icons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 10px;
        }
        
        .social-icon {
            font-size: 24px;
            color: #4CAF50;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #111111 !important;
            border-radius: 8px;
            font-weight: 600;
            color: white !important;
        }
        
        /* Hide all divider lines and bars */
        .streamlit-expanderContent div div div,
        div[data-testid="stExpander"] div div div,
        .css-9ycgxx,
        .st-emotion-cache-9ycgxx,
        .st-emotion-cache-ue6h4q,
        .st-emotion-cache-1y4p8pa,
        .st-emotion-cache-1gulkj5,
        section > .block-container > div, 
        div[data-testid="stVerticalBlock"] > div,
        [data-testid="stVerticalBlock"] > div > div,
        div.element-container div.stButton,
        div.element-container div,
        div[data-testid="stVerticalBlock"] > div::after,
        div[data-testid="stVerticalBlock"] > div::before {
            border-bottom: none !important;
            border-top: none !important;
            padding-bottom: 0 !important;
            margin-bottom: 0 !important;
        }
        
        /* Target Analyze Food Button specifically */
        button[kind="primaryFormSubmit"] {
            background-color: #111111 !important;
            color: #ff6b6b !important;
            border: 1px solid #333333 !important;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Ensure logo emoji is not cut off */
        .emoji-container {
            padding: 10px;
            margin: 5px 0;
            display: inline-block;
        }
        
        /* Fix the section dividers completely */
        .element-container:has(div.stButton) {
            border-bottom: none !important;
        }
        
        /* Target any remaining bars */
        hr, .horizontal-rule, div[role="separator"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Streamlit Page Configuration
st.set_page_config(
    page_title="NutriGuard - Food Analysis",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

apply_custom_css()

# Header with emoji logo - fixed to prevent cutting
st.markdown(
    """
    <div class="title-container">
        <div class="emoji-container">
            <span class="logo-emoji">🥗</span>
        </div>
        <h1 class="logo-text">NutriGuard</h1>
        <p class="subtitle">AI-powered nutrition analyzer to help you make healthier food choices</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Upload Food Image Section
st.markdown('<div class="section-header">Upload Food Image</div>', unsafe_allow_html=True)

# File uploader without the bar
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# Display image if uploaded
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
else:
    st.markdown("""
    <div style="text-align: center; padding: 35px 0; background-color: #222222; border-radius: 12px; border: 1px solid #333333; margin-bottom: 20px;">
        <div style="font-size: 48px;">📸</div>
        <p style="color: #AAAAAA; margin-top: 10px;">Drag and drop your food image here</p>
    </div>
    """, unsafe_allow_html=True)
# Inject custom HTML to remove top margin
st.markdown("<div style='margin-top: -15px;'></div>", unsafe_allow_html=True)

# Analysis Button - Now with black background
analyze_button = st.button("🔍 Analyze Food", key="analyze_button")

if analyze_button:
    if uploaded_file is None:
        st.error("⚠️ Please upload a food image before analyzing.")
    else:
        # Display results container
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        
        # Prompt to Gemini
        input_prompt = """
        You are an expert nutritionist. Review the food items in the uploaded image and provide:
        1. A list of all food items with their estimated:
           - Calories
           - Protein content (in grams)
        2. Mention any disease risks associated with the identified food items.
        3. State whether the food is healthy overall on a scale of 1-10, with a brief explanation.
        4. Suggest 2-3 healthy alternatives in the same format:
           - Item - calories, protein (g)
           
        Format your response with clear headings and bullet points for readability.
        """
        
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Simulated progress for better UX
            status_text.text("Preparing image for analysis...")
            progress_bar.progress(10)
            time.sleep(0.5)
            
            image_data = input_image_setup(uploaded_file)
            progress_bar.progress(30)
            status_text.text("Identifying food items...")
            time.sleep(0.5)
            
            progress_bar.progress(50)
            status_text.text("Calculating nutritional information...")
            time.sleep(0.5)
            
            response = get_gemini_response(input_prompt, image_data)
            progress_bar.progress(90)
            status_text.text("Finalizing results...")
            time.sleep(0.5)
            
            progress_bar.progress(100)
            status_text.empty()
            
            # Display results
            st.success("✅ Analysis Complete!")
            st.markdown("### Nutritional Analysis Results:")
            st.write(response)
            
            # Download option
            st.download_button(
                label="📥 Download Analysis",
                data=response,
                file_name="nutriguard_analysis.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            st.info("Please try again with a clearer image or check your internet connection.")
        
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # Empty results container with message
    st.markdown('<div class="results-container" style="margin-top: 10px;">', unsafe_allow_html=True)
    st.info("Upload an image above and click 'Analyze Food' to see results here.")
    st.markdown('</div>', unsafe_allow_html=True)

with st.expander("ℹ️ How NutriGuard Works"):
    st.write("""
    **NutriGuard** analyzes your food images using AI to provide:
    
    1. Detailed list of food items
    2. Estimated calories and protein content
    3. Potential health risks associated with the food
    4. Overall healthiness assessment
    5. Healthier alternative suggestions
    
    Simply upload a clear image of your meal and click 'Analyze Food' to get started!
    """)

# Contact Section
with st.expander("📬 Contact Us"):
    st.markdown(
        """
        <div class="contact-container">
            <div class="contact-header">Connect with the Developer</div>
            <p>Have questions, suggestions, or feedback? Feel free to reach out:</p>
            <div class="social-icons">
                <a href="https://github.com/harsh-pratapsingh24" target="_blank">
                    <svg class="social-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#4CAF50"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                </a>
                <a href="https://www.linkedin.com/in/harshpratapsingh333/" target="_blank">
                    <svg class="social-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#4CAF50"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
                </a>
                <a href="mailto:harsh.psingh2005@gmail.com">
                    <svg class="social-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#4CAF50"><path d="M12 12.713l-11.985-9.713h23.971l-11.986 9.713zm-5.425-1.822l-6.575-5.329v12.501l6.575-7.172zm10.85 0l6.575 7.172v-12.501l-6.575 5.329zm-1.557 1.261l-3.868 3.135-3.868-3.135-8.11 8.848h23.956l-8.11-8.848z"/></svg>
                </a>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Footer
st.markdown(
    """
    <div class="footer">
        <p>⚠️ <b>Disclaimer:</b> NutriGuard provides estimated nutritional information using AI analysis. Results may vary and should not replace professional dietary advice.</p>
        <p>© 2025 NutriGuard | AI-Powered Nutrition Analysis</p>
    </div>
    """, 
    unsafe_allow_html=True
)
