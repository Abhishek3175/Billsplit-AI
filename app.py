import streamlit as st
import requests
import base64
import json
from PIL import Image
from io import BytesIO

# -------------------------
# CONFIG
# -------------------------
API_KEY = "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"  # Replace with your actual OpenRouter key
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "meta-llama/llama-4-maverick:free"  # Supported multimodal model

def encode_image(file_bytes):
    return base64.b64encode(file_bytes).decode("utf-8")

def extract_bill_from_image(image_b64):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = """
Analyze this bill image and extract the following information in a structured JSON format:
{
    "Bill_Number": "extract bill/invoice number if present",
    "Date": "extract date in YYYY-MM-DD format",
    "Vendor_Name": "extract store/restaurant name",
    "Items": [
        {
            "Item_Name": "extract item name",
            "Quantity": "extract quantity",
            "Price": "extract price as number"
        }
    ],
    "Subtotal": "extract subtotal as number",
    "Tax": "extract tax amount as number",
    "Total_Amount": "extract total amount as number"
}
Ensure all numeric values are returned as numbers, not strings.
If any field is not found, use null.
"""

    try:
        data = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are a precise bill data extraction assistant. Return only valid JSON."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                ]}
            ]
        }

        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()
        
        response_data = response.json()
        if "choices" in response_data and len(response_data["choices"]) > 0:
            content = response_data["choices"][0]["message"]["content"]
            try:
                # Try to find JSON content within the response
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = content[json_start:json_end]
                    return json.loads(json_str)
                else:
                    return {"error": "No valid JSON found in response"}
            except json.JSONDecodeError:
                return {"error": "Failed to parse JSON from response"}
        else:
            return {"error": "No valid response from API"}
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

st.set_page_config(page_title="Bill Extractor AI", page_icon="🧾", layout="centered")
st.title("🧾 Bill Extractor (Image → JSON)")

uploaded_file = st.file_uploader("Upload a Bill Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Read bytes once and reuse
    file_bytes = uploaded_file.read()

    # Show preview using BytesIO
    st.image(Image.open(BytesIO(file_bytes)), caption="Uploaded Bill", use_column_width=True)

    if st.button("Extract Bill Data"):
        with st.spinner("🔍 Extracting data from bill..."):
            try:
                image_b64 = encode_image(file_bytes)
                result = extract_bill_from_image(image_b64)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("✅ Extraction Complete!")
                    st.json(result)
            except Exception as e:
                st.error(f"Failed to process image: {str(e)}")