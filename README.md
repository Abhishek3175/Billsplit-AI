# Bill Split AI

An AI-powered bill extraction tool that converts bill images to structured JSON data.

## Features

- Upload bill images (JPG, JPEG, PNG)
- Extract bill details including:
  - Bill Number
  - Date
  - Vendor Name
  - Items with quantities and prices
  - Subtotal, Tax, and Total Amount
- Display results in JSON format

## Setup

1. Clone the repository:
```bash
git clone https://github.com/Abhishek3175/Billsplit-AI.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenRouter API key in app.py

4. Run the application:
```bash
streamlit run app.py
```

## Technologies Used

- Streamlit
- OpenRouter AI API
- Python
- PIL (Python Imaging Library)