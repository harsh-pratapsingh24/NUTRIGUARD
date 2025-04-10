from dotenv import load_dotenv
load_dotenv()  # Load environment variables
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

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

# Streamlit Page Configuration
st.set_page_config(page_title="NutriGuard", page_icon="🥗", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🥗 NutriGuard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload your food picture and get a nutrition analysis with calorie breakdown, health suggestions, and more!</p>", unsafe_allow_html=True)
st.divider()

# Upload Section
with st.container():
    uploaded_file = st.file_uploader("📷 Upload a food image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

# Prompt to Gemini
input_prompt = """
You are an expert nutritionist. Review the food items in the uploaded image and provide:

1. A list of all food items with their estimated:
   - Calories
   - Protein content

2. Mention any disease risks associated with the identified food items.

3. State whether the food is healthy overall.
4.Rate the product on a scale of 0 to 10 based on how healthy it is.
5. Suggest some healthy alternatives in the same format:
   - Item - no of calories, protein
"""

# Analyze Button
if st.button("🔍 Analyze Picture"):
    if uploaded_file is None:
        st.error("Please upload an image before analyzing.")
    else:
        with st.spinner("Analyzing the food items..."):
            try:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_prompt, image_data)
                st.success("Analysis complete!")

                with st.expander("📄 View Nutritional Analysis"):
                    st.write(response)

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Footer warning
st.markdown("---")
st.info("⚠️ NutriGuard uses AI and may occasionally provide inaccurate or estimated results. Always consult a professional for medical or dietary advice.")
